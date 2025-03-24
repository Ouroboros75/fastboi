import socket
import struct
import os
import time

SERVER_IP = "192.168.1.11"  # Change this to receiver's IP if remote
#SERVER_IP = "127.0.0.1"  # Change this to receiver's IP if remote
SERVER_PORT = 12345
#PACKET_SIZE = 65535  # Bytes per packet
PACKET_SIZE = 8184  # Bytes per packet
FILE_CHUNK_SIZE = 81840
#PACKET_SIZE = 8192  # Bytes per packet
#FILE_CHUNK_SIZE = 81920
SEND_BUFFER_SIZE = 16 * 1024 * 1024  # 16MB send buffer (increase if needed)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUFFER_SIZE)  # Increase send buffer
#sock.setsockopt(socket.IPPROTO_IP, IN.IP_MTU_DISCOVER, IN.IP_PMTUDISC_DO)
#sock.setsockopt(socket.IPPROTO_IP, 10,                  0)

def send_file(filename):
    file_size = os.path.getsize(filename)
    total_packets = (file_size // FILE_CHUNK_SIZE) + \
            (file_size % FILE_CHUNK_SIZE != 0)

    with open(filename, "rb") as f:
        #mark = time.time() 
        for seq_num in range(total_packets):
            chunk = f.read(FILE_CHUNK_SIZE)
            for i in range(0, FILE_CHUNK_SIZE, PACKET_SIZE):
                packet = chunk[i:i+PACKET_SIZE]
                sock.sendto(packet, (SERVER_IP, SERVER_PORT))

                #time.sleep(0.001)

    print(f"File '{filename}' sent successfully.")

# Example usage
send_file("file_send")  # Replace with the file you want to send
