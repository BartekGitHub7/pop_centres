from tkinter import *
from tkinter import messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup

centres = [
    {"name": "Centrum Konferencyjne w Warszawie", "clients":[{"name": "Mariusz Pudzianowski", "reservation": ["Centrum Konferencyjne w Warszawie", "Centrum Konferencyjne w Poznaniu"]}, {"name": "Władysław Łokietek", "reservation": ["Centrum Konferencyjne w Warszawie", "Centrum Konferencyjne w Gdańsku"]}], "employees":[{"name": "Anna Nowak"}, {"name": "Piotr Kowalski"}]},
    {"name": "Centrum Konferencyjne w Poznaniu", "clients":[{"name": "Mariusz Pudzianowski", "reservation": ["Centrum Konferencyjne w Warszawie", "Centrum Konferencyjne w Poznaniu"]}, {"name": "Adam Nowak", "reservation": ["Centrum Konferencyjne w Poznaniu", "Centrum Konferencyjne w Krakowie"]}], "employees":[{"name": "Klaudia Mickiewicz"}, {"name": "Krzysztof Wiśniewski"}]},
    {"name": "Centrum Konferencyjne w Gdańsku", "clients":[{"name": "Jan Kowalski", "reservation": ["Centrum Konferencyjne w Lublinie", "Centrum Konferencyjne w Gdańsku"]}, {"name": "Władysław Łokietek", "reservation": ["Centrum Konferencyjne w Warszawie", "Centrum Konferencyjne w Gdańsku"]}], "employees":[{"name": "Marta Kwiatkowska"}, {"name": "Tomasz Jankowski"}]},
    {"name": "Centrum Konferencyjne w Krakowie", "clients":[{"name": "Adam Nowak", "reservation": ["Centrum Konferencyjne w Krakowie", "Centrum Konferencyjne w Poznaniu"]}, {"name": "Ferdynand Kiepski", "reservation": ["Centrum Konferencyjne w Krakowie", "Centrum Konferencyjne w Lublinie"]}], "employees":[{"name": "Julia Wiśniewska"}, {"name": "Michał Kamiński"}]},
    {"name": "Centrum Konferencyjne w Lublinie", "clients":[{"name": "Jan Kowalski", "reservation": ["Centrum Konferencyjne w Lublinie", "Centrum Konferencyjne w Gdańsku"]}, {"name": "Ferdynand Kiepski", "reservation": ["Centrum Konferencyjne w Lublinie", "Centrum Konferencyjne w Krakowie"]}], "employees":[{"name": "Agnieszka Wojciechowska"}, {"name": "Adam Woźniak"}]},
]

