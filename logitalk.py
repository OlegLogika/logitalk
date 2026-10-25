
from customtkinter import *
from socket import *
import threading


class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("LogiTalk")
        self.menu_width = 200
        self.frame_width = 0
        self.menu_show_speed = 20
        self.is_show_menu = False
        self.show_login()
    # АВТОРИЗАЦІЯ
    def show_login(self):
        self.login_frame = CTkFrame(self, width=300, height=220)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.login_frame.pack_propagate(False)
        self.login_label = CTkLabel(self.login_frame, text="Вхід у LogiTalk", font=("Arial", 22))
        self.login_label.pack(pady=20)
        self.name_entry = CTkEntry(self.login_frame, width=220, placeholder_text="Введіть ім'я")
        self.name_entry.pack(pady=10)
        self.login_button = CTkButton( self.login_frame, text="Увійти", command=self.login)
        self.login_button.pack(pady=15)


       
        self.name_entry.bind("<Return>", lambda event: self.login())
    # ВХІД
    def login(self):
        name = self.name_entry.get().strip()
        if name == "":
            return
        self.user_name = name
        self.login_frame.destroy()
        self.create_chat()
    # ОСНОВНИЙ ЧАТ
    def create_chat(self):
        # МЕНЮ
        self.frame = CTkFrame(self, width=0, height=300,  corner_radius=0)
        self.frame.place(x=0, y=0)
        self.frame.pack_propagate(False)
        # НАЛАШТУВАННЯ МЕНЮ
        self.label = CTkLabel(self.frame, text="Ваше ім'я:")
        self.label.pack(pady=30)
        self.name_label = CTkLabel(self.frame,  text=self.user_name)
        self.name_label.pack()
        self.label_theme = CTkOptionMenu(self.frame, values=["Темна", "Світла"], command=self.change_theme)
        self.label_theme.pack(side="bottom", pady=20 )
        # КНОПКА МЕНЮ
        self.btn = CTkButton(self, text="▶", width=35, height=30, command=self.toggle_show_menu)
        self.btn.place(x=0, y=0)
        # ЧАТ
        #TODO disable
        self.chat_text = CTkTextbox(self, width=400, height=210, state='disable')
        self.chat_text.place(x=0, y=35)
        self.message_input = CTkEntry(self, width=340, height=35, placeholder_text="Введи текст") # TODO дописати command
        self.message_input.place(x=5, y=255)


        self.send_button = CTkButton(self, text=">", width=45, height=35, command=self.send_message)
        self.send_button.place(x=350, y=255)
        self.btn.lift()


        #TODO
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('dchdu56evb.localto.net', 1610))
            hello = f"TEXT@{self.user_name}@[SYSTEM] {self.user_name} приєднався(лась) до чату!\n"
            self.sock.send(hello.encode('utf-8'))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Не вдалося підключитися до сервера: {e}")


    def toggle_show_menu(self):
        if self.is_show_menu:
            self.is_show_menu = False
            self.close_menu()
        else:
            self.is_show_menu = True
            self.show_menu()


    def show_menu(self):
        if self.frame_width < self.menu_width:
            self.frame_width += self.menu_show_speed
            if self.frame_width > self.menu_width:
                self.frame_width = self.menu_width
            self.frame.configure(width=self.frame_width)
            self.move_chat(self.frame_width)
            self.after(20, self.show_menu)


    def close_menu(self):
        if self.frame_width > 0:
            self.frame_width -= self.menu_show_speed
            if self.frame_width < 0:
                self.frame_width = 0
            self.frame.configure(width=self.frame_width)
            self.move_chat(self.frame_width)
            self.after(20, self.close_menu)


    def move_chat(self, x):
        self.chat_text.place(x=x, y=35)
        self.message_input.place(x=x+5, y=255)
        self.send_button.place(x=x+350, y=255)
        self.btn.place(x=x, y=0)


    def change_theme(self, value):
        if value == "Темна":
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")


    #TODO from send_message to add_message
    def add_message(self, text):
        self.chat_text.configure(state='normal')
        self.chat_text.insert(END, text + '\n')
        self.chat_text.configure(state='disable')
   
    #TODO
    def send_message(self):
           message = self.message_input.get()
           if message:
               self.add_message(f"{self.user_name}: {message}")
               data = f"TEXT@{self.user_name}@{message}\n"
               try:
                   self.sock.sendall(data.encode())
               except:
                   pass
           self.message_input.delete(0, END)


    #TODO def recv
    def recv_message(self):
           buffer = ""
           while True:
               try:
                   chunk = self.sock.recv(4096)
                   if not chunk:
                       break
                   buffer += chunk.decode()
   
                   while "\n" in buffer:
                       line, buffer = buffer.split("\n", 1)
                       self.handle_line(line.strip())
               except:
                   break
           self.sock.close()


    #TODO handle_line
    def handle_line(self, line):
        if not line:
            return
        parts = line.split("@", 3)
       
        if len(parts) >= 3:
                author = parts[1]
                message = parts[2]
                self.add_message(f"{author}: {message}")
        else:
            self.add_message(message)
           
win = MainWindow()
win.mainloop()
