# Thermal video target detection

![Example detection](https://public-files.gumroad.com/vl10vhq81zqu0gcjgekqlkr88kw9)

As a university course project we tried to find a method, which is capable of detecting moving persons in a forest with a static drone and a thermal camera. We used YoloV5 and achieved good results in the areas, where the target was fully visible. In the partly and fully occluded areas Yolo is definetly not the right choice, since the model has no chance in finding the human. Some kind of preprocessing is necessary to remove the occlusion.

[Prediction Video 1](https://youtu.be/_aqjhaKmv0g)

[Prediction Video 2](https://youtu.be/REYJ9RAcxq0)

## Implementation details

### Training the model:

The code for training the model is not included here, but is done based on the pretrained [Yolo Model](https://github.com/ultralytics/yolov5). Our final dataset includes about 5k images from the following provided videos. These 5k annotated images were then extendet to about 330k images through data-augmentation.

The following methods were used for that: 
- image-rotation
- blurring (gaussian, poisson, speckle)
- random-brightness-change

For our model we used the medium sized yolov5 model and the medium augmentation configuration of the model itself.
This produced our best.pt model weights.

### Detection/Tracing:

For the detection/tracing part we modified the detect.py and plots.py from the above mentioned pretrained Yolo Model.
The modifications:
- Removing the default target display (box + conf + label)
- Added fixed sized target bounding boxes
- Added method for storing the paths of targets
- Added method to draw the trace paths betweeen closest points (differ between mulitple targets)
- Added method to draw box for lost targets in area of previous appearance
- Added target reset if target is not moving after certain amount of time (if no movement detected = probably a tree) or if target is lost for too long (search for target outside of search area)

Based on these modifications and adaptations we implemented following hyperparameters:
- Confidence: float value
- ignore_target_threshold: int value, After how many frames the target is ignored, if there is no movement detected at all. Movement is based on the hyperparameter target_moving_tolerance.
- target_moving_tolerance: int value, Defines the moving tolerance for the drone and trees. Every movement in the range of this value in pixels is not recogniced as movement.
- extended_box_size: int value, Defines the area in which the target is assosiated as the previous target if it is lost.
- draw_path_threshold: int value, Defines after how many frames the path gets drawn/updated. Lower value leads to more precision of the paths, but need more computationpower and probably leads to a more shaky path.