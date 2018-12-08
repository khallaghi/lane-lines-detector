# Lane Lines Detection Project 

## Overview
Detecting lane lines in images or videos using python and opencv. 
This project is a solution for lane line detection project of self-driving car nano degree course in Udacity. 
The GitHub link of project description:
https://github.com/udacity/CarND-LaneLines-P1
The purpose of this project is to build a pipeline to detect lane lines of street. 
In the rest of this documentation every step of pipeline will described briefly. 
To run project first install requirements:
* `pip3 install opencv-python`
* `pip3 install Pillow`
* `pip3 install moviepy`
and then run:
```bash
python3 main.py
```
in the root of project directory 

## Overall Code Structure
The code structure here is so simple:
The main pipeline of project is in `pipeline.py` . 
Each step of pipeline using a helper function that implemented in `helper_funcs.py` using opencv and numpy but at the end of pipeline to aggregate detected lines and draw an average aggregated lines helper functions in `extrapolate.py` used in pipeline. 
The `main.py` file is responsible to convert either image or video to desired output and save them in appropriate location. 

## Main Test Image
![](Lane%20Lines%20Detection%20Project/solidWhiteCurve.jpg)

## Color Correction
At the first step to decrease the error of line detector which made by RGB colors we should turn image to grayscale instead of RGB and use Gaussian blur filter to make the pixel of a shape more like each other and decrease pixels of a shape that may consider as error pixels. 
In `pipeline.py` file there is a `def process_image(image) ` function that get an image and run all the steps of pipeline on it and return an image with overlay of two red line that detects lane lines. 
In `process_image` function the first two step that shown bellow do the above task. 
```python
    # make image gray
    gray_img = helper.grayscale(image)

    # apply  Gaussian blur 
    gauss_img = helper.gaussian_blur(gray_img, 3)
``` 

The reason that `kernel_size` parameter of `gaussian_blur` function set to 3 is by experience odd numbers between 3 to 11 and 3 was the best :D actually there is no firm reason to choose it. :D
Note that we could do plenty of color corrections on this step like turn image to HSL and HSV color space but there is no need to them for this specific project. 


![](Lane%20Lines%20Detection%20Project/solidWhiteCurve%202.jpg)


##  Detecting Edges of Image
In this step simply we detect edges of shapes using Canny algorithm and turn grayscale image to a solid black and white image that contains only edges of shapes. 
```python
# apply Canny transform
canny_img = helper.canny(gauss_img, 100, 200)
```

![](Lane%20Lines%20Detection%20Project/solidWhiteCurve%203.jpg)

## Define Region of Interest
The purpose of project is to find main lines in the street so we don’t need the lines of other lines or mountain or whatever so we cut the image and keep the only a triangle in the middle of picture. 
```python
    # cut out a triangle from image 
    plygn_verts = np.array([[
        [image.shape[1]/2, image.shape[0]/2],
        [image.shape[1], image.shape[0]],
        [0, image.shape[0]]
    ]], dtype=np.int32) 
    roi_img = helper.region_of_interest(canny_img, plygn_verts)
```

![](Lane%20Lines%20Detection%20Project/solidWhiteCurve%204.jpg)

## Detect lines
After above step we should detect only lane lines that obviously they are longer than other unnecessary lines so we use Hough algorithm to detect longest lines and ignore error lines.
According to test images we set `rho` and `theta` to 1 and `np.pi/180` so the accuracy of Hough will be 1 pixel and 1 degree to detect lines and also set `threshold` to 50 `max_line_gap` and `min_line_len` also set to 10 and 20 by experiencing different numbers. 
```python
line_img, lines = helper.hough_lines(roi_img, 1, np.pi/180, 50, 20, 10)
```

![](Lane%20Lines%20Detection%20Project/solidWhiteCurve%205.jpg)


## Extrapolate Lines
At the end we should extrapolate detected lane lines to draw a single line as detected lane line the `lane_lines` function in `extrapolate.py` has the responsibility to give the raw image and detected lines and return extrapolated lines. `draw_lane_line` draw them on the main image. 
The responsibility of `lane_lines` function is to return average detected lines in the right and left of car and return two single lines.  

```python
 # extrapolate and average detected lines and apply the new main line on image
    overlay_img = extrapolate.draw_lane_lines(image, extrapolate.lane_lines(image, lines))
```


![](Lane%20Lines%20Detection%20Project/solidWhiteCurve%206.jpg)
