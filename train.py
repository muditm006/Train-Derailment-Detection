import argparse
import cv2
import math
import numpy as np


def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, thickness=3):
    line_img = np.zeros(
        (
            img.shape[0],
            img.shape[1],
            3
        ),
        dtype=np.uint8
    )
    img = np.copy(img)
    if lines is None:
        return
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (int(x1), int(y1)), (int(x2), int(y2)), [149, 20, 196], thickness)
    img = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
    return img




def pipeline(image, special):
    h = image.shape[0]
    w = image.shape[1]
    if special:
        region_of_interest_vertices = [
            (w / 12, h),
            (w / 2, h / 2),
            (11 * w / 12, h),
        ]
    else:
        region_of_interest_vertices = [
            (w / 4, h),
            (11 * w / 24, h / 3),
            (7 * w / 12, h),
        ]
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cannyed_image = cv2.Canny(gray_image, 100, 200)

    cropped_image = region_of_interest(
        cannyed_image,
        np.array(
            [region_of_interest_vertices],
            np.int32
        ),
    )

    lines = cv2.HoughLinesP(
        cropped_image,
        rho=6,
        theta=np.pi / 60,
        threshold=160,
        lines=np.array([]),
        minLineLength=40,
        maxLineGap=25
    )

    left_line_x = []
    left_line_y = []
    right_line_x = []
    right_line_y = []

    line_printed = True
    if lines is None:
        image = cv2.circle(image, (500,500), 50, (0, 255, 255), -1)
        return image
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            if math.fabs(slope) < 1:
                continue
            if slope <= 0:
                left_line_x.extend([x1, x2])
                left_line_y.extend([y1, y2])
            else:
                right_line_x.extend([x1, x2])
                right_line_y.extend([y1, y2])

    if special:
        min_y = image.shape[0] * (2 / 5)
    else:
        min_y = image.shape[0] * (3 / 5)
    max_y = image.shape[0]

    line_image = image

    if left_line_x and left_line_y and right_line_x and right_line_y:
        if math.fabs((left_line_y[1]-left_line_y[0])/(left_line_x[1] - left_line_x[0])) > 3 and math.fabs((right_line_y[1] - right_line_y[0]) / (
                right_line_x[1] - right_line_x[0])) > 3:
            image = cv2.circle(image, (500,500), 50, (0, 255, 255), -1)

        poly_left = np.poly1d(np.polyfit(
            left_line_y,
            left_line_x,
            deg=1
        ))
        left_x_start = int(poly_left(max_y))
        left_x_end = int(poly_left(min_y))
        poly_right = np.poly1d(np.polyfit(
            right_line_y,
            right_line_x,
            deg=1
        ))
        right_x_start = int(poly_right(max_y))
        right_x_end = int(poly_right(min_y))

        line_image = draw_lines(
            image,
            [[
                [left_x_start, max_y, left_x_end, min_y],
                [right_x_start, max_y, right_x_end, min_y],
            ]],
            thickness=5,
        )
    else:
        line_printed = False

    if line_printed:
        line_image = cv2.circle(line_image, (500,500), 50, (0, 255, 0), -1)
    else:
        line_image = cv2.circle(line_image, (500,500), 50, (0, 255, 255), -1)

    return line_image


ap = argparse.ArgumentParser()
ap.add_argument("-vin", "--video in", required=True, help="Path to the video")
args = vars(ap.parse_args())

vid = cv2.VideoCapture(args["video in"])
if args["video in"] == "easy.MOV" or "easy.mov":
    yes = True
if args["video in"] == "hard.mov":
    yes = False


frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
frame_number = 0

size = (0, 0)
while frame_number < frames:
    ret1, img1 = vid.read()
    height, width, layers = img1.shape
    size = (width, height)
    output = img1.copy()
    output = pipeline(output, yes)
    cv2.imshow("Product", output)
    key = cv2.waitKey(1)
    frame_number += 1

cv2.destroyAllWindows()
vid.release()
