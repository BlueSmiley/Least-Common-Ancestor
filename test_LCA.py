# PyUnit test code
# No experience writing such code and havent made code yet
# So making comments on how to structure the tests
# Remove after code complete
# Also good test for using git with linux
# Need to test if insert() works properly so need a edges()
# Graph based rep of a binary tree so treating it as graph
# Key should be comparable and immutable-only conditions
# Test different immutable, comparable data types
# LCA() should return key or null equiv if not in graph
# Since treat as binary tree we can relax some assumptions
# Test LCA() for different types of nodes
# Make sure insert() and LCA() gives errors if wrong type
# Some errors bound to happen since unused to python +
# Might borrow code so might not have proper test constraints

import unittest
import graphlca

class LCATest(unittest.TestCase):

#test inserts add edegs properly,instantiate and test a graph edges
    def test_insert(self):
        self.assertItemsEqual({},{})

#test Lca should return correct key of LCA
    def test_LCA(self):
        self.assertEqual("","")

if __name__ == "__main__":
    unittest.main()
