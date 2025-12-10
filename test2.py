from smtplib import bCRLF
from tkinter import *
import sqlite3 as db
import datetime
import webbrowser
#import bcrypt
import re
from tkinter import messagebox

#rzeczy bazodanowe
conn = db.connect("ksiegarnia.db")
cur = conn.cursor()

current_user_id = None


def wyswietl_katalog():
    global labelka, lista_ksiazek, current_user_id
    lista_ksiazek.delete(0, END)
    labelka.grid(row=3, column=1, columnspan=3, pady=10)
    lista_ksiazek.grid(row=4, column=1, columnspan=3, pady=10, padx=10)


    cur.execute("SELECT Autor, Tytul, Ilosc_Dostepnych FROM Ksiazka")
    wynik = cur.fetchall()

    for ksiazka in wynik:
        autor, tytul, ilosc = ksiazka
        lista_ksiazek.insert(END, f"{autor} - {tytul} (Dostepnych: {ilosc})")


def wyslij_powiadomienie():
    mail = "milosz.duda@zsti.elblag.pl"
    temat = "Powiadomienie"
    tresc = "To jest wiadomosc z aplikacji."

    temat = temat.replace(" ", "%20")
    tresc = tresc.replace(" ", "%20")

    url = f"mailto:{mail}?subject={temat}&body={tresc}"
    webbrowser.open(url)
    messagebox.showinfo("Brawo", "mail został pomyślnie wysłany!(w zasadzie nie zostal ale powinno sie odpalic wysylanie maila jakos)")



def usun_ksiazke():
    global lista_ksiazeczek
    chosen = lista_ksiazeczek.curselection()
    if not chosen:
        messagebox.showerror("Błąd", "Nie zaznaczono żadnej książki do usunięcia!")
        return
    text = lista_ksiazeczek.get(chosen[0])
    try:
        autor, reszta = text.split(" - ", 1)
        tytul = reszta.split(" (Dostepnych:", 1)[0].strip()
    except Exception:
        messagebox.showerror("Błąd", "Nie udało się odczytać danych książki.")
        return
    cur.execute("SELECT ID_Ksiazka FROM Ksiazka WHERE Autor = ? AND Tytul = ?", (autor, tytul))
    wynik = cur.fetchone()
    if wynik is None:
        messagebox.showerror("Błąd", "Nie znaleziono książki w bazie.")
        return
    id_ksiazki = wynik[0]
    if not messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć książkę:\n{autor} - {tytul}?"):
        return
    cur.execute("DELETE FROM Ksiazka WHERE ID_Ksiazka = ?", (id_ksiazki,))
    conn.commit()
    lista_ksiazeczek.delete(0, END)
    cur.execute("SELECT Autor, Tytul, Ilosc_Dostepnych FROM Ksiazka")
    for ksiazka in cur.fetchall():
        autor, tytul, ilosc = ksiazka
        lista_ksiazeczek.insert(END, f"{autor} - {tytul} (Dostępnych: {ilosc})")

    messagebox.showinfo("Sukces", "Książka została usunięta!")



def wyjdz_z_pola_ksiazki():
    global tytul_entry, autor_entry, rok_wydania_entry, ilosc_dostepnych_entry, pola_ksiazki, lista_ksiazeczek

    tytul = tytul_entry.get().strip()
    autor = autor_entry.get().strip()
    rok_wydania = rok_wydania_entry.get().strip()
    ilosc = ilosc_dostepnych_entry.get().strip()
    if not tytul or not autor or not rok_wydania or not ilosc:
        messagebox.showerror("Blad", "Wszystkie pola musza byc wypelnione!")
        return
    if autor.isdigit():
        messagebox.showerror("Blad", "Autor nie mozee byc liczba!")
        return
    
    try:
        datetime.date.fromisoformat(rok_wydania)
    except ValueError:
        messagebox.showerror("Blad", "Data musi byc w formacie RRRR-MM-DD!")
        return

    if not ilosc.isdigit() or int(ilosc) <= 0:
        messagebox.showerror("Blad", "Ilosc musi byc dodatnia liczba całkowita!")
        return

    cur.execute("INSERT INTO Ksiazka (Tytul, Autor, Rok_Wydania, Ilosc_Dostepnych)VALUES (?, ?, ?, ?)", (tytul, autor, rok_wydania, int(ilosc)))
    conn.commit()
    lista_ksiazeczek.delete(0, END)
    cur.execute("SELECT Autor, Tytul, Ilosc_Dostepnych FROM Ksiazka")
    for book in cur.fetchall():
        aut, tyt, ilo = book
        lista_ksiazeczek.insert(END, f"{aut} - {tyt} (Dostepnych: {ilo})")
    messagebox.showinfo("Sukces!", "Książka została dodana pomyślnie!")

    pola_ksiazki.destroy()



