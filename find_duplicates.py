import os
import cv2
import glob
import argparse
import imagehash
import multiprocessing

from PIL import Image
from tqdm import tqdm
from joblib import Parallel, delayed

def hash_image(image_path):
    image = Image.open(image_path)
    image_name = image_path.split('/')[-1]
    hashes = []
    for angle in [ 0, 90, 180, 270 ]:
        if angle > 0:
            turned_img = image.rotate(angle, expand=True)
        else:
            turned_img = image
        hashes.append(str(imagehash.phash(turned_img)))
    hashes = ''.join(sorted(hashes))
    #width, height = image.size

    image_infos = {
        'name': image_name,
        'hash': hashes
    }
    return image_infos

def find_duplicates(image, image_list):
    duplicates = []
    duplicates.append(image)
    for item in image_list:
        if image['name'] != item['name'] and image['hash'] == item['hash']:
            duplicates.append(item)
    if len(duplicates) > 1:
        return duplicates
    return None

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
    duplicates = Parallel(n_jobs=num_cores)(
                delayed(find_duplicates)(item, hashed_images) for item in hashed_images)

    new_folder = 'duplicates'
    os.makedirs(new_folder, exist_ok=True)
    names_list = []
    cont = 0
    for item in duplicates:
        if item is not None:
            for elem in item:
                if elem['name'] not in names_list:
                    names_list.append(elem['name'])
                    old_path = folder_path + '/' + elem['name']
                    new_path = new_folder + '/' + str(cont) + '_' + elem['name']
                    os.system('mv ' + old_path + ' ' + new_path)
                    cont += 1


        