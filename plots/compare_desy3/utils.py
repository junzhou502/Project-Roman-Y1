from pathlib import Path
from collections.abc import Sequence
import re

import numpy as np


def _normalize_name(name: str) -> str:
    """
    Make parameter matching insensitive to capitalization,
    underscores, hyphens, and section prefixes.
    """
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _read_chain_header(filepath: str | Path) -> list[str]:
    """Read column names from the first commented line."""
    filepath = Path(filepath)

    with filepath.open("r") as f:
        first_line = f.readline()

    if not first_line.startswith("#"):
        raise ValueError(
            f"The first line of {filepath} is not a commented header."
        )

    columns = first_line.removeprefix("#").strip().split()

    if not columns:
        raise ValueError(f"No column names found in {filepath}.")

    return columns


def _find_column(parameter: str, columns: Sequence[str]) -> int:
    """
    Find a parameter column.

    Both full names and unique short names are accepted, for example:

        cosmological_parameters--omega_m
        omega_m
        omegam
    """
    target = _normalize_name(parameter)

    # First try the complete column name.
    full_matches = [
        i
        for i, column in enumerate(columns)
        if _normalize_name(column) == target
    ]

    if len(full_matches) == 1:
        return full_matches[0]

    # Then try the part after "--".
    suffix_matches = [
        i
        for i, column in enumerate(columns)
        if _normalize_name(column.split("--")[-1]) == target
    ]

    if len(suffix_matches) == 1:
        return suffix_matches[0]

    matches = full_matches or suffix_matches

    if len(matches) > 1:
        matching_names = [columns[i] for i in matches]
        raise ValueError(
            f"Parameter {parameter!r} is ambiguous.\n"
            f"Matching columns: {matching_names}\n"
            "Use the complete column name."
        )

    raise KeyError(
        f"Parameter {parameter!r} was not found.\n"
        f"Available columns:\n{columns}"
    )


def load_chain_parameters(
    filepath: str | Path,
    required_parameters: Sequence[str],
    *,
    weight_name: str = "weight",
    drop_zero_weight: bool = False,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Load selected parameters and weights from a CosmoSIS text chain.

    Parameters
    ----------
    filepath
        Path to the chain file.

    required_parameters
        Parameter names in the desired output order. For example:

            ["omegam", "sigma8"]

        Full header names are also accepted:

            [
                "cosmological_parameters--omega_m",
                "COSMOLOGICAL_PARAMETERS--SIGMA_8",
            ]

    weight_name
        Name of the weight column. Default is "weight".

    drop_zero_weight
        If True, remove samples whose weights are zero.

    Returns
    -------
    parameter_array
        Shape: (number_of_samples, number_of_required_parameters)

    weights
        Shape: (number_of_samples,)
    """
    if isinstance(required_parameters, str):
        raise TypeError(
            "required_parameters must be a list, for example "
            "['omegam', 'sigma8']."
        )

    if len(required_parameters) == 0:
        raise ValueError("required_parameters cannot be empty.")

    columns = _read_chain_header(filepath)

    parameter_indices = [
        _find_column(parameter, columns)
        for parameter in required_parameters
    ]
    weight_index = _find_column(weight_name, columns)

    # Read only the requested columns, avoiding the large metadata block.
    selected_indices = parameter_indices + [weight_index]

    data = np.loadtxt(
        filepath,
        comments="#",
        usecols=selected_indices,
        dtype=float,
        ndmin=2,
    )

    parameter_array = data[:, :-1]
    weights = data[:, -1]

    valid = (
        np.all(np.isfinite(parameter_array), axis=1)
        & np.isfinite(weights)
    )

    if drop_zero_weight:
        valid &= weights > 0

    parameter_array = parameter_array[valid]
    weights = weights[valid]

    return parameter_array, weights