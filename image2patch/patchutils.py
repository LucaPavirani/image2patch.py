# The code is inspired by https://github.com/scikit-image/scikit-image/blob/main/skimage/util/shape.py
#
# Copyright (C) 2011, the scikit-image team All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# Neither the name of skimage nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import numpy as np
import numbers
from numpy.lib.stride_tricks import as_strided
import math

def findstep(image, patch_size, step, verbose):
    '''
    Takes the shape of the image and find the minimum overlap in order to obtain the best number of patches excluding the least number of pixels. 
    '''
    
    X = image.shape[0] 
    Y = image.shape[1]
    patch_size_x, patch_size_y = patch_size 
    
    # Number of patches: this number is lower except if the size is a multiple of the patch size
    N_patches_x = X//patch_size_x
    N_patches_y = Y//patch_size_y

    # Useful only when a step = None is given
    diff_y = Y - patch_size_y*N_patches_y
    ovr_pixel_y = math.ceil((patch_size_y - diff_y) / N_patches_y)
    diff_x = X - patch_size_x*N_patches_x
    ovr_pixel_x = math.ceil((patch_size_x - diff_x) / N_patches_x)

    # Step calculation on the y-axis
    if step == None: 
      if Y%patch_size_y == 0:
        step_y = patch_size_y
      else:
        step_y = patch_size_y - ovr_pixel_y
    else:
        step_y = step

    # Step calculation on the x-axis
    if step == None: 
      if X%patch_size_x == 0:
        step_x = patch_size_x
      else:
        step_x = patch_size_x - ovr_pixel_x
    else:
        step_x = step

    # Updated number of patching keeping the overlap due to the step size 
    N_patches_x = (X - patch_size_x) // step_x + 1
    N_patches_y = (Y - patch_size_y) // step_y + 1

    # Overlapping pixels
    overlapX = (patch_size_x - step_x) * (N_patches_x-1)
    overlapY = (patch_size_y - step_y) * (N_patches_y-1)

    if verbose == True:
    
        lost_pixel_y = (Y - (patch_size_y*(N_patches_y) - overlapY))
        lost_pixel_x = (X - (patch_size_x*(N_patches_x) - overlapX))
        
        print('Number of patches obtained: ', N_patches_x,', ',N_patches_y)
        print('Step along y axis:', step_x, ', x axis:', step_y)
        print(f"Overlapping pixels in y: {overlapX}/{X}, x: {overlapY}/{Y}")
        print(f"Lost pixels in y axis: {lost_pixel_x}/{X}, x axis: {lost_pixel_y}/{Y}")
            
    return step_x, step_y

def patchutils(img, patch_size, step, verbose):
    '''
    Apply a window step based on findstep in the x direction and y direction.
    '''
    num_dim = img.ndim

    # Check the input 
    if not isinstance(img, np.ndarray):
        raise TypeError("`img` must be a numpy ndarray")

    if isinstance(patch_size, numbers.Number):
        patch_size = (patch_size,) * num_dim
    if not (len(patch_size) == num_dim):
        raise ValueError("`patch_size` is incompatible with `img.shape`")

    step_x_axis, step_y_axis = findstep(img, patch_size, step, verbose)
    step = (step_y_axis, step_x_axis)

    if isinstance(step_x_axis, numbers.Number):
        if step_x_axis < 1:
            raise ValueError("`step_x` must be >= 1")
        step_x_axis = (step_x_axis,) * num_dim
    if isinstance(step_y_axis, numbers.Number):
        if step_y_axis < 1:
            raise ValueError("`step_y` must be >= 1")
        step_y_axis = (step_y_axis,) * num_dim

    if len(step_x_axis) != num_dim:
        raise ValueError("`step_x` is incompatible with `img.shape`")
    if len(step_y_axis) != num_dim:
        raise ValueError("`step_y` is incompatible with `img.shape`")

    arr_shape = np.array(img.shape)
    patch_size = np.array(patch_size, dtype=arr_shape.dtype)

    if ((arr_shape - patch_size) < 0).any():
        raise ValueError("`patch_size` is too large")

    if ((patch_size - 1) < 0).any():
        raise ValueError("`patch_size` is too small")

    # Create moving window 
    slicesx = tuple(slice(None, None, st) for st in step_x_axis)
    slicesy = tuple(slice(None, None, st2) for st2 in step_y_axis)

    tot_slices = []
    tot_slices.append(slicesx[0])
    tot_slices.append(slicesy[0])

    patch_strides = np.array(img.strides)
    strides_index = img[tuple(tot_slices)].strides

    win_indices_shape_x = (img.shape[0]- patch_size[0]) // step_x_axis[0] + 1
    win_indices_shape_y = (img.shape[1]- patch_size[1]) // step_y_axis[0] + 1

    final_patch=[]
    final_patch.append(win_indices_shape_x)
    final_patch.append(win_indices_shape_y)

    final_shape = tuple(list(final_patch) + list(patch_size))
    strides = tuple(list(strides_index) + list(patch_strides))

    output = as_strided(img, shape=final_shape, strides=strides)

    return output, step