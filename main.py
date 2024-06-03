#!/usr/bin/env python3
from customtkinter import *
from CTkMenuBar import *
from tkinter import messagebox
from tkinter import ttk
import platform
import gui
import netGUI

root = CTk()

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
    btn_corner_radius = 32

elif platform.system() == 'Linux':
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    win_width = int(screen_width/4)
    win_height = int(screen_width/4)
    x = int((screen_width / 2) - (win_width / 2))
    y = int((screen_height / 2) - (win_height / 1.8))
    real_width = screen_width
    btn_corner_radius = 0

else:
    win_width = 500
    win_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (win_width / 2))
    y = int((screen_height / 2) - (win_height / 1.8))
    real_width = screen_width
    btn_corner_radius = 32

font = ""
font_size = 25

root.geometry(f'{win_width}x{win_height}+{x}+{y}')
root.title('Glendy')
root.resizable(False, False)
set_appearance_mode('System')

def change_theme():
    if get_appearance_mode() == 'Dark':
        set_appearance_mode('Light')
    elif get_appearance_mode() == 'Light':
        set_appearance_mode('Dark')

def get_scale(bsize):
    match bsize:
        case 'Tiny':
            scale = int((real_width/125)/2)-5
        case 'Small':
            scale = int((real_width/125)/2)-3
        case 'Normal':
            scale = int((real_width/125)/2)-1
        case 'Large':
            scale = int((real_width/125)/2)+1
    return scale

def offline_game(window, difficulty, bsize):
    pygame_scale = get_scale(bsize)
    window.destroy()
    root.withdraw()
    game = gui.Glendy(difficulty, pygame_scale, get_appearance_mode())
    game.start()
    root.deiconify()

def online_game(window, player, server, bsize, mode):
    pygame_scale = get_scale(bsize)
    window.destroy()
    root.withdraw()
    game = netGUI.netGlendy(player, server, pygame_scale, mode)
    game.start()
    root.deiconify()
    
def offline_window():    
    newWin = CTkToplevel(root)
    if platform.system() == 'Windows':
        newWin.grab_set()
    newWin.title("Offline mode")
    newWin.geometry(f'{win_width}x{win_height}+{x}+{y}')
    newWin.resizable(False, False)
    lbl = CTkLabel(master=newWin, text="Select difficulty:", font=(font, font_size))
    lbl.place(relx=0.5, rely=0.2, anchor="center")
    lbl2 = CTkLabel(master=newWin, text="Select board size (visually):", font=(font, font_size))
    lbl2.place(relx=0.5, rely=0.4, anchor="center")
    if platform.system() == 'Linux':
        combo_difficulty = ttk.Combobox(master=newWin, values=['Easy', 'Medium', 'Hard', 'Impossible'], state='readonly', font=(font, font_size-5))
        combo_bsize = ttk.Combobox(master=newWin, values=['Tiny', 'Small', 'Normal', 'Large'], state='readonly', font=(font, font_size-5))
    else:
        combo_difficulty = CTkComboBox(master=newWin, values=['Easy', 'Medium', 'Hard', 'Impossible'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
        combo_bsize = CTkComboBox(master=newWin, values=['Tiny', 'Small', 'Normal', 'Large'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
    combo_difficulty.set('Easy')
    combo_bsize.set('Normal')
    combo_difficulty.place(relx=0.5, rely=0.3, anchor='center')
    combo_bsize.place(relx=0.5, rely=0.5, anchor='center')
    btn = CTkButton(master=newWin, text='Start the game!', command=lambda:offline_game(newWin, combo_difficulty.get(), combo_bsize.get()), corner_radius=btn_corner_radius, border_width=2, font=(font, font_size))
    btn.place(relx=0.5, rely=0.75, anchor="center")

def online_window():    
    newWin = CTkToplevel(root)
    if platform.system() == 'Windows':
        newWin.grab_set()
    newWin.title("Online mode")
    newWin.geometry(f'{win_width}x{win_height}+{x}+{y}')
    newWin.resizable(False, False)
    lbl = CTkLabel(master=newWin, text="Select player:", font=(font, font_size))
    lbl.place(relx=0.5, rely=0.1, anchor="center")
    lbl2 = CTkLabel(master=newWin, text="Select or enter server address:", font=(font, font_size))
    lbl2.place(relx=0.5, rely=0.3, anchor="center")
    lbl3 = CTkLabel(master=newWin, text="Select board size (visually):", font=(font, font_size))
    lbl3.place(relx=0.5, rely=0.5, anchor="center")
    if platform.system() == 'Linux':
        combo_player = ttk.Combobox(master=newWin, values=['Glenda', 'Trapper'], state='readonly', font=(font, font_size-5))
        combo_server = ttk.Combobox(master=newWin, values=['ir.cloud9p.org:1768'], font=(font, font_size-5))
        combo_bsize = ttk.Combobox(master=newWin, values=['Tiny', 'Small', 'Normal', 'Large'], state='readonly', font=(font, font_size-5))

    else:
        combo_player = CTkComboBox(master=newWin, values=['Glenda', 'Trapper'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
        combo_server = CTkComboBox(master=newWin, width=250, values=['ir.cloud9p.org:1768'], font=(font, font_size-5), dropdown_font=(font, font_size-10))
        combo_bsize = CTkComboBox(master=newWin, values=['Tiny', 'Small', 'Normal', 'Large'], state='readonly', font=(font, font_size-5), dropdown_font=(font, font_size-10))
    combo_player.set('Glenda')
    combo_server.set('ir.cloud9p.org:1768')
    combo_bsize.set('Normal')
    combo_player.place(relx=0.5, rely=0.2, anchor='center')
    combo_server.place(relx=0.5, rely=0.4, anchor='center')
    combo_bsize.place(relx=0.5, rely=0.6, anchor='center')
    radio_var = StringVar(value='')
    radio_mode1 = CTkRadioButton(master=newWin, text='Online multiplayer', value='Multiplayer', variable=radio_var, corner_radius=0, font=(font, font_size-5))
    radio_mode2 = CTkRadioButton(master=newWin, text='Online singleplayer', value='Singleplayer', variable=radio_var, corner_radius=0, font=(font, font_size-5))
    radio_mode1.select()
    radio_mode1.place(relx=0.25, rely=0.7, anchor='center')
    radio_mode2.place(relx=0.75, rely=0.7, anchor='center')
    btn = CTkButton(master=newWin, text='Start the game!', command=lambda:online_game(newWin, combo_player.get(), combo_server.get(), combo_bsize.get(), radio_var.get()), corner_radius=btn_corner_radius, border_width=2, font=(font, font_size))
    btn.place(relx=0.5, rely=0.86, anchor="center")

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
menu.add_cascade('Light/Dark mode', change_theme)
menu.add_cascade('Help', show_help)

lbl = CTkLabel(master=root, text='Glendy', font=(font, font_size+30))
lbl.place(relx=0.5, rely=0.25, anchor="center")

btn = CTkButton(master=root, text='Offline game', command=offline_window, corner_radius=btn_corner_radius, border_width=2, font=(font, font_size))
btn.place(relx=0.5, rely=0.55, anchor="center")

btn = CTkButton(master=root, text='Online game', command=online_window, corner_radius=btn_corner_radius, border_width=2, font=(font, font_size))
btn.place(relx=0.5, rely=0.75, anchor="center")

root.mainloop()
