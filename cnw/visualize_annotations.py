import argparse
from collections import defaultdict
import csv
import cv2
from utilities import datasets
import numpy as np
import os
from tqdm import tqdm


def parse_arguments():
    parser = argparse.ArgumentParser(description='create a combined visualization for each annotation')
    parser.add_argument('--bboxes', type=str, default='../data/bboxes',
                        help='input directory containing bounding-box annotations as csv files in sub-directories'
                             ' for each dataset variant')
    parser.add_argument('--label_ids', type=str, default='../data/labelIds',
                        help='input directory containing segmentation masks as single-channel png images '
                             'in sub-directories for each dataset variant')
    parser.add_argument('--images', type=str, default='../data/images', help='input image directory')
    parser.add_argument('--dataset', type=str, default='CropAndWeed', help='name of dataset to be visualized')
    parser.add_argument('--visualizations', type=str, default='..data/visualization',
                        help='output directory for visualizations in sub-directory named after dataset variant')
    parser.add_argument('--target_width', type=int, default=1920, help='target width for visualization images')
    parser.add_argument('--filter', type=str, default='', help='only visualize images containing filter text')

    args = parser.parse_args()

    os.makedirs(args.visualizations, exist_ok=True)
    return args


def visualize_annotations(label_ids, bboxes, dataset, images, visualizations, target_width, image_filter):
    if dataset not in datasets.DATASETS:
        raise RuntimeError(f'dataset {dataset} not defined in datasets.py')

    labels = datasets.DATASETS[dataset]
    background_id = len(labels.get_label_ids())

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    font_thickness = 1
    font_line_type = cv2.LINE_AA

    bboxes_dir = os.path.join(bboxes, f'{dataset}Eval')
    label_ids_dir = os.path.join(label_ids, dataset)
    visualizations_dir = os.path.join(visualizations, dataset)
    os.makedirs(visualizations_dir, exist_ok=True)

    for bboxes_file in tqdm(sorted(os.listdir(bboxes_dir))):
        target = os.path.splitext(bboxes_file)[0]
        if os.path.exists(os.path.join(bboxes, dataset, bboxes_file)) and image_filter in target:
            label_count = defaultdict(int)
            image_path = os.path.join(images, f'{target}.jpg')
            if os.path.exists(image_path):
                image = cv2.imread(image_path)
                with open(os.path.join(bboxes_dir, bboxes_file), 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file, delimiter=',',
                                                fieldnames=['left', 'top', 'right', 'bottom', 'label_id', 'stem_x',
                                                            'stem_y'])
                    for row in csv_reader:
                        label_id = int(row['label_id'])
                        color = (0, 0, 0) if label_id == background_id else labels.get_label_color(label_id, bgr=True)
                        label_count[label_id] += 1
                        cv2.rectangle(image, (int(row['left']), int(row['top'])),
                                      (int(row['right']), int(row['bottom'])), color, thickness=2)
                        cv2.circle(image, (int(row['stem_x']), int(row['stem_y'])), 15, color, thickness=2)

                target_size = (int(target_width * 0.5), int(image.shape[0] * (target_width * 0.5 / image.shape[1])))
                label_ids_path = os.path.join(label_ids_dir, f'{target}.png')
                label_ids = cv2.resize(ids2colors(cv2.imread(label_ids_path, 0), labels), target_size,
                                       cv2.INTER_LINEAR) if os.path.exists(label_ids_path) else np.zeros(
                    (target_size[1], target_size[0], 3), dtype=np.uint8)
                image = cv2.resize(image, target_size, cv2.INTER_LINEAR)
                cv2.putText(image, target, (10, 15), font, font_scale, (255, 255, 255),
                            thickness=font_thickness, lineType=font_line_type)
                image = cv2.hconcat([image, label_ids])
                image = cv2.copyMakeBorder(image, 0, 25, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])

                offset = 5
                for label_id, count in sorted(label_count.items(), key=lambda item: item[1], reverse=True):
                    label_name = labels.get_label_name(label_id)
                    if label_name is not None:
                        text = f'{"Vegetation" if label_name is None else label_name} ({count})  '
                        image = cv2.putText(image, text, (offset, target_size[1] + 20), font, font_scale,
                                            labels.get_label_color(label_id, bgr=True), thickness=font_thickness,
                                            lineType=font_line_type)
                        offset += cv2.getTextSize(text, font, font_scale, font_thickness)[0][0]

                cv2.imwrite(os.path.join(visualizations_dir, f'{target}.jpg'), image)
            else:
                print(f'{image_path} not found')


def ids2colors(label_ids, dataset):
    label_colors = np.zeros((label_ids.shape[0], label_ids.shape[1], 3), dtype=np.uint8)
    for label_id in dataset.get_label_ids():
        label_colors[label_ids == label_id] = dataset.get_label_color(label_id, bgr=True)
    return label_colors


def main():
    args = parse_arguments()
    visualize_annotations(args.label_ids, args.bboxes, args.dataset, args.images, args.visualizations,
                          args.target_width, args.filter)


if __name__ == '__main__':
    main()
