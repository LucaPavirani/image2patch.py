"""
adaptivepatch.py module
"""
from .patchutils import patchutils
from typing import Tuple, Union
import numpy as np

Imsize = Union[Tuple[int, int], Tuple[int, int, int]]
def adaptivepatch(image: np.ndarray, patch_size: Imsize, step = None, verbose = False): 
    """
    Divide a 2D or 3D image into smaller patches in order to do not exclude relevant pixels. The function finds the best way to split the image with overlapping.
    Parameters
    ----------
    image: the image to be split. It can be 2d (m, n) or 3d (k, m, n)
    patch_size: the size of a single patch
    step: if set to None it automatically detect the best split with overlapping and without excluding pixels, otherwise it is possible to choose a step size
    verbose: if True returns the parameters of interest as: Number of patches, overlapping pixels, step size and pixels excluded
    Examples
    --------
    >>> image = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    >>> patches = adaptivepatch(image, (2, 2), None)  # split image into 2*2 small 2*2 patches with 0 overlap in the x axis and overlap = 1 in the y axis. 0 pixels excluded.
    >>> assert patches.shape == (2, 2, 2, 2)
    """
    return patchutils(image, patch_size, step, verbose)