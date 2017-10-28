# unit tests for rates
import math
import os

import pyreaclib.networks as networks
import pyreaclib.rates as rates

from pytest import approx

class TestPythonNetwork(object):
    @classmethod
    def setup_class(cls):
        """ this is run once for each class before any tests """
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).split("pyreaclib")[0]
        cls.library_path = os.path.join(base_dir, "pyreaclib/pyreaclib/library/")

    @classmethod
    def teardown_class(cls):
        """ this is run once for each class after all tests """
        pass

    def setup_method(self):
        """ this is run before each test """
        files = ["c12-pg-n13-ls09",
                 "c13-pg-n14-nacr",
                 "n13--c13-wc12",
                 "n13-pg-o14-lg06",
                 "n14-pg-o15-im05",
                 "n15-pa-c12-nacr",
                 "o14--n14-wc12",
                 "o15--n15-wc12"]
        self.pyn = networks.PythonNetwork(files)
        self.rate = rates.Rate(os.path.join(self.library_path, "c13-pg-n14-nacr"))

    def teardown_method(self):
        """ this is run after each test """
        self.tf = None

    def test_ydot_string(self):
        ydot = self.pyn.ydot_string(self.rate)
        assert ydot == "rho*Y[ic13]*Y[ip]*lambda_c13_pg_n14" or \
               ydot == "rho*Y[ip]*Y[ic13]*lambda_c13_pg_n14"


    def test_jacobian_string(self):
        jac = self.pyn.jacobian_string(self.rate,
                                       self.rate.products[0],
                                       self.rate.reactants[0])
        assert jac == "rho*Y[ic13]*lambda_c13_pg_n14"


    def test_function_string(self):

        ostr = """
def c13_pg_n14(tf):
    # c13 + p --> n14
    rate = 0.0

    # nacrn
    rate += np.exp(  18.5155 + -13.72*tf.T913i + -0.450018*tf.T913
                  + 3.70823*tf.T9 + -1.70545*tf.T953 + -0.666667*tf.lnT9)
    # nacrr
    rate += np.exp(  13.9637 + -5.78147*tf.T9i + -0.196703*tf.T913
                  + 0.142126*tf.T9 + -0.0238912*tf.T953 + -1.5*tf.lnT9)
    # nacrr
    rate += np.exp(  15.1825 + -13.5543*tf.T9i
                  + -1.5*tf.lnT9)

    return rate
"""
        assert self.pyn.function_string(self.rate).replace(" ","").strip() == ostr.replace(" ","").strip()
