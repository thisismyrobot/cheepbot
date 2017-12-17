"""Look for commonalities between the two test images.

The pairs are about 1m apart.

Based on:

    https://docs.opencv.org/3.3.0/dc/dc3/tutorial_py_matcher.html

"""
import numpy
import cv2
import statistics


def go(existing, new, out):
    img_new = cv2.imread(new, 0)  # Taken 1m away.
    img_existing = cv2.imread(existing, 0)  # Initial/existing/baseline image.

    sift = cv2.xfeatures2d.SIFT_create()

    kp_new, des_new = sift.detectAndCompute(img_new, None)
    kp_existing, des_existing = sift.detectAndCompute(img_existing, None)

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des_new, des_existing, k=2)

    offsets_x = []
    offsets_y = []
    for i,(m, n) in enumerate(matches):
        if m.distance >= 0.7 * n.distance:
            continue

        existing_x, existing_y = kp_existing[m.trainIdx].pt
        new_x, new_y = kp_new[m.queryIdx].pt

        offsets_x.append(existing_x - new_x)
        offsets_y.append(existing_y - new_y)

    offset_x = statistics.median(offsets_x)
    offset_y = statistics.median(offsets_y)

    alpha_existing = numpy.ones(img_existing.shape, dtype=img_existing.dtype) * 50

    padded_existing = cv2.copyMakeBorder(
        cv2.merge((img_existing, img_existing, img_existing, alpha_existing)),
        int(-offset_y) if offset_y < 0 else 0,
        int(offset_y) if offset_y > 0 else 0,
        int(-offset_x) if offset_x < 0 else 0,
        int(offset_x) if offset_x > 0 else 0,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0, 0)
    )

    alpha_new = numpy.ones(img_new.shape, dtype=img_new.dtype) * 50

    padded_new = cv2.copyMakeBorder(
        cv2.merge((img_new, img_new, img_new, alpha_new)),
        int(offset_y) if offset_y > 0 else 0,
        int(-offset_y) if offset_y < 0 else 0,
        int(offset_x) if offset_x > 0 else 0,
        int(-offset_x) if offset_x < 0 else 0,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0, 0)
    )

    # TODO: Need to actually fade in and out based on how far moved and direction.
    new_background = cv2.addWeighted(padded_existing, 0.5, padded_new, 0.5, 0)

    cv2.imwrite(out, new_background)



if __name__ == '__main__':
    go('first.jpg', 'second.jpg', 'matches1.jpg')
    go('third.jpg', 'fourth.jpg', 'matches2.jpg')
