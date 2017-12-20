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

    offset_x = int(statistics.median(offsets_x))
    offset_y = int(statistics.median(offsets_y))

    # Pad out existing with transparency.
    img_existing = cv2.copyMakeBorder(
        img_existing,
#        cv2.cvtColor(img_existing, cv2.COLOR_GRAY2RGBA),
        -offset_y if offset_y < 0 else 0,
        offset_y if offset_y > 0 else 0,
        -offset_x if offset_x < 0 else 0,
        offset_x if offset_x > 0 else 0,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0)
    )

    # position
    if offset_x < 0:
        # New is out to left.
        if offset_y < 0:
            # New is out above
            img_existing[0:offset_y, 0:-offset_x] = img_new[0:, 0:-offset_x]
            img_existing[0:-offset_y, -offset_x:] = img_new[0:-offset_y, 0:]


    cv2.imwrite(out, img_existing)


    # Pad out new with transparency.
#    img_new = cv2.copyMakeBorder(
#        cv2.cvtColor(img_new, cv2.COLOR_GRAY2RGBA),
#        int(offset_y) if offset_y > 0 else 0,
#        int(-offset_y) if offset_y < 0 else 0,
#        int(offset_x) if offset_x > 0 else 0,
#        int(-offset_x) if offset_x < 0 else 0,
#        cv2.BORDER_CONSTANT,
#        value=(0, 0, 0, 0)
#    )

#    img_result = cv2.addWeighted(img_new, 0.5, img_existing, 0.5, 0)

#    cv2.imwrite(out, img_result)


if __name__ == '__main__':
    go('first.jpg', 'second.jpg', 'matches1.png')
