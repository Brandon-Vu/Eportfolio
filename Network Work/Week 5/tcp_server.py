import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 65432))
server_socket.listen(1)
print("TCP Server is listening on port 65432...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connected to {client_address}")
    
    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")
    
    # Echo the received data
    client_socket.sendall(b"ACK: " + data)
    client_socket.close()