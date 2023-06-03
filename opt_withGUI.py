import cv2
import os
import glob
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox

# Global variables
image_path = ''
data_path = ''
clicked_points = []
real_distance = 0.0
result_textboxes = []

# Mouse click event callback function
def on_mouse_click(event, x, y, flags, param):
    global clicked_points
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))

# Calculate distance between two points
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Check if point is inside the rectangle
def is_inside_rect(p, rect_points):
    a, b, c, d = rect_points
    v0 = np.array(c) - np.array(a)
    v1 = np.array(b) - np.array(a)
    v2 = np.array(p) - np.array(a)

    u = np.dot(v2, v0) / np.dot(v0, v0)
    v = np.dot(v2, v1) / np.dot(v1, v1)

    return (0 <= u <= 1) and (0 <= v <= 1)

# Select image file
def select_image_file():
    global image_path, clicked_points
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    clicked_points = []  # Reset clicked points

    if image_path:
        # Load image and set mouse callback
        image = cv2.imread(image_path)
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', on_mouse_click)

        while True:
            cv2.imshow('image', image)
            if len(clicked_points) == 4:  # Exit loop after 4 points are clicked
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit loop
                clicked_points = []  # Reset clicked points
                break

        cv2.destroyAllWindows()

# Apply real distance
def apply_real_distance():
    global real_distance
    real_distance = float(real_distance_entry.get())
    messagebox.showinfo("Success", "Real distance applied.")

# Select data folder
def select_data_folder():
    global data_path
    data_path = filedialog.askdirectory()

# Analyze CSV files
def analyze_csv_files():
    global real_distance, clicked_points, result_textboxes

    if image_path == '':
        messagebox.showinfo("Error", "Please select an image file.")
        return

    if len(clicked_points) < 4:
        messagebox.showinfo("Error", "Please select the four corners of the rectangle.")
        return

    if real_distance == 0.0:
        messagebox.showinfo("Error", "Please enter the real distance of one side of the rectangle.")
        return

    if data_path == '':
        messagebox.showinfo("Error", "Please select a data folder.")
        return

    # Load image
    image = cv2.imread(image_path)

    # Calculate scale
    scale = real_distance / distance(clicked_points[0], clicked_points[1])

    # Load CSV files
    csv_files = glob.glob(os.path.join(data_path, "*.csv"))

    for i, csv_file in enumerate(csv_files):
        # Read CSV file
        data = pd.read_csv(csv_file, header=2, usecols=["coords", "x", "y"])

        # Calculate move distance and enter/exit counts
        move_distance = 0
        enter_count = 0
        exit_count = 0
        prev_inside = is_inside_rect(data.iloc[0][['x', 'y']].to_numpy(), clicked_points)

        for j in range(1, len(data)):
            prev_point = data.iloc[j - 1][['x', 'y']].to_numpy()
            curr_point = data.iloc[j][['x', 'y']].to_numpy()
            move_distance += distance(prev_point, curr_point) * scale

            curr_inside = is_inside_rect(curr_point, clicked_points)
            if not prev_inside and curr_inside:
                enter_count += 1
            elif prev_inside and not curr_inside:
                exit_count += 1

            prev_inside = curr_inside

        # Calculate time inside the rectangle
        time_inside_rect = len(data[data.apply(lambda row: is_inside_rect(row[['x', 'y']].to_numpy(), clicked_points), axis=1)]) / 30

        # Build result string with file name
        result_text = f"File: {os.path.basename(csv_file)}\n"
        result_text += f"Move distance: {move_distance:.2f} meters\n"
        result_text += f"Enter count: {enter_count} times\n"
        result_text += f"Exit count: {exit_count} times\n"
        result_text += f"Time inside the rectangle: {time_inside_rect:.2f} seconds"

        # Create result text box for each file
        result_textbox = tk.Text(root, height=4, width=40)
        result_textbox.insert(tk.END, result_text)
        result_textbox.pack()
        result_textboxes.append(result_textbox)

# Copy results to clipboard
def copy_results():
    global result_textboxes
    result_text = ""
    for result_textbox in result_textboxes:
        result_text += result_textbox.get(1.0, tk.END)

    if result_text:
        root.clipboard_clear()
        root.clipboard_append(result_text)
        messagebox.showinfo("Success", "Results copied to clipboard.")

# Create UI
root = tk.Tk()
root.title("CSV Analysis")
root.geometry("400x400")

# Image file selection button
image_button = tk.Button(root, text="Select Image", command=select_image_file)
image_button.pack()

# Real distance input
real_distance_label = tk.Label(root, text="Real Distance (m):")
real_distance_label.pack()
real_distance_entry = tk.Entry(root)
real_distance_entry.pack()

# Apply real distance button
apply_button = tk.Button(root, text="Apply Real Distance", command=apply_real_distance)
apply_button.pack()

# Data folder selection button
data_folder_button = tk.Button(root, text="Select Data Folder", command=select_data_folder)
data_folder_button.pack()

# CSV analysis button
analyze_button = tk.Button(root, text="Analyze CSV Files", command=analyze_csv_files)
analyze_button.pack()

# Copy results button
copy_button = tk.Button(root, text="Copy Results", command=copy_results)
copy_button.pack()

root.mainloop()
