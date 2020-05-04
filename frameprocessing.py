import cv2
import glob
from PIL import Image
import io
import os
import os.path
import csv


dirname = os.path.dirname(__file__)
STATS_FILE_PATH = dirname + '/videostats.csv'


def detectKeyframes(videoname):
    input = dirname + '/' + videoname + '.avi'
    stream = os.popen('scenedetect -i ' + input + ' -s ' + STATS_FILE_PATH + ' detect-content list-scenes -f ' + str(videoname) + '.csv save-images -f ' + str(videoname))
    stream.read()

def rgbToPng(videofoldername):

    width = 352
    height = 288

    filenames = glob.glob(dirname + '/videos/' + videofoldername + '/*.rgb')
    filenames.sort()

    for img in filenames:
        im = open(img, 'rb')
        imBytes = im.read()

        newImg = Image.new("RGB", (width, height), "white")
        pixels = newImg.load()

        ind = 0
        for y in range(height):
            for x in range(width):
                r = imBytes[ind] & 0xff
                g = imBytes[ind + height * width] & 0xff
                b = imBytes[ind + height * width * 2] & 0xff
                # print(str(r) + " " + str(g) + " " + str(b))
                pixels[x, y] = (r, g, b)
                ind += 1
        outputDir = videofoldername + 'png'
        if not os.path.exists(dirname + '/videos/' + outputDir):
            os.makedirs(dirname + '/videos/' + outputDir)
        newImg.save(dirname + '/videos/' + outputDir + '/' + img[-14:-3] + 'png')

        # test = Image.frombytes("RGB", (352, 288), imBytes)
        # test.show()


def framesToVideo(videofoldername):

    video_name = videofoldername + '.avi'
    image_folder = os.path.join(dirname, 'videos', videofoldername + 'png')
    images = [img for img in os.listdir(image_folder)] #if img.endswith(".png")
    images.sort()
    # frame = cv2.imread(os.path.join(image_folder, images[0]))
    # height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 29.97, (352, 288))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


def getKeyframeNumsFromCsv(videoname):
    '''
    Obtain array of keyframe numbers from the csv file generated from detectKeyframes()
    '''
    f = open(os.path.join(dirname, videoname + '.csv'))
    csv_f = csv.reader(f)
    frameNums = []
    cnt = 0
    for row in csv_f:
        if cnt > 1:
            frameNums.append(int(row[1]))
        cnt += 1
    print(frameNums)
    return frameNums


def getKeyframeImg(videoname, frameNums):
    '''
    write the keyframe images to keyframes dir.
    This function can be used for storing mappings.
    '''
    video = os.path.join(dirname, videoname + '.avi')
    cap = cv2.VideoCapture(video)

    for frameNum in frameNums:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frameNum + 1)
        # print('Position:', int(cap.get(cv2.CAP_PROP_POS_FRAMES)))
        _, frame = cap.read()
        cv2.imwrite(os.path.join(dirname, 'keyframes', videoname + '_' + str(frameNum) + '.png'), frame)
        # cv2.imshow('frame', frame)
        # cv2.waitKey(2000)
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    # multiprocessing.set_start_method("spawn")
    video_folder = os.path.join(dirname, 'videos')
    videos = [video for video in os.listdir(video_folder) if not video.startswith('.')]
    for video in videos:
        rgbToPng(video)
        framesToVideo(video)
        detectKeyframes(video)
        getKeyframeImg(video, getKeyframeNumsFromCsv(video))