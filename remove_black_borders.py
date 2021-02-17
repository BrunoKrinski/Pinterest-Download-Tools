import os
import cv2
import glob
import argparse
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, dest='folder', action='store',
                        required=True, help='Path to a folder with images.')
    return parser.parse_args()

def remove_black_border(h, w, image):
    thresh = 3 * 5

    cx, cy = int(w/2), int(h/2)

    cw0 = 0
    cw1 = int(cx/2)
    cw2 = cx
    cw3 = cx + cw1
    cw4 = w - 1

    ch0 = 0
    ch1 = int(cy/2)
    ch2 = cy
    ch3 = cy + ch1
    ch4 = h - 1
    
    for i in range(cx, w):
        b = int(image[ch0, i, 0])
        g = int(image[ch0, i, 1])
        r = int(image[ch0, i, 2])
        s0 = b + r + g

        b = int(image[ch1, i, 0])
        g = int(image[ch1, i, 1])
        r = int(image[ch1, i, 2])
        s1 = b + r + g

        b = int(image[ch2, i, 0])
        g = int(image[ch2, i, 1])
        r = int(image[ch2, i, 2])
        s2 = b + r + g

        b = int(image[ch3, i, 0])
        g = int(image[ch3, i, 1])
        r = int(image[ch3, i, 2])
        s3 = b + r + g

        b = int(image[ch4, i, 0])
        g = int(image[ch4, i, 1])
        r = int(image[ch4, i, 2])
        s4 = b + r + g
        
        if s0 < thresh and s1 < thresh and s2 < thresh and s3 < thresh and s4 < thresh:
            break

    for j in range(cx, -1, -1):    
        b = int(image[ch0, j, 0])
        g = int(image[ch0, j, 1])
        r = int(image[ch0, j, 2])
        s0 = b + r + g

        b = int(image[ch1, j, 0])
        g = int(image[ch1, j, 1])
        r = int(image[ch1, j, 2])
        s1 = b + r + g

        b = int(image[ch2, j, 0])
        g = int(image[ch2, j, 1])
        r = int(image[ch2, j, 2])
        s2 = b + r + g

        b = int(image[ch3, j, 0])
        g = int(image[ch3, j, 1])
        r = int(image[ch3, j, 2])
        s3 = b + r + g

        b = int(image[ch4, j, 0])
        g = int(image[ch4, j, 1])
        r = int(image[ch4, j, 2])
        s4 = b + r + g
        
        if s0 < thresh and s1 < thresh and s2 < thresh and s3 < thresh and s4 < thresh:
            break

    for a in range(cy, h):
        b = int(image[a, cw0, 0])
        g = int(image[a, cw0, 1])
        r = int(image[a, cw0, 2])
        s0 = b + r + g

        b = int(image[a, cw1, 0])
        g = int(image[a, cw1, 1])
        r = int(image[a, cw1, 2])
        s1 = b + r + g

        b = int(image[a, cw2, 0])
        g = int(image[a, cw2, 1])
        r = int(image[a, cw2, 2])
        s2 = b + r + g

        b = int(image[a, cw3, 0])
        g = int(image[a, cw3, 1])
        r = int(image[a, cw3, 2])
        s3 = b + r + g

        b = int(image[a, cw4, 0])
        g = int(image[a, cw4, 1])
        r = int(image[a, cw4, 2])
        s4 = b + r + g
        
        if s0 < thresh and s1 < thresh and s2 < thresh and s3 < thresh and s4 < thresh:
            break
        
    for c in range(cy, -1, -1):
        b = int(image[c, cw0, 0])
        g = int(image[c, cw0, 1])
        r = int(image[c, cw0, 2])
        s0 = b + r + g

        b = int(image[c, cw1, 0])
        g = int(image[c, cw1, 1])
        r = int(image[c, cw1, 2])
        s1 = b + r + g

        b = int(image[c, cw2, 0])
        g = int(image[c, cw2, 1])
        r = int(image[c, cw2, 2])
        s2 = b + r + g

        b = int(image[c, cw3, 0])
        g = int(image[c, cw3, 1])
        r = int(image[c, cw3, 2])
        s3 = b + r + g

        b = int(image[c, cw4, 0])
        g = int(image[c, cw4, 1])
        r = int(image[c, cw4, 2])
        s4 = b + r + g
        
        if s0 < thresh and s1 < thresh and s2 < thresh and s3 < thresh and s4 < thresh:
            break

    return image[c:a,j:i]

if __name__ == '__main__':
    args = get_args()
    folder_path = args.folder

    output_folder = 'black_croped/'
    os.makedirs(output_folder, exist_ok=True)

    images = glob.glob(folder_path + '/*.png') + \
             glob.glob(folder_path + '/*.jpg')
    for image_path in images:
        
        image_name = image_path.split('/')[-1]
        print(image_name)
        image = cv2.imread(image_path)

        h,w,d = image.shape
        image = remove_black_border(h, w, image)

        cv2.imwrite(output_folder + image_name, image)
