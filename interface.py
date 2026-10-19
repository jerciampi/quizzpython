import tkinter as tk
from tkinter import *
TK_SILENCE_DEPRECATION=1

fenetre = tk.Tk()
fenetre.title("SQuizi")

listebox = tk.Listbox(fenetre, font=("Arial", 14), selectbackground="#5356f6", selectforeground="white")
listebox.pack(padx=120, pady=120, expand=True) 

entry = tk.Entry(fenetre, font=("Arial", 14))
entry.pack(padx=120, pady=120, expand=True)


label = tk.Label(fenetre, text="Texte par défaut", bg="yellow")
label.pack(pady=10)



listebox.pack(padx=20, pady=10)  # pas de expand=True
entry.pack(padx=20, pady=10)

label = tk.Label(fenetre, text="Texte par défaut", bg="yellow")
label.pack(pady=10)
value = StringVar() 
bouton1 = Radiobutton(fenetre, text="Oui", variable=value, value=1)
bouton2 = Radiobutton(fenetre, text="Non", variable=value, value=2)
bouton3 = Radiobutton(fenetre, text="Peu être", variable=value, value=3)
bouton1.pack()
bouton2.pack()
bouton3.pack()

value = StringVar() 
value.set("texte par défaut")
entree = Entry(fenetre, textvariable=str, width=30)
entree.pack()

frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(pady=5)

fenetre.mainloop()


