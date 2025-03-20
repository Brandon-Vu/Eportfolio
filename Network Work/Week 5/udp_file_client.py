import socket
import datetime

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 65433)

with open('file_to_send.txt', 'rb') as f:
    file_data = f.read()

start_time = datetime.datetime.now()
udp_client.sendto(file_data, server_address)
udp_client.sendto(b'EOF', server_address)
end_time = datetime.datetime.now()

print(f"File sent over UDP in {(end_time - start_time).total_seconds()} seconds")
udp_client.close()
