import socket
import struct
import os
import time

SERVER_IP = "192.168.1.11"  # Change this to receiver's IP if remote
SERVER_PORT  = 12345
PACKET_SIZE = 1452    # Bytes per packet
#PACKET_SIZE = 8184    # Bytes per packet
#FILE_CHUNK_SIZE = 81840
SEND_BUFFER_SIZE = 32 * 1024 * 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUFFER_SIZE)
#sock.setsockopt(socket.IPPROTO_IP, IN.IP_MTU_DISCOVER, IN.IP_PMTUDISC_DO)
#sock.setsockopt(socket.IPPROTO_IP, 10,                 0)

def send_file(filename):
    file_size = os.path.getsize(filename)
    total_packets = (file_size // PACKET_SIZE) + \
            (file_size % PACKET_SIZE != 0)

    with open(filename, "rb") as f:
        for seq_num in range(total_packets):
            chunk = f.read(PACKET_SIZE)
            packet = struct.pack("!II", seq_num, total_packets) + chunk
            prob = sock.sendto(packet, (SERVER_IP, SERVER_PORT))
            #if no free space in send buffer -> \
            #program terminates actually
            if(prob!=1460):
                print(prob)
            #for i in range(1000):
            #    pass

    print(f"File '{filename}' sent successfully.")

while(True):
    send_file("file_send")  # Replace with the file you want to send
