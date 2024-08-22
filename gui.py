import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import os
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import threading
import fsample4 as fs4
from matplotlib.figure import Figure

import matplotlib.patches as patches

# ####################################################################################################
# ####################################################################################################
# GLOBAL VARIABLES:

pil_img = None # pillow Image for original image
image_axes = None
data_norm = None #  numpy array for norm data

df_result = None

tkfig_result = None


colors = {"red":[255, 0, 0, 255], "green":[0, 255, 0, 255], "blue":[0, 0, 255, 255]}


GUI_VERSION = "0.1.1"

# ####################################################################################################
# ####################################################################################################
# TKINTER ROOT:
root = tk.Tk()
root.title("Scientific Image Data Extraction Software")
root.geometry("1200x600")

# ####################################################################################################
# ####################################################################################################
# TK VARIABLES:

value_inside = tk.StringVar(root, "color")

strvar_filepath = tk.StringVar(root, "select a file name ....")

strvar_sframe_x1 = tk.StringVar(root, 0)
strvar_sframe_y1 = tk.StringVar(root, 0)
strvar_sframe_x2 = tk.StringVar(root, 0)
strvar_sframe_y2 = tk.StringVar(root, 0)

strvar_color_red = tk.StringVar(root, 0)
strvar_color_green = tk.StringVar(root, 0)
strvar_color_blue = tk.StringVar(root, 0)
strvar_color_alpha = tk.StringVar(root, 0)

strvar_filter_red_min = tk.StringVar(root, 0)
strvar_filter_red_max = tk.StringVar(root, 0)

strvar_filter_green_min = tk.StringVar(root, 0)
strvar_filter_green_max = tk.StringVar(root, 0)

strvar_weight_red = tk.StringVar(root, 1)
strvar_weight_green = tk.StringVar(root, 1)
strvar_weight_blue = tk.StringVar(root, 1)
strvar_weight_alpha = tk.StringVar(root, 1)

strvar_filter_norm_min = tk.StringVar(root, 0)
strvar_filter_norm_max = tk.StringVar(root, 1)

# ####################################################################################################
# ####################################################################################################
# VAR METHODS:

def get_sframe():
    return (int(strvar_sframe_x1.get()), int(strvar_sframe_y1.get()), int(strvar_sframe_x2.get()), int(strvar_sframe_y2.get()))

def get_rcolor():
    return (int(strvar_color_red.get()), int(strvar_color_green.get()), int(strvar_color_blue.get()), int(strvar_color_alpha.get()))

def get_ncweight():
    return (int(strvar_weight_red.get()), int(strvar_weight_green.get()), int(strvar_weight_blue.get()), int(strvar_weight_alpha.get()))

def get_nfilter():
    return (float(strvar_filter_norm_min.get()), float(strvar_filter_norm_max.get()))

# ####################################################################################################
# ####################################################################################################
# BUTTON METHODS:

def btn_load_image():
    global pil_img, image_axes, tkfig_img, aggcanvas_img
    # select file name:
    path = tk.filedialog.askopenfilename()
    strvar_filepath.set(path)
    print(f'setting filepath to: {path}')

    pil_img = Image.open(path)
    
    image_axes.clear()

    image_axes.imshow(np.asarray(pil_img))

    navtool_img.update()
    aggcanvas_img.draw()


def btn_update_visuals():
    global image_axes, aggcanvas_img
    image_axes.patches.clear() # clear axes

    sframe = get_sframe()
    rect = patches.Rectangle((sframe[0], sframe[1]), sframe[2]-sframe[0], sframe[3]-sframe[1], linewidth=1, edgecolor='r', facecolor='none')
    image_axes.add_patch(rect)

    aggcanvas_img.draw()


def btn_calcnorm():
    print("sampling image ...")

    # sampling frame as tuple: (x1, y1, x2, y2)
    sframe = get_sframe()

    # sampling reference color as tuple: (r, g, b, a)
    rcolor = get_rcolor()
    print(f"rcolor={rcolor}")

    # get norm weight as tuple: (r, g, b, a)
    ncweight = get_ncweight()

    # get image data
    img_data = np.asanyarray(pil_img)


    # calculate norm values
    
    def thread_func():
        global data_norm, norm_axes
        print("calcularting color norm ...")
        data_norm = fs4.calculate_color_norm(img_data, sframe, rcolor, ncweight)# calculate norm matrix
        np.savetxt("norm.csv", data_norm, delimiter=",") # save norm for debug purposes

        print(" ... finished")

        norm_axes.clear()
        norm_axes.imshow(data_norm, cmap="Greys")
        aggcanvas_norm.draw()

    thread1 = threading.Thread(target=thread_func)
    thread1.start()  


