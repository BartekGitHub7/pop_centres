import requests
from bs4 import BeautifulSoup

def get_coordinates()->list:
    location = input('podaj nazwę miejscowości: ')

    url:str=f'https://pl.wikipedia.org/wiki/{location}'
    response=requests.get(url)
    # print(response.text)
    response_html=BeautifulSoup(response.text,'html.parser')
    # print(response_html)
    response_html_lat: list = response_html.select('.latitude')[1].text.replace(',', '.')
    response_html_lng: list = response_html.select('.longitude')[1].text.replace(',', '.')
    print (response_html_lat)
    print (response_html_lng)
    return [response_html_lat, response_html_lng]
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
