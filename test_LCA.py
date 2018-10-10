# PyUnit test code

import unittest
from graphlca import LCAGraph
from collections import Counter

class LCATest(unittest.TestCase):

    # test inserts add edges properly,instantiate and test a graph edges
    def test_insert(self):
        graph = LCAGraph()
        root = TestNums(0)
        graph.add_node(root)

        result = graph.edges(root)
        expect = []
        self.assertItemsEqual(result,expect,"checking when root empty: exp= " + 
                            str(expect) + " res= " + str(result))

        graph.add_edge(root,TestNums(1))
        result = graph.edges(root)
        expect = [TestNums(1)]
        self.assertItemsEqual(result,expect,"root one child: exp= " + 
                            str(expect) + " res= " + str(result))

        result = graph.edges(TestNums(1))
        expect = []
        self.assertItemsEqual(result,expect,"leaf node: exp= " + 
                            str(expect) + " res= " + str(result))

        graph.add_edge(root,TestNums(1))
        result = graph.edges(root)
        expect = [TestNums(1)]
        self.assertItemsEqual(result,expect,"no duplicate edges: exp= " + 
                            str(expect) + " res= " + str(result))

        graph.add_edge(root,TestNums(2))
        result = graph.edges(root)
        expect = [TestNums(1),TestNums(2)]
        self.assertItemsEqual(result,expect,"root two children: exp= " + 
                            str(expect) + " res= " + str(result))

        graph.add_edge(TestNums(1),TestNums(3))
        graph.add_edge(TestNums(1),TestNums(5))
        graph.add_edge(TestNums(2),TestNums(4))
        result = graph.edges(TestNums(1))
        expect = [TestNums(5),TestNums(3)]
        self.assertItemsEqual(result,expect,"non-root two children: exp= " + 
                            str(expect) + " res= " + str(result))

        result = graph.edges(TestNums(2))
        expect = [TestNums(4)]
        self.assertItemsEqual(result,expect,"non-root one child: exp= " + 
                            str(expect) + " res= " + str(result))
 
        graph.add_edge(TestNums(4),root)
        result = graph.edges(TestNums(4))
        expect = []
        self.assertItemsEqual(result,expect,"No loops: exp= " + 
                            str(expect) + " res= " + str(result))
        
    def test_LCA(self):
        graph = LCAGraph()
        root = TestNums(1)
        graph.add_node(root)
        graph.add_edge(root,TestNums(2))
        graph.add_edge(root,TestNums(3))
        graph.add_edge(TestNums(2),TestNums(4))
        graph.add_edge(TestNums(2),TestNums(5))
        graph.add_edge(TestNums(3),TestNums(6))
        graph.add_edge(TestNums(3),TestNums(7))
        result = graph.lowest_common_ancestor(root,[TestNums(4),TestNums(5)])
        expect = TestNums(2)
        self.assertEqual(result,expect,"two leaf nodes same parent: exp= " 
                        + str(expect) + " res= " + str(result))

        result = graph.lowest_common_ancestor(root,[TestNums(4),TestNums(6)])
        expect = TestNums(1)
        self.assertEqual(result,expect,"two leaf nodes different parent: exp= " 
                        + str(expect) + " res= " + str(result))

        result = graph.lowest_common_ancestor(root,[TestNums(3),TestNums(4)])
        expect = TestNums(1)
        self.assertEqual(result,expect,"one leaf node and one non-leaf node: exp= " 
                        + str(expect) + " res= " + str(result))

        result = graph.lowest_common_ancestor(root,[TestNums(2),TestNums(4)])
        expect = TestNums(2)
        self.assertEqual(result,expect,"parent and child leaf node: exp= " 
                        + str(expect) + " res= " + str(result))

        result = graph.lowest_common_ancestor(root,[TestNums(1),TestNums(4)])
        expect = TestNums(1)
        self.assertEqual(result,expect,"leaf node and root with params swapped: exp= " 
                        + str(expect) + " res= " + str(result))
        
        graph.add_node(TestNums(9))
        # checking doesnt give false positives
        self.assertIsNone(
            graph.lowest_common_ancestor(root,[TestNums(2),TestNums(8)]),
            "lca non-existent node")
        
        self.assertIsNone(
            graph.lowest_common_ancestor(root,[TestNums(1),TestNums(9)]),
            "lca disconnected node")

        self.assertIsNone(
            graph.lowest_common_ancestor(TestNums(2),[TestNums(3),TestNums(6)]),
            "Doesnt recurse past root and treats as seperate components")

        self.assertIsNone(
            graph.lowest_common_ancestor(root,[]),
            "Empty node list")
        
        # checking gives correct answer if two params same
        result = graph.lowest_common_ancestor(root,[TestNums(1),TestNums(1)])
        expect = TestNums(1)
        self.assertEqual(result,expect,"root and both nodes root: exp= " 
                        + str(expect) + " res= " + str(result))
        
        result = graph.lowest_common_ancestor(root,[TestNums(2),TestNums(1)])
        expect = TestNums(1)
        self.assertEqual(result,expect,"root and child node with lca = root: exp= " 
                        + str(expect) + " res= " + str(result))
        
        result = graph.lowest_common_ancestor(root,[TestNums(2),TestNums(2)])
        expect = TestNums(2)
        self.assertEqual(result,expect,"child with both nodes child: exp= " 
                        + str(expect) + " res= " + str(result))
    
    def test_mulitple_nodes_LCA(self):
        graph = LCAGraph()
        root = TestNums(1)
        graph.add_node(root)
        graph.add_edge(root,TestNums(2))
        graph.add_edge(root,TestNums(3))
        graph.add_edge(TestNums(2),TestNums(4))
        graph.add_edge(TestNums(2),TestNums(5))
        graph.add_edge(TestNums(3),TestNums(6))
        graph.add_edge(TestNums(3),TestNums(7))
        graph.add_edge(TestNums(4),TestNums(8))
        graph.add_edge(TestNums(4),TestNums(9))
        graph.add_edge(TestNums(5),TestNums(10))
        graph.add_edge(TestNums(5),TestNums(11))
        graph.add_edge(TestNums(6),TestNums(12))
        graph.add_edge(TestNums(6),TestNums(13))
        graph.add_edge(TestNums(7),TestNums(14))
        graph.add_edge(TestNums(7),TestNums(15))
        result = graph.lowest_common_ancestor(
            root,[TestNums(8),TestNums(9),TestNums(11),TestNums(10)])
        expect = TestNums(2)
        self.assertEqual(result,expect,"4 leaf nodes: exp= " 
                        + str(expect) + " res= " + str(result))
        
        result = graph.lowest_common_ancestor(root,[TestNums(8),TestNums(9),TestNums(4)])
        expect = TestNums(4)
        self.assertEqual(result,expect,"2 leaf nodes and parent: exp= " 
                        + str(expect) + " res= " + str(result))

        result = graph.lowest_common_ancestor(
            root,[TestNums(8),TestNums(9),TestNums(12),TestNums(13),
            TestNums(10),TestNums(11),TestNums(14),TestNums(15)])
        expect = root
        self.assertEqual(result,expect,"8 leaf nodes: exp= " 
                        + str(expect) + " res= " + str(result))

    def test_dag_LCA(self):
        graph = LCAGraph()
        one = TestNums(TestNums(1))
        root = one
        graph.add_node(root)
        graph.add_edge(root,TestNums(2))
        graph.add_edge(TestNums(2),TestNums(3))
        graph.add_edge(TestNums(2),TestNums(4))
        graph.add_edge(TestNums(3),TestNums(4))
        graph.add_edge(TestNums(2),TestNums(5))
        graph.add_edge(TestNums(3),TestNums(5))
        self.assertEqual(graph.lowest_common_ancestor(root,[TestNums(4),TestNums(5)]),TestNums(3),
            "TestNums(2) leaf nodes:expected TestNums(3) but got " + 
            str(graph.lowest_common_ancestor(root,[TestNums(4),TestNums(5)])))
        result = graph.lowest_common_ancestor(root,[TestNums(4),TestNums(5),TestNums(3)])
        expect = TestNums(3)
        self.assertEqual(result,expect,"three nodes one parent:" + 
                        str(expect) + ":" + str(result))
        graph.add_edge(root,TestNums(6))
        result = graph.lowest_common_ancestor(root,[TestNums(4),TestNums(5),TestNums(6)])
        expect = root
        self.assertEqual(result,expect,"three leaf nodes different branches:" + 
                        str(expect) + ":" + str(result))
        graph.add_edge(TestNums(2),TestNums(7))
        result = graph.lowest_common_ancestor(root,[TestNums(4),TestNums(5),TestNums(7)])
        expect = TestNums(2)
        self.assertEqual(result,expect,"three leaf nodes same parent:" + 
                        str(expect) + ":" + str(result))
        graph.add_edge(TestNums(6),TestNums(7))
        graph.add_edge(TestNums(6),TestNums(8))
        graph.add_edge(TestNums(2),TestNums(8))
        result = graph.lowest_common_ancestor(root,[TestNums(8),TestNums(7)])
        expect = TestNums(2)
        self.assertEqual(result,expect,"two lcas-should pick first one:" + 
                        str(expect) + ":" + str(result))
        result = graph.lowest_common_ancestor(root,[TestNums(7),TestNums(7)])
        expect = TestNums(7)
        self.assertEqual(result,expect,"Same node twice:" + 
                        str(expect) + ":" + str(result))

class TestNums(object):
    # Test object, also implements str for easy debugging in unit test
    # Can prove it works generally for all classes that implement eq and hash
    # By using dummy object as parameter
    def __init__(self,value):
        self.value =  value
    
    def __eq__(self,other):
        if isinstance(other, self.__class__):
            return self.value == other.value
    
    def __str__(self):
        return str(self.value)
    
    def __hash__(self):
        return hash(self.value)


if __name__ == "__main__":
    unittest.main()
