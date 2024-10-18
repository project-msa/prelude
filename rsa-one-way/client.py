from Crypto.Util.number import *
import socket 

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4576

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

connection_message = f"[+] Established connection with server at {SERVER_HOST}:{SERVER_PORT}"
print(connection_message)

params = client.recv(1024).decode()
print(params)

n, e = eval(params.strip().split(' = ')[1])
public_key = (n, e)

counter = 1

def encrypt(msg):
    msg = bytes_to_long(msg.encode())
    msg = pow(msg, e, n)
    return hex(msg)[2:]

while True:
    message = input("Enter the message (limit size = 1024): ")

    encrypted_message = encrypt(message)
    print(f"[*] Encrypted message {counter} sent: {encrypted_message}\n")

    client.send(encrypted_message.encode())
    counter += 1
