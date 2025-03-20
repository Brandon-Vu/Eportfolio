import socket

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('localhost', 65433))
print("UDP Server is listening on port 65433...")

while True:
    data, client_address = udp_server.recvfrom(1024)
    print(f"Received from {client_address}: {data.decode()}")
    udp_server.sendto(b"ACK: " + data, client_address)