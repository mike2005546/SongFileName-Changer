from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import logging
import fnmatch
from tinytag import TinyTag


class Music:
    def __init__(self, input_location=None, music_file_name=None, music_file_location=None, music_track_name=None,
                 music_file_type=None):
        self.input_location = input_location
        self.music_file_name = music_file_name
        self.music_file_location = music_file_location
        self.music_file_type = music_file_type
        self.music_track_name = music_track_name
        self.music_file_list = (".flac", ".m4a", ".wav", ".mp3", ".aac", ".mp4", ".wma")

    def get_music_info(self, music_location):
        if os.path.splitext(music_location)[1] in self.music_file_list:
            self.input_location = music_location
            self.music_file_name = os.path.splitext(os.path.basename(music_location))[0]
            self.music_file_type = os.path.splitext(music_location)[1]
            self.music_file_location = os.path.dirname(music_location)
            tag = TinyTag.get(music_location)
            self.music_track_name = tag.title
        else:
            print("This is not a music file!")


root = Tk()
root.title("Name Changer")
root.geometry("1000x300")
root.resizable(0, 0)


# menu
def add_files():
    m = Music()
    file_dirs = filedialog.askopenfilename(initialdir="C:/Users/MikE/Desktop", title="Select File",
                                           filetypes=(("Music Files", "*.flac;*.m4a;*.wav;*.mp3;*.aac;*.mp4;*.wma"),
                                                      ("All Files", "*.*")), multiple=True)
    if file_dirs != "":
        for file_dir in file_dirs:
            m.get_music_info(file_dir)
            if m.music_track_name is not None:
                tree.insert("", "end", values=(m.music_file_name, m.music_track_name, m.music_file_type,
                                               m.music_file_location))
            else:
                print("There is no track name!")
        btn1['state'] = NORMAL
        btn2['state'] = NORMAL
    else:
        print("Canceled.")


def add_file_directory():
    m = Music()
    directory = filedialog.askdirectory()

    if directory != "":
        for file in os.listdir(directory):
            for types in m.music_file_list:
                if fnmatch.fnmatch(file, "*" + types):
                    file_dir = directory + "/" + file
                    m.get_music_info(file_dir)
                    if m.music_track_name is not None:
                        tree.insert("", "end", values=(m.music_file_name, m.music_track_name, m.music_file_type,
                                                       m.music_file_location))
                    else:
                        print("There is no track name!")
                btn1['state'] = NORMAL
                btn2['state'] = NORMAL
    else:
        print("Canceled.")


menu_bar = Menu(root)
root.config(menu=menu_bar)
menu1 = Menu(menu_bar, tearoff=0)
menu1.add_command(label="Add Files", command=add_files)
menu1.add_command(label="Add File Directory", command=add_file_directory)
menu1.add_separator()
menu1.add_command(label="Exit", command=root.quit)

menu_bar.add_cascade(label="File", menu=menu1)


# Treeview
tree = ttk.Treeview(root, columns=["1", "2", "3", "4"], show="headings")
tree.column("1", width=170, minwidth=170, stretch=NO)
tree.column("2", width=170, minwidth=170, stretch=NO)
tree.column("3", width=60, minwidth=60, stretch=NO)
tree.column("4", width=600, minwidth=600, stretch=NO)

tree.heading("1", text="File Name", anchor=W)
tree.heading("2", text="Track Name", anchor=W)
tree.heading("3", text="File Type", anchor=W)
tree.heading("4", text="Directory", anchor=W)

tree.pack(side=TOP, fill=X)


# Button
def clear_all():
    tree.delete(*tree.get_children())
    btn1['state'] = DISABLED
    btn2['state'] = DISABLED


def change_name():
    for child in tree.get_children():
        location = tree.item(child)["values"][3]
        file_name = tree.item(child)["values"][0]
        track_name = tree.item(child)["values"][1]
        file_type = tree.item(child)["values"][2]
        try:
            os.renames(location + "/" + str(file_name) + file_type, location + "/" + track_name + file_type)
        except Exception as e:
            logging.exception(e)
    print("Done!")
    tree.delete(*tree.get_children())
    btn1['state'] = DISABLED
    btn2['state'] = DISABLED


btn1 = Button(root, text='Change Name', state=DISABLED, width=15, height=2, command=change_name)
btn1.pack(padx=20, pady=14, anchor=NW, side=LEFT)

btn2 = Button(root, text="Clear All", state=DISABLED, width=15, height=2, command=clear_all)
btn2.pack(pady=14, anchor=NW, side=LEFT)


def main():
    root.mainloop()


if __name__ == '__main__':
    main()
