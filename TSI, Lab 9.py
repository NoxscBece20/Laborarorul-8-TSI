import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import Counter


###########################################################################
def calculate_letter_frequency(text):
    text = text.replace(" ", "").upper()
    letter_frequency = Counter(text)
    total_characters = sum(letter_frequency.values())
    letter_frequency_percentage = {char: (count / total_characters) * 100 for char, count in letter_frequency.items()}
    return letter_frequency_percentage


def display_letter_frequency(text, title):
    letter_frequency = calculate_letter_frequency(text)
    print(f"{title} Letter Frequency:")
    for char, frequency in letter_frequency.items():
        print(f"{char}: {frequency:.2f}%")
    print("==========================")


def show_letter_frequency():
    crypted_text = result_text.get(1.0, tk.END).strip()
    decrypted_text = text_entry.get()
    display_letter_frequency(crypted_text, "Textul criptat")
    display_letter_frequency(decrypted_text, "Textul decriptat")

    total_text = crypted_text + decrypted_text
    display_letter_frequency(total_text, "Total")
###########################################################################


def brute_force_attack(ciphertext, key2=None):
    decrypted_texts = []
    for key in range(26):
        decrypted_text = decrypt(ciphertext, key, key2)
        decrypted_texts.append((key, decrypted_text))
    return decrypted_texts


def perform_brute_force_attack():
    ciphertext = result_text.get(1.0, tk.END).strip()
    key2 = key2_entry.get().upper() if key2_entry.get() else None
    decrypted_texts = brute_force_attack(ciphertext, key2)
    brute_force_result_window = tk.Toplevel(root)
    brute_force_result_window.title("Brute Force Attack Result")

    row = 0
    col = 0
    for key, decrypted_text in decrypted_texts:
        result_button = tk.Button(brute_force_result_window, text=f"Key: {key}, Vizualizează",
                                  command=lambda text=decrypted_text: show_decrypted_text(text))
        result_button.grid(row=row, column=col, sticky="ew", padx=5, pady=5)
        col += 1
        if col == 2:
            col = 0
            row += 1

    brute_force_result_window.geometry("265x465")
    brute_force_result_window.resizable(False, False)


def show_decrypted_text(decrypted_text):
    decrypted_text_window = tk.Toplevel(root)
    decrypted_text_window.title("Decrypted Text")
    text_label_new = tk.Label(decrypted_text_window, text=decrypted_text, padx=10, pady=10)
    text_label_new.pack()


###########################################################################
def generate_new_alphabet(key2=None):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if key2:
        key2_upper = key2.upper()
        filtered_alphabet = ''.join(char for char in alphabet if char not in key2_upper)
        new_alphabet = key2_upper + filtered_alphabet
        new_alphabet = ''.join(sorted(set(new_alphabet), key=new_alphabet.index))
    else:
        new_alphabet = alphabet
    return new_alphabet


def validate_keys(key1, key2):
    if key1.isnumeric() and (key2.isalpha() or key2 == ""):
        return True
    else:
        return False


def encrypt(text, key1, key2=None):
    new_alphabet = generate_new_alphabet(key2)
    encrypted_text = ''
    for char in text.upper():
        if char in new_alphabet:
            index = (new_alphabet.index(char) + key1) % 26
            encrypted_text += new_alphabet[index]
        else:
            encrypted_text += char
    return encrypted_text


def decrypt(text, key1, key2=None):
    new_alphabet = generate_new_alphabet(key2)
    decrypted_text = ''
    for char in text.upper():
        if char in new_alphabet:
            index = (new_alphabet.index(char) - key1) % 26
            decrypted_text += new_alphabet[index]
        else:
            decrypted_text += char
    return decrypted_text


def process_text():
    operation = operation_var.get()
    key1 = int(key1_entry.get())
    key2 = key2_entry.get().upper() if key2_entry.get() else None
    text = text_entry.get()

    if validate_keys(key1_entry.get(), key2_entry.get()):
        if operation == "Encrypt":
            result = encrypt(text, key1, key2)
        else:
            result = decrypt(text, key1, key2)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
    else:
        messagebox.showerror("Error", "Key 1 must be int and Key 2 must be a string.")


def save_result():
    result = result_text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(result)


def load_text():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text = file.read()
            text_entry.delete(0, tk.END)
            text_entry.insert(0, text)


root = tk.Tk()
root.title("Caesar Cipher")

main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.place(relx=0.5, rely=0.5, anchor="center")

operation_var = tk.StringVar()
operation_var.set("Encrypt")
operation_menu = tk.OptionMenu(root, operation_var, "Encrypt", "Decrypt")
operation_menu.configure(bg="light slate gray")


key1_label = tk.Label(root, text=" Key 1:")
key1_entry = tk.Entry(root)
key2_label = tk.Label(root, text=" Key 2:")
key2_entry = tk.Entry(root)
text_label = tk.Label(root, text="   Text:")
text_entry = tk.Entry(root)

result_label = tk.Label(root, text="Result:")
result_text = tk.Text(root, height=5, width=50)

process_button = tk.Button(root, text="Process", command=process_text)

save_button = tk.Button(root, text="Save Result", command=save_result)
save_button.configure(bg="light slate gray")
load_button = tk.Button(root, text="Load Text", command=load_text)
load_button.configure(bg="light slate gray")

#######################################################################
operation_menu.grid(row=0, column=1, columnspan=1, padx=5, pady=10, sticky="ew")

key1_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
key1_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
key2_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
key2_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
text_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
text_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

result_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
result_text.grid(row=4, column=1, padx=5, pady=5, sticky="w")

save_button.grid(row=5, column=0, padx=5, pady=2)
process_button.grid(row=5, column=1, padx=5, pady=2, sticky="ew")
load_button.grid(row=5, column=2, padx=5, pady=2, sticky="ew")


brute_force_button = tk.Button(root, text="Brute Force Attack", command=perform_brute_force_attack)
brute_force_button.grid(row=6, column=1, padx=5, pady=2, sticky="ew")
brute_force_button.configure(bg="light slate gray")

letter_frequency_button = tk.Button(root, text="Show Letter Frequency", command=show_letter_frequency)
letter_frequency_button.grid(row=7, column=1, padx=5, pady=2, sticky="ew")
letter_frequency_button.configure(bg="light slate gray")


root.resizable(width=False, height=False)
root.mainloop()
