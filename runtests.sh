#!/bin/bash

echo "--- Tests for Python 3.6 ---"
python3.6 -m nose -v --with-coverage test/
echo "--- Tests for Python 2.7 ---"
python2.7 -m nose -v --with-coverage test/