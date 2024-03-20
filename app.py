from tkinter import (Tk, Button, filedialog, PanedWindow, HORIZONTAL, END,
                     messagebox, Checkbutton, IntVar, PhotoImage)
from merger import Merger
from smlistbox import SmartListbox
from favicon import icon_b64

# with open('favicon.png', 'rb') as file:
#     icon_converted = base64.b64encode(file.read())

# with open('favicon.txt', 'wb') as file:
#     file.write(icon_converted)


class App(Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk",
                 useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.render_ui()

    def render_ui(self):
        self.geometry('500x400')
        self.title('PDF merge')
        self.grid_columnconfigure(0, weight=1)
        self.iconphoto(False, PhotoImage(data=icon_b64))

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
