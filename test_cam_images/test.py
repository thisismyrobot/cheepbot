"""Look for commonalities between the two test images.

The pairs are about 1m apart.

Based on:

    https://docs.opencv.org/3.3.0/dc/dc3/tutorial_py_matcher.html

"""
import cv2
import json


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

    matchesMask = [[0,0] for i in range(len(matches))]
    # ratio test as per Lowe's paper
    for i,(m, n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)

    img3 = cv2.drawMatchesKnn(img_new, kp_new, img_existing, kp_existing, matches, None, **draw_params)
    cv2.imwrite(out, img3)


if __name__ == '__main__':
    go('first.jpg', 'second.jpg', 'matches1.jpg')
    go('third.jpg', 'fourth.jpg', 'matches2.jpg')
