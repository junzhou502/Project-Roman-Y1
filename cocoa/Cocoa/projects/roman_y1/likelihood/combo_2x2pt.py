from cobaya.likelihoods.roman_y1._cosmolike_prototype_base import _cosmolike_prototype_base
import cosmolike_roman_y1_interface as ci
import numpy as np

class combo_2x2pt(_cosmolike_prototype_base):
  def initialize(self):
    super(combo_2x2pt,self).initialize(probe="2x2pt")