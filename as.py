import tkinter as tk
from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

# Proste twardo zakodowane dane logowania użytkowników
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
        self.root.state('zoomed')  # Pełny ekran
        self.root.title("Centre Manager")

        self.centres = centres
        self.markers = {}

        # Ramki
        self.frame_list = Frame(root, width=300, height=800, padx=10, pady=10)
        self.frame_details = Frame(root, width=700, height=800, padx=10, pady=10)
        self.frame_map = Frame(root, width=800, height=800, padx=10, pady=10)

        self.frame_list.grid(row=0, column=0, sticky="ns")
        self.frame_details.grid(row=0, column=1, sticky="ns")
        self.frame_map.grid(row=0, column=2, sticky="ns")

        # Lista centrów
        self.label_centre = Label(self.frame_list, text='Centres')
        self.listbox_centre = Listbox(self.frame_list)
        self.button_show_clients = Button(self.frame_list, text="Show Clients", command=self.show_clients)
        self.button_show_employees = Button(self.frame_list, text="Show Employees", command=self.show_employees)

        self.label_centre.pack()
        self.listbox_centre.pack(fill="y")
        self.button_show_clients.pack(pady=5)
        self.button_show_employees.pack(pady=5)

        for centre in self.centres:
            self.listbox_centre.insert(END, centre["name"])

        # Szczegóły centrów
        self.label_details = Label(self.frame_details, text='Details')
        self.label_details.pack()

        self.listbox_details = Listbox(self.frame_details)
        self.listbox_details.pack(fill="y")

        self.label_clients = Label(self.frame_details, text='Clients')
        self.label_employees = Label(self.frame_details, text='Employees')

        self.listbox_clients = Listbox(self.frame_details)
        self.listbox_clients.pack(fill="y")

        self.listbox_reservations = Listbox(self.frame_details)
        self.listbox_reservations.pack(fill="y")

        self.entry_reservation_name = Entry(self.frame_details)
        self.entry_reservation_name.pack(pady=5)

        self.button_add_reservation = Button(self.frame_details, text="Add Reservation", command=self.add_reservation)
        self.button_add_reservation.pack(pady=5)

        self.button_show_reservations = Button(self.frame_details, text="Show Reservations",
                                               command=self.display_client_reservations)
        self.button_show_reservations.pack(pady=5)

        # Mapa
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=800, height=600, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_position(52.237049, 21.017532)  # Warszawa

        self.selected_centre = None
        self.selected_client = None

    def show_clients(self):
        selected_index = self.listbox_centre.curselection()
        if selected_index:
            selected_index = selected_index[0]
            self.selected_centre = self.centres[selected_index]
            self.label_clients.pack()
            self.listbox_clients.pack()
            self.listbox_clients.delete(0, END)
            for client in self.selected_centre["clients"]:
                self.listbox_clients.insert(END, client["name"])

    def show_employees(self):
        selected_index = self.listbox_centre.curselection()
        if selected_index:
            selected_index = selected_index[0]
            self.selected_centre = self.centres[selected_index]
            self.label_employees.pack()
            self.listbox_clients.pack()
            self.listbox_clients.delete(0, END)
            for employee in self.selected_centre["employees"]:
                self.listbox_clients.insert(END, employee["name"])

    def refresh_reservation_list(self):
        self.listbox_reservations.delete(0, END)
        if self.selected_client:
            for reservation in self.selected_client["reservation"]:
                self.listbox_reservations.insert(END, reservation["name"])

    def add_reservation(self):
        reservation_name = self.entry_reservation_name.get()
        selected_client_index = self.listbox_clients.curselection()
        if selected_client_index and reservation_name:
            selected_client_index = selected_client_index[0]
            coordinates = self.get_coordinates_from_wikipedia(reservation_name)
            if coordinates:
                lat, lon = coordinates
                reservation = {"name": reservation_name, "latitude": lat, "longitude": lon}
                self.selected_centre["clients"][selected_client_index]["reservation"].append(reservation)
                self.selected_client = self.selected_centre["clients"][selected_client_index]
                self.refresh_reservation_list()

    def display_client_reservations(self):
        selected_client_index = self.listbox_clients.curselection()
        if selected_client_index:
            selected_client_index = selected_client_index[0]
            client = self.selected_centre["clients"][selected_client_index]
            reservations = client["reservation"]
            # Usuń istniejące markery (jeśli są)
            for marker in self.markers.values():
                self.map_widget.remove_marker(marker)
            self.markers.clear()
            # Dodaj markery dla każdej rezerwacji
            for reservation in reservations:
                lat = reservation.get("latitude")
                lon = reservation.get("longitude")
                if lat and lon:
                    marker = self.map_widget.set_marker(float(lat), float(lon), text=reservation["name"])
                    self.markers[reservation["name"]] = marker

    def get_coordinates_from_wikipedia(self, location):
        url = f"https://pl.wikipedia.org/wiki/{location}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        coordinates = soup.find("span", {"class": "geo"})
        if coordinates:
            lat, lon = coordinates.text.split("; ")
            return lat.strip(), lon.strip()
        return None


def main():
    root = Tk()

    def on_login_success():
        login_window.frame_login.pack_forget()
        CentreManager(root)

    login_window = LoginWindow(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()