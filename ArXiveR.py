from Tkinter import *
import tkMessageBox
import tkFileDialog
from papers import papers
import subprocess


class MainApp(Frame):

    def loadPapers(self):
        self.papers = papers()
        self.refreshDirs()
        self.refreshPapers()
    

    def createWidgets(self):
        #add dir
        self.imp_button = Button(self.top_frame, text='Add Path', width = 10,  command=self.openDir)
        self.imp_button.pack(side=RIGHT)

        #update button
        self.update_button = Button(self.top_frame, text='Update',width = 10,  command=self.update)
        self.update_button.pack(side=RIGHT)
        
        self.open_button = Button(self.top_frame, text='Open Paper',width = 10,  command=self.openSelected)
        self.open_button.pack(side=RIGHT)

        self.update_button = Button(self.top_frame, text='BibTex',width = 10,  command=self.openBib)
        self.update_button.pack(side=RIGHT)
        
        #directory list box
        self.dscrollbar = Scrollbar(self.bottom_frame)
        self.dscrollbar.pack(side=LEFT, fill=Y)
        self.dirbox = Listbox(self.bottom_frame, height = 14)
        self.dirbox.pack(side=LEFT)
        self.dirbox.config(yscrollcommand=self.dscrollbar.set)
        self.dscrollbar.config(command=self.dirbox.yview)
        
        #paper list box
        self.pscrollbar = Scrollbar(self.bottom_frame)
        self.pscrollbar.pack(side=LEFT, fill=Y)
        self.paperbox = Listbox(self.bottom_frame, height = 14)
        self.paperbox.bind('<<ListboxSelect>>', self.fSelect)
        self.paperbox.pack(side=LEFT)
        self.paperbox.config(yscrollcommand=self.pscrollbar.set)
        self.pscrollbar.config(command=self.paperbox.yview)

        #paper details
        #output name list
        self.outstrs = ['Title: ','Year: ','Path: ']

        self.scrollbar = Scrollbar(self.bottom_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.txt = Text(self.bottom_frame, wrap=WORD, height=14) # wrap=CHAR, wrap=NONE
        self.txt.pack(expand=1, fill=BOTH)

        self.txt.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.txt.yview)

   
    
    #refresh papers and lists in gui
    def update(self):
        self.papers.update(True)
        self.refreshDirs()
        self.refreshPapers()

    #add a directory to sync
    def openDir(self):
        path = tkFileDialog.askdirectory()
        print self.dirs
        if path == '':
            return
        
        if path in self.dirs:
            tkMessageBox.showwarning('warning', 'Directory already added')
            return   
            
        self.papers.addDir(path)
        self.papers.update()
        self.refreshPapers()
        self.refreshDirs()

    #open paper in pdf viewer
    #TODO set custom pdf viewer/use default 
    def openSelected(self):
        try:
            id = str(self.paperbox.get(self.paperbox.curselection()))
        except Exception as e:
            print e
            tkMessageBox.showwarning('Paper Selection', 'Please select a document')
            return
        fdir = self.papers.findEntry(id)['loc']
        subprocess.call("evince " + fdir, shell=True)
    
    #open bibtex info
    #TODO set custom program to open in
    def openBib(self):
        try:
            bib = self.doc['bib']
        except KeyError as e:
            tkMessageBox.showwarning('Error', 'Not found')
            return
            
        with open("tmp/bib.txt", "w") as ftxt:
            ftxt.write(bib)
        
        subprocess.call("mousepad " + "tmp/bib.txt", shell=True)
            
    #retrieve and display info for selected paper
    def fSelect(self, evt):
        id = str(self.paperbox.get(self.paperbox.curselection()))
        self.doc = self.papers.findEntry(id)

        self.sel_title = self.doc['title'].encode('utf-8')
        self.sel_year = self.doc['year'].encode('utf-8')
        self.sel_dir = self.doc['loc'].encode('utf-8')
        self.sel_list = [self.sel_title, self.sel_year, self.sel_dir]
        
        self.txt.delete(1.0, END)
            
        for x, y in zip(self.outstrs, self.sel_list):
            self.txt.insert(END, x)
            self.txt.insert(END, y)
            self.txt.insert(END, '\n\n')

    #TODO add button for this
    def removeDir(self):
        try:
            dname = str(self.dirbox.get(self.dirbox.curselection()))
        except Exception as e:
            print e
            tkMessageBox.showwarning('Directory Selection', 'Please select a directory')
            return
    

    def refreshDirs(self):
        self.dirs = self.papers.getDirs()
        #clear  box and load in new paths
        self.dirbox.delete(0, END)
            
        for path in self.dirs:
            self.dirbox.insert(END, path)
    

    def refreshPapers(self):
        
        self.pdfs = self.papers.getPapers()
        self.paperbox.delete(0, END)
        
        for pdf in self.pdfs:
            self.paperbox.insert(END, pdf)


    def __init__(self, master=None):    
        Frame.__init__(self, master)
        self.top_frame = Frame(self)
        self.bottom_frame = Frame(self)
        self.createWidgets()
        self.loadPapers()
        self.top_frame.pack(side=TOP)
        self.bottom_frame.pack(side=BOTTOM)
        self.pack()
        
        
#main app window
root = Tk()
root.resizable(0,0)
root.title('ArXiveR')
root.geometry('600x300+200+200')
app = MainApp(master=root)
app.mainloop()
