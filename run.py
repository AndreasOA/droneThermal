######################################################################
#
# This file should help to understand how the python files and 
# functions can be combined.
#
#######################################################################

import os
from src.DataPipeline.getImagesFromVideo import getImagesFromVideo
from src.DataPipeline.getVideoFromImages import getVideoFromImages
from src.Methods.threshold  import applyFuncToImagColl
from src.Methods.threshold  import drawRectFromThresholdInImage
from src.Methods.threshold_mean  import applyMeanSubtraction
from src.Methods.threshold_mean  import applyFuncToImagColl_WithMean
from src.Methods.threshold_mean import drawRectFromThresholdInImage_new


# STEP 1
# Download the .zip file with all videos from moodle, paste it in the project folder
# and !!!!!EXTRACT IT!!!!!!
# STEP 2
# Convert Video/s to Imagesy
#getImagesFromVideo("data_target_tracking/", ".mp4", "gen")    # For all videos
video_nr = '020'
#getImagesFromVideo(f"data_target_tracking/video_{video_nr}.mp4", ".mp4", "gen")      # For single videos
# STEP 3
# Process images
tol = 0.1 # Threshhold tolerance, only important for this method 
applyFuncToImagColl(drawRectFromThresholdInImage, f"gen/{video_nr}/", f"gen/{video_nr}/func/", (tol, [], [60,60], [], 0))
# STEP 4
# Convert images back to video for presentation
#mean_imgs = applyMeanSubtraction("gen/020/", 0.10)
#applyFuncToImagColl_WithMean(drawRectFromThresholdInImage, "gen/020/", "gen/020/func/", mean_imgs, (tol, [], [30,30], [], 0))


getVideoFromImages(f'gen/{video_nr}/func/', f'video_{video_nr}' ,30)
# Now you should see a new file in the project root folder called pred_video.mp4

# for nr in range(21):
#     applyFuncToImagColl(drawRectFromThresholdInImage, f"gen/{nr:03}/", f"gen/{nr:03}/func/", (tol, [], [60,60], [], 0))
#     # STEP 4
#     # Convert images back to video for presentation
#     getVideoFromImages(f'gen/{nr:03}/func/', f'video_{nr:03}' ,30)

