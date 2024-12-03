import os
from PIL import Image, ImageTk
import customtkinter as ctk
# Function to load and display the latest image from the path in last_created_folder.txt
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

