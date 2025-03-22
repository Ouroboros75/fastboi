import socket
import struct

RECEIVER_IP = "0.0.0.0"  # Listen on all interfaces
RECEIVER_PORT = 12345
PACKET_SIZE = 8184       # Bytes per packet
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
    
while True:
    try:
        full_packet, addr = sock.recvfrom(PACKET_SIZE+8)  #Max UDP payload (header + data)
        """
        data, addr = sock.recvfrom(PACKET_SIZE+8)  #Max UDP payload (header + data)
        full_packet += data
        if (len(full_packet) < PACKET_SIZE+8) and (prev != total_packets - 1):
            print(f">not whole packet at {prev} != {total_packets}")
            continue
        if len(full_packet) > PACKET_SIZE+8:
            tail = full_packet[PACKET_SIZE+8:]
            full_packet = full_packet[:PACKET_SIZE+8]
            print(f"cut length == {len(full_packet)}")
            """

        seq_num, total_packets = struct.unpack("!II", full_packet[:8])  # Extract header
        payload = full_packet[8:]  # Extract file chunk

        if(seq_num != prev):
            print(f"out-of-order {seq_num} != {prev}")
            prev = seq_num
        prev += 1

        buffer[seq_num] = payload  # Store chunk
        expected_packets = total_packets  # Update expected count
        """
        full_packet = tail
        tail = b""
        """

        if(seq_num == expected_packets - 1):
            print(f">> got last packet. received {len(buffer)} / {expected_packets}")
            if(len(buffer) != expected_packets):
                break
            print("All packets received. Writing to file...")
            with open("received_file.bin", "wb") as f:
                for i in range(expected_packets):
                    f.write(buffer[i])  # Write chunks in order // only after receiving all chunks -> not gonna cut it i think
            print("File received successfully as 'received_file.bin'.")
            buffer.clear()  # Reset for next file transfer
            break

    except BlockingIOError:
        pass
