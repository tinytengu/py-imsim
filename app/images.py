from PIL import Image
import imagehash

from skimage.metrics import structural_similarity as ssim
import numpy as np
import cv2


def get_similarity(path1: str, path2: str) -> int | float:
    """Get images similarity percentage."""
    hash1 = imagehash.average_hash(Image.open(path1))
    hash2 = imagehash.average_hash(Image.open(path2))
    return 100 - (hash1 - hash2)


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # the lower the error, the more "similar" the two images are
    return err


def get_mse_ssim(path1: str, path2: str) -> (float, float):
    """Get images similarity percentage."""
    im1 = cv2.imread(path1)
    im2 = cv2.imread(path2)

    h1, w1, _ = im1.shape
    h2, w2, _ = im2.shape

    if h1 * w1 > h2 * w2:
        im1 = cv2.resize(im1, (w2, h2), interpolation=cv2.INTER_LINEAR)
    elif h1 * w1 < h2 * w2:
        im2 = cv2.resize(im2, (w1, h1), interpolation=cv2.INTER_LINEAR)

    # cv2.imshow('im1', im1)
    # cv2.waitKey(0)
    # cv2.imshow('im2', im2)
    # cv2.waitKey(0)

    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    try:
        _mse = mse(im1, im2)
    except ValueError:
        _mse = -1

    try:
        _ssim = ssim(im1, im2)
    except ValueError:
        _ssim = -1

    return (_mse, _ssim)
