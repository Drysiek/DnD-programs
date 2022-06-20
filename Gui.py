import os
import sys
from tkinter import *
from tkinter import messagebox
import tkinter as tk
# import tkinter.font as tkf


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class CipherApp:
    def __init__(self):
        self.dictionary = dict()
        self.make_dictionary()

        self.window = Tk()
        self.window.title('D&D cipher helper')
        self.window.iconphoto(False, PhotoImage(file=resource_path('images/icon.ico')))

        label = tk.Label(self.window, text='Enter cipher key:')
        label.grid(row=0, column=0)
        self.input_key = tk.Entry(self.window)
        self.input_key.grid(row=0, column=1)

        self.input_text = tk.Text(self.window, wrap=tk.WORD)
        self.input_text.grid(row=1, column=0, columnspan=2)
        self.input_text.configure(height=7, width=50)

        self.output_text = tk.Text(self.window)
        self.output_text.grid(row=3, column=0, columnspan=2)
        self.output_text.configure(height=7, width=50)

        button = tk.Button(self.window, command=self.encipher, text='Encipher')
        button.grid(row=2, column=0)
        button.configure(width=20)

        button = tk.Button(self.window, command=self.decipher, text='Decipher')
        button.grid(row=2, column=1)
        button.configure(width=20)

        self.window.resizable(False, False)
        self.window.mainloop()

    def make_dictionary(self):
        iterator = 0
        for i in range(33, 123):
            self.dictionary.update({chr(i): iterator})
            iterator += 1
        for i in (260, 262, 280, 321, 323, 211, 346, 377, 379, 261, 263, 281, 322, 324, 243, 347, 378, 380):
            self.dictionary.update({chr(i): iterator})
            iterator += 1

    def encipher(self):
        text = self.input_text.get('1.0', END)
        key = self.input_key.get()
        key_size = len(key)
        final_text = ''
        if text != '\n':
            if key != '':
                # move = 0
                for i in range(len(text)):
                    if text[i] == '\n':
                        final_text += '\n'
                    elif text[i] == ' ':
                        final_text += ' '
                    else:
                        final_text += list(self.dictionary)[(self.dictionary[key[i % key_size]] +
                                                             self.dictionary[text[i]]) % len(self.dictionary)]
                self.output_text.delete(1.0, 'end')
                self.output_text.insert(1.0, final_text)
            else:
                messagebox.showinfo('Key entry is empty', 'Program can\'t operate with empty key')
        else:
            messagebox.showinfo('message entry is empty', 'Program can\'t encipher empty text')

    def decipher(self):
        text = self.input_text.get('1.0', END)
        key = self.input_key.get()
        key_size = len(key)
        final_text = ''
        if text != '\n':
            if key != '':
                move = 0
                for i in range(len(text)):
                    if text[i] == '\n':
                        final_text += '\n'
                    elif text[i] == ' ':
                        final_text += ' '
                    else:
                        final_text += list(self.dictionary)[(self.dictionary[text[i]] -
                                                             self.dictionary[key[i % key_size]]) % len(self.dictionary)]
                self.output_text.delete(1.0, 'end')
                self.output_text.insert(1.0, final_text)
            else:
                messagebox.showinfo('Key entry is empty', 'Program can\'t operate with empty key')
        else:
            messagebox.showinfo('message entry is empty', 'Program can\'t encipher empty text')
