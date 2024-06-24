import tkinter as tk
from tkinter import *
from tkinter import messagebox
import tkintermapview

# Simple hardcoded user credentials
USER_CREDENTIALS = {
    "admin": "2137"
}

centres = [
    {"name": "Centrum Konferencyjne w Warszawie", "location": "Warszawa", "clients": [{"name": "Mariusz Pudzianowski",
                                                                                       "reservation": [
                                                                                           "Centrum Konferencyjne w Warszawie",
                                                                                           "Centrum Konferencyjne w Poznaniu"]},
                                                                                      {"name": "Władysław Łokietek",
                                                                                       "reservation": [
                                                                                           "Centrum Konferencyjne w Warszawie",
                                                                                           "Centrum Konferencyjne w Gdańsku"]}],
     "employees": [{"name": "Anna Nowak"}, {"name": "Piotr Kowalski"}]},
    {"name": "Centrum Konferencyjne w Poznaniu", "location": "Poznań", "clients": [{"name": "Mariusz Pudzianowski",
                                                                                    "reservation": [
                                                                                        "Centrum Konferencyjne w Warszawie",
                                                                                        "Centrum Konferencyjne w Poznaniu"]},
                                                                                   {"name": "Adam Nowak",
                                                                                    "reservation": [
                                                                                        "Centrum Konferencyjne w Poznaniu",
                                                                                        "Centrum Konferencyjne w Krakowie"]}],
     "employees": [{"name": "Klaudia Mickiewicz"}, {"name": "Krzysztof Wiśniewski"}]},
    {"name": "Centrum Konferencyjne w Gdańsku", "location": "Gdańsk", "clients": [{"name": "Jan Kowalski",
                                                                                   "reservation": [
                                                                                       "Centrum Konferencyjne w Lublinie",
                                                                                       "Centrum Konferencyjne w Gdańsku"]},
                                                                                  {"name": "Władysław Łokietek",
                                                                                   "reservation": [
                                                                                       "Centrum Konferencyjne w Warszawie",
                                                                                       "Centrum Konferencyjne w Gdańsku"]}],
     "employees": [{"name": "Marta Kwiatkowska"}, {"name": "Tomasz Jankowski"}]},
    {"name": "Centrum Konferencyjne w Krakowie", "location": "Kraków", "clients": [
        {"name": "Adam Nowak", "reservation": ["Centrum Konferencyjne w Krakowie", "Centrum Konferencyjne w Poznaniu"]},
        {"name": "Ferdynand Kiepski",
         "reservation": ["Centrum Konferencyjne w Krakowie", "Centrum Konferencyjne w Lublinie"]}],
     "employees": [{"name": "Julia Wiśniewska"}, {"name": "Michał Kamiński"}]},
    {"name": "Centrum Konferencyjne w Lublinie", "location": "Lublin", "clients": [{"name": "Jan Kowalski",
                                                                                    "reservation": [
                                                                                        "Centrum Konferencyjne w Lublinie",
                                                                                        "Centrum Konferencyjne w Gdańsku"]},
                                                                                   {"name": "Ferdynand Kiepski",
                                                                                    "reservation": [
                                                                                        "Centrum Konferencyjne w Lublinie",
                                                                                        "Centrum Konferencyjne w Krakowie"]}],
     "employees": [{"name": "Agnieszka Wojciechowska"}, {"name": "Adam Woźniak"}]},
]


class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login")
        self.on_login_success = on_login_success

        self.frame_login = Frame(root, padx=10, pady=10)
        self.frame_login.pack()

        self.label_username = Label(self.frame_login, text='Username')
        self.entry_username = Entry(self.frame_login)
        self.label_password = Label(self.frame_login, text='Password')
        self.entry_password = Entry(self.frame_login, show='*')

        self.button_login = Button(self.frame_login, text='Login', command=self.login)

        self.label_username.grid(row=0, column=0, pady=5)
        self.entry_username.grid(row=0, column=1, pady=5)
        self.label_password.grid(row=1, column=0, pady=5)
        self.entry_password.grid(row=1, column=1, pady=5)
        self.button_login.grid(row=2, columnspan=2, pady=5)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            self.on_login_success()
        else:
            self.label_error = Label(self.frame_login, text='Invalid username or password', fg='red')
            self.label_error.grid(row=3, columnspan=2, pady=5)


