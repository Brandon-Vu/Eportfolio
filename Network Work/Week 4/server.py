# Exercise 1-4: UDP Chat Application

import socket

# Encryption Functions
def xor_cipher(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def encrypt_message(message, key):
    encrypted_bytes = xor_cipher(message.encode(), key.encode())
    return encrypted_bytes.hex()

def decrypt_message(hex_string, key):
    encrypted_bytes = bytes.fromhex(hex_string)
    decrypted_bytes = xor_cipher(encrypted_bytes, key.encode())
    return decrypted_bytes.decode()

# Users and Passwords for Authentication
valid_users = {
    "brandon": "pass123",
    "goldsmiths": "university"
}

# Dictionary to store authenticated clients
authenticated_clients = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 65433))
print("UDP Chat Server is running and waiting for messages on port 65433...")

while True:
    data, client_address = server_socket.recvfrom(4096)
    message = data.decode()
    if client_address not in authenticated_clients:
        if message.startswith("AUTH"):
            parts = message.split()
            if len(parts) == 3:
                _, username, password = parts
                if username in valid_users and valid_users[username] == password:
                    authenticated_clients[client_address] = username
                    server_socket.sendto("AUTH_SUCCESS".encode(), client_address)
                    print(f"{username} authenticated from {client_address}")
                else:
                    server_socket.sendto("AUTH_FAILED".encode(), client_address)
            else:
                server_socket.sendto("AUTH_FORMAT_ERROR".encode(), client_address)
        else:
            server_socket.sendto("PLEASE_AUTHENTICATE".encode(), client_address)
    else:
        try:
            decrypted_message = decrypt_message(message, "encrypted")
        except Exception as e:
            decrypted_message = "<decryption error>"
        sender = authenticated_clients[client_address]
        full_message = f"{sender}: {decrypted_message}"
        print(f"Broadcasting: {full_message}")
        for client, user in authenticated_clients.items():
            if client != client_address:
                # Encrypt the message before sending.
                encrypted_message = encrypt_message(full_message, "encrypted")
                server_socket.sendto(encrypted_message.encode(), client)