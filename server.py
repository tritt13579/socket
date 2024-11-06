import socket
import os
import threading

def handle_client(conn, addr):
    print(f"Connected by {addr}")

    # Xác định đường dẫn file nhận (đảm bảo nằm cùng thư mục với server.py)
    file_path = os.path.join(os.path.dirname(__file__), f"received_file_{addr[1]}.txt")
    received_size = 0  # Biến lưu kích thước đã nhận

    with open(file_path, "wb") as f:
        while True:
            data = conn.recv(1024)  # Nhận từng gói 1024 bytes
            if not data:
                break  # Thoát vòng lặp khi không còn dữ liệu
            f.write(data)
            received_size += len(data)

    if received_size > 0:
        print(f"File received successfully from {addr}. Total size: {received_size} bytes.")
    else:
        print(f"No data received from {addr}. File transfer failed.")

    conn.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print("Server is listening...")

    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        server_socket.close()

# Cấu hình IP và Port của server
HOST = 'localhost'
PORT = 5000

start_server(HOST, PORT)