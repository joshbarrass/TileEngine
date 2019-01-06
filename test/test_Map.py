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
