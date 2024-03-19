from tkinter import Tk, Button, filedialog, Listbox, PanedWindow, HORIZONTAL, END, messagebox
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

class DraggableListbox(Listbox):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dragger = Dragger()
        self.bind('<B1-Motion>', self.mouse_btn1_motion)
        self.bind('<ButtonRelease-1>', self.mouse_btn1_release)
        self.prev_pos = tuple()

    def insert_items(self, items):
        self.delete(0, END)
        for i, it in enumerate(items):
            self.insert(i, it)

    def mouse_btn1_motion(self, *_):
        cur_pos = self.curselection()
        prev_pos = self.prev_pos

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
    
class App(Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.renderUI()

    def renderUI(self):
        self.geometry('500x400')
        self.title('PDF merge')
        self.grid_columnconfigure(0, weight=1)

        top = PanedWindow(self, orient=HORIZONTAL, height=50, background='red')
        top.grid(sticky='we')

        self.button = Button(top, text='Add files', command=self.open_dialog)        
        self.button.place(relx=0, rely=0.5, anchor='w')
     
        self.listbox = DraggableListbox(self, height=18)
        self.listbox.grid(sticky='wens')
  
        self.merge_button = Button(self, text='Merge', command=self.save_dialog)
        self.merge_button.grid(sticky='w')

    def save_dialog(self, *_):
        self.title('PDF merge: PROCESSING...')
        pdf_files = self.listbox.get(0, END)

        if pdf_files:
            merger = Merger()
            output_file = filedialog.asksaveasfilename(initialfile='result', defaultextension='.pdf', filetypes=[('PDF files', '*.pdf')])
            if output_file:
                merger.merge_pdfs(pdf_files)
                merger.write_to_file(output_file)
                messagebox.showinfo('Result', 'Done!')
            else:
                messagebox.showwarning('Canceled', 'Merge is not completed')
            merger.close()
        else:
            messagebox.showerror('Canceled', 'No one files selected')

        self.title('PDF merge')

    def open_dialog(self, *_):
        files = filedialog.askopenfilenames(filetypes=[('PDF files', '*.pdf')])
        
        if files:
            self.listbox.insert_items(files)
