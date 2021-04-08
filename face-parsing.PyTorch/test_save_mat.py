#!/usr/bin/python
# -*- encoding: utf-8 -*-

from logger import setup_logger
from model import BiSeNet

import torch

import os
import numpy as np
from PIL import Image, ImageOps
import torchvision.transforms as transforms
import cv2
import scipy.io as sio
import argparse


def vis_parsing_maps(im, parsing_anno, stride, save_im=False, save_path='vis_results/parsing_map_on_im.jpg'):
    # Colors for all 20 parts
    part_colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0],
                   [255, 0, 85], [255, 0, 170],
                   [0, 255, 0], [85, 255, 0], [170, 255, 0],
                   [0, 255, 85], [0, 255, 170],
                   [0, 0, 255], [85, 0, 255], [170, 0, 255],
                   [0, 85, 255], [0, 170, 255],
                   [255, 255, 0], [255, 255, 85], [255, 255, 170],
                   [255, 0, 255], [255, 85, 255], [255, 170, 255],
                   [0, 255, 255], [85, 255, 255], [170, 255, 255]]

    im = np.array(im)
    vis_im = im.copy().astype(np.uint8)
    vis_parsing_anno = parsing_anno.copy().astype(np.uint8)
    vis_parsing_anno = cv2.resize(vis_parsing_anno, None, fx=stride, fy=stride, interpolation=cv2.INTER_NEAREST)
    vis_parsing_anno_color = np.zeros((vis_parsing_anno.shape[0], vis_parsing_anno.shape[1], 3)) + 255

    num_of_class = np.max(vis_parsing_anno)

    for pi in range(1, num_of_class + 1):
        index = np.where(vis_parsing_anno == pi)
        vis_parsing_anno_color[index[0], index[1], :] = part_colors[pi]

    vis_parsing_anno_color = vis_parsing_anno_color.astype(np.uint8)
    # print(vis_parsing_anno_color.shape, vis_im.shape)
    vis_im = cv2.addWeighted(cv2.cvtColor(vis_im, cv2.COLOR_RGB2BGR), 0.4, vis_parsing_anno_color, 0.6, 0)

    # Save result or not
    if save_im:
        cv2.imwrite(save_path[:-4] +'.png', vis_parsing_anno)
        cv2.imwrite(save_path, vis_im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    # return vis_im


def save_mat(parsing, img_name, save_path, im, im1):
    save_path = os.path.join(save_path, img_name[:-4])
    parsing = parsing.transpose(2, 1, 0)
    res = cv2.resize(parsing, (250, 200), interpolation=cv2.INTER_NEAREST)
    res = res.transpose(1, 0, 2)
    sio.savemat(save_path, {"res_label": res})

    print(save_path + " success")

def evaluate(respth='./res/test_res', dspth='./data', cp='model_final_diss.pth'):

    if not os.path.exists(respth):
        os.makedirs(respth)

    n_classes = 19
    net = BiSeNet(n_classes=n_classes)
    net.cuda()
    save_pth = os.path.join('res/cp', cp)
    net.load_state_dict(torch.load(save_pth))
    net.eval()

    to_tensor = transforms.Compose([
        # transforms.Pad((56, 6), padding_mode='edge'),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    with torch.no_grad():
        for image_path in os.listdir(dspth):
            img_1 = Image.open(os.path.join(dspth, image_path)).convert("RGB")
            image = img_1.resize((512, 512), Image.BILINEAR)
            # image2 = ImageOps.expand(image, border=(56,6,56,6), fill=0)
            img = to_tensor(image)
            img = torch.unsqueeze(img, 0)
            img = img.cuda()
            out = net(img)
            out = out[0]
            parsing = out.squeeze(0).cpu().numpy().argmax(0)
            # print(parsing)
            print(np.unique(parsing))
            # vis_parsing_maps(image, parsing, stride=1, save_im=True, save_path=osp.join(respth, image_path))
            save_mat(out.squeeze(0).cpu().numpy(), image_path, respth, img_1, image)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputPath', type=str, default='../data/CUHK_FERET/photos', help='image source folder')
    parser.add_argument('--savePath', type=str, default='../data/CUHK_FERET/photos_mat', help='save folder')
    args = parser.parse_args()
    evaluate(respth=args.savePath, dspth=args.inputPath, cp='79999_iter.pth')


