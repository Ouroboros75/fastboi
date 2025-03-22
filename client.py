import socket
import struct
import os
import time

SERVER_IP = "192.168.1.11"  # Change this to receiver's IP if remote
#SERVER_IP = "127.0.0.1"  # Change this to receiver's IP if remote
SERVER_PORT = 12345
#PACKET_SIZE = 8952  # Bytes per packet
PACKET_SIZE = 8184  # Bytes per packet

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.setsockopt(socket.IPPROTO_IP, IN.IP_MTU_DISCOVER, IN.IP_PMTUDISC_DO)
sock.setsockopt(socket.IPPROTO_IP, 10,                  0)

def send_file(filename):
    file_size = os.path.getsize(filename)
    total_packets = (file_size // PACKET_SIZE) + (file_size % PACKET_SIZE != 0)

    with open(filename, "rb") as f:
        mark = time.time() 
        count = 0
        for seq_num in range(total_packets):
            chunk = f.read(PACKET_SIZE)  # Read file chunk
            header = struct.pack("!II", seq_num, total_packets)  # seq_num (4B), total_packets (4B)
            packet = header + chunk  # Combine header and data
            
            sock.sendto(packet, (SERVER_IP, SERVER_PORT))
            count+=1
            if(time.time() - mark >= 1):
                print(f"bitrate: {(8 * count * PACKET_SIZE) / (1/(time.time()-mark))} bps")
                count = 0
                mark = time.time()

            time.sleep(0.000005)  # Small delay to prevent overwhelming the receiver // makes this the "wrangling" variable later
            

    print(f"File '{filename}' sent successfully.")

# Example usage
send_file("file_send")  # Replace with the file you want to send
