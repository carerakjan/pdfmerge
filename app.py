from tkinter import Tk, Label, Button, filedialog, Listbox, PanedWindow, HORIZONTAL, CENTER, END, messagebox
from merger import Merger
import shutil

class App(Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.renderUI()
        self.pdf_files = None

    def renderUI(self):
        self.geometry('500x400')
        self.title('PDF merge')
        self.grid_columnconfigure(0, weight=1)

        top = PanedWindow(self, orient=HORIZONTAL, height=50, background='red')
        top.grid(sticky='we')


        self.button = Button(top, text='Add files', command=self.__open_dialog)
        
        self.button.place(relx=0, rely=0.5, anchor='w')
     
        self.listbox = Listbox(self, height=18)
        self.listbox.grid(sticky='wens')

        self.merge_button = Button(self, text='Merge', command=self.__save_dialog)
        self.merge_button.grid(sticky='w')

    def __save_dialog(self):
        self.title('PDF merge: PROCESSING...')
        if self.pdf_files:
            merger = Merger()
            output_file = filedialog.asksaveasfilename(initialfile='result', defaultextension='.pdf', filetypes=[('PDF files', '*.pdf')])
            if output_file:
                merger.merge_pdfs(self.pdf_files)
                merger.write_to_file(output_file)
                messagebox.showinfo('Result', 'Done!')
            else:
                messagebox.showwarning('Canceled', 'Merge is not completed')
            merger.close()
        else:
            messagebox.showerror('Canceled', 'No one files selected')

        self.title('PDF merge')
   

    def __open_dialog(self, *_):
        files = self.pdf_files = filedialog.askopenfilenames(filetypes=[('PDF files', '*.pdf')])
        self.listbox.delete(0, END)
        if files:
            for i, f in enumerate(files):
                self.listbox.insert(i, f)
