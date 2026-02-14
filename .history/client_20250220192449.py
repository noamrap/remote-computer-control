import socket
import ssl
import pyautogui
import cv2
import numpy as np
import struct
import threading
import time

SERVER_IP = "192.168.1.133"
SERVER_PORT = 12345

def send_screen(client_socket):
    while True:
        try:
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            mouse_x, mouse_y = pyautogui.position()
            cursor_color = (0, 0, 255)
            cursor_size = 7
            cv2.circle(frame, (mouse_x, mouse_y), cursor_size, cursor_color, thickness=-1)
            _, buffer = cv2.imencode('.jpg', frame)
            data = buffer.tobytes()
            header = struct.pack('>I', len(data))
            client_socket.sendall(header + data)
        except Exception as e:
            print(f"Error sending screen: {e}")
            break

def receive_and_execute_commands(client_socket):
    while True:
        try:
            header = b""
            while len(header) < 4:
                chunk = client_socket.recv(4 - len(header))
                if not chunk:
                    raise ConnectionError("Socket closed while reading command header")
                header += chunk

            command_length = struct.unpack('>I', header)[0]
            command_data = b""
            while len(command_data) < command_length:
                chunk = client_socket.recv(command_length - len(command_data))
                if not chunk:
                    raise ConnectionError("Socket closed while reading command data")
                command_data += chunk

            command_text = command_data.decode('utf-8').strip()
            command = command_text.split()
            if not command:
                continue

            if "+" in command_text:
                hotkeys = command_text.split('+')
                pyautogui.hotkey(*hotkeys)  

            elif command[0] == "move_mouse":
                if len(command) >= 3:
                    x, y = int(command[1]), int(command[2])
                    pyautogui.moveTo(x, y)
            elif command[0] == "click":
                pyautogui.click()
            elif command[0] == "type_text":
                text = " ".join(command[1:])  
                pyautogui.write(text, interval=0.03)  
            elif command[0] == "scroll":
                if len(command) >= 2:
                    amount = int(command[1])
                    pyautogui.scroll(amount)
        except Exception as e:
            print(f"Error executing command: {e}")
            break

def main():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(client_socket, server_hostname="localhost")
    secure_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Securely connected to {SERVER_IP}:{SERVER_PORT}")
    threading.Thread(target=send_screen, args=(secure_socket,), daemon=True).start()
    threading.Thread(target=receive_and_execute_commands, args=(secure_socket,), daemon=True).start()
    secure_socket.close()

if __name__ == "__main__":
    main()
