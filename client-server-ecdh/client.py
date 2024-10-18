from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad
import threading
import hashlib
import socket 
import random
from time import time

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5825

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((SERVER_HOST, SERVER_PORT))

connection_message = f"[+] Established connection with server at {SERVER_HOST}:{SERVER_PORT}\n"
print(connection_message)

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0x0000000000000000000000000000000000000000000000000000000000000000
b = 0x0000000000000000000000000000000000000000000000000000000000000007
G = (0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)

E = EllipticCurve(GF(p), [a, b])
G = E(G)

server_public_key = server_socket.recv(2048).decode().strip()
print(server_public_key)
server_pub_x, server_pub_y, _ = server_public_key.split(' = ')[1][1:-2].split(' : ')
server_pub = E((int(server_pub_x), int(server_pub_y)))

client_priv = random.randint(2, p - 1)
client_pub = client_priv * G
shared_secret = client_priv * server_pub

public_key_message = f"client_pub = {client_pub}"
print(f"{public_key_message}\n")
server_socket.send((public_key_message + "\n").encode())

key = hashlib.sha256(long_to_bytes(int(shared_secret[0]))).digest()
cipher = AES.new(key, AES.MODE_ECB)

def encrypt(plaintext):
    ciphertext = hex(bytes_to_long(cipher.encrypt(pad(plaintext.encode(), AES.block_size))))[2:]
    return ciphertext

def decrypt(ciphertext):
    ciphertext = long_to_bytes(int(ciphertext, 16))
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return plaintext 

counter = 1

def server_receive(server_socket):
    global counter 
    while True: 
        try:
            encrypted_message = server_socket.recv(1024).decode()
            print(f"[*] Message {counter} received: {encrypted_message}")

            decrypted_message = decrypt(encrypted_message)
            print(f"[*] Decrypted message {counter}: {decrypted_message}\n")
            
            counter += 1
        except (ConnectionResetError, ValueError):
            print(f"[-] Connection with server at {SERVER_HOST}:{SERVER_PORT} disconnected.")
            server_socket.close()
            exit(0)
            break
    return

def client_send(server_socket):
    global counter
    while True:
        try:
            message = input("")

            encrypted_message = encrypt(message)
            print(f"[*] Encrypted message {counter} sent: {encrypted_message}\n")
            server_socket.send(encrypted_message.encode())
            
            counter += 1
        except (ConnectionResetError, ValueError):
            print(f"[-] Connection with server at {SERVER_HOST}:{SERVER_PORT} disconnected.")
            server_socket.close()
            exit(0)
            break
    return

try:
    recv_thread = threading.Thread(target=server_receive, args=(server_socket,))
    send_thread = threading.Thread(target=client_send, args=(server_socket,))

    recv_thread.start()
    send_thread.start()

    recv_thread.join()
    send_thread.join()
except: 
    print(f"[-] Connection with server at {SERVER_HOST}:{SERVER_PORT} disconnected.")
    server_socket.close()
    exit(0)