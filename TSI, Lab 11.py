import tkinter as tk
from tkinter import messagebox, filedialog
import random
import math


def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num


def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y


def generate_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randint(2, phi - 1)
        if math.gcd(e, phi) == 1:
            break
    _, d, _ = extended_gcd(e, phi)
    d = d % phi
    if d < 0:
        d += phi
    return (e, n), (d, n)


def encrypt(plaintext, get_public_key):
    e, n = get_public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext


def decrypt(ciphertext, get_private_key):
    d, n = get_private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext


def process_text():
    text = text_entry.get("1.0", "end-1c")
    if not text:
        messagebox.showerror("Eroare", "Introduceți text!")
        return
    if operation_var.get() == "Encrypt":
        result = encrypt(text, public_key)
    else:
        try:
            ciphertext = [int(char) for char in text.split()]
            result = decrypt(ciphertext, private_key)
        except ValueError:
            messagebox.showerror("Eroare", "Textul introdus nu este valid pentru decriptare!")
            return
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, result)


def load_text():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("Word Files", "*.docx")])
    if file_path:
        with open(file_path, "r") as file:
            text = file.read()
            text_entry.delete("1.0", tk.END)
            text_entry.insert(tk.END, text)


def save_text():
    text_to_save = result_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_to_save)


def show_keys():
    global public_key, private_key
    bits = int(bits_entry.get())
    public_key, private_key = generate_keys(bits)
    public_key_text.delete("1.0", tk.END)
    public_key_text.insert(tk.END, f"e: {public_key[0]}\nn: {public_key[1]}")
    private_key_text.delete("1.0", tk.END)
    private_key_text.insert(tk.END, f"d: {private_key[0]}\nn: {private_key[1]}")


initial_bits = 8
public_key, private_key = generate_keys(initial_bits)

root = tk.Tk()
root.title("RSA")

button_color_1 = "LightSteelBlue"
button_color_2 = "lightSlateGray"

operation_var = tk.StringVar()
operation_var.set("Encrypt")
operation_menu = tk.OptionMenu(root, operation_var, "Encrypt", "Decrypt")
operation_menu.configure(bg=button_color_2)
operation_menu.grid(row=0, column=1, columnspan=1, padx=5, pady=5, sticky="ew")

text_label = tk.Label(root, text="Textul:")
text_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
text_entry = tk.Text(root, height=5, width=50)
text_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

bits_label = tk.Label(root, text="Biți:")
bits_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
bits_entry = tk.Entry(root, width=5)
bits_entry.insert(tk.END, "8")
bits_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

generate_keys_button = tk.Button(root, text="Generare Chei", command=show_keys, bg=button_color_1, fg="black")
generate_keys_button.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

public_key_label = tk.Label(root, text="Cheia Publică:")
public_key_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
public_key_text = tk.Text(root, height=2, width=50)
public_key_text.grid(row=4, column=1, padx=5, pady=5, sticky="w")

private_key_label = tk.Label(root, text="Cheia Privată:")
private_key_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
private_key_text = tk.Text(root, height=2, width=50)
private_key_text.grid(row=5, column=1, padx=5, pady=5, sticky="w")

result_label = tk.Label(root, text="Rezultat:")
result_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
result_text = tk.Text(root, height=5, width=50)
result_text.grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky="w")

process_button = tk.Button(root, text="Process", command=process_text, width=10, bg=button_color_2, fg="white")
process_button.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

import_button = tk.Button(root, text="Load Text", command=load_text, bg=button_color_1, fg="black")
import_button.grid(row=7, column=2, padx=5, pady=5, sticky="w")

save_button = tk.Button(root, text="Save Text", command=save_text, bg=button_color_1, fg="black")
save_button.grid(row=7, column=0, padx=5, pady=5, sticky="e")

root.geometry("585x440")
root.resizable(width=False, height=False)
root.mainloop()
