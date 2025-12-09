from smtplib import bCRLF
from tkinter import *
import sqlite3 as db
#import bcrypt
import re
from tkinter import messagebox
#rzeczy bazodanowe
conn = db.connect("ksiegarnia.db")
cur = conn.cursor()

def wyswietl_katalog():
    # Miłosza robota
    print('a')

def wypozycz():
    # miłosza robota
    print('b')

def zwracanie():
    # miłosza robota
    print('c')

def historia_wypozyczen():
    # miłosza robota
    print('d')

def zaloguj_sie():
    login = entry_login.get()
    haslo = entry_haslo.get()
    if login == "" or haslo == "":
        messagebox.showerror("BŁAD", "Prosze wypełnić wszystkie pola")
        return
    cur.execute("SELECT haslo FROM Uzytkownik WHERE login = ?", (login,))
    wynik = cur.fetchone()

    if wynik is None:
        messagebox.showerror("Błąd", "Nie ma takiego użytkownika")
    else:
        fetched_haslo = wynik[0]
        if haslo == fetched_haslo:
            messagebox.showinfo(":D","Udało się zalogować")
            okno_uzytkownika = Tk()
            
            przycisk_wyswietl_katalog = Button(okno, text=f"Wyświetl Katalog", command=wyswietl_katalog)
            przycisk_wyswietl_katalog.grid(row=2, column=1, padx=15, pady=15)

            przycisk_wypozyczania = Button(okno, text=f"Wypożycz" , command=wypozycz) 
            przycisk_wypozyczania.grid(row=2, column=2, padx=15, pady=15)

            przycisk_zwracania = Button(okno, text=f"Zwróć" , command=zwracanie)
            przycisk_zwracania.grid(row=2, column=3, padx=15, pady=15) 
            przycisk_historia_wypozyczen = Button(okno, text=f"Sprawdz Historie", command=historia_wypozyczen)
            przycisk_historia_wypozyczen.grid(row=2, column=3, padx=15, pady=15) 
            
            okno.destroy()
            okno_uzytkownika.mainloop()
        else:
            messagebox.showerror(">:C", "Nie udało się zalogować")


def nie_pokazuj_hasla():
    entry_haslo.config(show="*")
    pokaz_haslo_button.config(text="Pokaz", command=pokaz_haslo)

def pokaz_haslo():
    entry_haslo.config(show="")
    pokaz_haslo_button.config(text="Nie pokazuj", command=nie_pokazuj_hasla)

def stworz_konto():
    login_reje = entry_login_reje.get()
    haslo_reje = entry_haslo_reje.get()
    p_haslo_reje = entry_powtorz_haslo_reje.get()
    regex = r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"

    if haslo_reje == "" or login_reje == "":
        messagebox.showerror("Error", "Pola nie są wypełnione (gdzies tutaj jeszcze trzeba dodac ze jak login uzytkownika juz istnieje to tez nie mozna)")
    elif not re.fullmatch(regex, haslo_reje):
        messagebox.showerror("Error", "Hasło nie spełnia wymagań (Bochen jak to czytasz to weź dodaj jakiegoś labela czerwonego że hasło musi mieć min 8 znakow, conajmniej 1 duża litere 1 cyfre i 1 znakspecjalny)")
    elif haslo_reje != p_haslo_reje:
        messagebox.showerror("Error", "Hasła nie są takie same")
    else:
        messagebox.showinfo("Udało się!", "Konto stworzone pomyślnie.")
        cur.execute("INSERT INTO Uzytkownik(Nazwa, login, haslo, ROLA) VALUES (?,?,?,?)",(login_reje, login_reje, haslo_reje, "Uzytkownik"))
        conn.commit()
        zmien_na_logowanie()
    
