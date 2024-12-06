from msts_and_deadlocks import DisjointSet, Graph, Solution
import pytest
import unittest

class Solution_Class(unittest.TestCase, Solution):
    def test_simple_graph(self):
        g = Graph(4)
        g.add_edge(0, 1, 10)
        g.add_edge(0, 2, 6)
        g.add_edge(0, 3, 5)
        g.add_edge(1, 3, 15)
        g.add_edge(2, 3, 4)
        mst = self.kruskal_mst(g)
        self.assertEqual(len(mst), 3)
        self.assertTrue((2, 3, 4) in mst)
        self.assertTrue((0, 3, 5) in mst)
        self.assertTrue((0, 1, 10) in mst or (0, 2, 6) in mst)

    def test_disconnected_graph(self):
        g = Graph(5)
        g.add_edge(0, 1, 1)
        g.add_edge(2, 3, 2)
        mst = self.kruskal_mst(g)
        self.assertEqual(len(mst), 2)
        self.assertTrue((0, 1, 1) in mst)
        self.assertTrue((2, 3, 2) in mst)

    def test_complete_graph(self):
        g = Graph(4)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 2)
        g.add_edge(0, 3, 3)
        g.add_edge(1, 2, 4)
        g.add_edge(1, 3, 5)
        g.add_edge(2, 3, 6)
        mst = self.kruskal_mst(g)
        self.assertEqual(len(mst), 3)
        self.assertTrue((0, 1, 1) in mst)
        self.assertTrue((0, 2, 2) in mst)
        self.assertTrue((0, 3, 3) in mst)

    def test_acyclic_graph(self):
        g = Graph(4)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 3, 3)
        self.assertFalse(self.is_cyclic(g))


    def test_cyclic_graph(self):
        g = Graph(4)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 3, 3)
        g.add_edge(3, 0, 4)
        self.assertTrue(self.is_cyclic(g))


    def test_disconnected_cyclic_graph(self):
        g = Graph(5)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 0, 3)
        g.add_edge(3, 4, 4)
        self.assertTrue(self.is_cyclic(g))


    def test_self_loop(self):
        g = Graph(3)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 2, 3)
        self.assertTrue(self.is_cyclic(g))


    def test_no_deadlock(self):
        g = Graph(4)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 3, 3)
        self.assertFalse(self.detect_deadlock(g))

    def test_deadlock(self):
        g = Graph(4)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 3, 3)
        g.add_edge(3, 0, 4)
        self.assertTrue(self.detect_deadlock(g))

    def test_complex_deadlock(self):
        g = Graph(5)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 3, 3)
        g.add_edge(3, 4, 4)
        g.add_edge(4, 1, 5)
        self.assertTrue(self.detect_deadlock(g))
        

    def test_multiple_cycles(self):
        g = Graph(6)
        g.add_edge(0, 1, 1)
        g.add_edge(1, 2, 2)
        g.add_edge(2, 0, 3)
        g.add_edge(3, 4, 4)
        g.add_edge(4, 5, 5)
        g.add_edge(5, 3, 6)
        self.assertTrue(self.detect_deadlock(g))