def dodaj_ksiazke():
    global pola_ksiazki, tytul_entry, autor_entry, rok_wydania_entry, ilosc_dostepnych_entry
    pola_ksiazki = Tk()
    pola_ksiazki.resizable("false", "false")

    tytul_label = Label(pola_ksiazki, text="Tytuł: ")
    tytul_label.grid(row=0, column=0)

    tytul_entry = Entry(pola_ksiazki)
    tytul_entry.grid(row=1, column=0)

    autor_label = Label(pola_ksiazki, text="Autor: ")
    autor_label.grid(row=2, column=0)

    autor_entry = Entry(pola_ksiazki)
    autor_entry.grid(row=3, column=0)

    rok_wydania_label = Label(pola_ksiazki, text="Data wydania: ")
    rok_wydania_label.grid(row=4, column=0)

    rok_wydania_entry = Entry(pola_ksiazki)
    rok_wydania_entry.grid(row=5, column=0)

    ilosc_dostepnych_label = Label(pola_ksiazki, text="Ilosc dostepnych: ")
    ilosc_dostepnych_label.grid(row=6, column=0)

    ilosc_dostepnych_entry = Entry(pola_ksiazki)
    ilosc_dostepnych_entry.grid(row=7, column=0)

    confirm = Button(pola_ksiazki, text="Ok", command=wyjdz_z_pola_ksiazki)
    confirm.grid(row=8, column=0)

    pola_ksiazki.mainloop()



def wyswietl_wypozyczone():
    global wypozyczenia, wypozyczenia
    cur.execute("SELECT * FROM Wypozyczenia")
    wszystko = cur.fetchall()
    for id_wypo, id_uzy, id_ksi, data, zwrot, status in wszystko:
        wypozyczenia.insert(END, f"{id_wypo} - {id_uzy} - {id_ksi}, {data}, {zwrot}, {status}")
    wypozyczenia.grid(row=3, column=4)



def usun_uzytkownika():
    global lista_uzytkownikow

    chosen = lista_uzytkownikow.curselection()
    if not chosen:
        messagebox.showerror("Błąd", "Nie zaznaczono żadnego użytkownika do usunięcia!")
        return

    tekst = lista_uzytkownikow.get(chosen[0])

    try:
        id_str, reszta = tekst.split(" - ", 1)
        login = reszta.split(",", 1)[0].strip()
        rola = reszta.split(",")[-1].strip()
        id_uzytkownika = int(id_str)
    except:
        messagebox.showerror("Błąd", "Nie udało się odczytać danych użytkownika.")
        return
    
    if rola.lower() == "admin":
        messagebox.showerror("Błąd", "Nie można usunąć administratora!")
        return
    cur.execute("SELECT ID_Uzytkownik FROM Uzytkownik WHERE ID_Uzytkownik = ?", (id_uzytkownika,))
    wynik = cur.fetchone()

    if wynik is None:
        messagebox.showerror("Błąd", "Nie znaleziono użytkownika w bazie.")
        return

    if not messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć użytkownika:\n{login}?"):
        return

    cur.execute("DELETE FROM Wypozyczenia WHERE Uzytkownik_ID = ?", (id_uzytkownika,))
    cur.execute("DELETE FROM Uzytkownik WHERE ID_Uzytkownik = ?", (id_uzytkownika,))
    conn.commit()

    lista_uzytkownikow.delete(0, END)
    cur.execute("SELECT * FROM Uzytkownik")

    for uzyt in cur.fetchall():
        id_, login_, haslo_, rola_ = uzyt
        lista_uzytkownikow.insert(END, f"{id_} - {login_}, {haslo_}, {rola_}")

    messagebox.showinfo("Sukces", "Użytkownik został usunięty!")




