# Exercise 1-4: UDP Chat Application

import socket
import threading

def xor_cipher(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def encrypt_message(message, key):
    encrypted_bytes = xor_cipher(message.encode(), key.encode())
    return encrypted_bytes.hex()

def decrypt_message(hex_string, key):
    encrypted_bytes = bytes.fromhex(hex_string)
    decrypted_bytes = xor_cipher(encrypted_bytes, key.encode())
    return decrypted_bytes.decode()

server_address = ('localhost', 65433)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

username = input("Enter username: ")
password = input("Enter password: ")

auth_message = f"AUTH {username} {password}"
client_socket.sendto(auth_message.encode(), server_address)
response, _ = client_socket.recvfrom(4096)
if response.decode() == "AUTH_SUCCESS":
    print("Authenticated successfully!")
else:
    print("Authentication failed:", response.decode())
    client_socket.close()
    exit()

def listen_for_messages():
    while True:
        try:
            data, _ = client_socket.recvfrom(4096)
            encrypted_message = data.decode()
            try:
                decrypted_message = decrypt_message(encrypted_message, "encrypted")
                print(decrypted_message)
            except Exception as e:
                print("Error decrypting message:", e)
        except:
            break

listener_thread = threading.Thread(target=listen_for_messages, daemon=True)
listener_thread.start()

print("You can now start sending messages. Type 'exit' to quit.")
while True:
    msg = input()
    if msg.lower() == "exit":
        break
    encrypted_msg = encrypt_message(msg, "encrypted")
    client_socket.sendto(encrypted_msg.encode(), server_address)

client_socket.close()
