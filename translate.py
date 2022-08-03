from tkinter import *
from tkinter import ttk, messagebox
import googletrans
import textblob
import pika
import json
import time

# adapted from: https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/translate.py
# date of retrieval: 07/01/22
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
root.configure(background="LightSkyBlue1")
root.title('Translator')
root.geometry("1250x780")

# get language list from GoogleTrans
languages = googletrans.LANGUAGES
language_list = list(languages.values())


def clear():
    """
    Clears the from_text and to_text text boxes.
    """
    # show alert to confirm choice to clear text boxes
    clear_text = messagebox.askyesno(title='Warning', message='Are you sure you want to clear this translation?')
    # clear the text boxes if user confirms to clear translations
    if clear_text:
        from_text.delete(1.0, END)
        to_text.delete(1.0, END)


def clear_from(event):
    """
    Clears initial text in from_text text box when the from_text text box is clicked.
    """
    from_text.configure(state=NORMAL)
    from_text.delete(1.0, END)
    from_text.unbind('<Button-1>', clicked)


def send_request():
    """
    Sends request to Random Sentence Generator Microservice using RabbitMQ.
    """
    # adapted from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html
    # date of retrieval: 08/02/22
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='get_sentence')

    channel.basic_publish(exchange='', routing_key='get_sentence', body='get_sentence')
    print(" [x] Sent 'get_sentence'")
    connection.close()
    time.sleep(3.0)
    get_rand_sentence()


def reformat_string(string):
    """
    Returns original string with quotation marks replaced with spaces, curly brackets removed, and the word 'result'
    removed.
    """
    trans_table = string.maketrans('"', ' ', "{}")
    string = string.translate(trans_table)
    string_final = string.replace('result : ', "")
    return string_final


def get_rand_sentence():
    """
    Reads JSON file containing JSON string returned from Random Sentence Generator microservice, re-formats string,
    and inserts string into demo_text text box.
    """
    # adapted from: https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
    # date of retrieval: 08/02/22
    with open('sentence.json', 'r') as openfile:
        # reading from json file
        json_object = json.load(openfile)

    rand_sentence = reformat_string(json_object)

    # delete previous text in demo_text box
    demo_text.delete(1.0, END)
    demo_text.insert(END, rand_sentence)


def copy_text():
    """
    Copies text in demo_text text box to clipboard.
    """
    # adapted from: https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard
    # date of retrieval: 08/02/22
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(demo_text.get(1.0, END))
    r.update()
    r.destroy()


def translate_text():
    """
    Translates text in from_text text box to language selected by user and inserts translation in to_text text box.
    Returns an error if the text input in from_text text box is invalid or if the user did not choose a different
    language to translate to.
    """
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

    except Exception:
        messagebox.showerror("translator", """There was an error processing your translation. Make sure that:\n\n 
        1. Your input was valid.\n 2. You have selected a different language to translate to.""")


# text box for original text
from_text = Text(root, height=20, width=50, wrap=WORD)
from_text.grid(row=0, column=0, pady=20, padx=10)
from_text.configure(font=('Sans Serif', 16))
from_text.insert('end', 'Type/Paste text to translate...')
clicked = from_text.bind('<Button-1>', clear_from)

# translate button
translate_button = Button(root, text='Translate', font=('Sans Serif', 40), command=translate_text)
translate_button.grid(row=0, column=1, padx=10)

# text box for translated text
to_text = Text(root, height=20, width=50, wrap=WORD)
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
clear_button = Button(root, text="Clear Translation", font=('Sans Serif', 24), command=clear)
clear_button.grid(row=6, column=1)

# text box for translator instructions
message = "How to use:\n\n 1. Choose language to translate from.\n 2. Type/Paste text to translate.\n 3. Choose " \
          "language to translate to.\n 4. Click 'translate' button to get translation.\n 5. Click 'clear' button to " \
          "start a new translation."
instructions_text = Text(root, height=10, width=40)
instructions_text.grid(row=8, column=2)
instructions_text.insert('end', message)
instructions_text.config(state='disabled')
instructions_text.configure(font=('Sans Serif', 16))

# text box for demo text
demo_text = Text(root, height=10, width=40, wrap=WORD)
demo_text.insert(END, 'Just demoing the translator? Click "Generate Random Sentence" to generate a random English '
                      'sentence and then copy and paste the generated text in the text box above...')
demo_text.grid(row=8, column=0)
demo_text.configure(font=('Sans Serif', 16), fg='gray')

# generate random sentence button
generate_rand_sentence_button = Button(root, text="Generate Random Sentence", font=('Sans Serif', 20),
                                       command=send_request)
generate_rand_sentence_button.grid(row=7, column=0, padx=10, pady=10)

# copy text button
copy_button = Button(root, text="Copy Random Sentence", font=('Sans Serif', 20), command=copy_text)
copy_button.grid(row=9, column=0, padx=10, pady=10)

root.mainloop()
