import socket 

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4576

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((SERVER_HOST, SERVER_PORT))
server.listen()

print(f"[+] Listening on {SERVER_HOST}:{SERVER_PORT}")

## public key parameters
from Crypto.Util.number import *

p = getPrime(512)
q = getPrime(512)

assert p != q 

n = p * q 
e = 0x10001 

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

public_key = (n, e)
private_key = (n, e, d)

def init(client_socket, client_address):
    connection_message = f"[+] Established connection with client at {client_address[0]}:{client_address[1]}\n"
    print(connection_message)

    return 

def public_key_param(client_socket):
    param_message = f"[+] public key params (n, e) = ({n}, {e})\n"
    client_socket.send(param_message.encode())
    return 

client_socket, client_address = server.accept()

init(client_socket, client_address)
public_key_param(client_socket)

counter = 1
while True:
    try:
        request = client_socket.recv(1024).decode()
        print(f"[*] Message {counter} Received: {request}")

        decrypted_message = long_to_bytes(pow(int(request, 16), d, n)).decode()
        print(f"[*] Decrypted Message {counter}: {decrypted_message}\n")
        counter += 1
    except (ConnectionResetError, ValueError):
        print(f"[-] Connection with client at {client_address[0]}:{client_address[1]} disconnected.")
        client_socket.close()
        break