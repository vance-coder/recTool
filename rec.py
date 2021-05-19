import os
from glob import glob

import cv2
import imagehash
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR

paddle_ocr = PaddleOCR(
    det_model_dir='models/det',
    rec_model_dir='models/rec',
    cls_model_dir='models/cls',
    use_gpu=False
)


def get_rotate_crop_image(img, points):
    img_crop_width = int(
        max(
            np.linalg.norm(points[0] - points[1]),
            np.linalg.norm(points[2] - points[3])))
    img_crop_height = int(
        max(
            np.linalg.norm(points[0] - points[3]),
            np.linalg.norm(points[1] - points[2])))
    pts_std = np.float32([[0, 0], [img_crop_width, 0],
                          [img_crop_width, img_crop_height],
                          [0, img_crop_height]])
    M = cv2.getPerspectiveTransform(points, pts_std)
    dst_img = cv2.warpPerspective(
        img,
        M, (img_crop_width, img_crop_height),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC)
    dst_img_height, dst_img_width = dst_img.shape[0:2]
    if dst_img_height * 1.0 / dst_img_width >= 1.5:
        dst_img = np.rot90(dst_img)
    return dst_img


def run():
    for path in glob('static/images/upload/*.png'):
        print(path)
        result = paddle_ocr.ocr(path, det=True, rec=True)
        img = cv2.imread(path)

        for row in result:
            points, text = row
            dst_img = get_rotate_crop_image(img, np.array(points, np.float32))
            dst_img = Image.fromarray(dst_img)
            image_name = 'static/images/result/' + str(imagehash.average_hash(dst_img)) + '.png'
            dst_img.save(image_name)


if __name__ == '__main__':
    run()
