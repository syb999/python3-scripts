#使用cryptography库,pip install cryptography
#GUI界面使用pysimplegui,pip install pysimplegui

import socket
import base64
import PySimpleGUI as sg
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os


def generate_key(password):
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def encrypt_message(message, key):
    iv = os.urandom(16)  # 生成随机的初始向量
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return base64.urlsafe_b64encode(iv + encrypted_message).decode().rstrip('=')

def decrypt_message(encrypted_message, key):
    decoded_message = base64.urlsafe_b64decode(encrypted_message + '=' * (-len(encrypted_message) % 4))
    iv = decoded_message[:16]
    encrypted_data = decoded_message[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # 移除填充
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return unpadded_data.decode()

key = generate_key('쵹昲⬛캻⌰㫍')

sg.SetOptions(font=('Arial', 12))
# GUI布局
layout = [
    [
        sg.Column([
            [sg.Text("服务器地址和端口号"),
            sg.Input(default_text='localhost', size=(15, 1), key='-ADDRESS-'),
            sg.Text(":"),
            sg.Input(key='-PORT-', default_text='12345', size=(6, 1))],
        ], justification='1'),
    ], 
    [sg.Text("发送消息:"),
    sg.Input(key='-MESSAGE-', size=(49, 2))],
    [sg.Text("本地加密:"),
    sg.Input(key='-MESSAGE2-', size=(49, 2))],
    [sg.Text("本地解密:"),
    sg.Input(key='-MESSAGE3-', size=(49, 2))],
    [sg.Button("发送"), sg.Button("本地加密"), sg.Button("本地解密"), sg.Button('清屏'), sg.Button("退出")],
    [sg.Multiline(size=(60, 20), key='-OUTPUT-', reroute_stdout=True)]
]

window = sg.Window("加解密客户端工具", layout)

# 创建套接字
client_socket = None

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == '退出':
        break

    if event == '发送':
        server_host = str(values['-ADDRESS-'])
        server_port = int(values['-PORT-'])
        message = values['-MESSAGE-']

        try:
            if client_socket is None:
                # 连接服务器
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((server_host, server_port))

                # 接收服务器端的欢迎消息
                welcome_message = client_socket.recv(1024).decode()
                print(welcome_message)


            # 发送消息
            encrypted_message = encrypt_message(message, key)
            client_socket.send(encrypted_message.encode())

            # 发送结束标志
            client_socket.send(b'EOF')


            # 接收加密数据
            received_data = b''
            while True:
                data = client_socket.recv(1024)
                #if not data:
                    #break
                received_data += data
                if b'EOF' in data:
                    break

            # 显示加密数据
            encrypted_data = received_data[:-3].decode()
            print("收到的加密数据:", encrypted_data)

            # 解密数据
            decrypted_data = decrypt_message(encrypted_data.strip(), key)
            print("解密后的数据:", decrypted_data)


        except Exception as e:
            print("发生错误:", str(e))

    elif event == '本地加密':
        local_message = values['-MESSAGE2-']
        try:
            encrypted_data = encrypt_message(local_message, key)
            print("加密后的数据:", encrypted_data)

        except Exception as e:
            print("发生错误:", str(e))

    elif event == '本地解密':
        decode_message = values['-MESSAGE3-']
        try:
            decrypted_data = decrypt_message(decode_message.strip(), key)
            print("解密后的数据:", decrypted_data)

        except Exception as e:
            print("发生错误:", str(e))

    elif event == '清屏':
        # 清空 Output 元素
        window['-OUTPUT-'].update('')


window.close()

# 关闭客户端套接字
if client_socket is not None:
    client_socket.close()
