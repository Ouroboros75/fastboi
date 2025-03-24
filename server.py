import socket
import struct

RECEIVER_IP = "0.0.0.0"  # Listen on all interfaces
RECEIVER_PORT = 12345
#PACKET_SIZE = 8184       # Bytes per packet
PACKET_SIZE = 1452
PreBuffer = [None] * 688706 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 200 * 1024 * 1024)  # 100MB buffer
sock.bind((RECEIVER_IP, RECEIVER_PORT))
sock.setblocking(False)

buffer = {}  # Store received packets
expected_packets = None  # Total packets expected

print("UDP Receiver is listening...")
prev = 0
total_packets = 2
tail = b""
full_packet = b""
count = 0
    
while True:
    try:
        full_packet, addr = sock.recvfrom(PACKET_SIZE+8)
        seq_num, total_packets = struct.unpack("!II", full_packet[:8])  
        payload = full_packet[8:]  # Extract file chunk

        if(seq_num != prev):
            print(f"out-of-order {seq_num} != {prev}")
            prev = seq_num
        prev += 1

        #if this buffer isn't pre-allocated -> guarranteed to lose some
        #packets in the first GIG
        PreBuffer[seq_num] = payload  # Store chunk
        expected_packets = total_packets  # Update expected count

        if(seq_num == expected_packets - 1):
            print(f">> got last packet. received {len(PreBuffer)} / {expected_packets} test number {count}")
            #if(len(buffer) != expected_packets):
            #    break
            #print("All packets received. Writing to file...")
            #with open("received_file.bin", "wb") as f:
            #    for i in range(expected_packets):
            #        f.write(buffer[i])
            #print("File received successfully as 'received_file.bin'.")
            #buffer.clear()  # Reset for next file transfer
                             # doing this causes lost packets for the next one as well -> too much overhead
            #break
            count += 1
            prev = 0
            total_packets = 2

    except BlockingIOError:
        pass
