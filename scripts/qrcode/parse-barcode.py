
from PIL import Image
from pyzbar.pyzbar import decode

# 打开图像文件
image_path = 'barcode.png'  # 替换为你的图像文件路径
image = Image.open(image_path)

# 解码条形码
decoded_objects = decode(image)

# 打印解码结果
for obj in decoded_objects:
    barcode_data = obj.data.decode('utf-8')
    barcode_type = obj.type
    print(f"解码结果：{barcode_data}")
    print(f"条形码类型：{barcode_type}")

