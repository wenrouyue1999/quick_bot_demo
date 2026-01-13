#!/usr/bin/env python
# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2026/1/12 下午3:52
# @Author  : wenrouyue
# @File    : qr_code.py

import qrcode
from PIL import Image


def get_qr_code(url, logo_type, out_trade_no):
    # 创建二维码对象
    qr = qrcode.QRCode(
        version=1,  # 控制二维码的大小
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 使用高纠错级别以便能容纳logo
        box_size=6,  # 每个格子的像素大小
        border=1.5,  # 边框的格子数，调整这里以减少白边
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    logo = Image.open(f'./img/logo/{logo_type}.png')
    logo_size = int(min(qr_image.size) / 4)  # 将logo大小设置为二维码的1/4
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    qr_width, qr_height = qr_image.size
    logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
    qr_image.paste(logo, logo_position, logo)
    qr_image.save(f'./img/order/{out_trade_no}.png')
    return f'./img/order/{out_trade_no}.png'
