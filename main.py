#from email.mime import image
import cv2
import argparse
import glob
import os
import sys
import time
from pathlib import Path
import classifier
import n2d_model



FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

global fps

# opt 따로 만들고 싶을 때 참고
# def parse_opt(known=False):
#     parser=argparse.ArgumentParser("VViewGAN parser")
#     parser.add_argument('')

#     parser.add_argument('--weights', type=str, default=ROOT / 'yolov5s.pt', help='initial weights path')

#     opt = parser.parse_known_args()[0] if known else parser.parse_args()
#     return opt


def get_data(path):
    image_file_paths=[]
    for root, dirs, filenames in os.walk(path):
        filenames = sorted(filenames)
        for filename in filenames:
            input_path = os.path.abspath(root)
            file_path = os.path.join(input_path, filename)
            if filename.endswith('.mp4') or filename.endswith('.avi'):
                image_file_paths.append(file_path)
        break
    #print(filenames) : ['v1.mp4', 'v2.mp4']
    #print(filename) : v2.mp4
    #print(input_path) : /home/user/cap/VViewGAN/video
    #print(file_path) : /home/user/cap/VViewGAN/video/v2.mp4
    #print(image_file_paths) : ['/home/user/cap/VViewGAN/video/v1.mp4', '/home/user/cap/VViewGAN/video/v2.mp4']

    return image_file_paths

def video2image(image_file_paths):
    #video_paths = glob.glob('opt.input+"/"*.mp4')
    #video_paths = './video/res.mp4'
    for vp in image_file_paths: # vp : /home/user/cap/VViewGAN/video/v1.mp4
        video_name= vp.split("/")[-1][:-4] # video_name : v1
        vidcap = cv2.VideoCapture(vp)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        success,image = vidcap.read() # success : True, image : real image
        count = 0
        new_path = './image/'
        while success: #while(vidcap.isOpened()):
            success,image = vidcap.read() # 이게 무슨 순서인지 모르겠는데 while문 안에 이게 있어야 vidcap.get(1)이 증가함
            if(int(vidcap.get(1)) % 30 == 0): #vidcap.get(1)은 fps value 인듯
                 
                cv2.imwrite(new_path+video_name+"_%04d.jpg" % count, image)     # save frame as JPEG file
                #success,image = vidcap.read()
                # print('Read a new frame: ', success)
                capture_path = os.path.join(new_path+video_name+"_%04d.jpg" % count)
                count += 1
                
                return capture_path # return 해버리면 여기서 끝남 사진 한 장으로, 여러 장을 보내고 싶으면 utils/video_capture.py 사용

def main(opt):
    data_path = opt.input
    capture_path = video2image(get_data(data_path))
    print(capture_path)
    isitnight = classifier.isitnight(capture_path)
    
    while isitnight:
        n2d_model.test(data_path)
        capture_path = video2image(get_data(data_path))
        isitnight = classifier.isitnight(capture_path)

    isitrain=classifier.isitrain(capture_path)

    while isitrain:
        rain_model.test(data_path)
        capture_path = video2image(get_data(data_path))
        isitrain=classifier.isitrain(capture_path)

    print("complete!!")
    filename = os.path.join(data_path.split("/")[-1][:-4]+"_convert.jpg")
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    frameSize = 720

    cv2.VideoWriter(filename, fourcc, fps, frameSize, isColor=None)

    

    # if isitnight==0:
    #     isitrain=classifier.isitrain(capture_path)
    # else:
    #     model.test(input)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=ROOT / 'video/', help='path to video directory')
    opt = parser.parse_args()

    main(opt)

# if __name__ == '__main__':
#     opt = parser_opt()
#     main(opt)

#     video2image(opt)