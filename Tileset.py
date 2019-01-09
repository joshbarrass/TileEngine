#!/usr/bin/env python3.6

## Tileset loader

# going to use PIL for now and adapt to pygame

from PIL import Image

from Constants import PY_VER

class Tileset(object):
    def __init__(self, tiles):
        self.tiles = tiles
        first = tiles[0]
        self.mode = first.mode
        self.tilewidth = first.width
        self.tileheight = first.height

    def __getitem__(self, tile):
        return self.tiles[tile]

    def render_map_to_image(self,m):
        size = (self.tilewidth*m.width, self.tileheight*m.height)
        im = Image.new(self.mode, size)

        for y in range(m.height):
            for x in range(m.width):
                tile = m[x,y][0]
                im.paste(self[tile], (x*self.tilewidth,y*self.tilewidth))

        return im


def openfile(fp,tilewidth,tileheight):
    im = Image.open(fp)
    imw, imh = im.size
    tiles = []
    for y in range(0, imh, tileheight):
        for x in range(0, imw, tilewidth):
            crop = (x, y, x+tilewidth, y+tileheight)
            tiles.append(im.crop(crop))
            
    return Tileset(tiles)