def zatwierdz_dodanie_uzytkownika():
    global login_entry, haslo_entry, rola_var, lista_uzytkownikow

    login = login_entry.get().strip()
    haslo = haslo_entry.get().strip()
    rola = rola_var.get()

    if not login or not haslo:
        messagebox.showerror("Błąd", "Proszę wypełnić wszystkie pola!")
        return

    cur.execute("SELECT ID_Uzytkownik FROM Uzytkownik WHERE login = ?", (login,))
    if cur.fetchone():
        messagebox.showerror("Błąd", "Użytkownik o takim loginie już istnieje!")
        return

    cur.execute("INSERT INTO Uzytkownik (login, haslo, Rola) VALUES (?, ?, ?)", (login, haslo, rola))
    conn.commit()

    lista_uzytkownikow.delete(0, END)
    cur.execute("SELECT * FROM Uzytkownik")
    for u in cur.fetchall():
        id_, login_, haslo_, rola_ = u
        lista_uzytkownikow.insert(END, f"{id_} - {login_}, {haslo_}, {rola_}")

    messagebox.showinfo("Sukces!", "Użytkownik został dodany pomyślnie!")
    okno_dodaj_uzytkownika.destroy()

def dodaj_uzytkownika():
    global okno_dodaj_uzytkownika, login_entry, haslo_entry, rola_var

    okno_dodaj_uzytkownika = Tk()
    okno_dodaj_uzytkownika.title("Dodaj Użytkownika")
    okno_dodaj_uzytkownika.resizable(False, False)

    login_label = Label(okno_dodaj_uzytkownika, text="Login:")
    login_label.grid(row=0, column=0)

    login_entry = Entry(okno_dodaj_uzytkownika)
    login_entry.grid(row=1, column=0, padx=10, pady=5)

    haslo_label = Label(okno_dodaj_uzytkownika, text="Hasło:")
    haslo_label.grid(row=2, column=0, padx=10, pady=10)

    haslo_entry = Entry(okno_dodaj_uzytkownika, show="*")
    haslo_entry.grid(row=3, column=0, padx=10, pady=5)

    rola_label = Label(okno_dodaj_uzytkownika, text="Rola:")
    rola_label.grid(row=4, column=0, padx=10, pady=10)

    rola_var = StringVar(value="user")

    rola_menu = OptionMenu(okno_dodaj_uzytkownika, rola_var, "user")
    rola_menu.grid(row=5, column=0, padx=10, pady=5)

    confirm_button = Button(okno_dodaj_uzytkownika, text="Dodaj", command=zatwierdz_dodanie_uzytkownika)
    confirm_button.grid(row=6, column=0, padx=10, pady=15)

    okno_dodaj_uzytkownika.mainloop()

def zarzadzaj_uzytkownikiem():
    global lista_uzytkownikow
    chosen = lista_uzytkownikow.curselection()
    if not chosen:
        messagebox.showerror("Błąd", "Nie zaznaczono żadnego użytkownika do zarzadzania!")
        return
    
    tekst = lista_uzytkownikow.get(chosen[0])
    try:
        id_str, reszta = tekst.split(" - ", 1)
        rola = reszta.split(",")[-1].strip()
        id_user = int(id_str)
    except:
        messagebox.showerror("Błąd", "Nie udało się odczytać danych użytkownika.")
        return
    if rola.lower() == "admin":
        messagebox.showerror("Błąd", "Nie można zmodyfikowac innego administratora!")
        return
    cur.execute("UPDATE Uzytkownik SET Rola = admin WHERE ID_Uzytkownik = ?",(id_user,))

    for uzyt in cur.fetchall():
        id_, login_, haslo_, rola_ = uzyt
        lista_uzytkownikow.insert(END, f"{id_} - {login_}, {haslo_}, {rola_}")

    messagebox.showinfo("Sukces", "Użytkownik został zmodyfikowany")

