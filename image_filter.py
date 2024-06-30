import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk

def read_image(image_path):
    """
    讀取圖像
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("無法讀取圖像，請檢查路徑是否正確。")
    return image

def apply_blur(image, ksize=(15, 15)):
    """
    應用模糊濾鏡
    """
    return cv2.GaussianBlur(image, ksize, 0)

def apply_sharpen(image):
    """
    應用銳化濾鏡
    """
    kernel = np.array([[0, -1, 0], 
                       [-1, 5, -1], 
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def apply_edge_detection(image):
    """
    應用邊緣檢測濾鏡
    """
    return cv2.Canny(image, 100, 200)

def apply_grayscale(image):
    """
    應用灰度濾鏡
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_sepia(image):
    """
    應用棕褐色濾鏡
    """
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    return cv2.transform(image, sepia_filter)

def apply_brightness(image, value=30):
    """
    增加亮度
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v = np.clip(v, 0, 255)
    final_hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

def apply_contrast(image, alpha=1.5):
    """
    增加對比度
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=0)

def resize_image(image, max_size=(400, 400)):
    """
    調整圖像大小以適應窗口
    """
    h, w = image.shape[:2]
    scaling_factor = min(max_size[0] / w, max_size[1] / h)
    new_size = (int(w * scaling_factor), int(h * scaling_factor))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

def display_image(image, panel):
    """
    顯示圖像在窗口中
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    imgtk = ImageTk.PhotoImage(image=img)
    panel.config(image=imgtk)
    panel.image = imgtk

def save_image(image_path, image):
    """
    保存圖像
    """
    cv2.imwrite(image_path, image)

def open_file():
    """
    打開文件選擇對話框
    """
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            global image, processed_image
            image = read_image(file_path)
            processed_image = None
            display_image(image, original_panel)
        except Exception as e:
            messagebox.showerror("錯誤", str(e))

def apply_filter():
    """
    根據選擇的濾鏡應用處理
    """
    global image, processed_image
    if image is None:
        messagebox.showerror("錯誤", "請先打開圖像文件。")
        return

    filter_type = filter_var.get()
    if filter_type == '模糊':
        processed_image = apply_blur(image)
    elif filter_type == '銳化':
        processed_image = apply_sharpen(image)
    elif filter_type == '邊緣檢測':
        processed_image = apply_edge_detection(image)
    elif filter_type == '灰度':
        processed_image = apply_grayscale(image)
    elif filter_type == '棕褐色':
        processed_image = apply_sepia(image)
    elif filter_type == '增加亮度':
        processed_image = apply_brightness(image)
    elif filter_type == '增加對比度':
        processed_image = apply_contrast(image)
    else:
        messagebox.showerror("錯誤", "請選擇一個有效的濾鏡。")
        return

    display_image(processed_image, processed_panel)

def download_image():
    """
    保存處理後的圖像文件
    """
    global processed_image
    if processed_image is None:
        messagebox.showerror("錯誤", "沒有處理過的圖像可供保存。")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        save_image(file_path, processed_image)
        messagebox.showinfo("保存成功", f"圖像已保存至: {file_path}")

# 創建主窗口
root = tk.Tk()
root.title("圖像濾鏡應用")
root.geometry("1000x700")

# 初始化圖像變量
image = None
processed_image = None

# 創建兩個圖像顯示區域
original_panel = tk.Label(root)
original_panel.pack(side="left", padx=10, pady=10, expand=True, fill="both")

processed_panel = tk.Label(root)
processed_panel.pack(side="right", padx=10, pady=10, expand=True, fill="both")

# 添加選擇照片按鈕
btn_open = ttk.Button(root, text="選擇照片", command=open_file)
btn_open.pack(pady=20, ipadx=10, ipady=10)  # 增加按鈕大小

# 添加濾鏡選項
filter_var = tk.StringVar(value='選擇濾鏡')
filters = ['模糊', '銳化', '邊緣檢測', '灰度', '棕褐色', '增加亮度', '增加對比度']
filter_menu = ttk.OptionMenu(root, filter_var, '選擇濾鏡', *filters)
filter_menu.pack(pady=20)

# 添加套用濾鏡按鈕
btn_apply = ttk.Button(root, text="套用濾鏡", command=apply_filter)
btn_apply.pack(pady=20, ipadx=10, ipady=10)  # 增加按鈕大小

# 添加下載照片按鈕
btn_download = ttk.Button(root, text="下載圖像", command=download_image)
btn_download.pack(pady=20, ipadx=10, ipady=10)  # 增加按鈕大小

# 運行主循環
root.mainloop()
