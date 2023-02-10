# image2patch
`image2patch` splits the image in different patches with automatic detection of the best step in order to minimize pixels loss. The overlap between patches depends on the patch size.
Alternatively, it is possible to choose the step size.  
The reconstruction of the original image is possible using `patch2image` which can merge the patches taking into account the overlap percentage among patches. Hence, the original image is perfectly restored. 
If there is a minimum pixels loss during patching procedure, resize to its original dimensions is possible. 

## Example
![pic](example.png)

## Installation
```Python
pip install image2patch
```
```Python
from image2patch import image2patch
```
```Python
from image2patch import patch2image
```
## How to use it
`image2patch(image, patch_size, step=None, verbose=False)`

In particular:
- image : 2D input image
- patch_size : dimension of the window
- step : the distance from one step to another, if =None it will be automatically detected in order to avoid pixels loss. If set = patch_size it will provide patches without overlapping but with pixels loss depending on the size of the input image. 
- verbose : if =True it provides details. 
 

`patch2image(patched_image, original_dims, step, resize_flag = True)`

In particular:
- patched_image : 2D input patches from image2patch
- original_dims : dimension of the original image
- step : step obtained from `image2patch`
- resize_flag : allows to resize the image to its original dimension in case of pixels loss. 

 Citing

    @misc{image2patch2022,
      Author = {Allegri, Giorgio and Pavirani, Luca},
      Title = {image2patch},
      Year = {2022},
      Publisher = {GitHub},
      Journal = {GitHub repository},
      Howpublished = {\url{https://github.com/LucaPavirani/image2patch.py}}
    }
 
## Licence
[MIT](https://choosealicense.com/licenses/mit/)

