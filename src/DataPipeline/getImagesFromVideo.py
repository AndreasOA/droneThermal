import cv2
from os import walk, path
import os


def getImagesFromVideo(path: str, file_ending: str, new_folder: str):
    """Master function, finds all file_ending files in path and converts them to images within new_folder

    Args:
        path (str): Path to videos or path + filename for just one video
        file_ending (str): File ending, e.g: .jpg
        new_folder (str): Name for new folder. Root folder for converted images
    """
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    if path[-3:] != "mp4":
        path = path if path[-1] ==  "/" or path[-1] ==  "\\" else path + "/"
        files = [file for file in os.listdir(path) if file.endswith(file_ending)]
        for file in files:
            print(file)
            convertVideo(path + file, file.split('_')[1].split('.')[0])
    else:
        print(path)
        convertVideo(path, path.split('/')[-1].split('.')[0].split("_")[1])






def convertVideo(filename: str, file_nr: str):
    """This function takes a video file and file number as input and splits it in multiple frames.
    Frames are stored in a folder called *file_nr*

    Args:
        filename (str): Name of file in data_target_tracking folder
        file_nr (str): Folder name for video frames
    """
    vidcap = cv2.VideoCapture(filename)
    success,image = vidcap.read()
    if not os.path.exists("gen/" + file_nr):
        os.makedirs("gen/" + file_nr)
    count = 0
    while success:
        cv2.imwrite(f"gen/{file_nr}/frame{count:06}.jpg", image)     # save frame as JPG file      
        success,image = vidcap.read()
        count += 1


if __name__ == "__main__":
    getImagesFromVideo("data_target_tracking/", ".jpg", "gen")