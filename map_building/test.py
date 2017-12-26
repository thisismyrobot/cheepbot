"""Look for commonalities across sets of images to build a map.

Based on:

    https://docs.opencv.org/3.3.0/dc/dc3/tutorial_py_matcher.html

"""
import enum
import glob
import statistics

import cv2
import numpy


class Paddings(enum.IntEnum):
    Top = 0
    Bottom = 1
    Left = 2
    Right = 3


def offsets(matches, kp_map, kp_new):
    """Given SIFT and knnMatch data, return the offset between the images.

    Assumes some overlap.
    """
    offsets_x = []
    offsets_y = []
    for i,(m, n) in enumerate(matches):
        if m.distance >= 0.7 * n.distance:
            continue

        map_x, map_y = kp_map[m.trainIdx].pt
        new_x, new_y = kp_new[m.queryIdx].pt

        offsets_x.append(map_x - new_x)
        offsets_y.append(map_y - new_y)

    offset_x = int(statistics.median(offsets_x))
    offset_y = int(statistics.median(offsets_y))

    return offset_x, offset_y


def map_pad(dim_map, dim_new, offset):
    """Return a map value from the map size, new image size and offset."""
    size_diff = dim_map - dim_new
    return (size_diff // 2) + offset - size_diff


def calc_paddings(shape_map, shape_new, offset_x, offset_y):
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


def add_to_map(img_map, img_new, offset_x, offset_y):
    """Apply a new image to an existing map and return."""

    # Pad out the map to fit the new image.
    paddings = calc_paddings(img_map.shape, img_new.shape, offset_x, offset_y)
    img_result = cv2.copyMakeBorder(
        img_map,
        paddings[Paddings.Top],
        paddings[Paddings.Bottom],
        paddings[Paddings.Left],
        paddings[Paddings.Right],
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0),
    )

    # Overlay the new image
    map_row_start = max(offset_y, 0)
    map_row_size = img_new.shape[0] + max(offset_y, 0)
    map_col_start = max(offset_x, 0)
    map_col_size = img_new.shape[1] + max(offset_x, 0)
    img_result[
        map_row_start:map_row_size,
        map_col_start:map_col_size,
    ] = img_new[
        0:img_new.shape[0],
        0:img_new.shape[1],
    ]

    return img_result, paddings, (  # Location in the new map of the center of the new image.
        map_col_start + (img_new.shape[1] // 2),
        map_row_start + (img_new.shape[0] // 2),
    )


def shift_path(existing_path, padding_top, padding_left):
    """Move existing points in path based on offsets of new map.

    Because 0, 0 coordinate is in the top-left, on the top and left
    padding moves the existing coordinates.
    """
    return [(x + padding_left, y + padding_top)
            for (x, y)
            in existing_path]


def save_progress(step_index, img_new, kp_new, img_map, kp_map, matches, offset_x, offset_y):
    """Diagnostic-helpers tracking progress."""

    # Basic KNN data.
    matchesMask = [[0,0] for i in range(len(matches))]
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
    step_img = cv2.drawMatchesKnn(
        img_new,
        kp_new,
        img_map,
        kp_map,
        matches,
        None,
        matchColor=(0,255,0),
        singlePointColor=(255,0,0),
        matchesMask=matchesMask,
        flags=0
    )

    # Other info.
    x, y = middle_coordinates(img_new)
    cv2.line(
        step_img,
        (x, y),
        (x + offset_x, y + offset_y),
        (255,0,0),
        2
    )
    cv2.circle(step_img, (x, y), 5, (0,0,255), -1)
    add_text(
        step_img,
        '{}, {}'.format(offset_x, offset_y),
        (x + offset_x, y + offset_y)
    )


    # Save it.
    cv2.imwrite('debug_{}.png'.format(step_index), step_img)


def step(map_path, img_map, img_new, debug=False):
    """Given a new image, update the map and path."""
    sift = cv2.xfeatures2d.SIFT_create()

    kp_new, des_new = sift.detectAndCompute(img_new, None)
    kp_map, des_map = sift.detectAndCompute(img_map, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des_new, des_map, k=2)

    offset_x, offset_y = offsets(matches, kp_map, kp_new)

    img_updated_map, paddings, new_centre = add_to_map(img_map, img_new, offset_x, offset_y)

    map_path = shift_path(map_path, paddings[Paddings.Top], paddings[Paddings.Left])
    map_path.append(new_centre)

    if debug:
        save_progress(
            len(map_path) - 1,
            img_new,
            kp_new,
            img_map,
            kp_map,
            matches,
            offset_x,
            offset_y,
        )

    return map_path, img_updated_map


def middle_coordinates(img):
    """Return a tuple of (x, y) pixel coordinates for the centre of the
    image.
    """
    return (img.shape[1] // 2, img.shape[0] // 2)


def add_text(img, text, location):
    cv2.putText(
        img,
        str(text),
        location,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.3,
        (0, 0, 0),
        1,
        cv2.LINE_AA
    )


def add_overlays(img_map, map_path):
    """Add overlays to the evolving map."""
    idx = 0
    start = map_path.pop(0)
    while True:
        if len(map_path) == 0:
            break
        next = map_path.pop(0)
        cv2.line(img_map, start, next, (255,0,0), 2)
        add_text(img_map, idx, start)
        start = next
        idx += 1
    add_text(img_map, idx, start)


def process_test():

    img_map = None
    map_path = []
    for file in sorted(glob.glob('img/*.jpg')):

        if img_map is None:
            img_map = cv2.imread(file, 0)
            map_path.append(middle_coordinates(img_map))
            continue

        img_new = cv2.imread(file, 0)
        map_path, img_map = step(map_path, img_map, img_new, debug=True)

    add_overlays(img_map, map_path)

    cv2.imwrite('combined.png', img_map)


if __name__ == '__main__':
    process_test()
