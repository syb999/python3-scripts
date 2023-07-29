#pip3 install qrcode
#pip3 install pillow

import qrcode
from PIL import Image

def generate_qrcode(data, output_path, box_size=10, border=4):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # 转换为RGB模式，因为PIL打开图像时默认使用L模式（灰度图像）
    img = img.convert("RGB")

    # 保存二维码图片
    img.save(output_path)

if __name__ == "__main__":
    # 要生成二维码的数据
    data_to_encode = "Hello, this is a QR code!"

    # 生成的二维码图片保存路径
    output_image_path = "qrcode.png"

    # 调用生成二维码的函数
    generate_qrcode(data_to_encode, output_image_path)

    print(f"二维码图片已生成并保存至 {output_image_path}")

