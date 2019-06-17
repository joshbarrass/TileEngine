#!/usr/bin/env python3.6

## MAP file reader/writer

import math

from Constants import PY_VER

class Map(object):
    def __init__(self, tiles, collisions, version=1):
        self.tiles = tiles
        self.collisions = collisions
        self.VERSION = version

    def __getitem__(self, coord):
        x, y = coord
        if isinstance(y, int):
            return (self.tiles[y][x], self.collisions[y][x])
        if isinstance(y, slice):
            return ([i[x] for i in self.tiles[y]],[i[x] for i in self.collisions[y]])

    def __setitem__(self, coord, value):
        x, y = coord
        if isinstance(value, int) and not isinstance(value, bool):
            value = (value, None)
        elif isinstance(value, bool):
            value = (None, value)
            
        if isinstance(x, int):
            x = slice(x,x+1)
        if isinstance(y, int):
            y = slice(y,y+1)
            
        for i in range(y.start,y.stop,y.step if y.step != None else 1):
            for j in range(x.start,x.stop,x.step if x.step != None else 1):
                self.set_tile((j, i), *value)

    @property
    def width(self):
        return len(self.tiles[0])

    @property
    def height(self):
        return len(self.tiles)

    def __len__(self):
        return self.height * self.width

    def __iter__(self):
        self._iteration_position = [0,0]
        return self

    def __next__(self):
        if self._iteration_position[0] >= self.width:
            self._iteration_position[0] = 0
            self._iteration_position[1] += 1
        if self._iteration_position[1] >= self.height:
            raise StopIteration
        to_return = self[self._iteration_position]
        self._iteration_position[0] += 1
        return to_return

    next = __next__

    def set_tile(self, coord, tile=None, solid=None):
        """Sets a tile to a particular type

        The tile number is changed so that the correct tile can be displayed
        during rendering. The solidity of the tile is also updated to
        determine whether a player can pass through it in-game.

        Parameters
        ----------
        coord : tuple
            Tuple of form (x, y) for the coordinates of the tile to be set
            
        tile : integer
            Tile number to change to
            
        solid : bool
            Whether or not the tile should be considered solid
        """
        x,y = coord
        if tile != None:
            self.tiles[y][x] = tile
        if solid != None:
            self.collisions[y][x] = solid

    def save(self, fp, bytes_per_tile=1):
        """Saves map to file

        File is structured as follows:

        Bytes 0-3:
            Version number (minus 1), unsigned, big-endian (for expansion)
        Byte 4:
            Number of bytes per tile (minus 1), unsigned

        The width and height of the map is then stored. Width is stored first,
        then height.
        These values are split into 7-bit segments (with leading 0s if
        required). They are stored as unsigned big-endian values. The last bit
        of each byte indicates whether the value is finished. If the last bit
        is a 1, the next byte must be read. If the last bit is a 0, this is
        the last byte of the property, and the next byte has a different
        purpose.

        The tile map is then stored, with the number of bytes per coordinate
        coming from the 5th byte of the file.

        The collision map is then stored. This is stored as one bit per tile,
        with additional 0s added to the end if required.

        Parameters
        ----------
        fp : string
            path to file where map will be saved
            
        bytes_per_tile : integer
            number of bytes per tile. Proportional to number of tiles in the tileset
        """

        if bytes_per_tile > 256:
            raise ValueError("bytes_per_tile must be <= 256")

        f = open(fp, "wb")
        f.write(self._number_to_bytes(self.VERSION-1, 4))

        f.write(self._number_to_bytes(bytes_per_tile-1, 1))

        f.write(self._encode_with_terminating_1(self.width))
        f.write(self._encode_with_terminating_1(self.height))

        collisions = ""
        for y in range(self.height):
            for x in range(self.width):
                tile,solid = self[x,y]
                f.write(self._number_to_bytes(tile,bytes_per_tile))
                collisions += "1" if solid else "0"

        f.write(self._binary_list_to_bytes(self._make_binary_list(collisions, prepend=False)))

        f.close()        

    def _to_binary(self,num):
        return bin(num)[2:]

    def _make_binary_list(self,b,bytelength=None,bits=8,prepend=True):
        while len(b) % bits != 0:
            if prepend:
                b = "0"+b
            else:
                b += "0"
        if bytelength != None:
            while len(b) / float(bits) != bytelength:
                if prepend:
                    b = "0"+b
                else:
                    b += "0"
        return [b[i:i+bits] for i in range(0,len(b),bits)]

    def _binary_list_to_bytes(self, l):
        data = [int(i, 2) for i in l]
        return bytes(data) if PY_VER == 3 else bytearray(data)

    def _number_to_bytes(self,number,num_bytes):
        b = self._to_binary(number)
        l = self._make_binary_list(b, bytelength=num_bytes)
        return self._binary_list_to_bytes(l)

    def _encode_with_terminating_1(self, number):
        b = self._to_binary(number)
        l = self._make_binary_list(b, bits=7)
        for i in range(len(l)-1):
            l[i] += "1"
        l[-1] += "0"
        return self._binary_list_to_bytes(l)
    
class MapFile(object):
    def __init__(self, fp):
        self.fp = fp
        
    def load(self):
        f = open(self.fp, "rb")
        version = self._convert_read_to_int(f.read(4)) + 1

        bytes_per_tile = self._convert_read_to_int(f.read(1)) + 1

        width = self._load_with_terminating_1(f)
        height = self._load_with_terminating_1(f)

        tiles = []
        for i in range(height):
            tiles.append([self._convert_read_to_int(f.read(bytes_per_tile)) for j in range(width)])

        c = list(self._str_to_binary(f.read()))
        f.close()

        collisions = [[] for i in range(height)]
        for y in range(height):
            for x in range(width):
                val = c.pop(0)
                if val == "1":
                    collisions[y].append(True)
                elif val == "0":
                    collisions[y].append(False)
        
        f.close()
        return Map(tiles, collisions, version)

    def _convert_read_to_int(self, data):
        if isinstance(data, int):
            return data
        if PY_VER == 3:
            return int.from_bytes(data, "big")
        else:
            b = ""
            for char in data:
                b += bin(ord(char))[2:]
            return int(b, 2)

    def _load_with_terminating_1(self, f):
        # read one byte and check last bit by checking evenness
        total = 0
        while 1:
            data = f.read(1)
            val = self._convert_read_to_int(data)
            total += val >> 1
            if val % 2: # if last bit is 1, do another loop
                continue
            break
        return total

    def _str_to_binary(self, s):
        binary = ""
        for char in s:
            if PY_VER == 2:
                char = ord(char)
            binary += "{0:08b}".format(char)
        return binary

def new(size, tile=0):
    width, height = size
    tiles = [[tile for i in range(width)] for j in range(height)]
    collisions = [[False for i in range(width)] for j in range(height)]
    return Map(tiles, collisions)

def openfile(fp):
    return MapFile(fp)
