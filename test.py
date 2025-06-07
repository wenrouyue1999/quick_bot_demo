# # #!/usr/bin/env python
# # # !/usr/bin/python3
# # # -*- coding: utf-8 -*-
# # # @Time    : 2024/9/17 下午6:47
# # # @Author  : wenrouyue
# # # @File    : test.py
# #
# # import requests
# # import time
# # from datetime import datetime
# #
# #
# # # 输出函数
# #
# # # 获取总页数的函数
# # def get_pages():
# #     response = requests.get("http://127.0.0.1:10000/bot/getDataBack?pageNum=1&pageSize=5")
# #
# #     if response.status_code != 200:
# #         print("获取 pages 失败")
# #         exit(1)
# #
# #     data = response.json()
# #     pages = data.get('data', {}).get('pages')
# #
# #     print(f"获取到 data.pages: {pages}")
# #     return pages
# #
# #
# # # 发送请求的函数
# # def send_request(index):
# #     response = requests.get(f"http://127.0.0.1:10001/send/{index}")
# #
# #     if response.status_code == 200:
# #         print(f"调用 /send/{index}")
# #     else:
# #         print(f"调用 /send/{index} 失败，状态码: {response.status_code}")
# #
# #
# # # 完成请求的函数
# # def done_request():
# #     response = requests.get("http://127.0.0.1:10001/done")
# #
# #     if response.status_code == 200:
# #         print("调用 /done")
# #     else:
# #         print(f"调用 /done 失败，状态码: {response.status_code}")
# #
# #
# # # 主函数
# # def main():
# #     pages = get_pages()
# #
# #     for i in range(1, int(pages) + 1):
# #         send_request(i)
# #         if i < pages:
# #             print("等待 5 分钟...")
# #             time.sleep(300)
# #
# #     print("等待 5 分钟以调用 /done ...")
# #     time.sleep(300)
# #
# #
# # # 执行主函数
# # if __name__ == "__main__":
# #     main()
#
# import pyautogui
# import time
#
#
# def get_mouse_position():
#     print("请将鼠标移到您想要获取的位置...")
#     time.sleep(5)  # 给用户5秒时间移动鼠标
#     x, y = pyautogui.position()  # 获取鼠标位置
#     print(f"当前鼠标位置: (x: {x}, y: {y})")
# def auto_click(x, y, clicks, interval):
#     """
#     自动点击指定位置的函数。
#
#     :param x: 点击位置的 x 坐标
#     :param y: 点击位置的 y 坐标
#     :param clicks: 总点击次数
#     :param interval: 每次点击之间的时间间隔（秒）
#     """
#     # 确保鼠标移动到目标位置
#     pyautogui.moveTo(x, y)
#     for i in range(clicks):
#         pyautogui.click(x, y)  # 在指定位置点击
#         print(f"点击位置: ({x}, {y}), 剩余点击次数: {clicks - i - 1}")
#         time.sleep(interval)  # 等待指定的时间间隔
#
# if __name__ == "__main__":
#     # get_mouse_position()
#     try:
#         auto_click(1838, 1364, 30, 3)
#     except KeyboardInterrupt:
#         print("自动点击已停止。")
#
#
#
#
#     # if __name__ == "__main__":
#     #     get_mouse_position()
#
import qrcode
from PIL import Image


# def generate_qr_code_with_logo(url, logo_type, out_trade_no):
#     # 创建二维码对象
#     qr = qrcode.QRCode(
#         version=1, # 控制二维码的大小
#         error_correction=qrcode.constants.ERROR_CORRECT_H,  # 使用高纠错级别以便能容纳logo
#         box_size=10, # 每个格子的像素大小
#         border=1.5, # 边框的格子数，调整这里以减少白边
#     )
#     qr.add_data(url)
#     qr.make(fit=True)
#     qr_image = qr.make_image(fill_color="black", back_color="white").convert('RGB')
#     logo = Image.open(f'../img/logo/{logo_type}.png')
#     logo_size = int(min(qr_image.size) / 2)  # 将logo大小设置为二维码的1/4
#     logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
#     qr_width, qr_height = qr_image.size
#     logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
#     qr_image.paste(logo, logo_position, logo)
#     qr_image.save(f'../img/order/{out_trade_no}.png')


#
# url = "https://www.example.com"
# logo_path = 'D:/Code/Python/tg_toujia_py/img/logo/alipay1.png' # 确保提供正确的logo文件路径
# output_filename = "qr_code_with_logo.png"
#
# generate_qr_code_with_logo(url, logo_path, output_filename)
#
# print(f"带有Logo的二维码已保存为：{output_filename}")


import base64
# https://t.me/ShenTouCatBot?start=rp_aHR0cHM6Ly90Lm1lL1NoZW5Ub3VDbHViLzQxMjcwOA==_MTg5Nzk0OTE0Mw==
# 编码的字符串
# encoded_strings = [
#     "aHR0cHM6Ly90Lm1lL1NoZW5Ub3VDbHViLzQxMjcxMA==",
#     "aHR0cHM6Ly90Lm1lL1NoZW5Ub3VDbHViLzQxMjcwOA==",
#     "NTkxMDkxNDM2MA==",
#     "MTg5Nzk0OTE0Mw=="
# ]

# 解码
# for encoded in encoded_strings:
    # decoded = base64.b64decode(encoded).decode('utf-8', errors='ignore')
    # print(decoded)

