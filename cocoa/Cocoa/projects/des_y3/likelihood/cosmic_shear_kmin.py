from cobaya.likelihoods.des_y3._cosmolike_prototype_base_kmin import _cosmolike_prototype_base, survey
import cosmolike_des_y3_interface as ci
import numpy as np

class cosmic_shear_kmin(_cosmolike_prototype_base):
  def initialize(self):
    super(cosmic_shear_kmin,self).initialize(probe="xi")
