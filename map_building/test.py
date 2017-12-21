"""Look for commonalities between the two test images.

The pairs are about 1m apart.

Based on:

    https://docs.opencv.org/3.3.0/dc/dc3/tutorial_py_matcher.html

"""
import numpy
import cv2
import statistics


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


def add_to_map(img_map, img_new, offset_x, offset_y):
    """Apply a new image to an existing map and return."""
    # Pad out new image to fit map size + offsets.
    img_result = cv2.copyMakeBorder(
        img_new,
        offset_y if offset_y > 0 else 0,
        -offset_y if offset_y < 0 else 0,
        offset_x if offset_x > 0 else 0,
        -offset_x if offset_x < 0 else 0,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0)
    )

    # Overlay the map
    img_result[-offset_y:, -offset_x:] = img_map[0:, 0:]

    # Re-overlay the new, dithered
    out_row_start, out_row_size = 0, img_new.shape[0]
    out_col_start, out_col_size= 0, img_new.shape[1]
    img_result[
        out_row_start:out_row_size:2,
        out_col_start:out_col_size:2,
    ] = img_new[
        out_row_start:out_row_size:2,
        out_col_start:out_col_size:2,
    ]
    img_result[
        out_row_start+1:out_row_size:2,
        out_col_start+1:out_col_size:2,
    ] = img_new[
        out_row_start+1:out_row_size:2,
        out_col_start+1:out_col_size:2,
    ]

    return img_result


def go(existing_map, new, out):
    img_new = cv2.imread(new, 0)  # Taken 1m away.
    img_map = cv2.imread(existing_map, 0)  # Initial/existing/baseline image.

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

    cv2.imwrite(out, img_updated_map)


if __name__ == '__main__':
    go('first.jpg', 'second.jpg', 'combined.png')
