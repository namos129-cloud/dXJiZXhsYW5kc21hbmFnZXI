import tkinter as tk
from tkinter import messagebox

# Credenziali di accesso (username e password)
USERNAME = "admin"
PASSWORD = "password123"

# Funzione di autenticazione
def authenticate(user, pwd):
    return user == USERNAME and pwd == PASSWORD

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
        # Distruggi la finestra di login e apri la dashboard
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

        self.locations = ["Teatro Mediterraneo", "Area Militare abbandonata", "Fabbrica abbandonata 2", 
                          "Fabbrica abbandonata 1", "Palazzo Trifletti", "Pizzeria Central Park (CEP)", "Altre aree"]
        
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
        # Puoi aprire una nuova finestra per la gestione del luogo scelto

# Esegui l'app
if __name__ == "__main__":
    root = tk.Tk()
    app = UrbexLandsApp(root)
    root.mainloop()
