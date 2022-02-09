import os

import cv2


def init_detail_templ():
    realpath = os.path.split(os.path.realpath(__file__))[0]

    # sinanews_templ
    image = cv2.imread(os.path.join(realpath, 'detail.png'))
    sinanews_templ = image[555:590, 470:770]
    cv2.imwrite(os.path.join(realpath, 'detail_sinanews_templ.png'), sinanews_templ)

    # delete_templ
    delete_templ = image[558:585, 788:892]
    cv2.imwrite(os.path.join(realpath, 'detail_delete_templ.png'), delete_templ)

    # detail_templ
    detail_templ = image[120:165, 460:610]
    cv2.imwrite(os.path.join(realpath, 'detail_detail_templ.png'), detail_templ)


def init_list_templ():
    realpath = os.path.split(os.path.realpath(__file__))[0]

    # my_posts_templ
    image = cv2.imread(os.path.join(realpath, 'list.png'))
    my_posts_templ = image[120:165, 420:640]
    cv2.imwrite(os.path.join(realpath, 'list_my_posts_templ.png'), my_posts_templ)

    # item_templ
    item_templ = image[377:377 + 10, 243 - 20:243 + 804 + 20]
    cv2.imwrite(os.path.join(realpath, 'list_item_templ.png'), item_templ)


if __name__ == '__main__':
    init_detail_templ()
    init_list_templ()
