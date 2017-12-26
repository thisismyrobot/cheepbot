"""Image geometry calculation helpers."""

def map_pad(dim_map, dim_new, offset):
    """Return a map value from the map size, new image size and offset."""
    size_diff = dim_map - dim_new
    return (size_diff // 2) + offset - size_diff


def paddings(shape_map, shape_new, offset_x, offset_y):
    pad_top = max(0, map_pad(shape_map[0], shape_new[0], -offset_y))
    pad_bottom = max(0, map_pad(shape_map[0], shape_new[0], offset_y))
    pad_left = max(0, map_pad(shape_map[1], shape_new[1], -offset_x))
    pad_right = max(0, map_pad(shape_map[1], shape_new[1], offset_x))
    return (
        pad_top,
        pad_bottom,
        pad_left,
        pad_right,
    )
