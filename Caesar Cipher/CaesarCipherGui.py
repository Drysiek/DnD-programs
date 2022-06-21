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


class CaesarCipherApp:
    def __init__(self):
        self.dictionary_small = dict()
        self.dictionary_large = dict()
        self.make_dictionary()

        self.window = Tk()
        self.window.title('D&D Caesar Cipher helper')
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
        for i in (65, 260, 66, 67, 262, 68, 69, 280, 70, 71, 72, 73, 74, 75, 76, 321, 77, 78, 323, 79, 211, 80, 81,
                  82, 83, 346, 84, 85, 86, 87, 88, 89, 90, 377, 379):
            self.dictionary_large.update({chr(i): iterator})
            self.dictionary_small.update({chr(i).lower(): iterator})
            iterator += 1

        print(list(self.dictionary_large))
        print(list(self.dictionary_small))

    def encipher(self):
        text = self.input_text.get('1.0', END)
        key = self.input_key.get()
        final_text = ''
        if text != '\n':
            if key.isnumeric():
                key = int(key)
                for i in range(len(text)):
                    if self.dictionary_large.__contains__(text[i]):
                        final_text += list(self.dictionary_large)[(self.dictionary_large[text[i]] + key) %
                                                                  len(self.dictionary_large)]
                    elif self.dictionary_small.__contains__(text[i]):
                        final_text += list(self.dictionary_small)[(self.dictionary_small[text[i]] + key) %
                                                                  len(self.dictionary_small)]
                    else:
                        final_text += text[i]
                self.output_text.delete(1.0, 'end')
                self.output_text.insert(1.0, final_text)
            else:
                messagebox.showinfo('Key entry is has to be a number',
                                    'Program can\'t operate with key that isn\'t a number')
        else:
            messagebox.showinfo('message entry is empty', 'Program can\'t encipher empty text')

    def decipher(self):
        text = self.input_text.get('1.0', END)
        key = self.input_key.get()
        final_text = ''
        if text != '\n':
            if key.isnumeric():
                key = int(key)
                for i in range(len(text)):
                    if self.dictionary_large.__contains__(text[i]):
                        final_text += list(self.dictionary_large)[(self.dictionary_large[text[i]] - key) %
                                                                  len(self.dictionary_large)]
                    elif self.dictionary_small.__contains__(text[i]):
                        final_text += list(self.dictionary_small)[(self.dictionary_small[text[i]] - key) %
                                                                  len(self.dictionary_small)]
                    else:
                        final_text += text[i]
                self.output_text.delete(1.0, 'end')
                self.output_text.insert(1.0, final_text)
            elif key == 'Mimir_the_black':
                self.output_text.delete(1.0, 'end')
                for j in range(32):
                    key = j
                    final_text = ''
                    for i in range(len(text)):
                        if self.dictionary_large.__contains__(text[i]):
                            final_text += list(self.dictionary_large)[(self.dictionary_large[text[i]] - key) %
                                                                      len(self.dictionary_large)]
                        elif self.dictionary_small.__contains__(text[i]):
                            final_text += list(self.dictionary_small)[(self.dictionary_small[text[i]] - key) %
                                                                      len(self.dictionary_small)]
                        else:
                            final_text += text[i]
                    self.output_text.insert(1.0, final_text)
                    self.output_text.insert(1.0, '----------\n')
            else:
                messagebox.showinfo('Key entry is has to be a number',
                                    'Program can\'t operate with key that isn\'t a number')
        else:
            messagebox.showinfo('message entry is empty', 'Program can\'t decipher empty text')
