import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import datetime
import sounddevice as sd
import numpy as np
import wavio

# Credenziali di accesso (username e password)
USERNAME = "admin"
PASSWORD = "password123"

# Funzione di autenticazione
def authenticate(user, pwd):
    return user == USERNAME and pwd == PASSWORD

# Funzione per registrare audio
def record_audio(filename):
    duration = 10  # durata della registrazione in secondi
    fs = 44100  # frequenza di campionamento
    print("Registrazione... (premi Ctrl+C per interrompere)")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()  # Aspetta che la registrazione sia completata
    wavio.write(filename, audio, fs, sampwidth=2)  # Salva il file audio
    print(f"Registrazione salvata come: {filename}")

# Creazione dell'app GUI
class UrbexLandsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UrbexLands - Login")
        self.root.geometry("400x300")
        self.root.config(bg="black")

        # Titolo
        self.title_label = tk.Label(root, text="UrbexLands - Login", font=("Arial", 24), fg="white", bg="black")
        self.title_label.pack(pady=20)

        # Campo Username
        self.user_label = tk.Label(root, text="Username", font=("Arial", 14), fg="white", bg="black")
        self.user_label.pack()
        self.username_entry = tk.Entry(root, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        # Campo Password
        self.pwd_label = tk.Label(root, text="Password", font=("Arial", 14), fg="white", bg="black")
        self.pwd_label.pack()
        self.password_entry = tk.Entry(root, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)

        # Pulsante di Login
        self.login_btn = tk.Button(root, text="Login", font=("Arial", 14), command=self.check_login)
        self.login_btn.pack(pady=20)

    def check_login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()

        if authenticate(user, pwd):
            self.open_dashboard()
        else:
            messagebox.showerror("Errore", "Username o Password errati!")

    def open_dashboard(self):
        self.root.destroy()
        dashboard = tk.Tk()
        Dashboard(dashboard)
        dashboard.mainloop()

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("UrbexLands - Dashboard")
        self.root.geometry("600x400")
        self.root.config(bg="black")

        # Titolo
        self.title_label = tk.Label(root, text="Benvenuto in UrbexLands", font=("Arial", 24), fg="white", bg="black")
        self.title_label.pack(pady=20)

        # Selezione del luogo
        self.location_label = tk.Label(root, text="Scegli posto abbandonato:", font=("Arial", 18), fg="white", bg="black")
        self.location_label.pack(pady=10)

        self.locations = [
            "Teatro Mediterraneo", 
            "Area Militare abbandonata", 
            "Fabbrica abbandonata 2", 
            "Fabbrica abbandonata 1", 
            "Palazzo Trifletti", 
            "Pizzeria Central Park (CEP)", 
            "Altre aree"
        ]
        
        self.location_var = tk.StringVar()
        self.location_var.set(self.locations[0])  # Imposta valore predefinito

        self.location_menu = tk.OptionMenu(root, self.location_var, *self.locations)
        self.location_menu.pack(pady=10)

        # Pulsante per confermare la selezione
        self.select_btn = tk.Button(root, text="Conferma", font=("Arial", 14), command=self.confirm_location)
        self.select_btn.pack(pady=20)

    def confirm_location(self):
        selected_location = self.location_var.get()
        messagebox.showinfo("Luogo selezionato", f"Hai selezionato: {selected_location}")
        self.open_management_page(selected_location)

    def open_management_page(self, location):
        # Crea una nuova finestra per la gestione del luogo
        management_window = tk.Toplevel(self.root)
        management_window.title(f"Gestione: {location}")
        management_window.geometry("600x400")
        management_window.config(bg="black")

        # Titolo della gestione
        management_label = tk.Label(management_window, text=f"Gestione di {location}", font=("Arial", 24), fg="white", bg="black")
        management_label.pack(pady=20)

        # Orario attuale
        self.current_time_label = tk.Label(management_window, font=("Arial", 16), fg="white", bg="black")
        self.current_time_label.pack(pady=10)
        self.update_time()

        # Pulsante Energy ON/OFF
        self.energy_status = tk.StringVar(value="OFF")
        self.energy_button = tk.Button(management_window, text="Energy OFF", font=("Arial", 14), command=self.toggle_energy)
        self.energy_button.pack(pady=20)

        # Note
        self.note_label = tk.Label(management_window, text="NOTE:", font=("Arial", 16), fg="white", bg="black")
        self.note_label.pack(pady=10)

        self.note_text = tk.Text(management_window, height=5, width=40)
        self.note_text.pack(pady=5)

        # Pulsante per aggiungere nota
        self.add_note_btn = tk.Button(management_window, text="Aggiungi Nota", font=("Arial", 14), command=self.add_note)
        self.add_note_btn.pack(pady=10)

        # Persone in servizio
        self.service_people_label = tk.Label(management_window, text="Persone in servizio:", font=("Arial", 16), fg="white", bg="black")
        self.service_people_label.pack(pady=10)

        self.service_people_text = tk.Text(management_window, height=5, width=40)
        self.service_people_text.pack(pady=5)

        # Pulsante per aggiungere crew
        self.add_crew_btn = tk.Button(management_window, text="Aggiungi Crew", font=("Arial", 14), command=self.add_crew)
        self.add_crew_btn.pack(pady=10)

        # Pulsante di registrazione audio
        self.record_btn = tk.Button(management_window, text="Registra Audio", font=("Arial", 14), command=self.record_audio)
        self.record_btn.pack(pady=20)

        # Percentuale di esplorazione
        self.exploration_percentage_label = tk.Label(management_window, text="Percentuale di esplorazione: 0%", font=("Arial", 16), fg="white", bg="black")
        self.exploration_percentage_label.pack(pady=10)

        # Pulsante di salvataggio
        self.save_button = tk.Button(management_window, text="Salva Dettagli", font=("Arial", 14), command=self.save_details)
        self.save_button.pack(pady=20)

    def update_time(self):
        now = datetime.datetime.now()
        self.current_time_label.config(text=f"Orario attuale: {now.strftime('%H:%M:%S %d/%m/%Y')}")
        self.root.after(1000, self.update_time)  # Aggiorna ogni secondo

    def add_note(self):
        note = self.note_text.get("1.0", tk.END).strip()
        if note:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            formatted_note = f"{timestamp}: {note}\n"
            self.note_text.insert(tk.END, formatted_note)
            self.note_text.delete("1.0", tk.END)  # Cancella il campo nota

    def add_crew(self):
        crew_member = simpledialog.askstring("Aggiungi Crew", "Nome membro della crew:")
        if crew_member:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S %d/%m/%Y')
            formatted_crew = f"{timestamp}: {crew_member} (Attivo)\n"
            self.service_people_text.insert(tk.END, formatted_crew)

    def record_audio(self):
        filename = f"recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        record_audio(filename)

    def toggle_energy(self):
        # Cambia lo stato dell'energia
        if self.energy_status.get() == "OFF":
            self.energy_status.set("ON")
            self.energy_button.config(text="Energy ON", bg="green")
        else:
            self.energy_status.set("OFF")
            self.energy_button.config(text="Energy OFF", bg="red")

    def save_details(self):
        # Funzione per salvare i dettagli in un file
        location = self.location_var.get()
        notes = self.note_text.get("1.0", tk.END).strip()
        service_people = self.service_people_text.get("1.0", tk.END).strip()
        
        # Nome del file basato sul luogo
        file_name = f"{location.replace(' ', '_')}_details.txt"
        
        with open(file_name, 'w') as file:
            file.write(f"NOTE:\n{notes}\n\n")
            file.write(f"PERSONE IN SERVIZIO:\n{service_people}\n\n")
            file.write(f"STATO ENERGIA: {self.energy_status.get()}\n")
        
        messagebox.showinfo("Salvato", f"Dati salvati in {file_name}")

# Esegui l'app
if __name__ == "__main__":
    root = tk.Tk()
    app = UrbexLandsApp(root)
    root.mainloop()
