from tkinter import *

okno = Tk()

okno.title("Księgarnia")

tekst_zaloguj = Label(okno, text="Zaloguj")
tekst_zaloguj.pack(padx=5, pady=5)

tekst_login = Label(okno, text="Login: ")
tekst_login.pack(padx=5, pady=5)

entry_login = Entry(okno)
entry_login.pack(padx=5, pady=5)


tekst_haslo = Label(okno, text="Hasło: ")
tekst_haslo.pack(padx=5, pady=5)

entry_haslo = Entry(okno)
entry_haslo.pack(padx=5, pady=5)


zaloguj = Button(okno, text="Zaloguj")
tekst_rejestracja = Label(okno, text=f"Jesli nie masz konta to -> Stwórz Konto")

zaloguj.pack(padx=5, pady=5),tekst_rejestracja.pack(padx=5, pady=5)


okno.mainloop()