"""Test we are calculating the paddings added to the map for a set of offsets.
"""
import mapbuilder
from mapbuilder.geometry import paddings


def test_same_size_box_moving_up():
    map_shape = [20, 20]
    new_shape = [20, 20]
    offsets = (0, -10)

    assert paddings(map_shape, new_shape, *offsets) == (10, 0, 0, 0)


def test_same_size_box_moving_down():
    map_shape = [20, 20]
    new_shape = [20, 20]
    offsets = (0, 10)

    assert paddings(map_shape, new_shape, *offsets) == (0, 10, 0, 0)


def test_same_size_box_moving_left():
    map_shape = [20, 20]
    new_shape = [20, 20]
    offsets = (-10, 0)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 10, 0)


def test_same_size_box_moving_right():
    map_shape = [20, 20]
    new_shape = [20, 20]
    offsets = (10, 0)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 10)


def test_smaller_box_contained_moving_up_and_staying_contained():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (0, -2)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 0)


def test_smaller_box_contained_moving_down_and_staying_contained():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (0, 2)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 0)


def test_smaller_box_contained_moving_left_and_staying_contained():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (-2, 0)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 0)


def test_smaller_box_contained_moving_right_and_staying_contained():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (2, 0)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 0)


def test_smaller_box_contained_moving_up_and_just_staying_contained():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (0, -5)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 0)


def test_smaller_box_contained_moving_down_and_just_staying_contained():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (0, 5)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 0)


def test_smaller_box_contained_moving_left_and_just_staying_contained():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (-5, 0)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 0)


def test_smaller_box_contained_moving_right_and_just_staying_contained():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (0, 5)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 0)


def test_smaller_box_contained_moving_up_and_exceeding_container():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (0, -6)

    assert paddings(map_shape, new_shape, *offsets) == (1, 0, 0, 0)


def test_smaller_box_contained_moving_down_and_exceeding_container():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (0, 6)

    assert paddings(map_shape, new_shape, *offsets) == (0, 1, 0, 0)


def test_smaller_box_contained_moving_left_and_exceeding_container():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (-6, 0)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 1, 0)


def test_smaller_box_contained_moving_up_and_exceeding_container():
    map_shape = [20, 20]
    new_shape = [10, 10]
    offsets = (6, 0)

    assert paddings(map_shape, new_shape, *offsets) == (0, 0, 0, 1)
