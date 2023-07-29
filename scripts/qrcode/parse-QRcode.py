#pip3 install pillow
#pip3 install pyzbar(for ubuntu: sudo apt-get install libzbar0)

from PIL import Image
from pyzbar.pyzbar import decode

def read_qrcode(image_path):
    # 读取图片
    image = Image.open(image_path)

    # 解码二维码
    decoded_data = decode(image)

    # 提取并返回信息
    if len(decoded_data) > 0:
        return decoded_data[0].data.decode("utf-8")
    else:
        return None

if __name__ == "__main__":
    # 二维码图片路径
    image_path = "qrcode.png"  # 替换成你的二维码图片路径

    # 调用解码函数
    result = read_qrcode(image_path)

    if result:
        print("解码结果：", result)
    else:
        print("未找到二维码或解码失败。")

