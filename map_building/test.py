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
    return int((size_diff / 2) + offset - size_diff)


def add_to_map(img_map, img_new, offset_x, offset_y):
    """Apply a new image to an existing map and return."""

    # Pad out the map to fit the new image.
    pad_top = max(0, map_pad(img_map.shape[0], img_new.shape[0], -offset_y))
    pad_bottom = max(0, map_pad(img_map.shape[0], img_new.shape[0], offset_y))
    pad_left = max(0, map_pad(img_map.shape[1], img_new.shape[1], -offset_x))
    pad_right = max(0, map_pad(img_map.shape[1], img_new.shape[1], offset_x))
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

    return img_result, (  # Location in the new map of the center of the new image.
        int(map_col_start + (img_new.shape[1] / 2)),
        int(map_row_start + (img_new.shape[0] / 2)),
    )


def step(map_path, img_map, img_new):
    sift = cv2.xfeatures2d.SIFT_create()

    kp_new, des_new = sift.detectAndCompute(img_new, None)
    kp_existing, des_existing = sift.detectAndCompute(img_map, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des_new, des_existing, k=2)

    offset_x, offset_y = offsets(matches, kp_existing, kp_new)

    img_updated_map, (x_center, y_center) = add_to_map(img_map, img_new, offset_x, offset_y)

    print (map_path[-1], (x_center, y_center))

    updated_path = [(int(x - offset_x),
                     int(y - offset_y))
                    for (x, y)
                    in map_path]

#    updated_path = map_path
    updated_path.append((x_center, y_center))

    print((x_center, y_center))

    return updated_path, img_updated_map


def middle_coordinates(img):
    """Return a tuple of (x, y) pixel coordinates."""
    return (
        int(img.shape[1] / 2),
        int(img.shape[0] / 2)
    )


def process_test():

    img_map = None
    map_path = []
    for file in sorted(glob.glob('img/*.jpg'))[:2]:

        if img_map is None:
            img_map = cv2.imread(file, 0)
            map_path.append(middle_coordinates(img_map))
            continue

        img_new = cv2.imread(file, 0)
        map_path, img_map = step(map_path, img_map, img_new)

    idx = 0
    start = map_path.pop(0)
    while True:
        if len(map_path) == 0:
            break
        next = map_path.pop(0)
        cv2.line(img_map, start, next, (255,0,0), 2)
        cv2.putText(img_map,str(idx),start, cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),1,cv2.LINE_AA)
        start = next
        idx += 1
    cv2.putText(img_map,str(idx),start, cv2.FONT_HERSHEY_SIMPLEX, 0.3,(0,0,0),1,cv2.LINE_AA)


    cv2.imwrite('combined.png', img_map)


if __name__ == '__main__':
    process_test()
