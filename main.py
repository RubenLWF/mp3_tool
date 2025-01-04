import os
import glob
from io import BytesIO
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
from tkinter import Label, Entry, Tk, Frame, Listbox, Button, messagebox, Scrollbar, filedialog as fd


def get_mp3_files():
    files = []
    os.chdir(r'./audio')
    for file in glob.glob('*.mp3'):
        files.append(file)

    return files


def handle_select(e=None):
    cs = list_box.curselection()
    filename = list_box.get(cs)

    audio = MP3(filename, ID3=ID3)

    modify_window(audio)


def modify_window(audio):
    tags = audio.tags

    modify = Tk()
    modify.title('Modify metadata')
    modify.geometry('300x430')
    modify.resizable(False, False)

    icon = ImageTk.PhotoImage(file='../assets/icon.png', master=modify)
    modify.iconphoto(False, icon)

    # Title
    title_label = Label(modify, text='Title:')
    title_label.pack()
    title_entry_frame = Frame(modify, padx=25)
    title_entry_frame.pack(fill='x', expand=True)
    title_entry = Entry(title_entry_frame, background='lightgrey')

    try:
        title_entry.insert(0, tags.get('TIT2'))
    except:
        pass

    title_entry.pack(fill='x', expand=True)

    # Artist
    artist_label = Label(modify, text='Artist:')
    artist_label.pack()
    artist_entry_frame = Frame(modify, padx=25)
    artist_entry_frame.pack(fill='x', expand=True)
    artist_entry = Entry(artist_entry_frame, background='lightgrey')

    try:
        artist_entry.insert(0, tags.get('TPE1'))
    except:
        pass

    artist_entry.pack(fill='x', expand=True)

    # Image
    image_label = Label(modify, text='Image:')
    image_label.pack()

    try:
        img = Image.open(BytesIO(tags.get('APIC:').data))
        img = img.resize((250, 250), Image.LANCZOS)
    except:
        img = Image.open('../assets/no_image.png')
        img = img.resize((250, 250), Image.LANCZOS)

    img = ImageTk.PhotoImage(img, master=modify)
    image_image = Label(modify, image=img)
    image_image.pack()

    image_entry = Entry(modify)

    def select_file():
        image_name = fd.askopenfilename(
            title='Pick an image',
            initialdir='/img',
            filetypes=[(('PNG', '*.png'))])

        if not image_name:
            return

        new_img = ImageTk.PhotoImage(Image.open(image_name).resize(
            (250, 250), Image.LANCZOS), master=modify)

        image_image.configure(image=new_img)
        image_image.image = new_img

        image_entry.insert(0, image_name)

    image_button_frame = Frame(modify)
    image_button_frame.pack(pady=5)

    image_button = Button(image_button_frame,
                          text='Select image...', command=select_file, background='lightgray')
    image_button.pack()

    # Update button

    def update():
        title = title_entry.get()
        artist = artist_entry.get()
        image = image_entry.get()

        try:
            audio.add_tags()
        except:
            pass

        audio.tags['TIT2'] = TIT2(encoding=0, text=[title])
        audio.tags['TPE1'] = TPE1(encoding=0, text=[artist])

        if image:
            audio.tags.add(APIC(encoding=0, mime='image/png',
                           type=3, data=open(image, 'rb').read()))

        audio.save()

        modify.destroy()
        messagebox.showinfo('Success', 'Tags have been updated')

    update_button_frame = Frame(modify)
    update_button_frame.pack(pady=5)

    update_button = Button(update_button_frame, text='Update tags', command=update, font=(
        'Arial', 10, 'bold'), background='lightgray')
    update_button.pack()

    modify.mainloop()


if __name__ == '__main__':
    root = Tk()
    root.title('MP3 Tag Editor')
    root.geometry('300x300')

    icon = ImageTk.PhotoImage(file='./assets/icon.png')
    root.iconphoto(False, icon)

    select_button_frame = Frame(root)
    select_button_frame.pack(pady=5)

    select_button = Button(select_button_frame,
                           text='Select file', command=handle_select)
    select_button.pack()

    scroll_frame = Frame(root)
    scroll_frame.pack(fill='both', expand=True)

    list_box = Listbox(scroll_frame, cursor='hand2')
    list_box.pack(side='left', fill='both', expand=True)
    for i, file in enumerate(get_mp3_files()):
        list_box.insert(i, file)

    list_box.bind('<Double-1>', handle_select)

    scrollbar = Scrollbar(scroll_frame, orient='vertical')
    scrollbar.config(command=list_box.yview)
    scrollbar.pack(side='right', fill='y')

    list_box.config(yscrollcommand=scrollbar.set)

    root.mainloop()
