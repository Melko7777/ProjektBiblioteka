from tkinter import *
from tkinter import messagebox
def zaloguj_sie():
    messagebox.showinfo("Udalo sie!", "Pomyslnie zalogowano!")

def nie_pokazuj_hasla():
    entry_haslo.config(show="*")
    pokaz_haslo_button.config(text="Pokaz", command=pokaz_haslo)

def pokaz_haslo():
    entry_haslo.config(show="")
    pokaz_haslo_button.config(text="Nie pokazuj", command=nie_pokazuj_hasla)

okno = Tk()

okno.title("Księgarnia")

tekst_zaloguj = Label(okno, text="Zaloguj")
tekst_zaloguj.grid(padx=5, pady=5)
tekst_login = Label(okno, text="Login: ")
tekst_login.grid(padx=5, pady=5)

entry_login = Entry(okno)
entry_login.grid(padx=5, pady=5)


tekst_haslo = Label(okno, text="Hasło: ")
tekst_haslo.grid(padx=5, pady=5)

entry_haslo = Entry(okno, show="*")
entry_haslo.grid(padx=5, pady=5)

pokaz_haslo_button = Button(okno, text="Pokaz", command=pokaz_haslo)
pokaz_haslo_button.grid(padx=5, pady=5) 

testowy_label = Label(okno)

zaloguj = Button(okno, text="Zaloguj", command=zaloguj_sie)
tekst_rejestracja = Label(okno, text=f"Jesli nie masz konta to -> Stwórz Konto")

zaloguj.grid(padx=5, pady=5),tekst_rejestracja.grid(padx=5, pady=5)

okno.mainloop()