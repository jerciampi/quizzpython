import tkinter as tk
from tkinter import messagebox

fenetre = tk.Tk()
fenetre.title("Quiz")

listebox = tk.Listbox(fenetre, font=("Arial", 14), selectbackground="#5356f6", selectforeground="white")
listebox.pack(padx=120, pady=120, expand=True) 

entry = tk.Entry(fenetre, font=("Arial", 14))
entry.pack(padx=120, pady=120, expand=True)

frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(pady=5)

fenetre.mainloop()

