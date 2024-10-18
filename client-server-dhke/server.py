from Crypto.Cipher import AES
from Crypto.Util.number import *
from Crypto.Util.Padding import pad, unpad
import threading
import hashlib
import socket 
import random

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5237

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f"[+] Listening on {SERVER_HOST}:{SERVER_PORT}")

## public key parameters
g = 2
p = getPrime(512)

server_priv = random.randint(2, p - 1)
server_pub = pow(g, server_priv, p)
public_key = (g, p, server_pub)

def init(client_socket, client_address):
    connection_message = f"[+] Established connection with client at {client_address[0]}:{client_address[1]}\n"
    print(connection_message)
    return 

def public_key_param(client_socket):
    public_key_message = f"server public key (g, p, server_pub) = ({g}, {p}, {server_pub})"
    print(public_key_message)
    client_socket.send((public_key_message + "\n").encode())
    return

client_socket, client_address = server_socket.accept()

init(client_socket, client_address)
public_key_param(client_socket)

client_public_key = client_socket.recv(2048).decode().strip()
print(f"{client_public_key}\n")
_, __, client_pub = eval(client_public_key.split(' = ')[1])
shared_secret = pow(client_pub, server_priv, p)

key = hashlib.sha256(long_to_bytes(shared_secret)).digest()
cipher = AES.new(key, AES.MODE_ECB)

def encrypt(plaintext):
    ciphertext = hex(bytes_to_long(cipher.encrypt(pad(plaintext.encode(), AES.block_size))))[2:]
    return ciphertext

def decrypt(ciphertext):
    ciphertext = long_to_bytes(int(ciphertext, 16))
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return plaintext 

counter = 1

def client_receive(client_socket, client_address):
    global counter
    while True:
        try:
            encrypted_message = client_socket.recv(1024).decode()
            print(f"[*] Message {counter} received: {encrypted_message}")

            decrypted_message = decrypt(encrypted_message)
            print(f"[*] Decrypted message {counter}: {decrypted_message}\n")
            
            counter += 1
        except (ConnectionResetError, ValueError):
            print(f"[-] Connection with client at {client_address[0]}:{client_address[1]} disconnected.")
            client_socket.close()
            exit(0)
            break
    return

def server_send(client_socket, client_address):
    global counter
    while True:
        try:
            message = input()

            encrypted_message = encrypt(message)
            print(f"[*] Encrypted message {counter} sent: {encrypted_message}\n")
            client_socket.send(encrypted_message.encode())
            
            counter += 1
        except (ConnectionResetError, ValueError):
            print(f"[-] Connection with client at {client_address[0]}:{client_address[1]} disconnected.")
            client_socket.close()
            exit(0)
            break
    return

try:
    recv_thread = threading.Thread(target=client_receive, args=(client_socket, client_address,))
    send_thread = threading.Thread(target=server_send, args=(client_socket, client_address,))

    recv_thread.start()
    send_thread.start()

    recv_thread.join()
    send_thread.join()
except (ConnectionResetError, ValueError):
    print(f"[-] Connection with client at {client_address[0]}:{client_address[1]} disconnected.")
    client_socket.close()
    exit(0)
