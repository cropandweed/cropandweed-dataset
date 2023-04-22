import argparse
import os
import shutil

import requests
import tarfile
from tqdm import tqdm
from utilities import datasets
from map_dataset import map_dataset


def parse_arguments():
    parser = argparse.ArgumentParser(description='download and extract all dataset images and annotations with '
                                                 'optional mapping to all pre-defined dataset variants')
    parser.add_argument('--data_root', type=str, default='../data',
                        help='directory for downloaded images and annotations')
    parser.add_argument('--no_mapping', dest='with_mapping', action='store_false', default=True,
                        help='skip mapping for predefined dataset variants')
    return parser.parse_args()


def setup(data_root, with_mapping):
    url_prefix = 'https://vitro-testing.com/wp-content/uploads/2022/12/'

    os.makedirs(data_root, exist_ok=True)

    for file_name in tqdm(
            ['cropandweed_annotations', 'cropandweed_images1of4', 'cropandweed_images2of4', 'cropandweed_images3of4',
             'cropandweed_images4of4'], desc='downloading and extracting files'):
        response = requests.get(f'{url_prefix}{file_name}.tar', stream=True)
        archive = tarfile.open(fileobj=response.raw, mode='r|')
        archive.extractall(data_root)

    shutil.move(os.path.join(data_root, 'bboxes'), os.path.join(data_root, 'CropAndWeed'))
    shutil.move(os.path.join(data_root, 'CropAndWeed'), os.path.join(data_root, 'bboxes', 'CropAndWeed'))

    if with_mapping:
        for dataset in datasets.DATASETS:
            if dataset != 'CropAndWeed':
                map_dataset(os.path.join(data_root, 'bboxes'), os.path.join(data_root, 'labelIds'), 'CropAndWeed',
                            dataset)

    for image_name in os.listdir('../images'):
        shutil.copy(os.path.join('../images', image_name), os.path.join(data_root, 'images', image_name))


def main():
    args = parse_arguments()
    setup(args.data_root, args.with_mapping)


if __name__ == '__main__':
    main()
