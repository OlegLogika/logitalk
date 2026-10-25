from customtkinter import *
from PIL import Image

icon = Image.open('./icon.png')
icon_ctk = CTkImage(light_image=icon, size=(50,50))
WIDTH = 800
HEIGHT= 300

win = CTk()
win.geometry(f'{WIDTH}x{HEIGHT}')
win.title('Logitalk')
message_field = CTkTextbox(win, width=WIDTH, height=HEIGHT-100, state='disable')
message_field.pack()

entry_btn_frame = CTkFrame(win, width=WIDTH, height=50)
icon_label = CTkLabel(entry_btn_frame, image=icon_ctk, width=50, height=50, text='')
icon_label.pack(side='left')
message_entry = CTkTextbox(entry_btn_frame, width=WIDTH-150, height=50, fg_color='grey')
message_entry.pack(side='left')

def send_message():
    text = message_entry.get('1.0', 'end')
    message_field.configure(state="normal")
    message_field.insert('end', text)
    message_field.configure(state="disable")
    message_entry.delete('1.0', 'end')

send_btn = CTkButton(entry_btn_frame, width=100, height=50, command=send_message)
send_btn.pack(side='left')
entry_btn_frame.pack(side='bottom')



win.mainloop()