def btn_evaluate():
    global df_result
    print("evaluating")

    # get norm filter as tuple: (min, max)
    nfilter = get_nfilter()
    xarr, yarr, val = fs4.evaluate_norm(data_norm, nfilter)

    df_result = pd.DataFrame({"x":xarr, "y":yarr, "val":val})
    df_result.to_csv("found.csv", sep=",", index=None)



    result_axes.clear()
    result_axes.plot(xarr, yarr, ".")
    result_axes.invert_yaxis()
    aggcanvas_result.draw()

    print("...finished")


def btn_savenorm():
    print("saving norm")


    path = tk.filedialog.asksaveasfilename()
    np.savetxt(path, data_norm)

    print("saved")


def btn_saveresult():
    print("saving result")

    path = tk.filedialog.asksaveasfilename()
    df_result.to_csv(path, sep=";", decimal=".")

    print("saved")

def omnu_color_handel(selection):
    print(selection)
    if selection in colors:
        print(f"selecting new reference color: {selection}")
        c = colors[selection]

        strvar_color_red.set(str(c[0]))
        strvar_color_green.set(str(c[1]))
        strvar_color_blue.set(str(c[2]))
        strvar_color_alpha.set(str(c[3]))
    else:
        print("unknown color!!!")

# ####################################################################################################
# ####################################################################################################
# EVENT METHODS:

def event_canvas_clicked(event, img):
    if img != None:
        print(f"clicked: x={event.x}, y={event.y}, C={img.getpixel((event.x, event.y))}")

# ####################################################################################################
# ####################################################################################################
# MENU FRAME:
frame_menu = tk.Frame(root, bg="red")


# menue header:
frame_menu_header = tk.Frame(frame_menu, bg="gray")

# software title:
label_menu_header = tk.Label(frame_menu_header, text="FigureSampleV4", font=("Arial", 25), bg="gray")
label_menu_guiversion = tk.Label(frame_menu_header, text="GUI VERSION: " + GUI_VERSION)
label_menu_libversion = tk.Label(frame_menu_header, text="LIB VERSION: " + fs4.LIB_VERSION)

label_menu_header.pack(expand=1, fill=tk.X)
label_menu_guiversion.pack(expand=1, fill=tk.X, side=tk.LEFT)
label_menu_libversion.pack(expand=1, fill=tk.X, side=tk.LEFT)

frame_menu_header.pack(side=tk.TOP, expand=1, fill=tk.X)



# menu tabs:
tabs_menu = ttk.Notebook(frame_menu)
tab_menu_main = ttk.Frame(tabs_menu)
tab_menu_design = ttk.Frame(tabs_menu)
tabs_menu.add(tab_menu_main, text='General Settings')
tabs_menu.add(tab_menu_design, text='Design & Drawing')


# main file loading:
lframe_file = ttk.LabelFrame(tab_menu_main, text="Load File:")
entry_file = tk.Entry(lframe_file, width=45, textvariable=strvar_filepath)
#button_file_select = tk.Button(lframe_file, text="Select")
button_file_load = tk.Button(lframe_file, text="Load", command=btn_load_image)

entry_file.pack(side=tk.LEFT)
#button_file_select.pack(side=tk.LEFT)
button_file_load.pack(side=tk.LEFT)
lframe_file.pack(side=tk.TOP, anchor=tk.NW, expand=True, fill="x")



# main menu sampling frame
lframe_sframe = ttk.LabelFrame(tab_menu_main, text="Sampling Frame:")
label_sframe_x1 = tk.Label(lframe_sframe, text="x1")
sbox_sframe_x1 = ttk.Spinbox(lframe_sframe, from_=0, to=100, width=5, validate='all', textvariable=strvar_sframe_x1)
label_sframe_y1 = tk.Label(lframe_sframe, text="y1")
sbox_sframe_y1 = ttk.Spinbox(lframe_sframe, from_=0, to=100, width=5, textvariable=strvar_sframe_y1)
label_sframe_x2 = tk.Label(lframe_sframe, text="x2")
sbox_sframe_x2 = ttk.Spinbox(lframe_sframe, from_=0, to=100, width=5, textvariable=strvar_sframe_x2)
label_sframe_y2 = tk.Label(lframe_sframe, text="y2")
sbox_sframe_y2 = ttk.Spinbox(lframe_sframe, from_=0, to=100, width=5, textvariable=strvar_sframe_y2)

