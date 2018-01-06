"""Test we are calculating the Region of Interest correctly after padding out
the map.

This is important because that's where the new image sits.
"""
import mapbuilder
from mapbuilder.geometry import map_roi


def test_new_in_top_left_corner():
    new_shape = [20, 20]
    offsets = (-10, -10)

    assert map_roi(new_shape, *offsets) == (0, 20, 0, 20)
