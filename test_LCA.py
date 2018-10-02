# PyUnit test code

import unittest
from graphlca import LCAGraph
from collections import Counter

class LCATest(unittest.TestCase):
    # test for other comparable objects as keys to make sure it still works
    # Sort of unnescary I think but just to test my lca is generalised
    # I feel this is the wrong way to go about it, but dont know right way
    # Better than no check I think

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
        graph.add_edge(4,1)
        self.assertItemsEqual(graph.edges(4),[],"no multiple links or duplicates")

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
        graph.add_edge("2child1","rootchild1")
        self.assertItemsEqual(graph.edges("2child1"),[],"no multiple links or duplicates")
        
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
    
    def test_int_mulitple_nodes_LCA(self):
        graph = LCAGraph()
        root = 1
        graph.add_node(root)
        graph.add_edge(root,2)
        graph.add_edge(root,3)
        graph.add_edge(2,4)
        graph.add_edge(2,5)
        graph.add_edge(3,6)
        graph.add_edge(3,7)
        graph.add_edge(4,8)
        graph.add_edge(4,9)
        graph.add_edge(5,10)
        graph.add_edge(5,11)
        graph.add_edge(6,12)
        graph.add_edge(6,13)
        graph.add_edge(7,14)
        graph.add_edge(7,15)
        self.assertEqual(graph.lowest_common_ancestor(root,[8,9,11,10]),2,
        "4 leaf nodes")
        self.assertEqual(graph.lowest_common_ancestor(root,[8,9,4]),4,
        "2 leaf nodes and parent:expected 4 but got" + 
            str(graph.lowest_common_ancestor(root,[4,8,9])))
        self.assertEqual(graph.lowest_common_ancestor(root,[8,9,12,13,10,11,14,15]),root,
        "8 leaf nodes: expect 1 got" + 
            str(graph.lowest_common_ancestor(root,[4,8,9])))

    def test_string_mulitple_nodes_LCA(self):
        graph = LCAGraph()
        root = "1"
        graph.add_node(root)
        graph.add_edge(root,"2")
        graph.add_edge(root,"3")
        graph.add_edge("2","4")
        graph.add_edge("2","5")
        graph.add_edge("3","6")
        graph.add_edge("3","7")
        graph.add_edge("4","8")
        graph.add_edge("4","9")
        graph.add_edge("5","10")
        graph.add_edge("5","11")
        graph.add_edge("6","12")
        graph.add_edge("6","13")
        graph.add_edge("7","14")
        graph.add_edge("7","15")
        self.assertEqual(graph.lowest_common_ancestor(root,["8","9","11","10"]),"2",
        "4 leaf nodes")
        self.assertEqual(graph.lowest_common_ancestor(root,["8","9","4"]),"4",
        "2 leaf nodes and parent:expected 4 but got" + 
            str(graph.lowest_common_ancestor(root,["4","8","9"])))
        self.assertEqual(graph.lowest_common_ancestor(root,["8","9","12","13","10","11","14","15"]),root,
        "8 leaf nodes: expect 1 got" + 
            str(graph.lowest_common_ancestor(root,["4","8","9"])))

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
