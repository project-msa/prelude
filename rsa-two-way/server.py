import socket 
from Crypto.Util.number import *

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4576

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((SERVER_HOST, SERVER_PORT))
server.listen()

print(f"[+] Listening on {SERVER_HOST}:{SERVER_PORT}")


## generate key
p = getPrime(512)
q = getPrime(512)

assert p != q

server_n = p*q
server_e = 0x10001

server_phi  = (p - 1)*(q - 1)
server_d = pow(server_e, -1, server_phi)

server_public_key = (server_n, server_e)
server_private_key = (server_n, server_e, server_d)

def init(client_address):
    connection_message = f"[+] Established connection with client at {client_address}"
    print(connection_message)

    return

def send_public_key_param(client_socket):
    param_message = f"[+] public key params (n, e) = ({server_n}, {server_e})\n"
    client_socket.send(param_message.encode())

    return

def recieve_public_key_param():
    params = client_socket.recv(1024).decode()
    n, e = eval(params.strip().split(' = ')[1])
    return (n , e)

def encrypt(msg):
    msg = bytes_to_long(msg.encode())
    msg = pow(msg, client_public_key[1], client_public_key[0])
    return hex(msg)[2:]


client_socket, client_address = server.accept()

# send server key and receive client key
init(client_address)
send_public_key_param(client_socket)
client_public_key = recieve_public_key_param()

counter = 1

while True:
    try:
        request = client_socket.recv(1024).decode()
        print(f"[*] Message {counter} Received: {request}")

        decrypted_message = long_to_bytes(pow(int(request, 16), server_d, server_n)).decode()
        print(f"[*] Decrypted Message {counter}: {decrypted_message}\n")
        counter += 1
    except (ConnectionResetError, ValueError):
        print(f"[-] Connection with client at {client_address[0]}:{client_address[1]} disconnected.")
        client_socket.close()
        break

    message = input("Enter the message to send to client (limit = 1024): ")
    encrypted_message = encrypt(message)
    print(f"[*] Encrypted message {counter} sent : {encrypted_message}\n")

    client_socket.send(encrypted_message.encode())
    counter += 1