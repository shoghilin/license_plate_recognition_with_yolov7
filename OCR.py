import pytesseract, os
import os.path as osp
import cv2
import matplotlib.pyplot as plt
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# read .txt to get x,y,w,h of ALPR
def read_txt(filepath, scale):
    f = open(filepath, 'r')
    lines = f.readlines()
    if len(lines) < 2:
        line=lines[0].rstrip()
        obj = [int(float(i) * s) for i, s in zip(line.split(' '), scale)]
        return [obj]

         
    # read objects from each line of .txt
    objects = []
    for line in lines:
        line=line.rstrip()
        obj = [int(float(i) * s) for i, s in zip(line.split(' '), scale)]
        objects.append(obj)

    return objects

def binarization(im):
    threshold = 180 # to be determined
    _, img_binarized = cv2.threshold(im, threshold, 255, cv2.THRESH_BINARY)
    pil_img = Image.fromarray(img_binarized)
    return img_binarized

def ocr(DETECT_PATH, IMG_NAME):
    img = cv2.imread(osp.join(DETECT_PATH, IMG_NAME+'.png'))
    plt.subplot(121)
    plt.imshow(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    org_w, org_h, _ = img.shape
    lics = read_txt(osp.join(DETECT_PATH , 'labels/', IMG_NAME+'.txt'), (0, org_h, org_w, org_h, org_w))
    
    plt.subplot(122)
    for lic in lics:
        c, x, y, w, h = lic
        # print(x,y,w,h) # center of the bounding box
        img_alpr = img[y-int(h/2):y+int(h/2),x-int(w/2):x+int(w/2)]
        # img_alpr = binarization(img_alpr)
        plt.imshow(img_alpr)
        txt = pytesseract.image_to_string(img_alpr)
        if txt == "": return None
        # print(txt)
    plt.title(txt)
    plt.show()

if __name__ == '__main__':
    DETECT_PATH = './yolov7/runs/detect/'
    DETECT_PATH += sorted(os.listdir(DETECT_PATH))[-1]
    # IMG_NAME    = ''
    for IMG_NAME in os.listdir(DETECT_PATH):
        if ".png" not in IMG_NAME and ".jpg" not in IMG_NAME: 
            continue
        
        IMG_NAME = os.path.splitext(IMG_NAME)[0]
        try:
            ocr(DETECT_PATH, IMG_NAME)
        except:
            print(IMG_NAME)