import argparse
import csv
import os
from tqdm import tqdm
from utilities import datasets
import cv2
import numpy as np


def parse_arguments():
    parser = argparse.ArgumentParser(description='map annotated classes between datasets')
    parser.add_argument('--bboxes', type=str, default='../data/bboxes',
                        help='directory for input and output bounding-box annotations as csv files in sub-directories '
                             'for each dataset variant')
    parser.add_argument('--labelids', type=str, default='../data/labelIds',
                        help='source directory for input and output semantic masks as single-channel png images '
                             'in sub-directories for each dataset variant')
    parser.add_argument('--dataset_source', type=str, default='CropAndWeed', help='name of source dataset')
    parser.add_argument('--dataset_target', type=str, required=True, help='name of target dataset')
    return parser.parse_args()


def map_dataset(bboxes_dir, labelids_dir, dataset_source, dataset_target):
    if dataset_target not in datasets.DATASETS:
        raise RuntimeError(f'target dataset {dataset_target} not defined in datasets.py')

    labels = datasets.DATASETS[dataset_target]
    n_labels = len(labels.get_label_ids())

    for postfix in ['', 'Eval']:
        os.makedirs(os.path.join(bboxes_dir, f'{dataset_target}{postfix}'), exist_ok=True)

    labelids_target = os.path.join(labelids_dir, dataset_target)
    os.makedirs(labelids_target, exist_ok=True)

    bboxes_source = os.path.join(bboxes_dir, dataset_source)
    for file_name in tqdm(os.listdir(bboxes_source),
                          desc=f'mapping bounding-box annotations to target dataset {dataset_target}'):
        with open(os.path.join(bboxes_source, file_name), 'r', newline='', encoding='utf-8') as anno_file:
            anno = csv.DictReader(anno_file,
                                  fieldnames=['left', 'top', 'right', 'bottom', 'label_id', 'stem_x', 'stem_y'])

            rows = []
            rows_eval = []
            for row in anno:
                label = int(row['label_id'])
                mapped_id = labels.get_mapped_id(label)
                if mapped_id is not None:
                    row['label_id'] = labels.get_mapped_id(label)
                    rows.append(row)
                else:
                    row['label_id'] = 255
                    rows_eval.append(row)

            if len(rows) > 0:
                with open(os.path.join(bboxes_dir, dataset_target, file_name), 'w', newline='',
                          encoding='utf-8') as output:
                    output_anno = csv.DictWriter(output, fieldnames=anno.fieldnames)
                    for row in rows:
                        output_anno.writerow(row)

            with open(os.path.join(bboxes_dir, f'{dataset_target}Eval', file_name), 'w', newline='',
                      encoding='utf-8') as output:
                output_anno = csv.DictWriter(output, fieldnames=anno.fieldnames)
                for row in rows + rows_eval:
                    output_anno.writerow(row)

    labelids_source = os.path.join(labelids_dir, dataset_source)
    for file_name in tqdm(os.listdir(labelids_source),
                          desc=f'mapping semantic masks to target dataset {dataset_target}'):
        mask = cv2.imread(os.path.join(labelids_source, file_name), cv2.IMREAD_GRAYSCALE)
        output_mask = np.zeros_like(mask)
        include = False
        for source_id in np.unique(mask):
            target_id = labels.get_mapped_id(source_id)
            if target_id is not None:
                output_mask[mask == source_id] = target_id
                include = True
            else:
                output_mask[mask == source_id] = n_labels
        if include:
            cv2.imwrite(os.path.join(labelids_target, file_name), output_mask)


def main():
    args = parse_arguments()
    map_dataset(args.bboxes, args.labelids, args.dataset_source, args.dataset_target)


if __name__ == '__main__':
    main()
