import os
import cv2
import glob
import argparse
import imagehash
import multiprocessing

from PIL import Image
from tqdm import tqdm
from joblib import Parallel, delayed
from iteration_utilities import unique_everseen, duplicates, all_equal

def hash_image(image_path):
    image = Image.open(image_path)
    hashed_image = str(imagehash.average_hash(image))

    image_name = image_path.split('/')[-1]
    width, height = image.size

    image_infos = {
        'name': image_name,
        'width': width,
        'height': height,
        'hash': hashed_image
    }
    return image_infos


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', type=str, dest='folder', action='store',
                        required=True, help='Path to a folder with images.')
    return parser.parse_args()

def get_hash(d):
    return d['hash']

if __name__ == '__main__':
    args = get_args()
    folder_path = args.folder

    image_paths = glob.glob(folder_path + '/*.png') + \
             glob.glob(folder_path + '/*.jpg')

    num_images = len(image_paths)
    num_cores = multiprocessing.cpu_count()

    hashed_images = Parallel(n_jobs=num_cores)(
                delayed(hash_image)(image_path) for image_path in image_paths)

    images = list(duplicates(hashed_images, get_hash ))
    print(images)
    print(len(images))
    #print(hashed_images - uniques)
    
    '''
    cont = 1
    for image_path in images:
        image_zero = Image.open(image_path)
        hashes0 = imagehash.average_hash(image_zero)
        print(image_path)
        #print(hashes0)
        for idx in range(cont, num_images):
            
            image = Image.open(images[idx])
            print(images[idx])
            hashes1 = imagehash.average_hash(image)
            print(hashes0 - hashes1)
            if hashes0 == hashes1: 
                print("--------------------------------")
                print(images[idx])
                print("--------------------------------")
        cont += 1
        print("===============================================================")
    ''' 
        

        