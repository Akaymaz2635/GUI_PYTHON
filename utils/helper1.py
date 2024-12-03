import os
from PIL import Image, ImageTk
import tkinter as tk

def display_last_photo(photo_path):
    # Fotoğrafın kaydedilip kaydedilmediğini kontrol edin
    if os.path.exists(photo_path):
        image = Image.open(photo_path)
        image = image.resize((400, 300))  # İsteğe bağlı boyutlandırma
        photo_image = ImageTk.PhotoImage(image)
        
        # Fotoğrafı göstermek için bir pencere oluşturun
        photo_window = tk.Toplevel()
        photo_window.title("Son Çekilen Fotoğraf")
        photo_window.geometry("450x350")
        
        # Fotoğrafı bir Label içinde gösterin
        photo_label = tk.Label(photo_window, image=photo_image)
        photo_label.image = photo_image
        photo_label.pack(pady=10)
    else:
        print(f"Fotoğraf bulunamadı: {photo_path}")
