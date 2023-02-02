import cv2
import os



def getVideoFromImages(path: str, name: str, fps: int):
    """Function convertes all images in path (based on the sorting in explorer) to Video.

    Args:
        path (str): Path to images
        name (str): Name of the generated video
        fps (int): Frames per second for the newly created video
    """
    images = [img for img in os.listdir(path) if img.endswith(".jpg")]
    images.sort()
    frame = cv2.imread(os.path.join(path, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(f'{name}.mp4', fourcc, fps, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(path, image)), )

    cv2.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    getVideoFromImages('gen/001/func/', 30)