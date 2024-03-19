import sys
from tkinter import (Tk, Button, filedialog, Listbox, PanedWindow, HORIZONTAL, END,
                     messagebox, Checkbutton, IntVar, Menu)
from typing import List
from merger import Merger


class Dragger:
    def __init__(self, items: List[str] = []):
        self.items = items

    def move(self, old_pos: int, new_pos: int):
        if old_pos >= 0 and new_pos >= 0:
            next_items = [it for i, it in enumerate(self.items) if i != old_pos]
            next_items.insert(new_pos, self.items[old_pos])
            self.items = next_items


class SmartListbox(Listbox):
    def __init__(self, *args, disable_flag=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.menu = Menu(self, tearoff=0)
        self.menu.add_command(label="Delete", command=self.delete_item)
        self.bind('<Button-2>' if sys.platform == 'darwin' else '<Button-3>', self.show_menu)
        self.bind('<B1-Motion>', self.mouse_btn1_motion)
        self.bind('<ButtonRelease-1>', self.mouse_btn1_release)
        self.prev_pos = tuple()
        self.disable_flag = disable_flag or IntVar()

    def insert_items(self, items):
        self.delete(0, END)
        for i, it in enumerate(items):
            self.insert(i, it)

    def show_menu(self, event):
        cur_pos = self.curselection()

        if not cur_pos:
            return

        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def delete_item(self, *_):
        cur_pos = self.curselection()
        if cur_pos:
            items = self.get(0, END)
            items = [it for i, it in enumerate(items) if i != cur_pos[0]]
            self.insert_items(items)

    def mouse_btn1_motion(self, *_):
        cur_pos = self.curselection()
        prev_pos = self.prev_pos

        if not self.disable_flag.get():
            return

        if len(prev_pos) > 0 and len(cur_pos) > 0:
            if abs(cur_pos[0] - prev_pos[0]) == 1:
                dragger = Dragger(self.get(0, END))
                dragger.move(prev_pos[0], cur_pos[0])
                self.insert_items(dragger.items)
                self.selection_set(cur_pos[0])

        self.config(cursor='exchange')
        self.prev_pos = cur_pos

    def mouse_btn1_release(self, *_):
        self.config(cursor='arrow')
        self.prev_pos = tuple()


class App(Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk",
                 useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.render_ui()

    def render_ui(self):
        self.geometry('500x400')
        self.title('PDF merge')
        self.grid_columnconfigure(0, weight=1)

        top = PanedWindow(self, orient=HORIZONTAL, height=50)
        top.grid(sticky='we')

        self.button = Button(top, text='Add files', command=self.open_dialog)
        self.button.place(relx=0, rely=0.5, anchor='w')

        checkbox_var = IntVar()
        self.checkbox = Checkbutton(top, text='Rearrange items', variable=checkbox_var)
        self.checkbox.pack()
        self.chekbox_checked = checkbox_var.get()

        def get_state(*_):
            self.chekbox_checked = int(not checkbox_var.get())
            self.listbox.configure(state='disabled' if not self.chekbox_checked else 'normal')

        self.checkbox.bind('<Button-1>', get_state)

        self.listbox = SmartListbox(self, height=18, disable_flag=checkbox_var)
        self.listbox.grid(sticky='wens')

        bottom = PanedWindow(self, orient=HORIZONTAL, height=50)
        bottom.grid(sticky='we')

        self.merge_button = Button(bottom, text='Merge', command=self.save_dialog)
        self.merge_button.place(relx=0, rely=0.5, anchor='w')

    def save_dialog(self, *_):
        self.title('PDF merge: PROCESSING...')
        pdf_files = self.listbox.get(0, END)

        if pdf_files:
            output_file = filedialog.asksaveasfilename(initialfile='result', defaultextension='.pdf',
                                                       filetypes=[('PDF files', '*.pdf')])
            if output_file:
                merger = Merger(pdf_files=pdf_files)
                merger.write_to_file(output_file)
                merger.close()
                messagebox.showinfo('Result', 'Done!')
            else:
                messagebox.showwarning('Canceled', 'Merge is not completed')
        else:
            messagebox.showerror('Canceled', 'No one files selected')

        self.title('PDF merge')

    def open_dialog(self, *_):
        files = filedialog.askopenfilenames(filetypes=[('PDF files', '*.pdf')])

        if files:
            self.listbox.configure(state='normal')
            self.listbox.insert_items(files)
            self.listbox.configure(state='disabled' if not self.chekbox_checked else 'normal')
