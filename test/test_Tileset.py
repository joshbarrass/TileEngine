#!/usr/bin/env python3.6

## Map test file

import unittest
import Map, Tileset

class MapTests(unittest.TestCase):
        
    def test_load(self):
        ts = Tileset.openfile("test/testtiles.png", 20, 20)
        self.assertEqual(len(ts), 25)
        self.assertEqual(ts.tilewidth, 20)
        self.assertEqual(ts.tileheight, 20)
        self.assertEqual(ts.mode, "RGBA")
        pix = ts[0].load()
        self.assertEqual(pix[0,0], (0,0,0,255))
        pix = ts[24].load()
        self.assertEqual(pix[0,0], (255,255,255,255))
        
    def test_render(self):
        m = Map.new((100,100), 24)
        m[25:75,25:75] = (8, True)
        m[26:74,26:74] = (7, True)
        m[27:73,27:73] = (14, False)

        ts = Tileset.openfile("test/testtiles.png", 20, 20)
        im = ts.render_map_to_image(m)
        pix = im.load()

        self.assertEqual(pix[1000,1000], (0,255,33,255))
        self.assertEqual(pix[0,0], (255,255,255,255))

    def test_coordinate(self):
        ts = Tileset.openfile("test/testtiles.png", 20, 20)
        self.assertEqual(ts.get_index_from_coord((0,0)), 0)
        self.assertEqual(ts.get_index_from_coord((1,2)), 11)