def sprawdz_termin():
    global wypozyczenia
    selected = wypozyczenia.curselection()
    if not selected:
        messagebox.showerror("Błąd", "Żadne wypożyczenie nie zostało wybrane")
        return
    tekst = wypozyczenia.get(selected[0])
    try:
        czesci = tekst.split(" - ")
        id_wypo_str = czesci[0].strip()
        id_wypo = int(id_wypo_str)
    except:
        messagebox.showerror("Błąd", "Nie udało się odczytać ID wypożyczenia")
        return
    cur.execute("SELECT Termin_Zwrotu, Status FROM Wypozyczenia WHERE ID_Wypozyczenia = ?", (id_wypo,))
    wynik = cur.fetchone()
    if not wynik:
        messagebox.showwarning("Uwaga", "Nie znaleziono wypożyczenia o podanym ID")
        return
    termin_zwrotu, status = wynik
    if status not in ('Wypozyczona', 'Przedluzona'):
        messagebox.showinfo("Informacja", f"To wypożyczenie ma status: {status}\nTermin zwrotu: {termin_zwrotu}")
    else:
        messagebox.showinfo("Termin zwrotu", f"Termin zwrotu: {termin_zwrotu}\nStatus: {status}")

def wypozycz():
    global lista_ksiazek, lista_historii_wypozyczen, current_user_id

    wybrana = lista_ksiazek.curselection()
    if not wybrana:
        messagebox.showerror("Blad", "Nie zaznaczono zadnej ksiazki")
        return

    tekst = lista_ksiazek.get(wybrana[0])
    try:
        autor, reszta = tekst.split(" - ", 1)
        tytul = reszta.split(" (Dostepnych:", 1)[0].strip()
    except Exception:
        messagebox.showerror("Blad", "Nie udalo sie odczytac danych ksiazki.")
        return

    cur.execute("SELECT ID_Ksiazka, Ilosc_Dostepnych FROM Ksiazka WHERE Autor = ? AND Tytul = ?", (autor, tytul))
    wynik = cur.fetchone()
    if wynik is None:
        messagebox.showerror("Blad", "Nie znaleziono ksiazki w bazie.")
        return

    id_ksiazki, dostepnosc = wynik

    if dostepnosc <= 0:
        messagebox.showerror("Niestety", "Brak ksiazki na stanie")
        return

    cur.execute("SELECT COUNT(*) FROM Wypozyczenia WHERE Uzytkownik_ID = ? AND Ksiazka_ID = ? AND Status = 'Wypozyczona' ", (current_user_id, id_ksiazki))
    
    if cur.fetchone()[0] > 0:
        messagebox.showerror("Error", "Masz juz te ksiazke wypozyczona! Wpierw ja zwroc.")
        return

    data_wyp = datetime.date.today().isoformat()
    termin_zwrotu = (datetime.date.today() + datetime.timedelta(days=14)).isoformat()

    cur.execute("INSERT INTO Wypozyczenia (Uzytkownik_ID, Ksiazka_ID, Data_wypozyczenia, Termin_Zwrotu, Status) VALUES (?, ?, ?, ?, ?)", (current_user_id, id_ksiazki, data_wyp, termin_zwrotu, "Wypozyczona"))
    
    cur.execute("UPDATE Ksiazka SET Ilosc_Dostepnych = Ilosc_Dostepnych - 1 WHERE ID_Ksiazka = ?", (id_ksiazki,))
    conn.commit()

    messagebox.showinfo("Sukces!", "Ksiazka zostala wypozyczona.")
    wyswietl_katalog()
    historia_wypozyczen(current_user_id)

def przedluz_wypozyczenie():
    global lista_historii_wypozyczen, current_user_id

    if not lista_historii_wypozyczen.curselection():
         messagebox.showwarning("Blad", "Zaznacz wypozyczenie, ktore chcesz przedluzyc") 
         return
    
    try:
        tytul = lista_historii_wypozyczen.get(lista_historii_wypozyczen.curselection()[0]).split(" - Data wypozyczenia:")[0].strip()
    except:
         messagebox.showerror("Blad", "Nie udalo sie odczytac tytulu ksiazki.")
         return
    
    cur.execute("SELECT w.ID_Wypozyczenia, w.Ksiazka_ID, w.Termin_Zwrotu, w.Data_wypozyczenia, w.Status FROM Wypozyczenia w JOIN Ksiazka k ON w.Ksiazka_ID = k.ID_Ksiazka WHERE w.Uzytkownik_ID = ? AND k.Tytul = ? AND w.Status IN ('Wypozyczona', 'Przedluzona')", (current_user_id, tytul))
    wynik = cur.fetchone()

    if not wynik:
         messagebox.showwarning("Uwaga", "To wypozyczenie nie jest aktywne lub juz zostalo zwrocone.");
         return
    id_wyp, id_ksiazki, termin_str, data_wyp_str, aktualny_status = wynik
    if aktualny_status == 'Przedluzona': 
        messagebox.showinfo("Nie mozna", "To wypozyczenie zostalo juz przedluzone raz. Nie mozna drugi raz!");
        return
    
    nowy_termin = datetime.date.fromisoformat(termin_str) + datetime.timedelta(days=14)

    cur.execute("UPDATE Wypozyczenia SET Termin_Zwrotu = ?, Status = 'Przedluzona' WHERE ID_Wypozyczenia = ?", (nowy_termin.isoformat(), id_wyp))
    conn.commit()
    messagebox.showinfo("Sukces!", f"Wypozyczenie przedluzone o 14 dni!\nNowy termin zwrotu: {nowy_termin}")
    historia_wypozyczen(current_user_id)

