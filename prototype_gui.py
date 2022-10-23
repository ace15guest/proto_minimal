import os
import pickle
import shutil
import tkinter
from tkinter import Tk, Listbox, StringVar, Entry, Button, IntVar, Checkbutton, END
from build import generated_folder_check

# Project Imports
from PrototypeOperations.makes import printex

try:
    shutil.rmtree("./generated/pdfs/temp")
    os.makedirs("./generated/pdfs/temp")
except:
    os.makedirs("./generated/pdfs/temp")


class ProtoGui:

    def __init__(self, root=Tk()):
        self.approve_proto_b = None
        self.html = []
        self.failed_latex = []
        self.root = root
        self.root.geometry("650x755")
        self.root.configure(bg='blue')
        self.root.resizable(False, True)
        # Initialize Lists
        self.proto_opt_list = []

        self.open_pdfs()
        self.add_old_comments = False
        self.scroll_proto()
        self.option_menu()

        self.EDITOR = os.environ.get('EDITOR', 'gvim')
        self.root.mainloop()

    # Build the Screen
    def scroll_proto(self):
        self.listbox = Listbox(self.root, width=30, height=40, bg='white', bd=0)
        self.listbox.place(x=0, y=30)
        # self.listbox.bind("<<ListboxSelect>>",)
        self.entr_string = StringVar()
        self.search_box = Entry(self.root, textvariable=self.entr_string)
        self.search_box.place(x=0, y=0)

        self.search_box.bind('<KeyRelease>', self.cb_search)

        self.root.update_idletasks()

    def option_menu(self):
        write_encyclo_pdf = Button(self.root, text="Write Encyclopedia PDFs", command=self.make_encyclopedia, width=25)
        write_encyclo_pdf.place(x=240, y=0)
        proto_inspector = Button(self.root, text="prototype inspector", command=self.prototype_inspector, width=25)
        proto_inspector.place(x=240, y=30)
        generate_cifs = Button(self.root, text="generate cifs", command=self.make_cif_files, width=25)
        generate_cifs.place(x=240, y=60)
        generate_html = Button(self.root, text="Generate HTML", command=self.make_html, width=25)
        generate_html.place(x=240, y=90)
        match_cifs = Button(self.root, text="Match cifs to prototypes", command=self.match_cifs_to_proto, width=25)
        match_cifs.place(x=240, y=120)

        self.pull_option_var = IntVar()
        self.pull_option = Checkbutton(self.root, variable=self.pull_option_var, text="show webpages", onvalue=1,
                                       offvalue=0)
        self.pull_option.place(x=465, y=35)

    # Initializers
    def open_pdfs(self):
        os.system('open ./generated/pdfs/123_proto_page.pdf')
        os.system('open ./generated/pdfs/proto_page.pdf')

    # Button Functions
    def cb_search(self, event):

        sstr = self.entr_string.get()
        self.listbox.delete(0, END)
        # If filter removed show all data
        if sstr == "":
            for val in self.successful:  # Puts items back in the list
                self.listbox.insert(END, val[0])

        filtered_data = list()
        for item in self.successful:
            item = item[0]
            try:
                if item.find(sstr) == 0:
                    filtered_data.append(item)
            except AttributeError:
                pass
        self.fill_listbox(filtered_data)

    def make_encyclopedia(self):
        # name_of_folder_pdfs = fd.askdirectory()

        name_of_folder_pdfs = "./generated/pdfs/"
        if not os.path.exists(name_of_folder_pdfs):
            generated_folder_check()

        pickle_in = open("essential_data/pickle/prototype.pickle", "rb")
        self.successful = pickle.load(pickle_in)
        options = [s[0] for s in self.successful]
        # p_map(partial(write_encyclopedia_util, name_of_folder_pdfs, self.failed_latex), options)

        # p_map(partial(printex, directory=name_of_folder_pdfs), options)

        for option in options:
            printex(option, name_of_folder_pdfs, self.failed_latex)
        pickle_out = open("essential_data/failed_latex.pickle", "wb")
        pickle.dump(self.failed_latex, pickle_out)
        pickle_out.close()
        for o in options:
            self.write_encyclopedia_util(o, name_of_folder_pdfs)

    def prototype_inspector(self):
        pass

    def make_cif_files(self):
        pass

    def make_html(self):
        pass

    def match_cifs_to_proto(self):
        pass



ProtoGui()
