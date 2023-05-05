#!/bin/sh

x_to_y ai < $1 > $1.new_to_old.i
invert_mapping.py --mapping $1.new_to_old.i
