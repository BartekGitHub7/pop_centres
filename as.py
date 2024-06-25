from tkinter import *
import tkintermapview
from geopy.geocoders import Nominatim

USER_CREDENTIALS = {
    "admin": "2137"
}

centres = [
    {"name": "Centrum Konferencyjne w Warszawie", "location": "Warszawa", "clients": [{"name": "Mariusz Pudzianowski",
                                                               "reservation": ["Centrum Konferencyjne w Warszawie",
                                                                               "Centrum Konferencyjne w Poznaniu"]},
                                                              {"name": "Władysław Łokietek",
                                                               "reservation": ["Centrum Konferencyjne w Warszawie",
                                                                               "Centrum Konferencyjne w Gdańsku"]}],
     "employees": [{"name": "Anna Nowak"}, {"name": "Piotr Kowalski"}]},
    {"name": "Centrum Konferencyjne w Poznaniu", "location": "Poznań", "clients": [{"name": "Mariusz Pudzianowski",
                                                              "reservation": ["Centrum Konferencyjne w Warszawie",
                                                                              "Centrum Konferencyjne w Poznaniu"]},
                                                             {"name": "Adam Nowak",
                                                              "reservation": ["Centrum Konferencyjne w Poznaniu",
                                                                              "Centrum Konferencyjne w Krakowie"]}],
     "employees": [{"name": "Klaudia Mickiewicz"}, {"name": "Krzysztof Wiśniewski"}]},
    {"name": "Centrum Konferencyjne w Gdańsku", "location": "Gdańsk", "clients": [{"name": "Jan Kowalski",
                                                             "reservation": ["Centrum Konferencyjne w Lublinie",
                                                                             "Centrum Konferencyjne w Gdańsku"]},
                                                            {"name": "Władysław Łokietek",
                                                             "reservation": ["Centrum Konferencyjne w Warszawie",
                                                                             "Centrum Konferencyjne w Gdańsku"]}],
     "employees": [{"name": "Marta Kwiatkowska"}, {"name": "Tomasz Jankowski"}]},
    {"name": "Centrum Konferencyjne w Krakowie", "location": "Kraków", "clients": [
        {"name": "Adam Nowak", "reservation": ["Centrum Konferencyjne w Krakowie", "Centrum Konferencyjne w Poznaniu"]},
        {"name": "Ferdynand Kiepski",
         "reservation": ["Centrum Konferencyjne w Krakowie", "Centrum Konferencyjne w Lublinie"]}],
     "employees": [{"name": "Julia Wiśniewska"}, {"name": "Michał Kamiński"}]},
    {"name": "Centrum Konferencyjne w Lublinie", "location": "Lublin", "clients": [{"name": "Jan Kowalski",
                                                              "reservation": ["Centrum Konferencyjne w Lublinie",
                                                                              "Centrum Konferencyjne w Gdańsku"]},
                                                             {"name": "Ferdynand Kiepski",
                                                              "reservation": ["Centrum Konferencyjne w Lublinie",
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
        self.geolocator = Nominatim(user_agent="centre_manager")

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

        self.show_all_centres_on_map()

    def setup_list_frame(self):
        self.label_list = Label(self.frame_list, text='Lista Centrów Konferencyjnych')
        self.listbox_centres = Listbox(self.frame_list, width=40, height=25)
        self.button_show_details = Button(self.frame_list, text='Pokaż szczegóły', command=self.show_centre_details)
        self.button_show_reservations = Button(self.frame_list, text='Pokaż rezerwacje',
                                               command=self.show_reservation_centres)
        self.button_add_centre = Button(self.frame_list, text='Dodaj centrum', command=self.add_centre)
        self.button_remove_centre = Button(self.frame_list, text='Usuń centrum', command=self.remove_centre)
        self.button_update_centre = Button(self.frame_list, text='Edytuj centrum', command=self.update_centre)
        self.button_show_all_centres = Button(self.frame_list, text='Pokaż wszystkie centra', command=self.show_all_centres_on_map)

        self.label_list.pack(pady=5)
        self.listbox_centres.pack(pady=5)
        self.button_show_all_centres.pack(pady=5)
        self.button_show_details.pack(side=LEFT, padx=5)
        self.button_show_reservations.pack(side=LEFT, padx=5)
        self.button_add_centre.pack(side=LEFT, padx=5)
        self.button_remove_centre.pack(side=LEFT, padx=5)
        self.button_update_centre.pack(side=LEFT, padx=5)


        self.refresh_centre_list()

    def setup_details_frame(self):
        self.label_details = Label(self.frame_details, text='Szczegóły centrum')
        self.label_name = Label(self.frame_details, text='Nazwa centrum')
        self.entry_name = Entry(self.frame_details, width=40)
        self.label_location = Label(self.frame_details, text='Miejscowość')
        self.entry_location = Entry(self.frame_details, width=40)
        self.label_clients = Label(self.frame_details, text='Klienci')
        self.listbox_clients = Listbox(self.frame_details, width=30, height=10)
        self.label_employees = Label(self.frame_details, text='Pracownicy')
        self.listbox_employees = Listbox(self.frame_details, width=30, height=10)
        self.label_reservations = Label(self.frame_details, text='Rezerwacje')
        self.listbox_reservations = Listbox(self.frame_details, width=30, height=10)

        self.entry_client_name = Entry(self.frame_details, width=30)
        self.entry_employee_name = Entry(self.frame_details, width=30)
        self.entry_reservation_name = Entry(self.frame_details, width=30)

        self.button_add_client = Button(self.frame_details, text='Dodaj klienta', command=self.add_client)
        self.button_remove_client = Button(self.frame_details, text='Usuń klienta', command=self.remove_client)
        self.button_edit_client = Button(self.frame_details, text='Edytuj klienta', command=self.edit_client)
        self.button_add_employee = Button(self.frame_details, text='Dodaj pracownika', command=self.add_employee)
        self.button_remove_employee = Button(self.frame_details, text='Usuń pracownika', command=self.remove_employee)
        self.button_edit_employee = Button(self.frame_details, text='Edytuj pracownika', command=self.edit_employee)
        self.button_add_reservation = Button(self.frame_details, text='Dodaj rezerwację', command=self.add_reservation)
        self.button_remove_reservation = Button(self.frame_details, text='Usuń rezerwację', command=self.remove_reservation)
        self.button_edit_reservation = Button(self.frame_details, text='Edytuj rezerwację', command=self.edit_reservation)



        self.label_details.grid(row=0, columnspan=2, pady=10)
        self.label_name.grid(row=1, column=0, sticky=W)
        self.entry_name.grid(row=1, column=1, columnspan=1, pady=5, sticky=W)
        self.label_location.grid(row=2, column=0, sticky=W)
        self.entry_location.grid(row=2, column=1, columnspan=1, pady=5, sticky=W)
        self.label_clients.grid(row=3, column=0, pady=5)
        self.listbox_clients.grid(row=4, column=0, pady=5)
        self.label_employees.grid(row=3, column=1, pady=5)
        self.listbox_employees.grid(row=4, column=1, pady=5)
        self.label_reservations.grid(row=9, column=0, pady=5)
        self.listbox_reservations.grid(row=10, column=0, pady=5)

        self.entry_client_name.grid(row=5, column=0, pady=5)
        self.entry_employee_name.grid(row=5, column=1, pady=5)
        self.entry_reservation_name.grid(row=11, column=0, pady=5)

        self.button_add_client.grid(row=6, column=0, pady=5)
        self.button_remove_client.grid(row=7, column=0, pady=5)
        self.button_edit_client.grid(row=8, column=0, pady=5)
        self.button_add_employee.grid(row=6, column=1, pady=5)
        self.button_remove_employee.grid(row=7, column=1, pady=5)
        self.button_edit_employee.grid(row=8, column=1, pady=5)
        self.button_add_reservation.grid(row=12, column=0, pady=5, sticky=W)
        self.button_remove_reservation.grid(row=12, column=0, pady=5, sticky=E)
        self.button_edit_reservation.grid(row=13, column=0, pady=5)



    def setup_map_frame(self):
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=800, height=800, corner_radius=0)
        self.map_widget.pack(fill=BOTH, expand=True)

    def refresh_centre_list(self):
        self.listbox_centres.delete(0, END)
        for centre in self.centres:
            self.listbox_centres.insert(END, centre['name'])

    def show_centre_details(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            centre = self.centres[selected_index[0]]
            self.entry_name.delete(0, END)
            self.entry_name.insert(0, centre['name'])
            self.entry_location.delete(0, END)
            self.entry_location.insert(0, centre['location'])
            self.listbox_clients.delete(0, END)
            for client in centre['clients']:
                self.listbox_clients.insert(END, client['name'])
            self.listbox_employees.delete(0, END)
            for employee in centre['employees']:
                self.listbox_employees.insert(END, employee['name'])
            self.selected_centre = centre

            self.show_selected_centre_on_map()

    def show_selected_centre_on_map(self):
        self.map_widget.set_zoom(6)  # Center map on Poland with zoom 6
        self.map_widget.set_position(52.2297, 19.0122)
        self.map_widget.delete_all_marker()

        location = self.geolocator.geocode(self.selected_centre['location'])
        if location:
            self.map_widget.set_position(location.latitude, location.longitude)
            self.map_widget.set_marker(location.latitude, location.longitude, text=self.selected_centre['name'])

    def show_reservation_centres(self):
        selected_client_index = self.listbox_clients.curselection()
        if selected_client_index:
            selected_client_name = self.listbox_clients.get(selected_client_index)
            self.listbox_reservations.delete(0, END)
            for client in self.selected_centre['clients']:
                if client['name'] == selected_client_name:
                    self.selected_client = client
                    for reservation in client['reservation']:
                        self.listbox_reservations.insert(END, reservation)
                    break
            self.show_client_reservations_on_map()

    def add_centre(self):
        name = self.entry_name.get()
        location = self.entry_location.get()
        if name and location:
            self.centres.append({"name": name, "location": location, "clients": [], "employees": []})
            self.refresh_centre_list()

    def remove_centre(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            self.centres.pop(selected_index[0])
            self.refresh_centre_list()

    def update_centre(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            self.centres[selected_index[0]] = {"name": self.entry_name.get(), "location": self.entry_location.get(),
                                               "clients": self.selected_centre['clients'],
                                               "employees": self.selected_centre['employees']}
            self.refresh_centre_list()

    def add_client(self):
        if not self.selected_centre:
            return
        client_name = self.entry_client_name.get()
        if client_name:
            self.selected_centre['clients'].append({"name": client_name, "reservation": []})
            self.listbox_clients.insert(END, client_name)
            self.show_centre_details()

    def remove_client(self):
        selected_index = self.listbox_clients.curselection()
        if not selected_index:
            return
        del self.selected_centre['clients'][selected_index[0]]
        self.listbox_clients.delete(selected_index[0])
        self.show_centre_details()

    def edit_client(self):
        selected_index = self.listbox_clients.curselection()
        if not selected_index:
            return
        new_name = self.entry_client_name.get()
        if new_name:
            self.selected_centre['clients'][selected_index[0]]['name'] = new_name
            self.listbox_clients.delete(selected_index[0])
            self.listbox_clients.insert(selected_index[0], new_name)


    def add_employee(self):
        if not self.selected_centre:
            return
        employee_name = self.entry_employee_name.get()
        if employee_name:
            self.selected_centre['employees'].append({"name": employee_name})
            self.listbox_employees.insert(END, employee_name)
            self.show_centre_details()

    def remove_employee(self):
        selected_index = self.listbox_employees.curselection()
        if not selected_index:
            return
        del self.selected_centre['employees'][selected_index[0]]
        self.listbox_employees.delete(selected_index[0])
        self.show_centre_details()

    def edit_employee(self):
        selected_index = self.listbox_employees.curselection()
        if not selected_index:
            return
        new_name = self.entry_employee_name.get()
        if new_name:
            self.selected_centre['employees'][selected_index[0]]['name'] = new_name
            self.listbox_employees.delete(selected_index[0])
            self.listbox_employees.insert(selected_index[0], new_name)


    def add_reservation(self):
        if not self.selected_centre:
            return
        reservation_name = self.entry_reservation_name.get()
        if reservation_name:
            selected_client_index = self.listbox_clients.curselection()
            if selected_client_index:
                self.selected_centre['clients'][selected_client_index[0]]['reservation'].append(reservation_name)
                self.listbox_reservations.insert(END, reservation_name)
            self.show_reservation_centres()

    def remove_reservation(self):
        selected_client_index = self.listbox_clients.curselection()
        selected_reservation_index = self.listbox_reservations.curselection()
        if not selected_client_index or not selected_reservation_index:
            return
        del self.selected_centre['clients'][selected_client_index[0]]['reservation'][selected_reservation_index[0]]
        self.listbox_reservations.delete(selected_reservation_index[0])
        self.show_reservation_centres()

    def edit_reservation(self):
        selected_client_index = self.listbox_clients.curselection()
        selected_reservation_index = self.listbox_reservations.curselection()
        if not selected_client_index or not selected_reservation_index:
            return
        new_reservation_name = self.entry_reservation_name.get()
        if new_reservation_name:
            self.selected_centre['clients'][selected_client_index[0]]['reservation'][selected_reservation_index[0]] = new_reservation_name
            self.listbox_reservations.delete(selected_reservation_index[0])
            self.listbox_reservations.insert(selected_reservation_index[0], new_reservation_name)

    def clear_details(self):
        self.entry_name.delete(0, END)
        self.entry_location.delete(0, END)
        self.listbox_clients.delete(0, END)
        self.listbox_employees.delete(0, END)
        self.listbox_reservations.delete(0, END)

    def show_all_centres_on_map(self):
        self.map_widget.set_position(52.2296756, 19.0122287)
        self.map_widget.set_zoom(6)
        for centre in self.centres:
            location = self.geolocator.geocode(centre['location'])
            if location:
                self.map_widget.set_marker(location.latitude, location.longitude, text=centre['name'])

    def show_client_reservations_on_map(self):
        if self.selected_client:
            self.map_widget.set_position(52.2296756, 19.0122287)
            self.map_widget.set_zoom(6)
            for reservation in self.selected_client['reservation']:
                centre = next((c for c in self.centres if c['name'] == reservation), None)
                if centre:
                    location = self.geolocator.geocode(centre['location'])
                    if location:
                        self.map_widget.set_marker(location.latitude, location.longitude, text=reservation)

def main():
    root = Tk()

    def on_login_success():
        login_window.frame_login.pack_forget()
        CentreManager(root)

    login_window = LoginWindow(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()