import socket
import datetime

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 65432))

with open('file_to_send.txt', 'rb') as f:
    start_time = datetime.datetime.now()
    client_socket.sendfile(f)
    end_time = datetime.datetime.now()

print(f"File sent over TCP in {(end_time - start_time).total_seconds()} seconds")
client_socket.close()