class CentreManager:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1200x800")
        self.root.title("Centre Manager")

        self.centres = centres

        self.frame_list = Frame(root, width=400, height=600, padx=10, pady=10)  # Changed width and height
        self.frame_details = Frame(root, width=700, height=600, padx=10, pady=10)  # Changed width
        self.frame_map = Frame(root, width=1100, height=400, padx=10, pady=10)

        self.frame_list.grid(row=0, column=0, padx=10, pady=10, sticky=N)
        self.frame_details.grid(row=0, column=1, padx=10, pady=10, sticky=N)
        self.frame_map.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=N)

        self.setup_list_frame()
        self.setup_details_frame()
        self.setup_map_frame()

        self.selected_centre = None
        self.selected_client = None

    def setup_list_frame(self):
        self.label_list = Label(self.frame_list, text='Lista Centrów Konferencyjnych')
        self.listbox_centres = Listbox(self.frame_list, width=40, height=30)  # Changed width
        self.button_show_details = Button(self.frame_list, text='Pokaż szczegóły', command=self.show_centre_details)
        self.button_add_centre = Button(self.frame_list, text='Dodaj centrum', command=self.add_centre)
        self.button_remove_centre = Button(self.frame_list, text='Usuń centrum', command=self.remove_centre)
        self.button_update_centre = Button(self.frame_list, text='Edytuj centrum', command=self.update_centre)

        self.label_list.grid(row=0, column=0, columnspan=3, pady=5)
        self.listbox_centres.grid(row=1, column=0, columnspan=3, pady=5)
        self.button_show_details.grid(row=2, column=0, pady=5)
        self.button_add_centre.grid(row=2, column=1, pady=5)
        self.button_remove_centre.grid(row=2, column=2, pady=5)
        self.button_update_centre.grid(row=3, column=0, columnspan=3, pady=5)

        self.refresh_centre_list()

    def setup_details_frame(self):
        self.label_details = Label(self.frame_details, text='Szczegóły centrum')
        self.label_name = Label(self.frame_details, text='Nazwa centrum')
        self.entry_name = Entry(self.frame_details, width=50)
        self.label_clients = Label(self.frame_details, text='Klienci')
        self.listbox_clients = Listbox(self.frame_details, width=40, height=15)  # Changed width and height
        self.button_show_reservations = Button(self.frame_details, text='Pokaż rezerwacje', command=self.show_reservations)
        self.label_employees = Label(self.frame_details, text='Pracownicy')
        self.listbox_employees = Listbox(self.frame_details, width=40, height=15)  # Changed width and height

        self.entry_client_name = Entry(self.frame_details, width=30)
        self.entry_employee_name = Entry(self.frame_details, width=30)
        self.entry_reservation_name = Entry(self.frame_details, width=60)

        self.button_add_client = Button(self.frame_details, text='Dodaj klienta', command=self.add_client)
        self.button_remove_client = Button(self.frame_details, text='Usuń klienta', command=self.remove_client)
        self.button_update_client = Button(self.frame_details, text='Edytuj klienta', command=self.update_client)
        self.button_add_employee = Button(self.frame_details, text='Dodaj pracownika', command=self.add_employee)
        self.button_remove_employee = Button(self.frame_details, text='Usuń pracownika', command=self.remove_employee)
        self.button_update_employee = Button(self.frame_details, text='Edytuj pracownika', command=self.update_employee)

        self.button_add_reservation = Button(self.frame_details, text='Dodaj rezerwację', command=self.add_reservation)
        self.button_remove_reservation = Button(self.frame_details, text='Usuń rezerwację', command=self.remove_reservation)
        self.button_update_reservation = Button(self.frame_details, text='Edytuj rezerwację', command=self.update_reservation)

        self.label_details.grid(row=0, column=0, columnspan=4, pady=5)
        self.label_name.grid(row=1, column=0, sticky=W)
        self.entry_name.grid(row=1, column=1, sticky=W, columnspan=3, pady=5)
        self.label_clients.grid(row=2, column=0, sticky=W, pady=5)
        self.label_employees.grid(row=2, column=2, sticky=W, pady=5)
        self.listbox_clients.grid(row=3, column=0, columnspan=2, pady=5)
        self.listbox_employees.grid(row=3, column=2, columnspan=2, pady=5)

        self.entry_client_name.grid(row=4, column=0, columnspan=2, pady=5)
        self.entry_employee_name.grid(row=4, column=2, columnspan=2, sticky=E, pady=5)
        self.entry_reservation_name.grid(row=6, column=0, columnspan=4, pady=5)

        self.button_add_client.grid(row=5, column=0, pady=5)
        self.button_remove_client.grid(row=5, column=1, pady=5)
        self.button_update_client.grid(row=6, column=0, columnspan=2, pady=5)

        self.button_add_employee.grid(row=5, column=2, pady=5)
        self.button_remove_employee.grid(row=5, column=3, pady=5)
        self.button_update_employee.grid(row=6, column=2, columnspan=2, pady=5)

        self.button_add_reservation.grid(row=7, column=0, pady=5)
        self.button_show_reservations.grid(row=7, column=1, pady=5)  # Moved next to 'Dodaj rezerwację'
        self.button_remove_reservation.grid(row=7, column=2, pady=5)
        self.button_update_reservation.grid(row=7, column=3, pady=5)

    def setup_map_frame(self):
        self.label_map = Label(self.frame_map, text='Mapa')
        self.label_map.grid(row=0, column=0, pady=5)
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=1100, height=400, corner_radius=0)
        self.map_widget.grid(row=1, column=0, pady=5)
        self.map_widget.set_position(52.229675, 21.012230)
        self.map_widget.set_zoom(6)

    def refresh_centre_list(self):
        self.listbox_centres.delete(0, END)
        for centre in self.centres:
            self.listbox_centres.insert(END, centre['name'])

    def show_centre_details(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            self.selected_centre = self.centres[selected_index[0]]
            self.entry_name.delete(0, END)
            self.entry_name.insert(0, self.selected_centre['name'])
            self.refresh_client_list()
            self.refresh_employee_list()

    def refresh_client_list(self):
        self.listbox_clients.delete(0, END)
        if self.selected_centre:
            for client in self.selected_centre['clients']:
                self.listbox_clients.insert(END, client['name'])

    def refresh_employee_list(self):
        self.listbox_employees.delete(0, END)
        if self.selected_centre:
            for employee in self.selected_centre['employees']:
                self.listbox_employees.insert(END, employee['name'])

    def add_centre(self):
        centre_name = self.entry_name.get()
        if centre_name:
            self.centres.append({'name': centre_name, 'clients': [], 'employees': []})
            self.refresh_centre_list()
            self.entry_name.delete(0, END)

    def remove_centre(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            self.centres.pop(selected_index[0])
            self.refresh_centre_list()
            self.entry_name.delete(0, END)
            self.selected_centre = None
            self.listbox_clients.delete(0, END)
            self.listbox_employees.delete(0, END)

    def update_centre(self):
        selected_index = self.listbox_centres.curselection()
        if selected_index:
            centre_name = self.entry_name.get()
            if centre_name:
                self.centres[selected_index[0]]['name'] = centre_name
                self.refresh_centre_list()

    def add_client(self):
        client_name = self.entry_client_name.get()
        if self.selected_centre and client_name:
            self.selected_centre['clients'].append({'name': client_name, 'reservation': []})
            self.refresh_client_list()
            self.entry_client_name.delete(0, END)

    def remove_client(self):
        selected_index = self.listbox_clients.curselection()
        if self.selected_centre and selected_index:
            self.selected_centre['clients'].pop(selected_index[0])
            self.refresh_client_list()

    def update_client(self):
        selected_index = self.listbox_clients.curselection()
        client_name = self.entry_client_name.get()
        if self.selected_centre and selected_index and client_name:
            self.selected_centre['clients'][selected_index[0]]['name'] = client_name
            self.refresh_client_list()
            self.entry_client_name.delete(0, END)

    def show_reservations(self):
        selected_index = self.listbox_clients.curselection()
        if self.selected_centre and selected_index:
            self.selected_client = self.selected_centre['clients'][selected_index[0]]
            self.entry_reservation_name.delete(0, END)
            self.entry_reservation_name.insert(0, ', '.join(self.selected_client['reservation']))

    def add_reservation(self):
        reservation_name = self.entry_reservation_name.get()
        if self.selected_client and reservation_name:
            self.selected_client['reservation'].append(reservation_name)
            self.entry_reservation_name.delete(0, END)
            self.show_reservations()

    def remove_reservation(self):
        reservation_name = self.entry_reservation_name.get()
        if self.selected_client and reservation_name in self.selected_client['reservation']:
            self.selected_client['reservation'].remove(reservation_name)
            self.entry_reservation_name.delete(0, END)
            self.show_reservations()

    def update_reservation(self):
        reservation_name = self.entry_reservation_name.get()
        selected_index = self.listbox_clients.curselection()
        if self.selected_client and selected_index and reservation_name:
            self.selected_client['reservation'][selected_index[0]] = reservation_name
            self.entry_reservation_name.delete(0, END)
            self.show_reservations()

    def add_employee(self):
        employee_name = self.entry_employee_name.get()
        if self.selected_centre and employee_name:
            self.selected_centre['employees'].append({'name': employee_name})
            self.refresh_employee_list()
            self.entry_employee_name.delete(0, END)

    def remove_employee(self):
        selected_index = self.listbox_employees.curselection()
        if self.selected_centre and selected_index:
            self.selected_centre['employees'].pop(selected_index[0])
            self.refresh_employee_list()

    def update_employee(self):
        selected_index = self.listbox_employees.curselection()
        employee_name = self.entry_employee_name.get()
        if self.selected_centre and selected_index and employee_name:
            self.selected_centre['employees'][selected_index[0]]['name'] = employee_name
            self.refresh_employee_list()
            self.entry_employee_name.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = CentreManager(root)
    root.mainloop()
