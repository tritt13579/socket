# import socket
# import os
# import tkinter as tk
# from tkinter import filedialog, ttk
# import threading

# def send_file(host, port, filename, progress_var):
#     if not os.path.exists(filename):
#         update_status(f"File '{filename}' không tồn tại. Vui lòng kiểm tra đường dẫn.")
#         return
    
#     try:
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect((host, port))
#         update_status(f"Connected to server at {host}:{port}")

#         # Lấy kích thước file
#         file_size = os.path.getsize(filename)
#         sent_size = 0

#         # Đọc và gửi file từng phần
#         with open(filename, 'rb') as f:
#             while chunk := f.read(1024):
#                 client_socket.sendall(chunk)
#                 sent_size += len(chunk)
#                 progress_var.set((sent_size / file_size) * 100)
#                 root.update_idletasks()
#                 update_status(f"Sent {sent_size}/{file_size} bytes")

#         update_status("File sent successfully.")
#     except Exception as e:
#         update_status(f"Error: {e}")
#         progress_var.set(0)  # Reset progress bar only on error
#     finally:
#         client_socket.close()

# def update_status(message):
#     """Hàm cập nhật thông báo lên nhãn trạng thái."""
#     if 'root' in globals():
#         current_text = status_label.cget("text")
#         new_text = f"{current_text}\n{message}" if current_text else message
#         status_label.config(text=new_text)
#         root.update_idletasks()

# # Cấu hình IP, Port của server và file cần gửi
# HOST = 'localhost'
# PORT = 5000
# selected_file = None

# # Hàm để chọn file
# def select_file():
#     global selected_file
#     # Mở cửa sổ chọn file
#     file_path = filedialog.askopenfilename()
#     if not file_path:
#         update_status("Không có file nào được chọn.")
#         return
    
#     selected_file = file_path
#     file_label.config(text=f"File đã chọn: {os.path.basename(file_path)}")

# # Hàm để gửi file đã chọn
# def send_selected_file():
#     if not selected_file:
#         update_status("Chưa có file nào được chọn.")
#         return
    
#     # Gọi hàm send_file với file đã chọn trong một luồng riêng
#     threading.Thread(target=send_file, args=(HOST, PORT, selected_file, progress_var)).start()

# # Thiết lập giao diện đơn giản với Tkinter
# root = tk.Tk()
# root.title("Client File Sender")

# # Thêm nhãn tiêu đề
# title_label = ttk.Label(root, text="Client File Sender", font=("Helvetica", 16))
# title_label.pack(pady=10)

# # Thêm nút chọn file
# select_file_btn = ttk.Button(root, text="Chọn file", command=select_file)
# select_file_btn.pack(pady=10)

# # Thêm nhãn hiển thị tên file đã chọn
# file_label = ttk.Label(root, text="Chưa có file nào được chọn", font=("Helvetica", 12))
# file_label.pack(pady=10)

# # Thêm nút gửi file
# send_file_btn = ttk.Button(root, text="Gửi file", command=send_selected_file)
# send_file_btn.pack(pady=20)

# # Thêm thanh tiến trình
# progress_var = tk.DoubleVar()
# progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
# progress_bar.pack(pady=10, fill=tk.X, padx=20)

# # Thêm nhãn trạng thái
# status_label = ttk.Label(root, text="", font=("Helvetica", 12))
# status_label.pack(pady=10)

# # Bắt đầu giao diện Tkinter
# root.mainloop()
import socket
import os
import tkinter as tk
from tkinter import filedialog, ttk
import threading

def send_file(host, port, filename, progress_var):
    if not os.path.exists(filename):
        update_status(f"File '{filename}' không tồn tại. Vui lòng kiểm tra đường dẫn.")
        return
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        update_status(f"Connected to server at {host}:{port}")

        # Gửi tên file trước
        file_name = os.path.basename(filename)
        client_socket.sendall(file_name.encode() + b'\n')

        # Lấy kích thước file
        file_size = os.path.getsize(filename)
        sent_size = 0

        # Đọc và gửi file từng phần
        with open(filename, 'rb') as f:
            while chunk := f.read(1024):
                client_socket.sendall(chunk)
                sent_size += len(chunk)
                progress_var.set((sent_size / file_size) * 100)
                root.update_idletasks()
                update_status(f"Sent {sent_size}/{file_size} bytes")

        update_status("File sent successfully.")
    except Exception as e:
        update_status(f"Error: {e}")
        progress_var.set(0)  # Reset progress bar only on error
    finally:
        client_socket.close()

def update_status(message):
    """Hàm cập nhật thông báo lên nhãn trạng thái."""
    if 'root' in globals():
        current_text = status_label.cget("text")
        new_text = f"{current_text}\n{message}" if current_text else message
        status_label.config(text=new_text)
        root.update_idletasks()

# Cấu hình IP, Port của server và file cần gửi
HOST = 'localhost'
PORT = 5000
selected_file = None

# Hàm để chọn file
def select_file():
    global selected_file
    # Mở cửa sổ chọn file
    file_path = filedialog.askopenfilename()
    if not file_path:
        update_status("Không có file nào được chọn.")
        return
    
    selected_file = file_path
    file_label.config(text=f"File đã chọn: {os.path.basename(file_path)}")

# Hàm để gửi file đã chọn
def send_selected_file():
    if not selected_file:
        update_status("Chưa có file nào được chọn.")
        return
    
    # Gọi hàm send_file với file đã chọn trong một luồng riêng
    threading.Thread(target=send_file, args=(HOST, PORT, selected_file, progress_var)).start()

# Thiết lập giao diện đơn giản với Tkinter
root = tk.Tk()
root.title("Client File Sender")

# Thêm nhãn tiêu đề
title_label = ttk.Label(root, text="Client File Sender", font=("Helvetica", 16))
title_label.pack(pady=10)

# Thêm nút chọn file
select_file_btn = ttk.Button(root, text="Chọn file", command=select_file)
select_file_btn.pack(pady=10)

# Thêm nhãn hiển thị tên file đã chọn
file_label = ttk.Label(root, text="Chưa có file nào được chọn", font=("Helvetica", 12))
file_label.pack(pady=10)

# Thêm nút gửi file
send_file_btn = ttk.Button(root, text="Gửi file", command=send_selected_file)
send_file_btn.pack(pady=20)

# Thêm thanh tiến trình
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, fill=tk.X, padx=20)

# Thêm nhãn trạng thái
status_label = ttk.Label(root, text="", font=("Helvetica", 12))
status_label.pack(pady=10)

# Bắt đầu giao diện Tkinter
root.mainloop()