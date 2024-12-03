import os
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as messagebox
import time
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
from utils import camera
from utils.camera import launch_camera_app
from utils.combo_box_lists import projects
from utils.combo_box_lists import defect_types

# CustomTkinter başlatma
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
base_path = os.path.dirname(__file__)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 'data' klasörünün içinde 'last_created_folder.txt' dosyasının yolunu oluştur
data_folder = os.path.join(current_dir, 'data')
last_created_folder_path = os.path.join(data_folder, 'last_created_folder.txt')

class App(ctk.CTk):


    def center_window(self):
        width = 1440
        height = 960

        # Ekranın genişliğini ve yüksekliğini al
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Ekranın ortasına yerleştirmek için x, y koordinatlarını hesapla
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) - 50

        # Pencereyi yerleştir
        self.geometry(f"{width}x{height}+{x}+{y}")

    def delete_last_created_folder_file(self):
        # last_created_folder.txt dosyasının yolunu belirle
        last_created_folder_path = os.path.join(os.path.dirname(__file__), 'data\\last_created_folder.txt')

        # Dosyanın var olup olmadığını kontrol et ve içeriğini temizle
        if os.path.exists(last_created_folder_path):
            with open(last_created_folder_path, 'w') as file:
                file.write('')  # Dosya içeriğini temizle
            print("last_created_folder.txt dosyasının içeriği silindi.")
        else:
            print("last_created_folder.txt dosyası bulunamadı.")

    def on_closing(self):
        # Pencereyi kapatmadan önce dosyayı temizle
        self.delete_last_created_folder_file()
        self.destroy()  # Pencereyi kapat

    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("Modern Arayüz")
        self.center_window()  # Pencereyi ortalamak için doğrudan çağır
        self.last_checked = time.time()

        # Pencereyi kapatma işlemi sırasında dosyayı temizle
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # İkonlar için dosya yolu
        base_path = os.path.dirname(__file__)
        icons_path = os.path.join(base_path, "icons")
        self.project_images_path = os.path.join(base_path, "Project_Images")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0, fg_color="#1E275C")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Butonlar sözlüğü (takip için)
        self.buttons = {}

        # İkonların yüklenmesi
        self.information_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "information.png")).resize((128, 128)))
        self.inspection_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "inspection.png")).resize((128, 128)))
        self.update_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "update.png")).resize((128, 128)))
        self.report_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "report.png")).resize((128, 128)))
        self.settings_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "settings.png")).resize((128, 128)))
        self.submit_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "submit.png")).resize((128, 128)))
        self.camere_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "camera.png")).resize((128, 128)))
        self.save_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "save.png")).resize((128, 128)))
        
        # Butonlar ve hover efektleri
        self.create_button("Information", self.information_icon, self.show_information)
        self.create_button("Inspection", self.inspection_icon, self.show_inspection)
        self.create_button("Update", self.update_icon, self.show_update)
        self.create_button("Report", self.report_icon, self.show_report)
        self.create_button("Settings", self.settings_icon, self.show_settings)

        # Çerçeve Alanı
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=1, sticky="nsew")

        # Pencere satır/kolon yapılandırması
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Başlangıçta "Information" sekmesini göster
        self.active_button = None
        self.show_information()
        self.select_button("Information", self.show_information)

    def create_button(self, text, icon, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            image=icon,
            compound="top",
            command=lambda b=text: self.select_button(b, command),
            fg_color="transparent",
            text_color="white",
            hover_color="gray",
            font=("Poppins SemiBold", 20)
        )
        button.pack(pady=10, padx=20, fill="both", expand=True)
        self.buttons[text] = button

    def select_button(self, button_name, command):
        for name, btn in self.buttons.items():
            btn.configure(fg_color="transparent", text_color="white")

        self.buttons[button_name].configure(fg_color="#D9D9D9", text_color="black")
        self.active_button = button_name
        command()

    def show_information(self):
        self.display_frame("Information")
        self.create_information_frame()


    def show_inspection(self):
        self.display_frame("Inspection")
        self.create_inspection_frame()

    def show_update(self):
        self.display_frame("Update")

    def show_report(self):
        self.display_frame("Report")

    def show_settings(self):
        self.display_frame("Settings")

    def display_frame(self, text):
        for widget in self.frame.winfo_children():
            widget.destroy()


    def create_information_frame(self):

        # Part Number label and text box
        part_label = ctk.CTkLabel(self.frame, text="Part Number", font=("Arial", 20))
        part_label.grid(row=1, column=1, padx=10, pady=(10, 0), sticky="w")

        self.part_entry = ttk.Entry(self.frame,width=20, font=("Arial", 20))
        self.part_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Serial Number label and text box
        serial_label = ctk.CTkLabel(self.frame, text="Serial Number", font=("Arial", 20))
        serial_label.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="w")

        self.serial_entry = ttk.Entry(self.frame,width=20, font=("Arial", 20))
        self.serial_entry.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="ew")

        # Operation Number label and text box
        operation_label = ctk.CTkLabel(self.frame, text="Operation Number", font=("Arial", 20))
        operation_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        self.operation_entry = ttk.Entry(self.frame,width=20, font=("Arial", 20))
        self.operation_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Inspector label and text box
        inspector_label = ctk.CTkLabel(self.frame, text="Inspector", font=("Arial", 20))
        inspector_label.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")

        self.inspector_entry = ttk.Entry(self.frame,width=20, font=("Arial", 20))
        self.inspector_entry.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Date label and DateEntry with today's date pre-filled
        date_label = ctk.CTkLabel(self.frame, text="Date", font=("Arial", 20))
        date_label.grid(row=3, column=2, padx=10, pady=(10, 0), sticky="w")

        # Get today's date and format it as required
        today = datetime.now()

        self.date_entry = DateEntry(self.frame, font=("Arial", 20), width=20,
                                    background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='mm/dd/yyyy')
        self.date_entry.set_date(today)  # Set today's date
        self.date_entry.grid(row=4, column=2, padx=10, pady=(0, 10), sticky="ew")  # Position for DateEntry

        # Submit button
        self.submit_button = ctk.CTkButton(self.frame, text="Submit", image=self.submit_icon,
                                            compound="left", command=self.submit_button_command,
                                            fg_color="#1E275C", text_color="white", hover_color="gray", width=150, height=40,font=("Poppins SemiBold", 20))
        self.submit_button.grid(row=5, column=2, padx=10, pady=(10, 20), sticky="se")  # Position for Submit button

        def load_image(path):
            try:
                img = Image.open(path)
                img_resized = img.resize((700, 500))  # Resize to fit the canvas
                return ImageTk.PhotoImage(img_resized)
            except Exception as e:
                print(f"Error loading image: {e}")
                return None

        # Function to handle combobox selection change
        def on_combobox_change(event):
            # Debug print to confirm the function is triggered
            print("Combobox selection changed!")

            # Get selected value
            selected_value = self.project_combobox.get()
            print(f"Selected value: {selected_value}")  # Print selected value for debugging

            if selected_value:
                # Update image path based on selection
                image_path = base_path + f"\\Project_Images\\{selected_value}.jpg"
                print(f"Loading image from: {image_path}")  # Print image path for debugging

                # Load and display the new image
                new_image = load_image(image_path)
                if new_image:  # Check if image loading was successful
                    canvas.itemconfig(canvas_image, image=new_image)
                    canvas.image = new_image  # Keep a reference to avoid garbage collection
                else:
                    print("Failed to load new image.")

        # Project label and combo box
        project_label = ctk.CTkLabel(self.frame, text="Engine Project", font=("Arial", 20))
        project_label.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")

        # List for combobox options]
        project_list = sorted(projects)
        self.project_combobox = ttk.Combobox(self.frame, values=project_list,width=20, font=("Arial", 20))

        # Set a default initial value
        self.project_combobox.set(projects[0])  # Set to "a" initially
        self.project_combobox.bind("<<ComboboxSelected>>", on_combobox_change)
        self.project_combobox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Canvas for displaying the image
        canvas = tk.Canvas(self.frame, width=700, height=500)
        canvas.grid(row=6, column=0, columnspan=3, pady=(10, 0))

        # Load and display the initial image
        initial_image_path = base_path + f"\\Project_Images\\{projects[0]}.jpg"
        initial_image = load_image(initial_image_path)
        canvas_image = canvas.create_image(350, 250, image=initial_image)
        canvas.image = initial_image  # Keep a reference to avoid garbage collection


    def save_last_created_folder(self, folder_path):
        # last_created_folder.txt dosyasına yazma
        last_created_folder_path = os.path.join(os.path.dirname(__file__), 'data\\last_created_folder.txt')  # Dosya yolunu belirle
        with open(last_created_folder_path, 'w') as file:
            file.write(folder_path)


    def submit_button_command(self):
        # Desktop dizinini al
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        report_folder = os.path.join(desktop_path, 'Report')

        # Kullanıcı girişlerini al
        part_number = self.part_entry.get().strip()
        operation_number = self.operation_entry.get().strip()
        serial_number = self.serial_entry.get().strip()

        # Klasörlerin isimlerini oluştur
        if not part_number or not operation_number or not serial_number:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        part_folder = os.path.join(report_folder, part_number)
        operation_folder = os.path.join(part_folder, operation_number)
        serial_folder = os.path.join(operation_folder, serial_number)

        # Klasörleri oluştur
        for folder in [report_folder, part_folder, operation_folder, serial_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # En son oluşturulan klasör yolunu kaydet
        self.save_last_created_folder(serial_folder)

        # Kullanıcıya başarılı bir işlem mesajı göster
        messagebox.showinfo("Başarılı", f"Rapor klasörü oluşturuldu:\n{serial_folder}")

    def display_last_photo(self):
        # Read the path from last_created_folder.txt
        with open('data/last_created_folder.txt', 'r') as file:
            folder_path = file.read().strip()

        # Check if the directory exists
        if os.path.exists(folder_path):
            # Get list of image files in the folder, sorted by last modified time (most recent first)
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if image_files:
                # Sort files by modification time
                image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)), reverse=True)
                latest_photo_path = os.path.join(folder_path, image_files[0])

                # Load and resize the image for display on the canvas
                image = Image.open(latest_photo_path)
                image = image.resize((400, 300), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                # Display the image on the canvas
                self.canvas_last_photo.image = photo  # Keep a reference
                self.canvas_last_photo.create_image(0, 0, anchor="nw", image=photo)     
            else:
                print("No image files found in the specified folder.")
        else:
            print("The specified folder path does not exist.")
    
    def display_last_photo_trigger(self):
        # Polling every 500ms to see if there's any change in the folder
        if time.time() - self.last_checked > 0.5:  # Check every 500ms
            self.last_checked = time.time()
            self.display_last_photo()  # Trigger photo display if content changes
        
        # Call itself again after 100ms to keep checking
        self.after(100, self.display_last_photo_trigger)

    def start(self):
        self.display_last_photo_trigger()

    def create_inspection_frame(self):
        # Label ve Combobox
        defect_type_label = ctk.CTkLabel(self.frame, text="Defect Type", font=("Poppins SemiBold", 20))
        defect_type_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        
        # Stil oluşturuyoruz
        style = ttk.Style()
        style.configure("TCombobox", font=("Poppins SemiBold", 20))  # Font ve boyut ayarı
        style.configure("TCombobox", padding=10)  # İç boşluk (yüksekliği artırır)
        
        self.defect_type_combobox = ttk.Combobox(self.frame, width=20, values=defect_types, state="readonly", font=("Poppins SemiBold", 20))
        self.defect_type_combobox.bind("<<ComboboxSelected>>", self.on_defect_type_combobox)  # Bind the combobox change event
        self.defect_type_combobox.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        # Diğer etiketler ve giriş kutuları
        labels = [
            ("Depth", 3, 1),
            ("Width", 5, 1),
            ("Length", 7, 1),
            ("Radius", 9, 1),
            ("Angle", 11, 1),
            ("Color", 13, 1),
            ("Defect Sample Image", 1, 4),
            ("Last Photo Preview", 8, 4)
        ]
        
        for text, row, column in labels:
            label = ctk.CTkLabel(self.frame, text=text, font=("Poppins SemiBold", 20))
            label.grid(row=row, column=column, padx=20, pady=10, sticky="w")

        # Giriş kutuları (Entry)
        self.entry_vars = []
        for i, (row, column) in enumerate([(4, 1), (6, 1), (8, 1), (10, 1), (12, 1), (14, 1)]):
            entry_var = ctk.CTkEntry(self.frame, width=400, height=40, fg_color="#D9D9D9", text_color="#000716", font=("Poppins SemiBold", 20))
            entry_var.grid(row=row, column=column, padx=20, pady=10, sticky="w")
            self.entry_vars.append(entry_var)

        # "Defect Sample" ve "Last Photo Preview" için alanlar
        self.defect_sample_frame = ctk.CTkFrame(self.frame, width=400, height=300, fg_color="#D9D9D9")
        self.defect_sample_frame.grid(row=2, column=4, padx=20, pady=10, rowspan=6)

        self.canvas = ctk.CTkCanvas(self.defect_sample_frame, width=400, height=300, bg="#D9D9D9")
        self.canvas.pack(fill="both", expand=True)

        self.image_id = None  # Resim kimliğini tutmak için

        self.last_photo_frame = ctk.CTkFrame(self.frame, width=400, height=300, fg_color="#D9D9D9")
        self.last_photo_frame.grid(row=9, column=4, padx=20, pady=10, rowspan=6)

        self.canvas_last_photo = ctk.CTkCanvas(self.last_photo_frame, width=400, height=300, bg="#D9D9D9")
        self.canvas_last_photo.pack(fill="both", expand=True)

        def get_entry_inputs():
            # Tüm giriş kutularındaki değerleri alıp bir sözlükte saklayalım
            entry_labels = ["Depth", "Width", "Length", "Radius", "Angle", "Color"]
            inputs = {}

            for label, entry in zip(entry_labels, self.entry_vars):
                inputs[label] = entry.get()  # Giriş kutusundaki metni al

            # Verileri kontrol için yazdırabilir veya başka bir işlemde kullanabilirsiniz
            print("Giriş Değerleri:", inputs)

            return inputs


        # Butonlar
        button_6 = ctk.CTkButton(self.frame, text="Kaydet", image=self.save_icon,
                                compound="left", command=get_entry_inputs,
                                fg_color="#1E275C", text_color="white",
                                hover_color="gray", width=150, height=150, font=("Poppins SemiBold", 18))
        button_6.grid(row=16, column=4, padx=20, pady=10, sticky="nsew")

        button_7 = ctk.CTkButton(self.frame, text="Kamera", image=self.camere_icon,
                                compound="left", command=launch_camera_app, 
                                fg_color="#1E275C", text_color="white", 
                                hover_color="gray", width=150, height=150, font=("Poppins SemiBold", 18))
        button_7.grid(row=16, column=1, padx=20, pady=10, sticky="nsew")


        # Trigger the display_last_photo function after a short delay to ensure the frame is updated
        self.after(100, self.display_last_photo_trigger)  # Call it here directly

    def load_image(self, path):
        """Verilen yoldan resmi yükle ve yeniden boyutlandır."""
        try:
            img = Image.open(path)
            img_resized = img.resize((400, 300))  # Resmi çerçeveye uydur
            return ImageTk.PhotoImage(img_resized)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None


    def on_defect_type_combobox(self, event):
        """Combobox değiştiğinde çalışacak fonksiyon."""
        # Seçilen değeri al
        selected_value = self.defect_type_combobox.get()
        print(f"Selected value: {selected_value}")  # Debug için

        if selected_value:
            # Resim yolunu güncelle
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Defect_Images", f"{selected_value}.jpg")
            print(f"Loading image from: {image_path}")  # Debug için

            # Resmi yükle ve görüntüle
            new_image = self.load_image(image_path)
            if new_image:  # Resim yükleme başarılı olduysa
                if self.image_id:
                    self.canvas.delete(self.image_id)  # Önceki resmi sil
                
                # Canvas boyutlarını al
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()

                # Resmin genişlik ve yüksekliğini al
                image_width = new_image.width()
                image_height = new_image.height()

                # Ortalanmış konumları hesapla
                x = (canvas_width - image_width) // 2
                y = (canvas_height - image_height) // 2

                # Yeni resmi ortalayarak yükle
                self.image_id = self.canvas.create_image(x, y, anchor="nw", image=new_image)
                self.canvas.image = new_image  # Garbage collection'ı önlemek için referansı sakla
            else:
                print("Failed to load new image.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
