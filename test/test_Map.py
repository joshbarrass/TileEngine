#!/usr/bin/env python3.6

## Map test file

import unittest
import Map
import os

class MapTests(unittest.TestCase):
        
    def test_new(self):
        m = Map.new((10,5), 0)
        self.assertEqual(m.width, 10)
        self.assertEqual(m.height, 5)
        self.assertEqual(sum([sum(i) for i in m.tiles]),0)
        self.assertEqual(sum([sum(i) for i in m.collisions]),0)

    def test_set_tile(self):
        m = Map.new((10,5), 0)
        m.set_tile((5,2), 12, True)
        self.assertEqual(m[5,2], (12, True))
        m.set_tile((5,3), 11, False)
        self.assertEqual(m[5,3], (11, False))

    def test_setitem(self):
        m = Map.new((10,5), 0)
        m[5,2] = (12, True)
        self.assertEqual(m[5,2], (12, True))
        m[5,3] = 13
        self.assertEqual(m[5,3], (13, False))
        m[5,4] = True
        self.assertEqual(m[5,4], (0, True))

    def test_save_and_open_file(self):
        m = Map.new((10,5), 0)
        m.set_tile((5,2), 12, True)
        self.assertEqual(m[5,2], (12, True))
        m.save("tempmap.tmp")
        mf = Map.openfile("tempmap.tmp")
        n = mf.load()
        self.assertEqual(m.tiles, n.tiles)
        self.assertEqual(m.collisions, n.collisions)

    def tearDown(self):
        if os.path.isfile("tempmap.tmp"):
            os.remove("tempmap.tmp")

    def test_len(self):
        m = Map.new((10,5), 0)
        self.assertEqual(len(m), 50)

    def test_iterating(self):
        m = Map.new((2,2), 0)
        m[0,0] = 1
        l = [i for i in m]
        self.assertEqual(l, [(1,False), (0,False),
                             (0,False), (0,False)])

    def test_get_slice(self):
        m = Map.new((3,3), 0)
        m[0,0] = (1, True)
        self.assertEqual(m[0:2,0], ([1,0],[True,False]))
        self.assertEqual(m[0,0:2], ([1,0],[True,False]))
        self.assertEqual(m[0:2,0:2], ([[1,0],[0,0]],[[True,False],[False,False]]))

    def test_set_slice(self):
        m = Map.new((3,3), 0)
        m[0:2,0] = (1, True)
        self.assertEqual(m[0:2,0], ([1,1],[True,True]))
        m[0,0:2] = (1, True)
        self.assertEqual(m[0,0:2], ([1,1],[True,True]))
        m[0:2,0:2] = (2, False)
        self.assertEqual(m[0:2,0:2], ([[2,2],[2,2]],[[False,False],[False,False]]))
        
        
