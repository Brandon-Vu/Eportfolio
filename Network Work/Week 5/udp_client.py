import socket
import datetime

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 65433)

message = input("Enter message: ")
start_time = datetime.datetime.now()
udp_client.sendto(message.encode(), server_address)
response, _ = udp_client.recvfrom(1024)
end_time = datetime.datetime.now()

print(f"Server response: {response.decode()}")
print(f"Time taken to send data over UDP: {(end_time - start_time).total_seconds()} seconds")
udp_client.close()