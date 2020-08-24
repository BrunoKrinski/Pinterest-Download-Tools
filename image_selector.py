import os
import cv2
import glob
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, dest='folder', action='store',
                        required=True, help='Path to a folder with images.')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    folder_path = args.folder

    images = glob.glob(folder_path + '/*.png') + \
             glob.glob(folder_path + '/*.jpg')

    for image_path in images:
        
        image_name = image_path.split('/')[-1]
        print(image_name)
        image = cv2.imread(image_path)
        height, width, channels = image.shape 
        mv = True
        rm = False
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('image', (1200, 700))
        while(1): 
            cv2.imshow('image', image)
            k = cv2.waitKey(33)
            if k == 48:
                folder = 'folder0/'
                break
            elif k == 49:
                folder = 'folder1/'
                break
            elif k == 50:
                folder = 'folder2/'
                break
            elif k == 51:
                folder = 'folder3/'
                break
            elif k == 52:
                folder = 'folder4/'
                break
            elif k == 53:
                folder = 'folder5/'
                break
            elif k == 54:
                folder = 'folder6/'
                break
            elif k == 55:
                folder = 'folder7/'
                break
            elif k == 56:
                folder = 'folder8/'
                break
            elif k == 57:
                folder = 'folder9/'
                break
            elif k == 100:
                folder = 'trash/'
                break
            elif k == 110:
                mv = False
                break
            elif k == 113:
                exit()
            elif k == 115:
                folder = 'saved/'
                break
        if mv:
            os.makedirs(folder, exist_ok=True)
            new_path = folder + image_name
            os.system('mv ' + image_path + ' ' + new_path)
        cv2.destroyAllWindows()
        
