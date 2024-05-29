#!/usr/bin/env python3
from customtkinter import *
from CTkMenuBar import *
from tkinter import messagebox
from tkinter import ttk
import platform
import gui
import netGUI

root = CTk()
pygame_scale = 5
pygame_scale_constant = 1

if platform.system() == 'Windows':
    import ctypes
    scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    win_width = 500
    win_height = 500
    scaled_width = root.winfo_screenwidth()
    scaled_height = root.winfo_screenheight()
    x = int(((scaled_width / 2) - (win_width / 2)) * (scale_factor/100))
    y = int(((scaled_height / 2) - (win_height / 1.8)) * (scale_factor/100))
    real_width = ctypes.windll.user32.GetSystemMetrics(0)
    pygame_scale = int((real_width/125)/2)-pygame_scale_constant
    btn_corner_radius = 32

elif platform.system() == 'Linux':
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    win_width = int(screen_width/4)
    win_height = int(screen_width/4)
    x = int((screen_width / 2) - (win_width / 2))
    y = int((screen_height / 2) - (win_height / 1.8))
    pygame_scale = int((screen_width/125)/2)-pygame_scale_constant
    btn_corner_radius = 0

else:
    win_width = 500
    win_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (win_width / 2))
    y = int((screen_height / 2) - (win_height / 1.8))
    pygame_scale = int((screen_width/125)/2)-pygame_scale_constant
    btn_corner_radius = 32

font = ""
text_color = "#000000"
font_size = 25
btn_fg_color = '#CDE8E5'
btn_hover_color = '#6DC5D1'
btn_border_color = '#FEB941'

root.geometry(f'{win_width}x{win_height}+{x}+{y}')
root.title('Glendy')
root.resizable(False, False)
set_appearance_mode("light")

def online_game():
    root.withdraw()
    game = netGUI.netGlendy(pygame_scale)
    game.start()
    root.deiconify()

def offline_game(window, difficulty):
    window.destroy()
    root.withdraw()
    game = gui.Glendy(difficulty, pygame_scale)
    game.start()
    root.deiconify()
    
def offline_window():    
    newWin = CTkToplevel(root)
    if platform.system() == 'Windows':
        newWin.grab_set()
    newWin.title("Offline mode")
    newWin.geometry(f'{win_width}x{win_height}+{x}+{y}')
    newWin.resizable(False, False)

    lbl = CTkLabel(master=newWin, text="Select difficulty:", font=(font, font_size), text_color=text_color)
    lbl.place(relx=0.5, rely=0.2, anchor="center")
    if platform.system() == 'Windows':
        combo = CTkComboBox(master=newWin, values=['Easy', 'Medium', 'Hard', 'Impossible'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
    elif platform.system() == 'Linux':
        combo = ttk.Combobox(master=newWin, values=['Easy', 'Medium', 'Hard', 'Impossible'], state='readonly', font=(font, font_size-5))
    else:
        combo = CTkComboBox(master=newWin, values=['Easy', 'Medium', 'Hard', 'Impossible'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
    combo.set('Easy')
    combo.place(relx=0.5, rely=0.3, anchor="center")

    btn = CTkButton(master=newWin, text='Start the game!', command=lambda:offline_game(newWin, combo.get()), corner_radius=btn_corner_radius, fg_color=btn_fg_color, hover_color=btn_hover_color, border_color=btn_border_color, border_width=2, text_color=text_color, font=(font, font_size))
    btn.place(relx=0.5, rely=0.7, anchor="center")

def show_help():
    messagebox.showinfo(master=root, title="Help", message=
    '''Glendy is a simple game.
One player plays as TRAPPER,
and the other as GLENDA.
GLENDA tries to escape by reaching sides,
and TRAPPER tries to trap GLENDA in walls.
To put a wall as TRAPPER, click on any
free circle on the board each turn.
To escape as GLENDA, you can choose from
6 neighboring circles around GLENDA each turn.''')

menu = CTkMenuBar(master=root)
menu.add_cascade("Help", show_help)

lbl = CTkLabel(master=root, text="Glendy", font=(font, font_size+30), text_color=text_color)
lbl.place(relx=0.5, rely=0.25, anchor="center")

btn = CTkButton(master=root, text='Offline game', command=offline_window, corner_radius=btn_corner_radius, fg_color=btn_fg_color, hover_color=btn_hover_color, border_color=btn_border_color, border_width=2, text_color=text_color, font=(font, font_size))
btn.place(relx=0.5, rely=0.55, anchor="center")

btn = CTkButton(master=root, text='Online game', command=online_game, corner_radius=btn_corner_radius, fg_color=btn_fg_color, hover_color=btn_hover_color, border_color=btn_border_color, border_width=2, text_color=text_color, font=(font, font_size))
btn.place(relx=0.5, rely=0.75, anchor="center")

root.mainloop()