class CentreManager:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')  # Fullscreen
        self.root.title("Centre Manager")

        self.centres = centres
        self.markers = {}

        # Frames
        self.frame_list = Frame(root, width=300, height=800, padx=10, pady=10)
        self.frame_details = Frame(root, width=700, height=800, padx=10, pady=10)
        self.frame_map = Frame(root, width=800, height=800, padx=10, pady=10)

        self.frame_list.grid(row=0, column=0, padx=10, pady=10, sticky=N + S)
        self.frame_details.grid(row=0, column=1, padx=10, pady=10, sticky=N + S)
        self.frame_map.grid(row=0, column=2, padx=10, pady=10, sticky=N + S + E + W)

        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Setup frames
        self.setup_list_frame()
        self.setup_details_frame()
        self.setup_map_frame()

        self.selected_centre = None
        self.selected_client = None

        # Display all centre markers at startup
        self.display_all_markers()

    def setup_list_frame(self):
        self.label_list = Label(self.frame_list, text='Lista Centrów Konferencyjnych')
        self.listbox_centres = Listbox(self.frame_list, width=40, height=25)
        self.button_show_details = Button(self.frame_list, text='Pokaż szczegóły', command=self.show_centre_details)
        self.button_add_centre = Button(self.frame_list, text='Dodaj centrum', command=self.add_centre)
        self.button_remove_centre = Button(self.frame_list, text='Usuń centrum', command=self.remove_centre)
        self.button_update_centre = Button(self.frame_list, text='Edytuj centrum', command=self.update_centre)

        self.label_list.pack(pady=5)
        self.listbox_centres.pack(pady=5)
        self.button_show_details.pack(side=LEFT, padx=5)
        self.button_add_centre.pack(side=LEFT, padx=5)
        self.button_remove_centre.pack(side=LEFT, padx=5)
        self.button_update_centre.pack(side=LEFT, padx=5)

        self.refresh_centre_list()

    def setup_details_frame(self):
        self.label_details = Label(self.frame_details, text='Szczegóły centrum')
        self.label_name = Label(self.frame_details, text='Nazwa centrum')
        self.entry_name = Entry(self.frame_details, width=50)
        self.label_location = Label(self.frame_details, text='Lokalizacja centrum')
        self.entry_location = Entry(self.frame_details, width=50)
        self.label_clients = Label(self.frame_details, text='Klienci')
        self.listbox_clients = Listbox(self.frame_details, width=30, height=10)
        self.label_employees = Label(self.frame_details, text='Pracownicy')
        self.listbox_employees = Listbox(self.frame_details, width=30, height=10)
        self.label_reservation = Label(self.frame_details, text='Rezerwacje')
        self.listbox_reservation = Listbox(self.frame_details, width=30, height=10)

        self.entry_client_name = Entry(self.frame_details, width=30)
        self.entry_employee_name = Entry(self.frame_details, width=30)
        self.entry_reservation_name = Entry(self.frame_details, width=30)

        self.button_add_client = Button(self.frame_details, text='Dodaj klienta', command=self.add_client)
        self.button_remove_client = Button(self.frame_details, text='    Usuń klienta    ', command=self.remove_client)
        self.button_update_client = Button(self.frame_details, text='Edytuj klienta', command=self.update_client)
        self.button_add_employee = Button(self.frame_details, text='Dodaj prac.', command=self.add_employee)
        self.button_remove_employee = Button(self.frame_details, text='Usuń prac.',
                                             command=self.remove_employee)
        self.button_update_employee = Button(self.frame_details, text='Edytuj pracownika',
                                             command=self.update_employee)
        self.button_add_reservation = Button(self.frame_details, text='Dodaj rezerwację', command=self.add_reservation)
        self.button_remove_reservation = Button(self.frame_details, text='Usuń rezerwację',
                                                command=self.remove_reservation)
        self.button_update_reservation = Button(self.frame_details, text='Edytuj rezerwację',
                                                command=self.update_reservation)
        self.button_show_reservations = Button(self.frame_details, text='Pokaż rezerwacje',
                                               command=self.show_reservations)

        self.label_details.grid(row=0, column=0, pady=5)
        self.label_name.grid(row=1, column=0, pady=5)
        self.entry_name.grid(row=1, column=1, pady=5)
        self.label_location.grid(row=2, column=0, pady=5)
        self.entry_location.grid(row=2, column=1, pady=5)
        self.label_clients.grid(row=3, column=0, pady=5)
        self.listbox_clients.grid(row=5, column=0, pady=5)
        self.label_employees.grid(row=3, column=1, pady=5)
        self.listbox_employees.grid(row=5, column=1, pady=5)
        self.label_reservation.grid(row=10, column=0, pady=5)
        self.listbox_reservation.grid(row=11, column=0, pady=5)

        self.entry_client_name.grid(row=6, column=0, pady=5)
        self.entry_employee_name.grid(row=6, column=1, pady=5)
        self.entry_reservation_name.grid(row=12, column=0, pady=5)

        self.button_add_client.grid(row=7, column=0, pady=5, sticky=W)
        self.button_remove_client.grid(row=7, column=0, pady=5)
        self.button_update_client.grid(row=8, column=0, pady=5, sticky=W)
        self.button_add_employee.grid(row=7, column=1, pady=5)
        self.button_remove_employee.grid(row=7, column=1, pady=5, sticky=E)
        self.button_update_employee.grid(row=8, column=1, pady=5)
        self.button_add_reservation.grid(row=13, column=0, pady=5, padx=5, sticky=W)
        self.button_remove_reservation.grid(row=13, column=0, pady=5, padx=5, sticky=E)
        self.button_update_reservation.grid(row=14, column=0, pady=5)
        self.button_show_reservations.grid(row=8, column=0, pady=5, sticky=E)

    def setup_map_frame(self):
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=800, height=800, corner_radius=0)
        self.map_widget.pack(pady=10, padx=10)
        self.map_widget.set_position(52.2297, 19.0122)  # Central Poland
        self.map_widget.set_zoom(6)

    def refresh_centre_list(self):
        self.listbox_centres.delete(0, END)
        for centre in self.centres:
            self.listbox_centres.insert(END, centre["name"])

    def show_centre_details(self):
        try:
            index = self.listbox_centres.curselection()[0]
            self.selected_centre = self.centres[index]
            self.entry_name.delete(0, END)
            self.entry_name.insert(END, self.selected_centre["name"])
            self.entry_location.delete(0, END)
            self.entry_location.insert(END, self.selected_centre["location"])

            self.listbox_clients.delete(0, END)
            for client in self.selected_centre["clients"]:
                self.listbox_clients.insert(END, client["name"])

            self.listbox_employees.delete(0, END)
            for employee in self.selected_centre["employees"]:
                self.listbox_employees.insert(END, employee["name"])

            self.display_centre_marker()
        except IndexError:
            messagebox.showerror("Błąd", "Nie wybrano centrum!")

    def add_centre(self):
        name = self.entry_name.get()
        location = self.entry_location.get()
        if name and location:
            self.centres.append({"name": name, "location": location, "clients": [], "employees": []})
            self.refresh_centre_list()
            self.display_all_markers()
        else:
            messagebox.showerror("Błąd", "Proszę podać nazwę i lokalizację centrum!")

    def remove_centre(self):
        try:
            index = self.listbox_centres.curselection()[0]
            self.centres.pop(index)
            self.refresh_centre_list()
            self.map_widget.delete_all_marker()
            self.display_all_markers()
        except IndexError:
            messagebox.showerror("Błąd", "Nie wybrano centrum!")

    def update_centre(self):
        try:
            index = self.listbox_centres.curselection()[0]
            name = self.entry_name.get()
            location = self.entry_location.get()
            if name and location:
                self.centres[index]["name"] = name
                self.centres[index]["location"] = location
                self.refresh_centre_list()
                self.display_all_markers()
            else:
                messagebox.showerror("Błąd", "Proszę podać nazwę i lokalizację centrum!")
        except IndexError:
            messagebox.showerror("Błąd", "Nie wybrano centrum!")

    def add_client(self):
        client_name = self.entry_client_name.get()
        if client_name and self.selected_centre:
            self.selected_centre["clients"].append({"name": client_name, "reservation": []})
            self.show_centre_details()
        else:
            messagebox.showerror("Błąd", "Proszę podać nazwę klienta!")

    def remove_client(self):
        try:
            index = self.listbox_clients.curselection()[0]
            self.selected_centre["clients"].pop(index)
            self.show_centre_details()
        except IndexError:
            messagebox.showerror("Błąd", "Nie wybrano klienta!")

    def update_client(self):
        try:
            index = self.listbox_clients.curselection()[0]
            client_name = self.entry_client_name.get()
            if client_name:
                self.selected_centre["clients"][index]["name"] = client_name
                self.show_centre_details()
            else:
                messagebox.showerror("Błąd", "Proszę podać nazwę klienta!")
        except IndexError:
            messagebox.showerror("Błąd", "Nie wybrano klienta!")

    def add_employee(self):
        employee_name = self.entry_employee_name.get()
        if employee_name and self.selected_centre:
            self.selected_centre["employees"].append({"name": employee_name})
            self.show_centre_details()
        else:
            messagebox.showerror("Błąd", "Proszę podać nazwę pracownika!")

    def remove_employee(self):
        try:
            index = self.listbox_employees.curselection()[0]
            self.selected_centre["employees"].pop(index)
            self.show_centre_details()
        except IndexError:
            messagebox.showerror("Błąd", "Nie wybrano pracownika!")

    def update_employee(self):
        try:
            index = self.listbox_employees.curselection()[0]
            employee_name = self.entry_employee_name.get()
            if employee_name:
                self.selected_centre["employees"][index]["name"] = employee_name
                self.show_centre_details()
            else:
                messagebox.showerror("Błąd", "Proszę podać nazwę pracownika!")
        except IndexError:
            messagebox.showerror("Błąd", "Nie wybrano pracownika!")

    def add_reservation(self):
        if self.selected_centre:
            selected = self.listbox_clients.curselection()
            if selected:
                client_name = self.listbox_clients.get(selected)
                for client in self.selected_centre["clients"]:
                    if client["name"] == client_name:
                        reservation_name = self.entry_reservation_name.get()
                        if reservation_name:
                            client["reservation"].append(reservation_name)
                        else:
                            messagebox.showwarning("Warning", "Nazwa rezerwacji nie może być pusta")
                        break
                self.show_centre_details()
            else:
                messagebox.showwarning("Warning", "Wybierz klienta, aby dodać rezerwację")

    def remove_reservation(self):
        if self.selected_centre:
            selected = self.listbox_clients.curselection()
            if selected:
                client_name = self.listbox_clients.get(selected)
                for client in self.selected_centre["clients"]:
                    if client["name"] == client_name:
                        reservation_name = self.entry_reservation_name.get()
                        if reservation_name in client["reservation"]:
                            client["reservation"].remove(reservation_name)
                        else:
                            messagebox.showwarning("Warning", "Podana rezerwacja nie istnieje")
                        break
                self.show_centre_details()
            else:
                messagebox.showwarning("Warning", "Wybierz klienta, aby usunąć rezerwację")

    def update_reservation(self):
        if self.selected_centre:
            selected = self.listbox_clients.curselection()
            if selected:
                client_name = self.listbox_clients.get(selected)
                for client in self.selected_centre["clients"]:
                    if client["name"] == client_name:
                        old_reservation_name = self.entry_reservation_name.get()
                        new_reservation_name = self.entry_reservation_name.get()
                        if old_reservation_name in client["reservation"]:
                            client["reservation"][client["reservation"].index(old_reservation_name)] = new_reservation_name
                        else:
                            messagebox.showwarning("Warning", "Podana rezerwacja nie istnieje")
                        break
                self.show_centre_details()
            else:
                messagebox.showwarning("Warning", "Wybierz klienta, aby edytować rezerwację")

    def show_reservations(self):
        if self.selected_centre:
            selected = self.listbox_clients.curselection()
            if selected:
                client_name = self.listbox_clients.get(selected)
                for client in self.selected_centre["clients"]:
                    if client["name"] == client_name:
                        reservations = client["reservation"]
                        self.listbox_reservation.insert(END, client["reservation"])
                        break


    def ensure_client_in_centre(self, centre_name):
        for centre in self.centres:
            if centre['name'] == centre_name:
                if self.selected_client and self.selected_client not in centre['clients']:
                    centre['clients'].append(self.selected_client)

    def ensure_client_not_in_centre(self, centre_name):
        for centre in self.centres:
            if centre['name'] == centre_name and self.selected_client:
                client_has_reservation = False
                for client in centre['clients']:
                    if centre_name in client['reservation']:
                        client_has_reservation = True
                        break
                if not client_has_reservation:
                    centre['clients'] = [client for client in centre['clients'] if client != self.selected_client]

    def display_centre_marker(self):
        if self.selected_centre:
            location = self.selected_centre["location"]
            if location not in self.markers:
                # For demonstration purposes, using static lat-long for known locations
                if location == "Warszawa":
                    lat, lon = 52.229675, 21.012230
                elif location == "Poznań":
                    lat, lon = 52.406374, 16.9251681
                elif location == "Gdańsk":
                    lat, lon = 54.352025, 18.6466384
                elif location == "Kraków":
                    lat, lon = 50.0646501, 19.9449799
                elif location == "Lublin":
                    lat, lon = 51.246454, 22.5684463
                else:
                    lat, lon = 52.229675, 21.012230  # Default to Warsaw if not found

                marker = self.map_widget.set_marker(lat, lon, text=self.selected_centre["name"])
                self.markers[location] = marker
            else:
                self.markers[location].set_text(self.selected_centre["name"])


    def display_all_markers(self):
        self.map_widget.delete_all_marker()
        self.markers = {}
        for centre in self.centres:
            location = centre["location"]
            if location == "Warszawa":
                lat, lon = 52.229675, 21.012230
            elif location == "Poznań":
                lat, lon = 52.406374, 16.9251681
            elif location == "Gdańsk":
                lat, lon = 54.352025, 18.6466384
            elif location == "Kraków":
                lat, lon = 50.0646501, 19.9449799
            elif location == "Lublin":
                lat, lon = 51.246454, 22.5684463
            else:
                lat, lon = 52.229675, 21.012230  # Default to Warsaw if not found

            marker = self.map_widget.set_marker(lat, lon, text=centre["name"])
            self.markers[location] = marker

def main():
    root = Tk()

    def on_login_success():
        login_window.frame_login.pack_forget()
        CentreManager(root)

    login_window = LoginWindow(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
