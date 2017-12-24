"""Look for commonalities across sets of images to build a map.

Based on:

    https://docs.opencv.org/3.3.0/dc/dc3/tutorial_py_matcher.html

"""
import glob
import statistics

import cv2
import numpy


def offsets(matches, kp_existing, kp_new):
    """Given SIFT and knnMatch data, return the offset between the images.

    Assumes some overlap.
    """
    offsets_x = []
    offsets_y = []
    for i,(m, n) in enumerate(matches):
        if m.distance >= 0.7 * n.distance:
            continue

        existing_x, existing_y = kp_existing[m.trainIdx].pt
        new_x, new_y = kp_new[m.queryIdx].pt

        offsets_x.append(existing_x - new_x)
        offsets_y.append(existing_y - new_y)

    offset_x = int(statistics.median(offsets_x))
    offset_y = int(statistics.median(offsets_y))

    return offset_x, offset_y


def map_pad(dim_map, dim_new, offset):
    """Return a map value from the map size, new image size and offset."""
    size_diff = dim_map - dim_new
    return max(0, int((size_diff / 2) + offset - size_diff))


def add_to_map(img_map, img_new, offset_x, offset_y):
    """Apply a new image to an existing map and return."""

    # Pad out the map to fit the new image.
    pad_top = map_pad(img_map.shape[0], img_new.shape[0], -offset_y)
    pad_bottom = map_pad(img_map.shape[0], img_new.shape[0], offset_y)
    pad_left = map_pad(img_map.shape[1], img_new.shape[1], -offset_x)
    pad_right = map_pad(img_map.shape[1], img_new.shape[1], offset_x)
    img_result = cv2.copyMakeBorder(
        img_map,
        pad_top,
        pad_bottom,
        pad_left,
        pad_right,
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

    return img_result


def step(img_map, img_new):
    sift = cv2.xfeatures2d.SIFT_create()

    kp_new, des_new = sift.detectAndCompute(img_new, None)
    kp_existing, des_existing = sift.detectAndCompute(img_map, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des_new, des_existing, k=2)

    offset_x, offset_y = offsets(matches, kp_existing, kp_new)

    img_updated_map = add_to_map(img_map, img_new, offset_x, offset_y)

    return img_updated_map


def process_test():

    img_map = None
    for file in glob.glob('img/*.jpg'):

        if img_map is None:
            img_map = cv2.imread(file, 0)
            continue

        img_new = cv2.imread(file, 0)
        img_map = step(img_map, img_new)

    cv2.imwrite('combined.png', img_map)


if __name__ == '__main__':
    process_test()
