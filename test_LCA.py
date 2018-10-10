# PyUnit test code

import unittest
from graphlca import LCAGraph
from collections import Counter

class LCATest(unittest.TestCase):

    # test inserts add edges properly,instantiate and test a graph edges
    def test_insert(self):
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
        self.assertItemsEqual(graph.edges(2),[4],"non-root one child")
        graph.add_edge(4,root)
        self.assertItemsEqual(graph.edges(4),[],"No loops.[]:" + 
        str(graph.edges(4)))
        
    def test_LCA(self):
        graph = LCAGraph()
        root = 1
        graph.add_node(root)
        graph.add_edge(root,2)
        graph.add_edge(root,3)
        graph.add_edge(2,4)
        graph.add_edge(2,5)
        graph.add_edge(3,6)
        graph.add_edge(3,7)
        value = graph.lowest_common_ancestor(root,[4,5])
        self.assertEqual(value,2,
        "two leaf nodes same parent.%nExpected 2 but got " + str(value))
        value = graph.lowest_common_ancestor(root,[4,6])
        result = 1
        self.assertEqual(value,result,
        "two leaf nodes different parent.%n" + str(result) + ":" + str(value))
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
        self.assertIsNone(graph.lowest_common_ancestor(root,[]),
        "Empty node list")
        # checking gives correct answer if two params same
        self.assertEqual(graph.lowest_common_ancestor(root,[1,1]),1,
        "root and both nodes root")
        self.assertEqual(graph.lowest_common_ancestor(root,[2,1]),1,
        "root and child node with lca = root")
        self.assertEqual(graph.lowest_common_ancestor(root,[2,2]),2,
        "child with both nodes child")
    
    def test_mulitple_nodes_LCA(self):
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
        "2 leaf nodes and parent:expected 4 but got " + 
            str(graph.lowest_common_ancestor(root,[4,8,9])))
        self.assertEqual(graph.lowest_common_ancestor(root,[8,9,12,13,10,11,14,15]),root,
        "8 leaf nodes: expect 1 got " + 
            str(graph.lowest_common_ancestor(root,[4,8,9])))

    def test_dag_LCA(self):
        graph = LCAGraph()
        root = 1
        graph.add_node(root)
        graph.add_edge(root,2)
        graph.add_edge(2,3)
        graph.add_edge(2,4)
        graph.add_edge(3,4)
        graph.add_edge(2,5)
        graph.add_edge(3,5)
        self.assertEqual(graph.lowest_common_ancestor(root,[4,5]),3,
            "2 leaf nodes:expected 3 but got " + 
            str(graph.lowest_common_ancestor(root,[4,5])))
        result = graph.lowest_common_ancestor(root,[4,5,3])
        expect = 3
        self.assertEqual(result,expect,"three nodes one parent:" + 
                        str(expect) + ":" + str(result))
        graph.add_edge(root,6)
        result = graph.lowest_common_ancestor(root,[4,5,6])
        expect = root
        self.assertEqual(result,expect,"three leaf nodes different branches:" + 
                        str(expect) + ":" + str(result))
        graph.add_edge(2,7)
        result = graph.lowest_common_ancestor(root,[4,5,7])
        expect = 2
        self.assertEqual(result,expect,"three leaf nodes same parent:" + 
                        str(expect) + ":" + str(result))
        graph.add_edge(6,7)
        graph.add_edge(6,8)
        graph.add_edge(2,8)
        result = graph.lowest_common_ancestor(root,[8,7])
        expect = 2
        self.assertEqual(result,expect,"two lcas-should pick first one:" + 
                        str(expect) + ":" + str(result))
        result = graph.lowest_common_ancestor(root,[7,7])
        expect = 7
        self.assertEqual(result,expect,"Same node twice:" + 
                        str(expect) + ":" + str(result))


if __name__ == "__main__":
    unittest.main()
