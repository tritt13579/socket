# import socket
# import os
# import tkinter as tk
# from tkinter import ttk
# import threading
# import subprocess

# # Biến toàn cục để lưu trữ đường dẫn của file đã nhận cuối cùng
# received_files = []
# received_files_dir = os.path.join(os.path.dirname(__file__), "received_files")

# # Tạo thư mục nếu chưa tồn tại
# if not os.path.exists(received_files_dir):
#     os.makedirs(received_files_dir)

# def update_status(message, is_server_status=False):
#     """Hàm cập nhật thông báo lên nhãn trạng thái."""
#     if 'root' in globals() and is_server_status:
#         status_label.config(text=message)
#         root.update_idletasks()

# def handle_client(conn, addr):
#     global received_files

#     # Nhận tên file trước
#     file_name = conn.recv(1024).decode().strip()
#     file_path = os.path.join(received_files_dir, file_name)
#     received_size = 0  # Biến lưu kích thước đã nhận

#     with open(file_path, "wb") as f:
#         while True:
#             data = conn.recv(1024)  # Nhận từng gói 1024 bytes
#             if not data:
#                 break  # Thoát vòng lặp khi không còn dữ liệu
#             f.write(data)
#             received_size += len(data)

#     if received_size > 0:
#         received_files.append(file_path)  # Cập nhật danh sách file đã nhận
#         status_tree.insert("", "end", values=(addr[0], addr[1], os.path.basename(file_path), received_size))
#     else:
#         update_status(f"No data received from {addr}. File transfer failed.", is_server_status=True)

#     conn.close()

# def accept_connections():
#     global server_socket, is_running
#     try:
#         while is_running:
#             conn, addr = server_socket.accept()
#             threading.Thread(target=handle_client, args=(conn, addr)).start()
#     except Exception as e:
#         if is_running:  # Chỉ cập nhật trạng thái nếu server đang chạy
#             update_status(f"Error: {e}", is_server_status=True)
#     finally:
#         if server_socket:  # Kiểm tra nếu socket tồn tại
#             server_socket.close()

# def start_server():
#     global server_socket, is_running
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind(('localhost', 5000))
#     server_socket.listen(5)
#     is_running = True
#     start_btn.config(state=tk.DISABLED)
#     stop_btn.config(state=tk.NORMAL)
#     update_status("Server is listening...", is_server_status=True)

#     threading.Thread(target=accept_connections).start()

# def stop_server():
#     global is_running, server_socket
#     is_running = False
#     if server_socket:  # Kiểm tra nếu socket tồn tại
#         server_socket.close()
#         server_socket = None  # Đặt server_socket về None sau khi đóng
#     start_btn.config(state=tk.NORMAL)
#     stop_btn.config(state=tk.DISABLED)
#     update_status("Server is stopped", is_server_status=True)

# def open_selected_file():
#     """Hàm mở file được chọn từ bảng."""
#     selected_item = status_tree.selection()
#     if selected_item:
#         file_name = status_tree.item(selected_item[0], "values")[2]
#         file_path = os.path.join(received_files_dir, file_name)
#         if file_path and os.path.exists(file_path):
#             subprocess.Popen(['start', file_path], shell=True)
#         else:
#             update_status("No file to open or file does not exist.", is_server_status=True)
#     else:
#         update_status("No file selected.", is_server_status=True)

# # Thiết lập giao diện đơn giản với Tkinter
# root = tk.Tk()
# root.title("Server Controller")

# # Sử dụng khung để sắp xếp các thành phần giao diện
# frame = ttk.Frame(root, padding="10")
# frame.pack(fill=tk.BOTH, expand=True)

# # Thêm nhãn tiêu đề
# title_label = ttk.Label(frame, text="Server Controller", font=("Helvetica", 16))
# title_label.pack(pady=10)

# # Thêm nút bắt đầu và dừng server
# button_frame = ttk.Frame(frame)
# button_frame.pack(pady=20)

# start_btn = ttk.Button(button_frame, text="Start Server", command=start_server)
# start_btn.pack(side=tk.LEFT, padx=10)

# stop_btn = ttk.Button(button_frame, text="Stop Server", command=stop_server, state=tk.DISABLED)
# stop_btn.pack(side=tk.LEFT, padx=10)

# # Thêm nhãn trạng thái
# status_label = ttk.Label(frame, text="Server is stopped", font=("Helvetica", 12))
# status_label.pack(pady=10)

# # Thêm bảng trạng thái
# status_tree = ttk.Treeview(frame, columns=("IP", "Port", "File", "Size"), show="headings")
# status_tree.heading("IP", text="IP")
# status_tree.heading("Port", text="Port")
# status_tree.heading("File", text="File")
# status_tree.heading("Size", text="Size")
# status_tree.pack(pady=10, fill=tk.BOTH, expand=True)

# # Thêm sự kiện nhấp đúp vào bảng trạng thái để mở file
# def on_double_click(event):
#     open_selected_file()