def zwracanie():
    global lista_historii_wypozyczen, current_user_id

    wybrana = lista_historii_wypozyczen.curselection()
    if not wybrana:
        messagebox.showwarning("Blad", "Zaznacz ksiazke, ktora chcesz zwrocic")
        return

    tekst = lista_historii_wypozyczen.get(wybrana[0])

    try:
        tytul = tekst.split(" - Data wypozyczenia:")[0].strip()
    except:
        messagebox.showerror("Blad", "Nie udalo sie rozroznic tytulu ksiazki.")
        return


    cur.execute("""SELECT w.ID_Wypozyczenia, w.Ksiazka_ID, w.Termin_Zwrotu, k.Ilosc_Dostepnych FROM Wypozyczenia w JOIN Ksiazka k ON w.Ksiazka_ID = k.ID_Ksiazka WHERE w.Uzytkownik_ID = ? AND k.Tytul = ? AND w.Status = 'Wypozyczona'""", (current_user_id, tytul))
    wynik = cur.fetchone()
    if not wynik:
        messagebox.showwarning("Uwaga", "Ta ksiazka nie jest aktualnie przez ciebie wypozyczona")
        return

    id_wypozyczenia, id_ksiazki, termin_zwrotu, ilosc_dostepnych = wynik
    termin_zwrotu_date = datetime.date.fromisoformat(termin_zwrotu)
    
    dzisiaj = datetime.date.today()
    przetrzymanie = (dzisiaj - termin_zwrotu_date).days

    cur.execute("UPDATE Wypozyczenia SET Status = 'Zwrocona', Termin_zwrotu = ? WHERE ID_Wypozyczenia = ?",(dzisiaj.isoformat(), id_wypozyczenia))

    cur.execute("UPDATE Ksiazka SET Ilosc_Dostepnych = Ilosc_Dostepnych + 1 WHERE ID_Ksiazka = ?", (id_ksiazki,))

    conn.commit()

    if przetrzymanie > 0:
        messagebox.showwarning("Zwrocono z opoznieniem!", f"Ksiazka zwrocona {przetrzymanie} dni po terminie!")
    else:
        messagebox.showinfo("Sukces!", "Ksiazka zostala zwrocona. Dziekujemy!")

    wyswietl_katalog()
    historia_wypozyczen(current_user_id)

def historia_wypozyczen(uzytkownik_id):
    global labelka2, lista_historii_wypozyczen, Termin_zwrotu
    lista_historii_wypozyczen.delete(0, END)
    labelka2.grid(row=3, column=4, columnspan=3, pady=10)
    lista_historii_wypozyczen.grid(row=4, column=4, columnspan=4, pady=10, padx=10)

    cur.execute("SELECT Ksiazka.Tytul, Data_wypozyczenia, Termin_zwrotu, Status FROM Wypozyczenia JOIN Ksiazka ON Ksiazka_ID = ID_Ksiazka WHERE Uzytkownik_ID = ?", (uzytkownik_id,))
    wynik = cur.fetchall()

    for wypozyczenie in wynik:
        tytul, Data_wypozyczenia, Termin_zwrotu, Status = wypozyczenie
        lista_historii_wypozyczen.insert(END, f"{tytul} - Data wypozyczenia: {Data_wypozyczenia} -  Status: {Status}")

