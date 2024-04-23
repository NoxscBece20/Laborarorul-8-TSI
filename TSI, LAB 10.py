import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import Counter
import itertools


###########################################################################

def find_key():
    text = result_text.get(1.0, tk.END).strip()
    keys = generate_keys(5)
    meaningful_keys = [key for key in keys if select_keys(text, key)]
    if meaningful_keys:
        keys_text = "\n".join(meaningful_keys)
        messagebox.showinfo("Meaningful Keys", display(keys_text))
    else:
        messagebox.showinfo("Meaningful Keys", "No meaningful keys found.")


def generate_keys(n):
    alpha = alphabet()
    keys_found = 0
    keys = []
    while keys_found < n:
        for r in range(2, n):
            for combo in itertools.combinations(alpha, r):
                key = ''.join(combo)
                if select_keys("", key):
                    keys.append(key)
                    keys_found += 1
                    if keys_found >= n:
                        break
            if keys_found >= n:
                break
    return keys


def select_keys(text, key):
    decrypted_text = vigenere_decrypt(text, key)
    return logic_text(decrypted_text)


def display(text):
    rows = text.split('\n')
    rows_and_columns_text = ""
    for row in rows:
        row = row.ljust(20)
        rows_and_columns_text += row + '\n'
    return rows_and_columns_text


def logic_text(text, threshold=3):
    common_words = {'the', 'and', 'or', 'is', 'it', 'are', 'to', 'be'}
    common_combinations = {'th', 'he', 'in', 'en', 'nt', 're', 'er', 'an', 'ti', 'es', 'on', 'at', 'se', 'nd', 'or',
                           'ar', 'al', 'te', 'co', 'de', 'to', 'ra', 'et', 'ed', 'it', 'sa', 'em', 'ro'}
    uncommon_combinations = {'bk', 'fq', 'jc', 'jt', 'mj', 'qh', 'qx', 'vj', 'wz', 'zh',
                             'bq', 'fv', 'jd', 'jv', 'mq', 'qj', 'qy', 'vk', 'xb', 'zj',
                             'bx', 'fx', 'jf', 'jw', 'mx', 'qk', 'qz', 'vm', 'xg', 'zn',
                             'cb', 'fz', 'jg', 'jx', 'mz', 'ql', 'sx', 'vn', 'xj', 'zq',
                             'cf', 'gq', 'jh', 'jy', 'pq', 'qm', 'sz', 'vp', 'xk', 'zr',
                             'cg', 'gv', 'jk', 'jz', 'pv', 'qn', 'tq', 'vq', 'xv', 'zs',
                             'cj', 'gx', 'jl', 'kq', 'px', 'qo', 'tx', 'vt', 'xz', 'zx',
                             'cp', 'hk', 'jm', 'kv', 'qb', 'qp', 'vb', 'vw', 'yq',
                             'cv', 'hv', 'jn', 'kx', 'qc', 'qr', 'vc', 'vx', 'yv',
                             'cw', 'hx', 'jp', 'kz', 'qd', 'qs', 'vd', 'vz', 'yz',
                             'cx', 'hz', 'jq', 'lq', 'qe', 'qt', 'vf', 'wq', 'zb',
                             'dx', 'iy', 'jr', 'lx', 'qf', 'qv', 'vg', 'wv', 'zc',
                             'fk', 'jb', 'js', 'mg', 'qg', 'qw', 'vh', 'wx', 'zg'}

    words = text.split()
    words = [word.lower() for word in words]
    words = [word for word in words if len(word) > 1]

    alpha_chars = sum(c.isalpha() for word in words for c in word)
    non_alpha_chars = len(''.join(words)) - alpha_chars

    common_count = sum(word.count(comb) for word in words for comb in common_combinations)
    uncommon_count = sum(word.count(comb) for word in words for comb in uncommon_combinations)

    return (len(words) >= threshold
            and any(word in common_words for word in words)
            and alpha_chars > non_alpha_chars
            and common_count > 0
            and uncommon_count == 0)

