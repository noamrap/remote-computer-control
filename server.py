import socket
import ssl
import threading
import cv2
import numpy as np
import struct
import time
SERVER_IP = "192.168.1.133"
SERVER_PORT = 54321

def handle_client(client_socket):
    print("Handling client...")
    try:
        while True:
            header = b""
            while len(header) < 4:
                chunk = client_socket.recv(4 - len(header))
                if not chunk:
                    raise ConnectionError("Socket closed while reading header")
                header += chunk

            data_length = struct.unpack('>I', header)[0]

            data = b""
            while len(data) < data_length:
                chunk = client_socket.recv(data_length - len(data))
                if not chunk:
                    raise ConnectionError("Socket closed while reading image data")
                data += chunk

            frame = np.frombuffer(data, dtype=np.uint8)
            img = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            if img is not None:
                cv2.imshow("Client Screen", img)
                if cv2.waitKey(1) in [ord('q'), ord('Q'), ord('/')] :
                    print("Closing window...")
                    break
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        print("Client disconnected.")
        client_socket.close()
        cv2.destroyAllWindows()
        
COMMAND_RATE_LIMIT = 0.1  
last_command_time = 0  

def send_commands(client_socket):
    global last_command_time
    try:
        while True:
            command = input("Enter command (e.g., 'move_mouse 300 400', 'click', 'type_text Hello', 'alt+shift', 'scroll 10'): ")

            if command.strip().lower() == "exit":
                print("Exiting command mode...")
                break

            current_time = time.time()
            if current_time - last_command_time < COMMAND_RATE_LIMIT:
                print(f"Rate Limit: Please wait before sending another command.")
                continue

            last_command_time = current_time

            command_bytes = command.encode('utf-8')
            header = struct.pack('>I', len(command_bytes))
            client_socket.sendall(header + command_bytes)

    except Exception as e:
        print(f"Error sending command: {e}")

def main():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(3)
    print(f"Server is securely listening on {SERVER_IP}:{SERVER_PORT}")

    secure_socket = context.wrap_socket(server_socket, server_side=True)

    while True:
        print("Waiting for a client to connect...")
        client_socket, client_address = secure_socket.accept()
        print(f"Client connected: {client_address}")
        
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
        threading.Thread(target=send_commands, args=(client_socket,), daemon=True).start()

        

if __name__ == "__main__":
    main()
