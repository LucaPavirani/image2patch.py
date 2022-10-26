# adaptivepatch
adaptivepatch can split the image in different patches with automatic detection of the best step in order to do not lose pixels. The overlap between patches depends on the patch size. 

## Example
![pic](example.png)

## Installation
```Python
pip install adaptivepatch
```
## How to use it
`adaptivepatch(image, patch_size, step=None, verbose=False)`

In particular:
- image : input image which can be a 2D or 3D array
- patch_size : dimension of the window
- step : the distance from one step to another, if =None it will be automatically detected in order to avoid pixels loss. If set = patch_size it will provide patches without overlapping but with pixels loss depending on the input image. 
- verbose : if =True it provides details. 
 
## Licence
[MIT](https://choosealicense.com/licenses/mit/)

