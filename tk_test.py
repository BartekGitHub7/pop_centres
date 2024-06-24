import tkinter as tk
from tkinter import *
import tkintermapview
from bs4 import BeautifulSoup
import requests


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
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=800, height=600, corner_radius=0)
        self.map_widget.grid(row=0, column=0, padx=10, pady=10, sticky=N + S + E + W)

    def refresh_centre_list(self):
        self.listbox_centres.delete(0, END)
        for centre in self.centres:
            self.listbox_centres.insert(END, centre["name"])

    def display_all_markers(self):
        self.map_widget.set_position(52.237049, 21.017532)  # Default position over Poland
        self.map_widget.set_zoom(6)

        locations = {
            "Warszawa": (52.237049, 21.017532),
            "Poznań": (52.406374, 16.9251681),
            "Gdańsk": (54.3520252, 18.6466384),
            "Kraków": (50.0646501, 19.9449799),
            "Lublin": (51.2464536, 22.5684463),
        }

        for centre in self.centres:
            location = centre["location"]
            if location in locations:
                lat, lon = locations[location]
                marker = self.map_widget.set_marker(lat, lon, text=centre["name"])
                self.markers[centre["name"]] = marker

    def update_map_markers(self):
        for markers in self.markers.values():
            markers.delete()
        self.markers.clear()

        if self.selected_centre:
            coordinates = self.get_coordinates_from_wikipedia(self.selected_centre['name'])
            if coordinates:
                lat, lon = coordinates
                marker_text = self.selected_centre["name"]
                marker = self.map_widget.set_marker(lat, lon, text=marker_text)
                self.markers[self.selected_centre["name"]] = marker

    def show_centre_details(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            index = selected_index[0]
            self.selected_centre = self.centres[index]

            self.entry_name.delete(0, END)
            self.entry_name.insert(0, self.selected_centre["name"])
            self.entry_location.delete(0, END)
            self.entry_location.insert(0, self.selected_centre["location"])

            self.listbox_clients.delete(0, END)
            for client in self.selected_centre["clients"]:
                self.listbox_clients.insert(END, client["name"])

            self.listbox_employees.delete(0, END)
            for employee in self.selected_centre["employees"]:
                self.listbox_employees.insert(END, employee["name"])

            self.listbox_reservation.delete(0, END)

            # Show single centre marker
            self.display_single_marker(self.selected_centre["location"])
            self.update_map_markers()

    def display_single_marker(self, location):
        self.map_widget.set_position(52.237049, 21.017532)  # Default position over Poland
        self.map_widget.set_zoom(6)

        locations = {
            "Warszawa": (52.237049, 21.017532),
            "Poznań": (52.406374, 16.9251681),
            "Gdańsk": (54.3520252, 18.6466384),
            "Kraków": (50.0646501, 19.9449799),
            "Lublin": (51.2464536, 22.5684463),
        }

        # Clear all existing markers
        self.map_widget.delete_all_marker()

        if location in locations:
            lat, lon = locations[location]
            self.map_widget.set_marker(lat, lon, text=location)
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(10)

    def add_centre(self):
        name = self.entry_name.get()
        location = self.entry_location.get()
        if name and location:
            new_centre = {"name": name, "location": location, "clients": [], "employees": []}
            self.centres.append(new_centre)
            self.refresh_centre_list()

    def remove_centre(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            index = selected_index[0]
            del self.centres[index]
            self.refresh_centre_list()

    def update_centre(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            index = selected_index[0]
            name = self.entry_name.get()
            location = self.entry_location.get()
            if name and location:
                self.centres[index]["name"] = name
                self.centres[index]["location"] = location
                self.refresh_centre_list()

    def add_client(self):
        name = self.entry_client_name.get()
        if name and self.selected_centre:
            new_client = {"name": name, "reservation": []}
            self.selected_centre["clients"].append(new_client)
            self.listbox_clients.insert(END, name)

    def remove_client(self):
        selected_index = self.listbox_clients.curselection()
        if selected_index and self.selected_centre:
            index = selected_index[0]
            del self.selected_centre["clients"][index]
            self.listbox_clients.delete(index)

    def update_client(self):
        selected_index = self.listbox_clients.curselection()
        if selected_index and self.selected_centre:
            index = selected_index[0]
            name = self.entry_client_name.get()
            if name:
                self.selected_centre["clients"][index]["name"] = name
                self.listbox_clients.delete(index)
                self.listbox_clients.insert(index, name)



    def show_reservations(self):
        selected_client_index = self.listbox_clients.curselection()
        if selected_client_index and self.selected_centre:
            client_index = selected_client_index[0]
            self.selected_client = self.selected_centre["clients"][client_index]

            self.listbox_reservation.delete(0, END)
            for reservation in self.selected_client["reservation"]:
                self.listbox_reservation.insert(END, reservation)

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
                        break
                self.show_centre_details()

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
                        break
                self.show_centre_details()

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
                            client["reservation"][
                                client["reservation"].index(old_reservation_name)] = new_reservation_name
                        break
                self.show_centre_details()

    def add_employee(self):
        name = self.entry_employee_name.get()
        if name and self.selected_centre:
            new_employee = {"name": name}
            self.selected_centre["employees"].append(new_employee)
            self.listbox_employees.insert(END, name)

    def remove_employee(self):
        selected_index = self.listbox_employees.curselection()
        if selected_index and self.selected_centre:
            index = selected_index[0]
            del self.selected_centre["employees"][index]
            self.listbox_employees.delete(index)

    def update_employee(self):
        selected_index = self.listbox_employees.curselection()
        if selected_index and self.selected_centre:
            index = selected_index[0]
            name = self.entry_employee_name.get()
            if name:
                self.selected_centre["employees"][index]["name"] = name
                self.listbox_employees.delete(index)
                self.listbox_employees.insert(index, name)

    def get_coordinates_from_wikipedia(self, location):
        try:
            url = f"https://pl.wikipedia.org/wiki/{location}"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            coordinates = soup.find("span", {"class": "geo"})
            if coordinates:
                latitude = float(coordinates[0]['lat'])
                longtitude = float(coordinates[0]['lon'])
                return latitude, longtitude
            return None
        except Exception as e:
            print('Błąd podczas pobierania kordynatów:', e)
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