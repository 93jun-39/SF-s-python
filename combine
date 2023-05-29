import tkinter as tk
import numpy as np
import math
from tkinter import filedialog
import glob, os
import pandas as pd
import pyperclip


# picp4_calculate function (calculate_distance)
def calculate_distance(p1x, p1y, p2x, p2y):
    picp1 = np.array([p1x, p1y])
    picp2 = np.array([p2x, p2y])
    picp3 = picp1 - picp2
    pixel_distance = math.hypot(picp3[0], picp3[1])
    return pixel_distance

# multidata function
def muti_data(filepath, picp4, actual_distance, x1, x2, y1, y2):
    i = 0
    p4 = 0
    p5 = 0

    path = filepath
    file = glob.glob(os.path.join(path, "*.csv"))
    print(file)
    dl = []
    for f in file:
        dl.append(pd.read_csv(f, header=2, usecols=["coords", "x", "y"]))

    for i in range(len(dl)):
        data1 = dl[i]
        id = data1['coords']
        x = data1['x']
        y = data1['y']

        # Calculate distance
        for d1 in range(len(id) - 1):
            p1 = np.array([x[d1], y[d1]])
            p2 = np.array([x[d1 + 1], y[d1 + 1]])
            p3 = p2 - p1
            p4 = math.hypot(p3[0], p3[1])
            p5 = p4 + p5
        data_distance = (p5 / picp4) * actual_distance
        datadistance = str(data_distance)
        p5 = 0
        result_text.insert(tk.END, file[i] + "的總移動距離為*" + datadistance + "mm\n")

        data2 = data1[data1['x'].between(x1, x2) & data1['y'].between(y1, y2)]
        id2 = data2['coords']
        id2l = len(id2)
        i2 = 0
        id2count = 0
        # Calculate enter and exit count
        for i2 in range(id2l - 1):
            idx1 = (id2.iloc[i2])
            idx2 = (id2.iloc[i2 + 1])
            if idx1 + 1 != idx2:
                id2count += 1
        result_text.insert(tk.END, file[i] + "進出中心*" + str(id2count) + "次\n")
        midtime = id2l / 14.57
        result_text.insert(tk.END, file[i] + "中心停留時間為*" + str(midtime) + "秒\n\n")

def select_folder():
    folder = filedialog.askdirectory()
    folder_var.set(folder)

# Run function
def run():
    p1x = int(x1_entry.get())
    p1y = int(y1_entry.get())
    p2x = int(x2_entry.get())
    p2y = int(y2_entry.get())
    actual_distance = float(actual_distance_entry.get())
    distance = calculate_distance(p1x, p1y, p2x, p2y)

    file_path = folder_var.get()
    muti_data(file_path, distance, actual_distance, int(x1_entry.get()), int(x2_entry.get()), int(y1_entry.get()), int(y2_entry.get()))

def copy_result():
    pyperclip.copy(result_text.get("1.0", tk.END))

# Main app window
app = tk.Tk()
app.title("Multidata App")

x1_label = tk.Label(app, text="X1:")
x1_label.grid(row=0, column=0)
x1_entry = tk.Entry(app)
x1_entry.grid(row=0, column=1)

y1_label = tk.Label(app, text="Y1:")
y1_label.grid(row=1, column=0)
y1_entry = tk.Entry(app)
y1_entry.grid(row=1, column=1)

x2_label = tk.Label(app, text="X2:")
x2_label.grid(row=2, column=0)
x2_entry = tk.Entry(app)
x2_entry.grid(row=2, column=1)

y2_label = tk.Label(app, text="Y2:")
y2_label.grid(row=3, column=0)
y2_entry = tk.Entry(app)
y2_entry.grid(row=3, column=1)

actual_distance_label = tk.Label(app, text="Actual Distance (mm):")
actual_distance_label.grid(row=4, column=0)
actual_distance_entry = tk.Entry(app)
actual_distance_entry.grid(row=4, column=1)

folder_label = tk.Label(app, text="Folder:")
folder_label.grid(row=5, column=0)
folder_var = tk.StringVar()
folder_entry = tk.Entry(app, textvariable=folder_var)
folder_entry.grid(row=5, column=1)
select_folder_button = tk.Button(app, text="Select Folder", command=select_folder)
select_folder_button.grid(row=5, column=2)

run_button = tk.Button(app, text="Run", command=run)
run_button.grid(row=6, column=0, columnspan=3)

result_label = tk.Label(app, text="Result:")
result_label.grid(row=7, column=0)
result_text = tk.Text(app, wrap=tk.WORD, height=10, width=40)
result_text.grid(row=7, column=1, columnspan=2)

copy_button = tk.Button(app, text="Copy Result", command=copy_result)
copy_button.grid(row=8, column=0, columnspan=3)

app.mainloop()
