# Project Name

This project is to explore the cosmology for Roman-Y1 with varying analyses choices such as galaxy redshift distribution, survey area, scale cut, cosmology model, and parameter prior

## Project Structure

\`\`\`
Project-Roman-Y1/
├── cocoa/       # the analysis software for data vector simulation and MCMC
├── plots/       # data visualization
\`\`\`

## File Reference

| File/Folder | Description |
|-------------|-------------|
| `/project/chihway/junzhou/plots/` | there are plenty of plots from which you can learn experience |


## Common Commands
'caslake' : apply a intel-CPU computation node
'kicp'    : apply a intel-CPU computation node
'amd'     : apply a amd-CPU computation node


# Install dependencies
for visualization, mainly uses env 'conda activate plot_dist'


## Important Notes

- You are only allowed to modify things under '/project/chihway/junzhou/Project-Roman-Y1'
- Never Use 'rm -rf *'
- You are responsible to read the literature and decide what analyses to do
- You are responsible to visualize results and devide the direction we should go
- You are not responsible for the usage of software COCOA, ComsoLike, CosmoCoV, and ETC.Tasks related to them should handle to the agent 'COCOA-operator' to complete.

## Software delegation

All operations involving COCOA must be delegated to the
`COCOA-operator` sub-agent.

The main agent may:

- define the desired project outcome;
- prepare domain-level requirements;
- interpret the returned results;
- combine the software results with other project work.

The main agent must not:

- operate COCOA directly;
- invent software commands or settings;
- interpret a failed software run as a valid result;
- modify COCOA-generated files without consulting the operator.

When delegating, provide:

1. the objective;
2. input files;
3. required output;
4. fixed parameters;
5. parameters the operator may choose;
6. validation requirements.

After receiving the result, the main agent should evaluate its project-level
meaning rather than repeating the software execution.