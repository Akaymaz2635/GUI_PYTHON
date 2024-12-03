import os
import tkinter as tk
import customtkinter as ctk
import tkinter.messagebox as messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
from utils import camera
from utils.camera import launch_camera_app
from utils.combo_box_lists import projects
from utils.combo_box_lists import defect_types

# CustomTkinter settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
base_path = os.path.dirname(__file__)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 'data' folder and last_created_folder.txt path
data_folder = os.path.join(current_dir, 'data')
last_created_folder_path = os.path.join(data_folder, 'last_created_folder.txt')

class App(ctk.CTk):

    def center_window(self):
        width = 1440
        height = 960
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2) - 50
        self.geometry(f"{width}x{height}+{x}+{y}")

    def delete_last_created_folder_file(self):
        # Clear the content of 'last_created_folder.txt'
        if os.path.exists(last_created_folder_path):
            with open(last_created_folder_path, 'w') as file:
                file.write('')
            print("last_created_folder.txt file has been cleared.")
        else:
            print("last_created_folder.txt file not found.")

    def on_closing(self):
        self.delete_last_created_folder_file()
        self.destroy()  # Close the window

    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Modern Arayüz")
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Icon paths
        icons_path = os.path.join(base_path, "icons")
        self.project_images_path = os.path.join(base_path, "Project_Images")

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=150, corner_radius=0, fg_color="#1E275C")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # Button icons
        self.information_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "information.png")).resize((128, 128)))
        self.inspection_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "inspection.png")).resize((128, 128)))
        self.update_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "update.png")).resize((128, 128)))
        self.report_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "report.png")).resize((128, 128)))
        self.settings_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "settings.png")).resize((128, 128)))
        self.submit_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "submit.png")).resize((128, 128)))
        self.camera_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "camera.png")).resize((128, 128)))
        self.save_icon = ctk.CTkImage(Image.open(os.path.join(icons_path, "save.png")).resize((128, 128)))

        # Sidebar buttons
        self.create_button("Information", self.information_icon, self.show_information)
        self.create_button("Inspection", self.inspection_icon, self.show_inspection)
        self.create_button("Update", self.update_icon, self.show_update)
        self.create_button("Report", self.report_icon, self.show_report)
        self.create_button("Settings", self.settings_icon, self.show_settings)

        # Frame area for main content
        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=1, sticky="nsew")

        # Window grid configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Start by showing the "Information" section
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

        self.part_entry = ttk.Entry(self.frame, width=20, font=("Arial", 20))
        self.part_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Serial Number label and text box
        serial_label = ctk.CTkLabel(self.frame, text="Serial Number", font=("Arial", 20))
        serial_label.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="w")

        self.serial_entry = ttk.Entry(self.frame, width=20, font=("Arial", 20))
        self.serial_entry.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="ew")

        # Operation Number label and text box
        operation_label = ctk.CTkLabel(self.frame, text="Operation Number", font=("Arial", 20))
        operation_label.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="w")

        self.operation_entry = ttk.Entry(self.frame, width=20, font=("Arial", 20))
        self.operation_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

        # Inspector label and text box
        inspector_label = ctk.CTkLabel(self.frame, text="Inspector", font=("Arial", 20))
        inspector_label.grid(row=3, column=1, padx=10, pady=(10, 0), sticky="w")

        self.inspector_entry = ttk.Entry(self.frame, width=20, font=("Arial", 20))
        self.inspector_entry.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Date label and DateEntry with today's date pre-filled
        date_label = ctk.CTkLabel(self.frame, text="Date", font=("Arial", 20))
        date_label.grid(row=3, column=2, padx=10, pady=(10, 0), sticky="w")

        today = datetime.now()
        self.date_entry = DateEntry(self.frame, font=("Arial", 20), width=20,
                                    background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='mm/dd/yyyy')
        self.date_entry.set_date(today)  # Set today's date
        self.date_entry.grid(row=4, column=2, padx=10, pady=(0, 10), sticky="ew")

        # Submit button
        self.submit_button = ctk.CTkButton(self.frame, text="Submit", image=self.submit_icon,
                                            compound="left", command=self.submit_button_command,
                                            fg_color="#1E275C", text_color="white", hover_color="gray", width=150, height=40, font=("Poppins SemiBold", 20))
        self.submit_button.grid(row=5, column=2, padx=10, pady=(10, 20), sticky="se")

        def load_image(path):
            try:
                img = Image.open(path)
                img_resized = img.resize((700, 500))  # Resize to fit the canvas
                return ImageTk.PhotoImage(img_resized)
            except Exception as e:
                print(f"Error loading image: {e}")
                return None

        # Combobox for selecting project
        project_label = ctk.CTkLabel(self.frame, text="Engine Project", font=("Arial", 20))
        project_label.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="w")

        self.project_combobox = ttk.Combobox(self.frame, values=projects, font=("Arial", 20), state="readonly")
        self.project_combobox.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.project_combobox.set(projects[0])  # Set the default value

        # Combobox for defect types
        defect_type_label = ctk.CTkLabel(self.frame, text="Defect Type", font=("Arial", 20))
        defect_type_label.grid(row=5, column=1, padx=10, pady=(10, 0), sticky="w")

        self.defect_type_combobox = ttk.Combobox(self.frame, values=defect_types, font=("Arial", 20), state="readonly")
        self.defect_type_combobox.grid(row=6, column=1, padx=10, pady=(0, 10), sticky="ew")
        self.defect_type_combobox.set(defect_types[0])  # Set the default value

        # Camera section
        camera_frame = ctk.CTkFrame(self.frame)
        camera_frame.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.start_camera_button = ctk.CTkButton(camera_frame, text="Start Camera", image=self.camera_icon,
                                                  compound="left", command=self.start_camera,
                                                  fg_color="#1E275C", text_color="white", hover_color="gray", width=150, height=40, font=("Poppins SemiBold", 20))
        self.start_camera_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    def start_camera(self):
        launch_camera_app()

    def submit_button_command(self):
        # Example of file operations
        part_number = self.part_entry.get()
        operation_number = self.operation_entry.get()
        serial_number = self.serial_entry.get()
        inspector_name = self.inspector_entry.get()
        inspection_date = self.date_entry.get_date()

        # Creating folders on the desktop
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        report_folder = os.path.join(desktop_path, "Report")

        # Check if the report folder exists, if not create it
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)

        # Save last created folder
        last_created_folder = os.path.join(report_folder, part_number, operation_number, serial_number)
        os.makedirs(last_created_folder, exist_ok=True)

        with open(last_created_folder_path, 'w') as file:
            file.write(last_created_folder)

        print(f"Folder created: {last_created_folder}")
        messagebox.showinfo("Success", "Inspection report submitted successfully.")

app = App()
app.mainloop()
