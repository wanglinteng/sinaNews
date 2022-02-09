import os
import time

import cv2


# Android Device Resolution 2340 * 1080

ADB_PATH = '/usr/local/bin/adb'
TMP_PATH = './tmp/'
TEMPL_PATH = './templ'


def match_templ(image, templ_name, alpha):
    templ = cv2.imread(os.path.join(TEMPL_PATH, templ_name), cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(image=image, templ=templ, method=cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print('match_templ', templ_name, min_val, max_val, min_loc, max_loc)

    if min_val <= alpha:
        pos_y, pos_x = min_loc
        len_x, len_y = templ.shape
        return pos_x + int(len_x / 2), pos_y + int(len_y / 2)
    else:
        return -1, -1


def templ_in_image(image, templ_name, alpha):
    templ = cv2.imread(os.path.join(TEMPL_PATH, templ_name), cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(image=image, templ=templ, method=cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print('templ_in_image', templ_name, min_val, max_val, min_loc, max_loc)

    if min_val <= alpha:
        return True
    else:
        return False


def item_tap_loc():
    image = cv2.imread(os.path.join(TMP_PATH, 'tmp_sinanews_share_list.png'), cv2.IMREAD_GRAYSCALE)
    return match_templ(image=image, templ_name='list_item_templ.png', alpha=500)


def del_tap_loc():
    image = cv2.imread(os.path.join(TMP_PATH, 'tmp_sinanews_share_detail.png'), cv2.IMREAD_GRAYSCALE)

    if templ_in_image(image=image, templ_name='list_my_posts_templ.png', alpha=500):
        return False, 0, 0

    x, y = match_templ(image=image, templ_name='detail_sinanews_templ.png', alpha=500)
    if x < 0:
        return False, 53, 140  # return button

    x, y = match_templ(image=image, templ_name='detail_delete_templ.png', alpha=4000)
    if x < 0:
        return False, 53, 140  # return button
    else:
        return True, y, x


def ok_tap_loc():
    return 760, 1355


def cp_pic(name):
    os.system('{} shell screencap -p /sdcard/{}.png'.format(ADB_PATH, name))
    os.system('{} pull /sdcard/{}.png {}'.format(ADB_PATH, name, TMP_PATH))


def cp_list_pic():
    cp_pic(name='tmp_sinanews_share_list')


def cp_detail_pic():
    cp_pic(name='tmp_sinanews_share_detail')


def tap(x, y):
    os.system('{} shell input tap {} {}'.format(ADB_PATH, x, y))
    time.sleep(0.15)


def swipe():
    os.system('{} shell input swipe {} {} {} {} {}'.format(ADB_PATH, 540, 1170, 540, 1170 - 150, 500))
    time.sleep(0.5)


def run():
    while True:
        cp_list_pic()
        select_x, select_y = item_tap_loc()
        print('item_tap_loc {} {}'.format(select_x, select_y))
        tap(select_x, select_y)

        cp_detail_pic()
        status, delete_x, delete_y = del_tap_loc()
        print('delete_tap_loc {} {} {} '.format(status, delete_x, delete_y))
        tap(delete_x, delete_y)

        if status:  # delete True
            ok_x, ok_y = ok_tap_loc()
            tap(ok_x, ok_y)
            print('ok_tap_loc {} {}'.format(ok_x, ok_y))
        else:
            swipe()


if __name__ == '__main__':
    run()
