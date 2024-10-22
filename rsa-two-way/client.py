from Crypto.Util.number import *
import socket 
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4576

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

connection_message = f"[+] Established connection with server at {SERVER_HOST}:{SERVER_PORT}"
print(connection_message)

## generate key
p = getPrime(512)
q = getPrime(512)

assert p != q

client_n = p*q
client_e = 0x10001

client_phi  = (p - 1)*(q - 1)
client_d = pow(client_e, -1, client_phi)

client_public_key = (client_n, client_e)
client_private_key = (client_n, client_e, client_d)

def send_public_key_param():
    param_message = f"[+] public key params (n, e) = ({client_n}, {client_e})\n"
    client.send(param_message.encode())

    return

def recieve_public_key_param():
    params = client.recv(1024).decode()
    n, e = eval(params.strip().split(' = ')[1])
    return (n , e)

def encrypt(msg):
    msg = bytes_to_long(msg.encode())
    msg = pow(msg, server_public_key[1], server_public_key[0])
    return hex(msg)[2:]

def decrypt(msg):
    decrypted_message = long_to_bytes(pow(int(msg, 16), client_d, client_n)).decode()
    return decrypted_message
server_public_key = recieve_public_key_param()
send_public_key_param()

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
            client.send(encrypted_message.encode())
            
            counter += 1
        except (ConnectionResetError, ValueError):
            print(f"[-] Connection with server at {SERVER_HOST}:{SERVER_PORT} disconnected.")
            client.close()
            exit(0)
            break
    return

try:
    recv_thread = threading.Thread(target=server_receive, args=(client,))
    send_thread = threading.Thread(target=client_send, args=(client,))

    recv_thread.start()
    send_thread.start()

    recv_thread.join()
    send_thread.join()
except: 
    print(f"[-] Connection with server at {SERVER_HOST}:{SERVER_PORT} disconnected.")
    client.close()
    exit(0)