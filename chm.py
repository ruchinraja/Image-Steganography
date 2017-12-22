import sys

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
from skimage.measure import structural_similarity
import numpy as np
import math

def main():
    file1, file2 = sys.argv[1:1+2]
    # read images as 2D arrays (convert to grayscale for simplicity)
    img1 = to_grayscale(imread(file1).astype(float))
    img2 = to_grayscale(imread(file2).astype(float))
    # compare
    n_m, n_0 = compare_images(img1, img2)
    #n_mse = mse(imread(file1),imread(file2))
    n_mse = mse(img1, img2)
    n_psnr = PSNR(n_mse)
    n_ssim = structural_similarity(img1, img2)
    print "Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size
    print "Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size
    print "Mean Square Error:", n_mse
    print "Peak Signal to Noise Ratio:", n_psnr
    print "SSIM:", n_ssim

def compare_images(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)

def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

def mse(imageA, imageB):
	err = np.sum((imageA.astype("float")-imageB.astype("float"))**2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	return err

def PSNR(mse):
	return 20 * math.log10(255 / math.sqrt(mse)) 

if __name__ == "__main__":
    main()
