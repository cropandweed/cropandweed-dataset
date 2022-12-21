import argparse
import io
import os
import requests
from tqdm import tqdm
import zipfile
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
    print('source files will be available by January 2023')
    return

    url_prefix = 'https://vitro-testing.com/test-data/cropandweed-dataset/'

    os.makedirs(data_root, exist_ok=True)

    for file_name in tqdm(
            ['bboxes', 'images_part1of4', 'images_part2of4', 'images_part3of4', 'images_part4of4', 'labelIds',
             'params'], desc='downloading and extracting zip files'):
        response = requests.get(f'{url_prefix}{file_name}.zip', stream=True)
        zip_archive = zipfile.ZipFile(io.BytesIO(response.content))
        zip_archive.extractall(os.path.join(data_root, file_name.split('_')[0]))

    if with_mapping:
        for dataset in datasets.DATASETS:
            if dataset != 'CropAndWeed':
                map_dataset(os.path.join(data_root, 'bboxes'), os.path.join(data_root, 'labelIds'), 'CropAndWeed',
                            dataset)


def main():
    args = parse_arguments()
    setup(args.data_root, args.with_mapping)


if __name__ == '__main__':
    main()
