"""
A script for sina news app share

step 0: init
step 1: search sina logo and tap
step 2: search one news and tap
step 3: tap share button, tap tencent moment logo, tap Last Group, tap Post
step 4: tap return button, slide up, goto step 2
"""

import os
import time

import cv2
from goto import with_goto

TMP_PATH = 'tmp/share'
ADB_PATH = '/usr/local/bin/adb'
TEMPL_PATH = 'templ/share'


def screenshot(screen_name, local_path):
    os.system('{} shell screencap -p /sdcard/{}.png'.format(ADB_PATH, screen_name))
    os.system('{} pull /sdcard/{}.png {}'.format(ADB_PATH, screen_name, local_path))
    return os.path.join(local_path, '{}.png'.format(screen_name))


def tap(y, x, sleep=0.15):
    os.system('{} shell input tap {} {}'.format(ADB_PATH, y, x))
    time.sleep(sleep)


def swipe(height=100, t=100):
    os.system('{} shell input swipe {} {} {} {} {}'.format(ADB_PATH, 540, 1170, 540, 1170 - height, t))


def match_templ(templ_name, alpha, retry=1, image_path=None):
    y = -1
    x = -1
    for _ in range(retry):
        if not image_path:
            image_path = screenshot(screen_name='share_image_{}'.format(templ_name), local_path=TMP_PATH)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        templ = cv2.imread(os.path.join(TEMPL_PATH, '{}.png'.format(templ_name)), cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(image=image, templ=templ, method=cv2.TM_SQDIFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if min_val <= alpha:
            pos_y, pos_x = min_loc
            len_x, len_y = templ.shape
            y = pos_y + int(len_y / 2)
            x = pos_x + int(len_x / 2) + 2
        print('match_templ', templ_name, alpha, min_val, max_val, min_loc, max_loc, y, x)
        if y + x != -2:
            return y, x
        else:
            image_path = None
            time.sleep(1)
    return y, x


def tap_return_button():
    while True:
        image_path = screenshot(screen_name='share_image_return', local_path=TMP_PATH)

        y_0, x_0 = match_templ(templ_name='white_return', alpha=4000000, image_path=image_path)
        if y_0 + x_0 != -2:
            tap(y=y_0, x=x_0, sleep=1)
            return

        y_1, x_1 = match_templ(templ_name='black_return', alpha=4000000, image_path=image_path)
        if y_1 + x_1 != -2:
            tap(y=y_1, x=x_1, sleep=1)
            return

        time.sleep(1)


@with_goto
def pipeline():
    # step 0: init
    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)

    # step 1: search sina logo and tap
    y, x = match_templ(templ_name='logo', alpha=3500000)
    tap(y=y, x=x, sleep=6)

    # step 2: search one news and tap by view icon
    label.step_2
    swipe(height=400, t=100)
    y, x = match_templ(templ_name='view', alpha=20000)
    tap(y=y, x=x, sleep=0.5)

    # step 3: tap share button, tap tencent moment logo, tap Last Group, tap Post
    y, x = match_templ(templ_name='share', alpha=60000)
    if y + x == -2:
        tap_return_button()
        goto.step_2
    else:
        tap(y=y, x=x, sleep=0.5)

    y, x = match_templ(templ_name='moment', alpha=500000)
    tap(y=y, x=x, sleep=1)
    y, x = match_templ(templ_name='last', alpha=150000)
    tap(y=y, x=x, sleep=0.1)
    y, x = match_templ(templ_name='post', alpha=4000000, retry=3)
    tap(y=y, x=x, sleep=0.1)

    # step 4: tap return button, slide up, goto step 2
    tap_return_button()
    goto.step_2


if __name__ == '__main__':
    pipeline()