label_sframe_x1.pack(side=tk.LEFT, expand=True, fill="x")
sbox_sframe_x1.pack(side=tk.LEFT)
label_sframe_y1.pack(side=tk.LEFT, expand=True, fill="x")
sbox_sframe_y1.pack(side=tk.LEFT)
label_sframe_x2.pack(side=tk.LEFT, expand=True, fill="x")
sbox_sframe_x2.pack(side=tk.LEFT)
label_sframe_y2.pack(side=tk.LEFT, expand=True, fill="x")
sbox_sframe_y2.pack(side=tk.LEFT)
lframe_sframe.pack(side=tk.TOP, anchor=tk.NW, expand=True, fill="x")


# main menu color aquisition
lframe_color = ttk.LabelFrame(tab_menu_main, text="Sampling Color:")
button_color_pxselect = tk.Button(lframe_color, text="Cursor")
omenu_color = tk.OptionMenu(lframe_color, value_inside, *["red", "blue", "green"], command=omnu_color_handel)
label_color_red = tk.Label(lframe_color, text="R")
sbox_color_red = ttk.Spinbox(lframe_color, from_=0, to=255, width=3, validate='all', textvariable=strvar_color_red)
label_color_green = tk.Label(lframe_color, text="G")
sbox_color_green = ttk.Spinbox(lframe_color, from_=0, to=255, width=3, validate='all', textvariable=strvar_color_green)
label_color_blue = tk.Label(lframe_color, text="B")
sbox_color_blue = ttk.Spinbox(lframe_color, from_=0, to=255, width=3, validate='all', textvariable=strvar_color_blue)
label_color_alpha = tk.Label(lframe_color, text="A")
sbox_color_alpha = ttk.Spinbox(lframe_color, from_=0, to=255, width=3, validate='all', textvariable=strvar_color_alpha)

button_color_pxselect.pack(side=tk.LEFT, anchor=tk.N)
omenu_color.pack(side=tk.LEFT, anchor=tk.N)
label_color_red.pack(side=tk.LEFT, expand=True, fill="x")
sbox_color_red.pack(side=tk.LEFT)
label_color_green.pack(side=tk.LEFT, expand=True, fill="x")
sbox_color_green.pack(side=tk.LEFT)
label_color_blue.pack(side=tk.LEFT, expand=True, fill="x")
sbox_color_blue.pack(side=tk.LEFT)
label_color_alpha.pack(side=tk.LEFT, expand=True, fill="x")
sbox_color_alpha.pack(side=tk.LEFT)
lframe_color.pack(side=tk.TOP, anchor=tk.NW, expand=True, fill="x")


# main menu norm color weight
lframe_weight = ttk.LabelFrame(tab_menu_main, text="Norm color weight:")
label_weight_red = tk.Label(lframe_weight, text="R")
sbox_weight_red = ttk.Spinbox(lframe_weight, from_=0, to=10, width=3, textvariable=strvar_weight_red)
label_weight_green = tk.Label(lframe_weight, text="G")
sbox_weight_green = ttk.Spinbox(lframe_weight, from_=0, to=10, width=3, textvariable=strvar_weight_green)
label_weight_blue = tk.Label(lframe_weight, text="B")
sbox_weight_blue = ttk.Spinbox(lframe_weight, from_=0, to=10, width=3, textvariable=strvar_weight_blue)
label_weight_alpha = tk.Label(lframe_weight, text="A")
sbox_weight_alpha = ttk.Spinbox(lframe_weight, from_=0, to=10, width=3, textvariable=strvar_weight_alpha)

label_weight_red.pack(side=tk.LEFT)
sbox_weight_red.pack(side=tk.LEFT)
label_weight_green.pack(side=tk.LEFT)
sbox_weight_green.pack(side=tk.LEFT)
label_weight_blue.pack(side=tk.LEFT)
sbox_weight_blue.pack(side=tk.LEFT)
label_weight_alpha.pack(side=tk.LEFT)
sbox_weight_alpha.pack(side=tk.LEFT)
lframe_weight.pack(side=tk.TOP, anchor=tk.NW, expand=True, fill="x")


# main menu filter & boundary settings 
lframe_filter = ttk.LabelFrame(tab_menu_main, text="Norm filter:")
label_filter_norm_min = tk.Label(lframe_filter, text="min")
sbox_filter_norm_min = ttk.Spinbox(lframe_filter, from_=0, to=255, width=3, validate='all', textvariable=strvar_filter_norm_min)
label_filter_norm_max = tk.Label(lframe_filter, text="max")
sbox_filter_norm_max = ttk.Spinbox(lframe_filter, from_=0, to=255, width=3, validate='all', textvariable=strvar_filter_norm_max)

label_filter_norm_min.pack(side=tk.LEFT)
sbox_filter_norm_min.pack(side=tk.LEFT)
label_filter_norm_max.pack(side=tk.LEFT)
sbox_filter_norm_max.pack(side=tk.LEFT)
lframe_filter.pack(side=tk.TOP, anchor=tk.NW, expand=True, fill="x")


