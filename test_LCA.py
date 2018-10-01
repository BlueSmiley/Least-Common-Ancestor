# PyUnit test code

import unittest
from graphlca import LCAGraph
from collections import Counter

class LCATest(unittest.TestCase):

    # test inserts add edegs properly,instantiate and test a graph edges
    def test_int_insert(self):
        graph = LCAGraph()
        root = 0
        graph.add_node(root)
        self.assertItemsEqual(graph.edges(root),[],"checking when root empty")
        graph.add_edge(root,1)
        self.assertItemsEqual(graph.edges(root),[1],"root one child")
        self.assertItemsEqual(graph.edges(1),[],"leaf node")
        graph.add_edge(root,1)
        self.assertItemsEqual(graph.edges(root),[1],"no duplicate edges")
        graph.add_edge(root,2)
        self.assertItemsEqual(graph.edges(root),[1,2],"root two children")
        graph.add_edge(1,3)
        graph.add_edge(1,5)
        graph.add_edge(2,4)
        self.assertItemsEqual(graph.edges(1),[5,3],"non-root two children")
        self.assertItemsEqual(graph.edges(2),[4]),"non-root one child"
        graph.add_edge(1,6)
        self.assertItemsEqual(graph.edges(1),[3,5],"node third child ignored")

    def test_string_insert(self):
        graph = LCAGraph()
        root = "root"
        graph.add_node(root)
        self.assertItemsEqual(graph.edges(root),[],
        "checking when root empty")
        graph.add_edge(root,"rootchild1")
        self.assertItemsEqual(graph.edges(root),["rootchild1"],
        "root one child")
        self.assertItemsEqual(graph.edges("rootchild1"),[],"leaf node")
        graph.add_edge(root,"rootchild1")
        self.assertItemsEqual(graph.edges(root),["rootchild1"],
        "no duplicate edges")
        graph.add_edge(root,"rootchild2")
        self.assertItemsEqual(graph.edges(root),["rootchild1","rootchild2"],
        "root two children")
        graph.add_edge("rootchild1","1child1")
        graph.add_edge("rootchild1","1child2")
        graph.add_edge("rootchild2","2child1")
        self.assertItemsEqual(graph.edges("rootchild1"),["1child1","1child2"],
        "non-root two children")
        self.assertItemsEqual(graph.edges("rootchild2"),["2child1"]),
        "non-root one child"
        graph.add_edge("rootchild1","1child3")
        self.assertItemsEqual(graph.edges("rootchild1"),["1child2","1child1"],
        "node third child ignored")
        




    # test Lca should return correct key of LCA
    def test_int_LCA(self):
        graph = LCAGraph()
        root = 1
        graph.add_node(root)
        graph.add_edge(root,2)
        graph.add_edge(root,3)
        graph.add_edge(2,4)
        graph.add_edge(2,5)
        graph.add_edge(3,6)
        graph.add_edge(3,7)
        self.assertEqual(graph.lowest_common_ancestor(root,[4,5]),2,
        "two leaf nodes same parent")
        self.assertEqual(graph.lowest_common_ancestor(root,[4,6]),1,
        "two leaf nodes different parent")
        self.assertEqual(graph.lowest_common_ancestor(root,[3,4]),1,
        "one leaf node and one non-leaf node")
        self.assertEqual(graph.lowest_common_ancestor(root,[2,4]),2,
        "parent and child leaf node")
        self.assertEqual(graph.lowest_common_ancestor(root,[1,4]),1,
        "leaf node and root with params swapped")
        graph.add_node(9)
        # checking doesnt give false positives
        self.assertIsNone(graph.lowest_common_ancestor(root,[2,8]),
        "lca non-existent node")
        self.assertIsNone(graph.lowest_common_ancestor(root,[1,9]),
        "lca disconnected node")
        self.assertIsNone(graph.lowest_common_ancestor(2,[3,6]),
        "Doesnt recurse past root and treats as seperate components")
        # checking gives correct answer if two params same
        self.assertEqual(graph.lowest_common_ancestor(root,[1,1]),1,
        "root and both nodes root")
        self.assertEqual(graph.lowest_common_ancestor(root,[2,1]),1,
        "root and child node with lca = root")
        self.assertEqual(graph.lowest_common_ancestor(root,[2,2]),2,
        "child with both nodes child")

        # test for other comparable objects as keys to make sure it still works
        # Sort of unnescary I think but just to make sure my lca is generalised
        # I feel this is the wrong way to go about it, but dont know right way
        # Better than no check I think
    def test_string_LCA(self):
        graph = LCAGraph()
        root = "1"
        graph.add_node(root)
        graph.add_edge(root,"2")
        graph.add_edge(root,"3")
        graph.add_edge("2","4")
        graph.add_edge("2","5")
        graph.add_edge("3","6")
        graph.add_edge("3","7")
        self.assertEqual(graph.lowest_common_ancestor(root,["4","5"]),"2",
        "two leaf nodes same parent")
        self.assertEqual(graph.lowest_common_ancestor(root,["4","6"]),"1",
        "two leaf nodes different parent")
        self.assertEqual(graph.lowest_common_ancestor(root,["3","4"]),"1",
        "one leaf node and one non-leaf node")
        self.assertEqual(graph.lowest_common_ancestor(root,["2","4"]),"2",
        "parent and child leaf node")
        self.assertEqual(graph.lowest_common_ancestor(root,["1","4"]),"1",
        "leaf node and root with params swapped")
        graph.add_node("9")
        # checking doesnt give false positives
        self.assertIsNone(graph.lowest_common_ancestor(root,["2","8"]),
        "lca non-existent node")
        self.assertIsNone(graph.lowest_common_ancestor(root,["1","9"]),
        "lca disconnected node")
        self.assertIsNone(graph.lowest_common_ancestor("2",["3","6"]),
        "Doesnt recurse past root and treats as seperate components")
        # checking gives correct answer if two params same
        self.assertEqual(graph.lowest_common_ancestor(root,["1","1"]),"1",
        "root and both nodes root")
        self.assertEqual(graph.lowest_common_ancestor(root,["2","1"]),"1",
        "root and child node with lca = root")
        self.assertEqual(graph.lowest_common_ancestor(root,["2","2"]),"2",
        "child with both nodes child")



if __name__ == "__main__":
    unittest.main()
