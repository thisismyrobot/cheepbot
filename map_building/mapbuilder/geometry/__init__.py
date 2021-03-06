"""Image geometry calculation helpers."""

def paddings(shape_map, shape_new, offset_x, offset_y):
    """Work out any paddings needed to be made to a the map shape to fit the
    new shape at the offsets provided.

    The loc_map is the origin in the map for the offsets.
    """
    pad_top = 0
    pad_bottom = 0
    pad_left = 0
    pad_right = 0

    if offset_y < 0:
        pad_top = -offset_y
    elif offset_y > 0:
        height_diff = shape_map[0] - shape_new[0]
        if offset_y > height_diff:
            pad_bottom = offset_y - height_diff

    if offset_x < 0:
        pad_left = -offset_x
    elif offset_x > 0:
        width_diff = shape_map[1] - shape_new[1]
        if offset_x > width_diff:
            pad_right = offset_x - width_diff

    return (
        pad_top,
        pad_bottom,
        pad_left,
        pad_right,
    )


def map_roi(shape_new, offset_x, offset_y):
    """Given a new shape and offsets on the map, return the ROI values."""
    map_row_start = max(offset_y, 0)
    map_row_size = shape_new[0] + max(offset_y, 0)
    map_col_start = max(offset_x, 0)
    map_col_size = shape_new[1] + max(offset_x, 0)

    return (
        map_row_start,
        map_row_size,
        map_col_start,
        map_col_size,
    )
