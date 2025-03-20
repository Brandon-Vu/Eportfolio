import socket

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('localhost', 65433))
print("UDP File Server is listening on port 65433...")

with open('received_file_udp.txt', 'wb') as f:
    while True:
        data, client_address = udp_server.recvfrom(1024)
        if data == b'EOF':
            break
        f.write(data)

print("File received over UDP and saved as 'received_file_udp.txt'")
