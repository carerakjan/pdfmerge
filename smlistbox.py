import sys
from tkinter import Listbox, Menu, IntVar, END


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
                self.rearrange_items(prev_pos[0], cur_pos[0])
                self.selection_set(cur_pos[0])

        self.config(cursor='fleur')
        self.prev_pos = cur_pos

    def mouse_btn1_release(self, *_):
        self.config(cursor='arrow')
        self.prev_pos = tuple()

    def rearrange_items(self, old_pos: int, new_pos: int):
        if old_pos >= 0 and new_pos >= 0:
            items = self.get(0, END)
            next_items = [it for i, it in enumerate(items) if i != old_pos]
            next_items.insert(new_pos, items[old_pos])
            self.insert_items(next_items)
