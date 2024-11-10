# import socket
# import os
# import tkinter as tk
# from tkinter import filedialog, ttk
# import threading

# # Cấu hình IP, Port của server và file cần gửi
# HOST = 'localhost'
# PORT = 5000
# selected_file = None

# def send_file(host, port, filename, progress_var):
#     if not os.path.exists(filename):
#         update_status(f"File '{filename}' không tồn tại. Vui lòng kiểm tra đường dẫn.")
#         return
    
#     try:
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect((host, port))
#         update_connection_status(f"Connected to server at {host}:{port}")

#         # Gửi tên file trước
#         file_name = os.path.basename(filename)
#         client_socket.sendall(file_name.encode() + b'\n')

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

#         update_status("File sent successfully.", highlight=True)
#     except ConnectionRefusedError:
#         update_connection_status("Không thể kết nối tới server. Vui lòng kiểm tra server và thử lại.")
#         progress_var.set(0)  # Reset progress bar on connection error
#     except Exception as e:
#         update_status(f"Error: {e}")
#         progress_var.set(0)  # Reset progress bar only on error
#     finally:
#         client_socket.close()

# def update_status(message, highlight=False):
#     """Hàm cập nhật thông báo lên nhãn trạng thái."""
#     if 'root' in globals():
#         status_text.config(state=tk.NORMAL)
#         if highlight:
#             status_text.insert(tk.END, message + "\n", "highlight")
#         else:
#             status_text.insert(tk.END, message + "\n")
#         status_text.config(state=tk.DISABLED)
#         status_text.see(tk.END)
#         root.update_idletasks()

# def update_connection_status(message):
#     """Hàm cập nhật thông báo kết nối lên nhãn trạng thái kết nối."""
#     if 'root' in globals():
#         connection_status_label.config(text=message)
#         root.update_idletasks()

# def reset_status():
#     """Hàm xóa nội dung của Text widget."""
#     if 'root' in globals():
#         status_text.config(state=tk.NORMAL)
#         status_text.delete(1.0, tk.END)
#         status_text.config(state=tk.DISABLED)
#         root.update_idletasks()

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
    
#     reset_status()  # Reset trạng thái trước khi gửi file mới
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

# # Thêm nhãn trạng thái kết nối
# connection_status_label = ttk.Label(root, text="", font=("Helvetica", 12))
# connection_status_label.pack(pady=10)

# # Thêm Text widget để hiển thị trạng thái với thanh cuộn
# status_frame = ttk.Frame(root)
# status_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# status_text = tk.Text(status_frame, wrap=tk.WORD, state=tk.DISABLED, height=10)
# status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=status_text.yview)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# status_text.config(yscrollcommand=scrollbar.set)

# # Thêm tag để làm nổi bật dòng chữ "File sent successfully."
# status_text.tag_configure("highlight", foreground="green", font=("Helvetica", 12, "bold"))

# # Bắt đầu giao diện Tkinter
# root.mainloop()
import socket
import os
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import hashlib

# Cấu hình IP, Port của server và file cần gửi
HOST = 'localhost'
PORT = 5000
selected_file = None

def calculate_checksum(data):
    """Tính toán checksum của một gói dữ liệu."""
    return hashlib.md5(data).hexdigest()

def send_file(host, port, filename, progress_var):
    if not os.path.exists(filename):
        update_status(f"File '{filename}' không tồn tại. Vui lòng kiểm tra đường dẫn.")
        return
    
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        update_connection_status(f"Connected to server at {host}:{port}")

        # Gửi tên file trước
        file_name = os.path.basename(filename)
        client_socket.sendall(file_name.encode() + b'\n')

        # Lấy kích thước file
        file_size = os.path.getsize(filename)
        sent_size = 0

        # Đọc và gửi file từng phần
        with open(filename, 'rb') as f:
            while chunk := f.read(1024):
                # Tính toán và gửi checksum
                checksum = calculate_checksum(chunk).encode()
                client_socket.sendall(checksum)  # Gửi checksum trước
                client_socket.sendall(chunk)  # Gửi dữ liệu sau

                # Nhận phản hồi từ server để xác nhận
                ack = client_socket.recv(3).decode()
                if ack == "ACK":
                    sent_size += len(chunk)
                    progress_var.set((sent_size / file_size) * 100)
                    root.update_idletasks()
                    update_status(f"Sent {sent_size}/{file_size} bytes")
                else:
                    # Nếu nhận được NACK, gửi lại gói dữ liệu hiện tại
                    update_status(f"Resending chunk due to integrity check failure.")
                    f.seek(sent_size)  # Quay lại vị trí gói bị lỗi để gửi lại

        update_status("File sent successfully.", highlight=True)
    except ConnectionRefusedError:
        update_connection_status("Không thể kết nối tới server. Vui lòng kiểm tra server và thử lại.")
        progress_var.set(0)  # Reset progress bar on connection error
    except Exception as e:
        update_status(f"Error: {e}")
        progress_var.set(0)  # Reset progress bar only on error
    finally:
        client_socket.close()

def update_status(message, highlight=False):
    """Hàm cập nhật thông báo lên nhãn trạng thái."""
    if 'root' in globals():
        status_text.config(state=tk.NORMAL)
        if highlight:
            status_text.insert(tk.END, message + "\n", "highlight")
        else:
            status_text.insert(tk.END, message + "\n")
        status_text.config(state=tk.DISABLED)
        status_text.see(tk.END)
        root.update_idletasks()

def update_connection_status(message):
    """Hàm cập nhật thông báo kết nối lên nhãn trạng thái kết nối."""
    if 'root' in globals():
        connection_status_label.config(text=message)
        root.update_idletasks()

def reset_status():
    """Hàm xóa nội dung của Text widget."""
    if 'root' in globals():
        status_text.config(state=tk.NORMAL)
        status_text.delete(1.0, tk.END)
        status_text.config(state=tk.DISABLED)
        root.update_idletasks()

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
    
    reset_status()  # Reset trạng thái trước khi gửi file mới
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

# Thêm nhãn trạng thái kết nối
connection_status_label = ttk.Label(root, text="", font=("Helvetica", 12))
connection_status_label.pack(pady=10)

# Thêm Text widget để hiển thị trạng thái với thanh cuộn
status_frame = ttk.Frame(root)
status_frame.pack(pady=10, fill=tk.BOTH, expand=True)

status_text = tk.Text(status_frame, wrap=tk.WORD, state=tk.DISABLED, height=10)
status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=status_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

status_text.config(yscrollcommand=scrollbar.set)

# Thêm tag để làm nổi bật dòng chữ "File sent successfully."
status_text.tag_configure("highlight", foreground="green", font=("Helvetica", 12, "bold"))

# Bắt đầu giao diện Tkinter
root.mainloop()
