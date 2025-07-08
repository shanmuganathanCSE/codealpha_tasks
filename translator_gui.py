import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import pyperclip # type: ignore
import pyttsx3 # type: ignore

translator = Translator()
engine = pyttsx3.init()

language_list = list(LANGUAGES.values())

root = tk.Tk()
root.title("Language Translator Tool")
root.geometry("600x400")
root.config(bg="#f2f2f2")

def translate_text():
    try:
        src_lang = from_lang_combo.get()
        tgt_lang = to_lang_combo.get()
        src_code = list(LANGUAGES.keys())[language_list.index(src_lang)]
        tgt_code = list(LANGUAGES.keys())[language_list.index(tgt_lang)]

        translated = translator.translate(text_entry.get("1.0", tk.END), src=src_code, dest=tgt_code)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

def copy_text():
    pyperclip.copy(output_text.get("1.0", tk.END).strip())

def speak_text():
    engine.say(output_text.get("1.0", tk.END))
    engine.runAndWait()

tk.Label(root, text="Enter Text:", bg="#f2f2f2", font=("Arial", 12)).pack(pady=5)
text_entry = tk.Text(root, height=4, width=70)
text_entry.pack(pady=5)

frame = tk.Frame(root, bg="#f2f2f2")
frame.pack(pady=10)

tk.Label(frame, text="From:", bg="#f2f2f2").grid(row=0, column=0, padx=10)
from_lang_combo = ttk.Combobox(frame, values=language_list, width=20)
from_lang_combo.set("english")
from_lang_combo.grid(row=0, column=1)

tk.Label(frame, text="To:", bg="#f2f2f2").grid(row=0, column=2, padx=10)
to_lang_combo = ttk.Combobox(frame, values=language_list, width=20)
to_lang_combo.set("french")
to_lang_combo.grid(row=0, column=3)

translate_btn = tk.Button(root, text="Translate", command=translate_text, bg="#4CAF50", fg="white", width=20)
translate_btn.pack(pady=10)

tk.Label(root, text="Translated Text:", bg="#f2f2f2", font=("Arial", 12)).pack(pady=5)
output_text = tk.Text(root, height=4, width=70)
output_text.pack(pady=5)

btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="Copy", command=copy_text, width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Speak", command=speak_text, width=15).grid(row=0, column=1, padx=10)

root.mainloop()
