import os
import glob
from io import BytesIO
from PIL import Image, ImageTk
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1
from tkinter import Label, Entry, Tk, Listbox, Button, messagebox, BOTH, filedialog as fd


def get_mp3_files():
    files = []
    os.chdir(r'./audio')
    for file in glob.glob('*.mp3'):
        files.append(file)

    return files


def handle_select(e):
    cs = Lb.curselection()
    filename = Lb.get(cs)

    audio = MP3(filename, ID3=ID3)

    modify_window(audio)


def modify_window(audio):
    tags = audio.tags

    modify = Tk()
    modify.title('Modify metadata')
    modify.geometry('300x450')

    # Title
    title_label = Label(modify, text='Title:')
    title_label.pack()
    title_entry = Entry(modify)
    try:
        title_entry.insert(0, tags.get('TIT2'))
    except:
        pass

    title_entry.pack()

    # Artist
    artist_label = Label(modify, text='Artist:')
    artist_label.pack()
    artist_entry = Entry(modify)

    try:
        artist_entry.insert(0, tags.get('TPE1'))
    except:
        pass

    artist_entry.pack()

    # Image
    image_label = Label(modify, text='Image:')
    image_label.pack()

    try:
        img = Image.open(BytesIO(tags.get('APIC:').data))
        img = img.resize((250, 250), Image.LANCZOS)
    except:
        img = Image.open('../img/no_image.png')
        img = img.resize((250, 250), Image.LANCZOS)

    img = ImageTk.PhotoImage(img, master=modify)
    image_image = Label(modify, image=img)
    image_image.pack()

    image_entry = Entry(modify)
    image_entry.pack()


    def select_file():
        image_name = fd.askopenfilename(
            title='Pick an image',
            initialdir='/img',
            filetypes=[(("PNG", "*.png"))])
        
        if not image_name:
            return

        new_img = ImageTk.PhotoImage(Image.open(image_name).resize(
            (250, 250), Image.LANCZOS), master=modify)

        image_image.configure(image=new_img)
        image_image.image = new_img

        image_entry.insert(0, image_name)
        

    image_button = Button(modify, text='Select image', command=select_file)
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


    update_button = Button(modify, text='Update tags', command=update)
    update_button.pack()

    modify.mainloop()


if __name__ == '__main__':
    root = Tk()
    root.title('MP3 Tag Editor')
    root.geometry('300x300')

    Lb = Listbox(root)
    for i, file in enumerate(get_mp3_files()):
        Lb.insert(i, file)

    Lb.bind('<Double-1>', handle_select)

    Lb.pack(fill=BOTH, expand=1)

    root.mainloop()