###########################################################################


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
    crypted_frequency = calculate_letter_frequency(crypted_text)
    decrypted_frequency = calculate_letter_frequency(decrypted_text)
    total_text = crypted_text + decrypted_text
    total_frequency = calculate_letter_frequency(total_text)

    frequency_message = "Letter Frequency:\n\n"
    frequency_message += (f"{'Character:':<10}"
                          f"\t{'Decrypted:':<10}"
                          f"\t{'Crypted:':<10}"
                          f"\t{'Total:':<10}\n")
    for char in sorted(set(crypted_frequency.keys()) | set(decrypted_frequency.keys())):
        if char.isalpha():
            frequency_message += (f"{char:<10}\t"
                                  f"\t{decrypted_frequency.get(char, 0):<10.2f}\t"
                                  f"\t{crypted_frequency.get(char, 0):<10.2f}\t"
                                  f"\t{total_frequency.get(char, 0):<10.2f}\t\n")

    messagebox.showinfo("Letter Frequency", frequency_message)
###########################################################################


###########################################################################
def alphabet():
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    return alpha


def validate_key(key):
    return isinstance(key, str)
###########################################################################


###########################################################################
def vigenere_encrypt(plaintext, key):
    encrypted_text = ""
    key_length = len(key)
    for i in range(len(plaintext)):
        char = plaintext[i]
        if char.isalpha():
            key_char = key[i % key_length]
            shift = ord(key_char.lower()) - ord('a')
            encrypted_text += chr((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26
                                  + ord('a' if char.islower() else 'A'))
        else:
            encrypted_text += char
    return encrypted_text


def vigenere_decrypt(ciphertext, key):
    decrypted_text = ""
    key_length = len(key)
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():
            key_char = key[i % key_length]
            shift = ord(key_char.lower()) - ord('a')
            decrypted_text += chr((ord(char) - ord('a' if char.islower() else 'A') - shift + 26) % 26
                                  + ord('a' if char.islower() else 'A'))
        else:
            decrypted_text += char
    return decrypted_text
###########################################################################


###########################################################################
def process_text():
    operation = operation_var.get()
    key = key_entry.get()
    text = text_entry.get()

    if validate_key(key):
        if operation == "Encrypt":
            result = vigenere_encrypt(text, key)
        else:
            result = vigenere_decrypt(text, key)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
    else:
        messagebox.showerror("Error", "Key trebuie să fie string.")


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
###########################################################################


###########################################################################
root = tk.Tk()
root.title("Vigenere Cipher")

main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.place(relx=0.5, rely=0.5, anchor="center")

operation_var = tk.StringVar()
operation_var.set("Encrypt")
operation_menu = tk.OptionMenu(root, operation_var, "Encrypt", "Decrypt")
operation_menu.configure(bg="light slate gray")

key_label = tk.Label(root, text="Key:")
key_entry = tk.Entry(root)
text_label = tk.Label(root, text="Text:")
text_entry = tk.Entry(root)

result_label = tk.Label(root, text="Result:")
result_text = tk.Text(root, height=5, width=50)

process_button = tk.Button(root, text="Process", command=process_text)

save_button = tk.Button(root, text="Save Result", command=save_result)
save_button.configure(bg="light slate gray")
load_button = tk.Button(root, text="Load Text", command=load_text)
load_button.configure(bg="light slate gray")
###########################################################################

###########################################################################
operation_menu.grid(row=0, column=1, columnspan=1, padx=5, pady=10, sticky="ew")
key_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
key_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
text_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
text_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
result_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
result_text.grid(row=3, column=1, padx=5, pady=5, sticky="w")
process_button.grid(row=4, column=1, padx=5, pady=2, sticky="ew")
save_button.grid(row=5, column=0, padx=5, pady=2)
load_button.grid(row=5, column=2, padx=5, pady=2)

find_key_button = tk.Button(root, text="Find Possible Keys", command=find_key)
find_key_button.grid(row=6, column=0, columnspan=3, padx=5, pady=2, sticky="ew")
find_key_button.configure(bg="light slate gray")

letter_frequency_button = tk.Button(root, text="Show Letter Frequency", command=show_letter_frequency)
letter_frequency_button.grid(row=5, column=1, padx=5, pady=2, sticky="ew")
letter_frequency_button.configure(bg="light slate gray")

root.resizable(width=False, height=False)
root.mainloop()
###########################################################################