# status_tree.bind("<Double-1>", on_double_click)

# # Bắt đầu giao diện Tkinter
# root.mainloop()
import socket
import os
import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import hashlib

# Biến toàn cục để lưu trữ đường dẫn của file đã nhận cuối cùng
received_files = []
received_files_dir = os.path.join(os.path.dirname(__file__), "received_files")

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(received_files_dir):
    os.makedirs(received_files_dir)

def calculate_checksum(data):
    """Tính toán checksum của một gói dữ liệu."""
    return hashlib.md5(data).hexdigest()

def update_status(message, is_server_status=False):
    """Hàm cập nhật thông báo lên nhãn trạng thái."""
    if 'root' in globals() and is_server_status:
        status_label.config(text=message)
        root.update_idletasks()

def handle_client(conn, addr):
    global received_files

    # Nhận tên file trước
    file_name = conn.recv(1024).decode().strip()
    file_path = os.path.join(received_files_dir, file_name)
    received_size = 0  # Biến lưu kích thước đã nhận

    with open(file_path, "wb") as f:
        while True:
            # Nhận checksum và gói dữ liệu từ client
            checksum = conn.recv(32).decode()
            data = conn.recv(1024)
            
            if not data:
                break  # Thoát vòng lặp khi không còn dữ liệu

            # Kiểm tra tính toàn vẹn của gói dữ liệu
            calculated_checksum = calculate_checksum(data)
            if calculated_checksum == checksum:
                f.write(data)
                received_size += len(data)
                conn.send(b"ACK")  # Xác nhận gói dữ liệu chính xác
            else:
                conn.send(b"NACK")  # Yêu cầu gửi lại gói

    if received_size > 0:
        received_files.append(file_path)  # Cập nhật danh sách file đã nhận
        status_tree.insert("", "end", values=(addr[0], addr[1], os.path.basename(file_path), received_size))
    else:
        update_status(f"No data received from {addr}. File transfer failed.", is_server_status=True)

    conn.close()

def accept_connections():
    global server_socket, is_running
    try:
        while is_running:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except Exception as e:
        if is_running:  # Chỉ cập nhật trạng thái nếu server đang chạy
            update_status(f"Error: {e}", is_server_status=True)
    finally:
        if server_socket:  # Kiểm tra nếu socket tồn tại
            server_socket.close()

def start_server():
    global server_socket, is_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(5)
    is_running = True
    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)
    update_status("Server is listening...", is_server_status=True)

    threading.Thread(target=accept_connections).start()

def stop_server():
    global is_running, server_socket
    is_running = False
    if server_socket:  # Kiểm tra nếu socket tồn tại
        server_socket.close()
        server_socket = None  # Đặt server_socket về None sau khi đóng
    start_btn.config(state=tk.NORMAL)
    stop_btn.config(state=tk.DISABLED)
    update_status("Server is stopped", is_server_status=True)

def open_selected_file():
    """Hàm mở file được chọn từ bảng."""
    selected_item = status_tree.selection()
    if selected_item:
        file_name = status_tree.item(selected_item[0], "values")[2]
        file_path = os.path.join(received_files_dir, file_name)
        if file_path and os.path.exists(file_path):
            subprocess.Popen(['start', file_path], shell=True)
        else:
            update_status("No file to open or file does not exist.", is_server_status=True)
    else:
        update_status("No file selected.", is_server_status=True)

# Thiết lập giao diện đơn giản với Tkinter
root = tk.Tk()
root.title("Server Controller")

# Sử dụng khung để sắp xếp các thành phần giao diện
frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

# Thêm nhãn tiêu đề
title_label = ttk.Label(frame, text="Server Controller", font=("Helvetica", 16))
title_label.pack(pady=10)

# Thêm nút bắt đầu và dừng server
button_frame = ttk.Frame(frame)
button_frame.pack(pady=20)

start_btn = ttk.Button(button_frame, text="Start Server", command=start_server)
start_btn.pack(side=tk.LEFT, padx=10)

stop_btn = ttk.Button(button_frame, text="Stop Server", command=stop_server, state=tk.DISABLED)
stop_btn.pack(side=tk.LEFT, padx=10)

# Thêm nhãn trạng thái
status_label = ttk.Label(frame, text="Server is stopped", font=("Helvetica", 12))
status_label.pack(pady=10)

# Thêm bảng trạng thái
status_tree = ttk.Treeview(frame, columns=("IP", "Port", "File", "Size"), show="headings")
status_tree.heading("IP", text="IP")
status_tree.heading("Port", text="Port")
status_tree.heading("File", text="File")
status_tree.heading("Size", text="Size")
status_tree.pack(pady=10, fill=tk.BOTH, expand=True)

# Thêm sự kiện nhấp đúp vào bảng trạng thái để mở file
def on_double_click(event):
    open_selected_file()

status_tree.bind("<Double-1>", on_double_click)

# Bắt đầu giao diện Tkinter
root.mainloop()
