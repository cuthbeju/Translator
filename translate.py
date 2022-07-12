from tkinter import *
import googletrans
import textblob
from tkinter import ttk, messagebox

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
root.configure(background="LightSkyBlue1")
root.title('Translator')
root.geometry("1395x640")

# get language list from GoogleTrans
languages = googletrans.LANGUAGES
language_list = list(languages.values())

l1 = Label(root, text="How to use:\n 1. Choose language to translate from.\n 2. Type/Paste text to translate.\n"
                      "3. Choose language to translate to.\n 4. Click 'translate' button to get translation. \n"
                      "5. Click 'clear' button to start a new translation.")
l1.grid(row=6, column=1, padx=20, pady=20)


def clear():
    # show alert to confirm choice to clear text boxes
    clear_text = messagebox.askyesno(title='Warning', message='Are you sure you want to clear this translation?')
    # clear the text boxes if user confirms to clear translations
    if clear_text:
        from_text.delete(1.0, END)
        to_text.delete(1.0, END)


def translate_text():
    # delete previous translations
    to_text.delete(1.0, END)
    try:
        # get languages from dictionary keys
        # get the from language key
        for key, value in languages.items():
            if value == from_combo.get():
                from_key = key

        # get the to language key
        for key, value in languages.items():
            if value == to_combo.get():
                to_key = key

        # turn original Text into a TextBlob
        text = textblob.TextBlob(from_text.get(1.0, END))

        # translate text
        text = text.translate(from_lang=from_key, to=to_key)

        # output translated text to screen
        to_text.insert(1.0, text)

    except Exception as e:
        messagebox.showerror("translator", e)


# text box for original text
from_text = Text(root, height=20, width=50)
from_text.grid(row=0, column=0, pady=20, padx=10)
from_text.configure(font=('Sans Serif', 16))

# translate button
translate_button = Button(root, text='Translate', font=('Sans Serif', 40), command=translate_text)
translate_button.grid(row=0, column=1, padx=10)

# text box for translated text
to_text = Text(root, height=20, width=50)
to_text.grid(row=0, column=2, pady=20, padx=10)
to_text.configure(font=('Sans Serif', 16))

# from language combo box
l_from = Label(root, text="Translate from: ")
l_from.grid(row=1, column=0)
from_combo = ttk.Combobox(root, width=50, value=language_list)
from_combo.current(21)
from_combo.grid(row=2, column=0)

# to language combo box
l_to = Label(root, text="Translate to: ")
l_to.grid(row=1, column=2)
to_combo = ttk.Combobox(root, width=50, value=language_list)
to_combo.current(21)
to_combo.grid(row=2, column=2)

# clear button
clear_button = Button(root, text="Clear", font=('Sans Serif', 24), command=clear)
clear_button.grid(row=5, column=1)


root.mainloop()


