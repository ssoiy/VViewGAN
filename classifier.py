from PIL import Image
import os
import numpy as np
import cv2 
import os

# video code link https://deep-learning-study.tistory.com/108 
# code YOLOX, Yolov5, night-day classifier

def isitnight(files_path):
    img_path_list=[]
    possible_img_extension = ['.jpg', '.jpeg', '.JPG', '.bmp', '.png']
    if len(files_path)>0:
        if os.path.splitext(files_path)[1] in possible_img_extension:
            img_path = files_path
            img_path_list.append(img_path)
        for pth in img_path_list:
            img = Image.open(pth)
            dir_m = os.path.basename(pth)
            dir, trash = os.path.splitext(dir_m)
            pix=np.array(img)
            sum=0
            brightness=0
            brightness = pix.sum()/(1280*720*3)
            b={'day': 0, 'night': 1}

            if brightness>=70:
                b=0
                save_path = os.path.join("./bdd_num/day/"+dir+".jpg")
                print("day")
                return b
        
            else:
                b=1
                save_path = os.path.join("./bdd_num/night/"+dir+".jpg")
                print("night")
                return b

def isitrain(files_path):
    img_path_list=[]
    possible_img_extension = ['.jpg', '.jpeg', '.JPG', '.bmp', '.png']
    if len(files_path)>0:
        if os.path.splitext(files_path)[1] in possible_img_extension:
            img_path = files_path
            img_path_list.append(img_path)






#capture_path가 배열일 경우

root_dir = './datasets/bdd100k/images/100k/trainA'
#parser.add_argument('--dataroot', required=True, default='./datasets/bdd100k/images/100k/trainA', help='path to images (should have subfolders trainA, trainB, valA, valB, etc)')

def isitnight_multipath(capture_path):
    img_path_list=[]
    possible_img_extension = ['.jpg', '.jpeg', '.JPG', '.bmp', '.png']
    for (root, dirs, files) in os.walk(root_dir): #얘는 파일명이 아니라 폴더 명을 넣어야함
        if len(files)>0:
            for file_name in files:
                if os.path.splitext(file_name)[1] in possible_img_extension:
                    img_path = root + '/' +file_name

                    img_path = img_path.replace('\\', '/')
                    img_path_list.append(img_path)

    datasets=img_path_list

    for pth in datasets:
        im = Image.open(pth)
        dir_m = os.path.basename(pth)
        dir, trash = os.path.splitext(dir_m)
        pix=np.array(im)
        sum=0
        brightness=0
        brightness = pix.sum()/(1280*720*3)
        b={'day': 0, 'night': 1}
        

        if brightness>=70:
            b=0
            #save_path = os.path.join("./bdd_num/day/"+dir+".jpg")
            im.save(save_path)
        
        else:
            b=1
            save_path = os.path.join("./bdd_num/night/"+dir+".jpg")
            #im.save(save_path)