def zaloguj_sie():
    global labelka, lista_ksiazek, labelka2, lista_historii_wypozyczen, current_user_id, lista_ksiazeczek, wypozyczenia, lista_uzytkownikow
    login = entry_login.get()
    haslo = entry_haslo.get()
    if login == "" or haslo == "":
        messagebox.showerror("BLAD", "Prosze wypelnic wszystkie pola")
        return
    
    cur.execute("SELECT ID_Uzytkownik, Rola, haslo FROM Uzytkownik WHERE login = ?", (login,))
    wynik = cur.fetchone()
    uzytkownik_id, rola, fetched_haslo = wynik
    if wynik is None:
        messagebox.showerror("Blad", "Nie ma takiego uzytkownika")
    else:
        fetched_haslo = wynik[2]
        if haslo == fetched_haslo:
            messagebox.showinfo(":D","Udalo sie zalogowac")
            cur.execute("SELECT ID_Uzytkownik, Rola FROM Uzytkownik WHERE login = ?", (login,))
            current_user_id = uzytkownik_id
            if rola == "admin":
                messagebox.showinfo("Witamy serdecznie", "Witam Adminie :D")
                okno_admina = Tk()
                okno_admina.geometry("1400x600")
                
                przycisk_zarzadzaj_uzo = Button(okno_admina, text=f"Zarzadzaj uzytkownikiem", command=zarzadzaj_uzytkownikiem)
                przycisk_zarzadzaj_uzo.grid(row=1, column=4, padx=15, pady=15)

                labelka_ksiazeczek = Label(okno_admina, text="Lista ksiazek")
                labelka_ksiazeczek.grid(row=2, column=1, columnspan=3, pady=10)

                lista_ksiazeczek = Listbox(okno_admina, width=60, height=15)
                lista_ksiazeczek.grid(row=3, column=1, pady=10, padx=10)

                cur.execute("SELECT Autor, Tytul, Ilosc_Dostepnych FROM Ksiazka")
                wynik = cur.fetchall()

                for ksiazka in wynik:
                    autor, tytul, ilosc = ksiazka
                    lista_ksiazeczek.insert(END, f"{autor} - {tytul} (Dostepnych: {ilosc})")

                labelka_uzytkownikow = Label(okno_admina, text="Uzytkownicy:")
                labelka_uzytkownikow.grid(row=2, column=6, columnspan=3, pady=10)
                
                lista_uzytkownikow = Listbox(okno_admina, width=60, height=15)
                lista_uzytkownikow.grid(row=3, column=6, pady=10, padx=10)

                cur.execute("SELECT * FROM Uzytkownik")
                wynik = cur.fetchall()

                for uzytkownik in wynik:
                    id, login, haslo, rola = uzytkownik
                    lista_uzytkownikow.insert(END, f"{id} - {login}, {haslo}, {rola}")

                przycisk_sprawdz_wypozyczone = Button(okno_admina, text=f"Wyswietl Wypozyczone Ksiazki", command=wyswietl_wypozyczone)
                przycisk_sprawdz_wypozyczone.grid(row=1, column=1, padx=15, pady=15)
                

                przycisk_dodaj_ksiazke = Button(okno_admina, text=f"Dodaj Ksiazke", command=dodaj_ksiazke)
                przycisk_dodaj_ksiazke.grid(row=1, column=2, padx=15, pady=15)


                przycisk_usun_ksiazke = Button(okno_admina, text=f"Usun Ksiazke", command=usun_ksiazke)
                przycisk_usun_ksiazke.grid(row=1, column=3, padx=15, pady=15)
                

                przycisk_dodaj_uzo = Button(okno_admina, text=f"Dodaj Uzytkownika", command=dodaj_uzytkownika)
                przycisk_dodaj_uzo.grid(row=1, column=4, padx=15, pady=15)
                
                
                przycisk_usun_uzo = Button(okno_admina, text=f"Usun Uzytkownika", command=usun_uzytkownika)
                przycisk_usun_uzo.grid(row=1, column=5, padx=15, pady=15)


                przycisk_sprawdz_termin = Button(okno_admina, text=f"Sprawdz Termin Zwrotu", command=sprawdz_termin)
                przycisk_sprawdz_termin.grid(row=1, column=6, padx=15, pady=15)
               
                
                przycisk_wyslij_powiadomienie = Button(okno_admina, text=f"Wyslij Powiadomienie", command=wyslij_powiadomienie)
                przycisk_wyslij_powiadomienie.grid(row=1, column=7, padx=15, pady=15)
                
                #tutaj listbox z wypozyczeniami
                wypozyczenia = Listbox(okno_admina, width=60, height=30)
                okno.destroy()
                okno_admina.mainloop()
            
            elif cur.fetchone()[1] == "Uzytkownik":
                okno_uzytkownika = Tk()
                okno_uzytkownika.geometry("1200x600")
                
                labelka = Label(okno_uzytkownika, text="Lista ksiazek")
                lista_ksiazek = Listbox(okno_uzytkownika, width=60, height=15)

                labelka2 = Label(okno_uzytkownika, text="Historia wypozyczen")
                lista_historii_wypozyczen = Listbox(okno_uzytkownika, width=97, height=15)

                przycisk_wyswietl_katalog = Button(okno_uzytkownika, text=f"Wyswietl Katalog", command=wyswietl_katalog)
                przycisk_wyswietl_katalog.grid(row=2, column=1, padx=15, pady=15)

                przycisk_wypozyczania = Button(okno_uzytkownika, text=f"Wypozycz" , command=wypozycz) 
                przycisk_wypozyczania.grid(row=2, column=2, padx=15, pady=15)

                przycisk_przedluz_wypozyczenie = Button(okno_uzytkownika, text=f"Przedluz wypozyczenie", command=przedluz_wypozyczenie)
                przycisk_przedluz_wypozyczenie.grid(row=2, column=3, padx=15, pady=15)

                przycisk_zwracania = Button(okno_uzytkownika, text=f"Zwroc" , command=zwracanie)
                przycisk_zwracania.grid(row=2, column=4, padx=15, pady=15) 

                przycisk_historia_wypozyczen = Button(okno_uzytkownika, text=f"Sprawdz Historie", command=lambda: historia_wypozyczen(uzytkownik_id))
                przycisk_historia_wypozyczen.grid(row=2, column=5, padx=15, pady=15) 
                
                okno.destroy()
                okno_uzytkownika.mainloop()
            else:
                messagebox.showerror(">:C", "Nie udalo sie zalogowac")


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
        messagebox.showerror("Error", "Pola nie sa wypelnione (gdzies tutaj jeszcze trzeba dodac ze jak login uzytkownika juz istnieje to tez nie mozna)")
    elif not re.fullmatch(regex, haslo_reje):
        messagebox.showerror("Error", "Haslo nie spelnienia wymagan (Bochen jak to czytasz to wez dodaj jakiegos labela czerwonego ze haslo musi miec min 8 znakow, conajmniej 1 duza litere 1 cyfre i 1 znakspecjalny)")
    elif haslo_reje != p_haslo_reje:
        messagebox.showerror("Error", "Hasla nie sa takie same")
    else:
        messagebox.showinfo("Udalo sie!", "Konto stworzone pomyslnie.")
        cur.execute("INSERT INTO Uzytkownik(login, haslo, ROLA) VALUES (?,?,?)",(login_reje, haslo_reje, "user"))
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

    zaloguj.config(text=f"Stworz Konto", command=stworz_konto)
    tekst_rejestracja_1.config(text=f"Jesli masz konto")
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
    tekst_rejestracja_1.config(text=f"Jesli nie masz konto")
    rejestracja.config(text=f"Stworz konto")
    rejestracja.bind("<Button-1>", lambda event:zmien_na_rejestracje())


okno = Tk()

okno.title("Ksiegarnia")
okno.geometry('430x300')
okno.resizable('False','False')
 
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

tekst_haslo = Label(okno, text="Haslo: ")
tekst_haslo.grid(row=3,padx=5, pady=5)

tekst_haslo_reje = Label(okno, text="Wpisz haslo:")
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

tekst_powtorz_haslo = Label(okno, text="Powtorz haslo: ")
tekst_powtorz_haslo.grid_forget()


entry_powtorz_haslo_reje = Entry(okno, show="*")
entry_powtorz_haslo_reje.grid_forget()

# Reszta rzeczy 

zaloguj = Button(okno, text="Zaloguj", command=zaloguj_sie)
tekst_rejestracja_1 = Label(okno, text=f"Jesli nie masz konta to")
rejestracja = Label(okno, text=f"Stworz Konto", fg='blue', cursor="hand2")

zaloguj.grid(row=7,padx=5, pady=5)

tekst_rejestracja_1.grid(row=8)
rejestracja.grid(row=9)
rejestracja.bind("<Button-1>",lambda event:zmien_na_rejestracje())

okno.grid_columnconfigure(0,weight=1)


okno.mainloop()