"""
image2patch.py module
"""

from .patchutils import patchutils
from typing import Tuple, cast
import numpy as np
import cv2

Imsize = Tuple[int, int]
Stepsize = Tuple[int, int]

def image2patch(image: np.ndarray, patch_size: Imsize, step = None, verbose = False)-> np.ndarray: 
    """
    Divide a 2D image into smaller patches in order to avoid pixels loss. The function finds the best way to split the image with the least overlap.

    Parameters
    ----------
    image: the 2d (m, n) image to be split;
    patch_size: the size of a single patch;
    step: if set to None it automatically detects the best split with overlap and without excluding pixels, otherwise it is possible to choose a fixed step size;
    verbose: if True returns the parameters of interest such as: Number of patches, overlapping pixels, step size and pixels excluded.
    
    Examples
    --------
    >>> image = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    >>> patches, step = image2patch(image, (2, 2), None)  # split image into 2*2 small 2*2 patches with 0 overlap in the x axis and overlap = 1 in the y axis. 0 pixels excluded.
    >>> assert patches.shape == (2, 2, 2, 2)
    """
    return patchutils(image, patch_size, step, verbose)


def patch2image(patched_image: np.ndarray, original_dims: Imsize, step: Stepsize, resize_flag = True) -> np.ndarray:
    """
    Reconstruct original image from the patches. Takes into account the overlap to avoid wrong merge.

    Parameters
    ----------
    patched_image: the patches to be merged. It must come from 2D image (n, m, x, y).
    original_dims: dimensions of the original image.
    step: step used to generate the overlapping patches.
    resize_flag: flag to resize the reconstructed image to its original dimensions. Useful if the patching procedure loses pixels.

    Examples
    --------
    >>> arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    >>> patches, step_ = image2patch(arr, (2, 2))  # split image into 2*2 small 2*2 patches.
    >>> assert patches.shape == (2, 2, 2, 2)
    >>> reconstructed_arr = patch2image(patches, arr.shape, step_)
    >>> assert (reconstructed_arr == arr).all()
    """

    assert len(patched_image.shape) / 2 == len(
        original_dims
    ), "The patches dimension is not equal to the original image size"

    if len(patched_image.shape) == 4:
        return _patch2image(patched_image, cast(Tuple[int, int], original_dims), cast(Tuple[int, int], step), resize_flag)
   
    else:
        raise NotImplementedError(
            "patch2image only supports a matrix of 2D patches (k, l, m, n)"
            f"but got: {patched_image.shape}"
        ) 

def _patch2image(patched_image: np.ndarray, original_dims: Tuple[int, int], step: Tuple[int, int], resize_flag = True) -> np.ndarray:

    assert len(patched_image.shape) == 4

    NpatchesY, NpatchesX, patchY, patchX = patched_image.shape
    stepX, stepY = step
    reconstructed_image = np.empty((stepY*(NpatchesY-1)+patchY, stepX*(NpatchesX-1)+patchX))

    px_0, py_0= 0

    for i_y in range(NpatchesY-1):
        for i_x in range(NpatchesX-1):
            reconstructed_image[py_0:(stepY+(i_y*stepY)), px_0: (stepX+(i_x*stepX))] = patched_image[i_y,i_x][:stepY,:stepX]
            px_0 = stepX+(i_x*stepX)
        px_0 = 0
        py_0 = stepY+(i_y*stepY)

    fpy_0 = 0
    fpx_0 = 0

    # Reconstruction of the last column
    for fi_y in range(NpatchesY-1):
        reconstructed_image[fpy_0:(stepY+(fi_y*stepY)), (stepX+(i_x*stepX)):] = patched_image[fi_y, (NpatchesX-1)][:stepY,:]
        fpy_0 = (stepY+(fi_y*stepY))

    # Reconstruction of the last row
    for fi_x in range(NpatchesX-1):
        reconstructed_image[py_0:py_0+patchX, fpx_0:(stepX+(fi_x*stepX))] = patched_image[(NpatchesY-1), fi_x][:,:stepX]
        fpx_0 = (stepX+(fi_x*stepX))

    # Reconstruction of last patch
    reconstructed_image[fpy_0:, fpx_0:] = patched_image[(NpatchesY-1), (NpatchesX-1)][:,:]

    original_dims = (original_dims[1], original_dims[0])
    
    # Resize to original dimension if resize_flag = True
    if resize_flag:
        reconstructed_image = cv2.resize(reconstructed_image, (original_dims))
    
    return reconstructed_image