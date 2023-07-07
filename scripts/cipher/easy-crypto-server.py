#使用cryptography库,pip3 install cryptography

import socket
from threading import Thread
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
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

def handle_client(client_socket, address, key):
    while True:
        try:
            # 接收消息
            received_data = b''
            while True:
                data = client_socket.recv(1024)
                #if not data:
                    #break
                received_data += data
                if b'EOF' in data:
                    break

            encrypted_message = received_data[:-3].decode()
            print("收到的加密数据:", encrypted_message)
            decrypted_message = decrypt_message(encrypted_message.strip(), key)
            print("收到的消息:", decrypted_message)

            # 根据收到的消息进行条件判断，发送相应的列表数据给客户端
            if decrypted_message == "1":
                # 构造列表数据1
                data_list = ["数据1", "数据2", "数据3"]
                # 将列表数据转换为字符串
                data_str = "\n".join(data_list)
                # 加密列表数据并发送给客户端
                encrypted_data = encrypt_message(data_str, key)
                client_socket.sendall(encrypted_data.encode() + b'EOF')
            elif decrypted_message == "2":
                # 构造要发送的数据
                data = "2"
                # 加密数据
                encrypted_data = encrypt_message(data, key)
                # 发送加密数据给客户端
                client_socket.sendall(encrypted_data.encode() + b'EOF')
            elif decrypted_message == "特定字符2":
                # 构造要发送的数据
                data = "这是加密数据2"
                # 加密数据
                encrypted_data = encrypt_message(data, key)
                # 发送加密数据给客户端
                client_socket.sendall(encrypted_data.encode() + b'EOF')
            else:
                # 发送默认回复
                reply_message = decrypted_message
                encrypted_reply = encrypt_message(reply_message, key)
                client_socket.sendall(encrypted_reply.encode() + b'EOF')



        except ConnectionResetError:
            print("客户端连接异常中断:", client_address)
            break


        #except ConnectionResetError:
            #print("客户端连接异常中断:", client_address)
            #client_socket.close()
        except Exception as e:
            print("发生错误:", str(e))

        #finally:
            # 关闭客户端套接字
            #client_socket.close()
            #print("客户端连接已关闭:", address)

key = generate_key('쵹昲⬛캻⌰㫍')

# 创建套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_host = 'localhost'
server_port = 12345
server_socket.bind((server_host, server_port))
server_socket.listen(100)
print("等待客户端连接...")

while True:
    # 接受客户端连接
    client_socket, client_address = server_socket.accept()
    print("客户端已连接:", client_address)

    # 发送欢迎消息
    welcome_message = "欢迎连接到服务器！"
    client_socket.send(welcome_message.encode())

    # 启动新线程处理客户端连接
    client_thread = Thread(target=handle_client, args=(client_socket, client_address, key))
    client_thread.start()