# main menu sampling
lframe_sampling = ttk.LabelFrame(tab_menu_main, text="Sampling:")
button_sampeling_loadconfig = tk.Button(lframe_sampling, text="Load config")
button_sampeling_update = tk.Button(lframe_sampling, text="Update visuals", command=btn_update_visuals)
button_sampeling_calcnorm = tk.Button(lframe_sampling, text="Calculate Norm", command=btn_calcnorm)
button_sampeling_evaluate = tk.Button(lframe_sampling, text="Evaluate", command=btn_evaluate)

button_sampeling_loadconfig.pack(side=tk.LEFT, anchor=tk.N)
button_sampeling_update.pack(side=tk.LEFT, anchor=tk.N)
button_sampeling_calcnorm.pack(side=tk.LEFT, anchor=tk.N)
lframe_sampling.pack(side=tk.TOP, anchor=tk.NW, expand=True, fill="x")
button_sampeling_evaluate.pack(side=tk.TOP, anchor=tk.NW, expand=True, fill="x")
lframe_sampling.pack()

# main menu save data:
lframe_save = ttk.LabelFrame(tab_menu_main, text="Save:")
button_save_norm = tk.Button(lframe_save, text="Save norm data", command=btn_savenorm)
button_save_result = tk.Button(lframe_save, text="Save result", command=btn_saveresult)

button_save_norm.pack(side=tk.LEFT, expand=True, fill="x")
button_save_result.pack(side=tk.LEFT, expand=True, fill="x")
lframe_save.pack(side=tk.LEFT, expand=True, fill="x")


tabs_menu.pack(expand=1, fill="both")
frame_menu.pack(side=tk.LEFT, anchor=tk.NW)




# ####################################################################################################
# ####################################################################################################
# MAIN FRAME:
frame_main = tk.Frame(root, bg="blue")

tabs_main = ttk.Notebook(frame_main)
tab_main_image = ttk.Frame(tabs_main)
tab_main_norm = ttk.Frame(tabs_main)
tab_main_result = ttk.Frame(tabs_main)


tabs_main.add(tab_main_image, text='Image')
tabs_main.add(tab_main_norm, text='Norm')
tabs_main.add(tab_main_result, text='Result')


# main view image tab:
label_img_title = tk.Label(tab_main_image, text="Image:")
frame_main_image = ttk.Frame(tab_main_image)

tkfig_img = Figure(figsize = (5, 5), dpi=100)
image_axes = tkfig_img.add_subplot(111) 

aggcanvas_img = FigureCanvasTkAgg(tkfig_img, master = frame_main_image)

aggcanvas_img.get_tk_widget().pack() 
navtool_img = NavigationToolbar2Tk(aggcanvas_img, frame_main_image) 

navtool_img.update()
aggcanvas_img.draw()

label_img_title.pack()
frame_main_image.pack()

# main view norm tab:
label_norm_title = tk.Label(tab_main_norm, text="Norm:")
frame_norm_plot = ttk.Frame(tab_main_norm)

label_norm_title.pack()
frame_norm_plot.pack()


#frame_norm_plot
tkfig_norm = Figure(figsize = (5, 5), dpi=100)
norm_axes = tkfig_norm.add_subplot(111) 

aggcanvas_norm = FigureCanvasTkAgg(tkfig_norm, master = frame_norm_plot)

aggcanvas_norm .get_tk_widget().pack() 
toolbar = NavigationToolbar2Tk(aggcanvas_norm , frame_norm_plot) 
toolbar.update()
aggcanvas_norm.draw()

aggcanvas_norm.get_tk_widget().pack()


# main view result tab:
label_result_title = tk.Label(tab_main_result, text="Extracted Data:")
frame_main_result_plot = ttk.Frame(tab_main_result)

#frame_result_plot
tkfig_result = Figure(figsize = (5, 5), dpi=100)
result_axes = tkfig_result.add_subplot(111) 
result_axes.invert_yaxis()

aggcanvas_result = FigureCanvasTkAgg(tkfig_result, master = frame_main_result_plot)

aggcanvas_result.get_tk_widget().pack() 
navtool_result = NavigationToolbar2Tk(aggcanvas_result , frame_main_result_plot) 
navtool_result.update()
aggcanvas_result.draw()

aggcanvas_result.get_tk_widget().pack()


label_result_title.pack()
frame_main_result_plot.pack()



tabs_main.pack(side=tk.TOP, anchor=tk.N, expand=1, fill="both")
frame_main.pack(side=tk.TOP, anchor=tk.N, expand=1, fill="both")








# ####################################################################################################
# ####################################################################################################

root.mainloop()