def zmien_na_rejestracje():
    entry_login.delete(0, END)
    entry_haslo.delete(0, END)

    tekst_zaloguj.grid_forget()
    tekst_rejestracja.grid(row=0, padx=5, pady=5)

    tekst_login.grid_forget()
    tekst_login_reje.grid(row=1, padx=5, pady=5)
    
    entry_login.grid_forget()
    entry_login_reje.grid(row=2, padx=5, pady=5)

    tekst_haslo.grid_forget()
    tekst_haslo_reje.grid(row=3, padx=5, pady=5)

    entry_haslo.grid_forget()
    entry_haslo_reje.grid(row=4, padx=5, pady=5)

    pokaz_haslo_button.grid_forget()

    tekst_powtorz_haslo.grid(row=5, padx=5, pady=5)
    entry_powtorz_haslo_reje.grid(row=6, padx=15, pady=5)

    zaloguj.config(text=f"Stwórz Konto", command=stworz_konto)
    tekst_rejestracja_1.config(text=f"Jeśli masz konto")
    rejestracja.config(text=f"Zaloguj sie")
    rejestracja.bind("<Button-1>", lambda event:zmien_na_logowanie())

def zmien_na_logowanie():
    entry_login_reje.delete(0, END)
    entry_haslo_reje.delete(0, END)
    entry_powtorz_haslo_reje.delete(0, END)

    tekst_zaloguj.grid(row=0, padx=5, pady=5)
    tekst_rejestracja.grid_forget()

    tekst_login.grid(row=1, padx=5, pady=5)
    tekst_login_reje.grid_forget()
    
    entry_login.grid(row=2, padx=5, pady=5)
    entry_login_reje.grid_forget()

    tekst_haslo.grid(row=3, padx=5, pady=5)
    tekst_haslo_reje.grid_forget()

    entry_haslo.grid(row=4, padx=5, pady=5)
    entry_haslo_reje.grid_forget()

    pokaz_haslo_button.grid(row=5, padx=5, pady=5)

    tekst_powtorz_haslo.grid_forget()
    entry_powtorz_haslo_reje.grid_forget()

    zaloguj.config(text=f"Zaloguj", command=zaloguj_sie)
    tekst_rejestracja_1.config(text=f"Jeśli nie masz konto")
    rejestracja.config(text=f"Stwórz konto")
    rejestracja.bind("<Button-1>", lambda event:zmien_na_rejestracje())

okno = Tk()

okno.title("Księgarnia")
okno.geometry('430x300')
 
tekst_zaloguj = Label(okno, text="Zaloguj")
tekst_zaloguj.grid(row=0,padx=5, pady=5)

tekst_rejestracja = Label(okno, text="Rejestracja")
tekst_rejestracja.grid_forget()



#Label Login

tekst_login = Label(okno, text="Login: ")
tekst_login.grid(row=1,padx=5, pady=5)

tekst_login_reje = Label(okno, text="Wpisz Login: ")
tekst_login_reje.grid_forget()


#Entry loginu

entry_login = Entry(okno)
entry_login.grid(row=2,padx=5, pady=5)

entry_login_reje = Entry(okno)
entry_login_reje.grid_forget()


# Label Haslo

tekst_haslo = Label(okno, text="Hasło: ")
tekst_haslo.grid(row=3,padx=5, pady=5)

tekst_haslo_reje = Label(okno, text="Wpisz hasło:")
tekst_haslo_reje.grid_forget()


# Entry Haslo

entry_haslo = Entry(okno, show="*")
entry_haslo.grid(row=4,column=0,padx=5, pady=5)

entry_haslo_reje = Entry(okno, show="*")
entry_haslo_reje.grid_forget()


# Przycisk pokaz haslo

pokaz_haslo_button = Button(okno, text="Pokaz", command=pokaz_haslo)
pokaz_haslo_button.grid(row=5,padx=15, pady=5)

# Label i entry powtorz haslo

tekst_powtorz_haslo = Label(okno, text="Powtórz hasło: ")
tekst_powtorz_haslo.grid_forget()


entry_powtorz_haslo_reje = Entry(okno, show="*")
entry_powtorz_haslo_reje.grid_forget()

zaloguj = Button(okno, text="Zaloguj", command=zaloguj_sie)
tekst_rejestracja_1 = Label(okno, text=f"Jesli nie masz konta to")
rejestracja = Label(okno, text=f"Stwórz Konto", fg='blue', cursor="hand2")

zaloguj.grid(row=7,padx=5, pady=5)

tekst_rejestracja_1.grid(row=8)
rejestracja.grid(row=9)
rejestracja.bind("<Button-1>",lambda event:zmien_na_rejestracje())

okno.grid_columnconfigure(0,weight=1)


okno.mainloop()
