import tkinter as tk
from PIL import ImageTk, Image
from tkinter import messagebox
from AutoLYCUS import AutoLYCUS

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == 'admin' and password == 'admin123':
        root.destroy()
        auto_lycus = AutoLYCUS('encrypted_sentences.csv')
        auto_lycus.load_data()
        open_decryption_page(auto_lycus)
    else:
        message = 'Invalid username or password.'
        messagebox.showinfo('Login Result', message)


def decrypt_message(auto_lycus, encrypted_entry,decryption_page):
    encrypted_string = encrypted_entry.get()
    probable_name = []
    for _ in range(100):
        auto_lycus.train_model()
        probable_name.append(auto_lycus.predict_encryption_name(encrypted_string))
    predicted_name, count = auto_lycus.find_most_probable(probable_name)

    # Create labels to display the results
    possibilities_label = tk.Label(decryption_page, text="Possibilities:", font=('Impact', 16), bg='#16417C',
                                   fg='red')
    possibilities_label.place(x=20, y=140)

    for i, key in enumerate(count.keys()):
        probability = f"{key}% : {count[key]}"
        probability_label = tk.Label(decryption_page, text=probability, font=('Impact', 16), bg='#16417C',
                                     fg='red')
        probability_label.place(x=20, y=180 + i * 40)

    predicted_label = tk.Label(decryption_page, text=f"Predicted Name: {predicted_name}", font=('Impact', 16),
                               bg='#16417C', fg='red')
    predicted_label.place(x=20, y=220 + len(count) * 40)

    most_probable_label = tk.Label(decryption_page, text=f"Most Probable: {predicted_name[0]}", font=('Impact', 16),
                                   bg='#16417C', fg='red')
    most_probable_label.place(x=20, y=260 + len(count) * 40)


def open_decryption_page(auto_lycus):
    decryption_page = tk.Tk()
    decryption_page.title('Decryption Page')

    # Load background image
    background_image = ImageTk.PhotoImage(Image.open('CS.png'))

    # Create background label
    background_label = tk.Label(decryption_page, image=background_image)
    background_label.pack()

    # Create encrypted string label and entry field
    encrypted_label = tk.Label(decryption_page, text='Encrypted String', font=('Impact', 16), bg='#16417C',
                               fg='darkorange')
    encrypted_label.place(x=20, y=20)

    encrypted_entry = tk.Entry(decryption_page, font=('Impact', 16))
    encrypted_entry.place(x=20, y=60)

    # Create decrypt button
    decrypt_button = tk.Button(decryption_page, text='Decrypt', font=('Impact', 16), bg='teal', fg='white',
                               command=lambda: decrypt_message(auto_lycus, encrypted_entry,decryption_page))
    decrypt_button.place(x=20, y=100)

    decryption_page.geometry('1022x564')
    decryption_page.mainloop()


root = tk.Tk()
root.title('Login Page')

# Load background image
background_image = ImageTk.PhotoImage(Image.open('CS.png'))

# Create background label
background_label = tk.Label(root, image=background_image)
background_label.pack()

# Create username label and entry field
username_label = tk.Label(root, text='Username', font=('Impact', 16), bg='#16417C', fg='darkorange')

username_label.place(x=20, y=20)

username_entry = tk.Entry(root, font=('Impact', 16))
username_entry.place(x=20, y=60)

# Create password label and entry field
password_label = tk.Label(root, text='Password', font=('Impact', 16), bg='#16417C', fg='darkorange')
password_label.place(x=20, y=100)

password_entry = tk.Entry(root, show='#', font=('Impact', 16))
password_entry.place(x=20, y=140)

# Create login button
login_button = tk.Button(root, text='Login', font=('Impact', 16), bg='teal', fg='white',
                         command=login)
login_button.place(x=20, y=180)

root.geometry('1022x564')
root.mainloop()

