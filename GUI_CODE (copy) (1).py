# Importing Required libraries & Modules
import os
import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

#defining togglable buttons
class CollapsiblePane(ttk.Frame):
    """
     -----USAGE-----
    collapsiblePane = CollapsiblePane(parent, 
                          expanded_text =[string],
                          collapsed_text =[string])
  
    collapsiblePane.pack()
    button = Button(collapsiblePane.frame).pack()
    """
  
    def __init__(self, parent, expanded_text ="Collapse <<", collapsed_text ="Expand >>"):
  
        ttk.Frame.__init__(self, parent)
  
        # These are the class variable
        # see a underscore in expanded_text and _collapsed_text
        # this means these are private to class
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text
  
        # Here weight implies that it can grow it's
        # size if extra space is available
        # default weight is 0
        self.columnconfigure(1, weight = 1)
  
        # Tkinter variable storing integer value
        self._variable = tk.IntVar()
  
        # Checkbutton is created but will behave as Button
        # cause in style, Button is passed
        # main reason to do this is Button do not support
        # variable option but checkbutton do
        self._button = ttk.Checkbutton(self, variable = self._variable, command = self._activate, style ="TButton")
        self._button.grid(row = 0, column = 0, sticky = NSEW)
  
        # This wil create a seperator
        # A separator is a line, we can also set thickness
        self._separator = ttk.Separator(self, orient ="horizontal")
        self._separator.grid(row = 0, column = 1, sticky ="we")
  
        self.frame = ttk.Frame(self, borderwidth = 2)
  
        # This will call activate function of class
        self._activate()
  
    def _activate(self):
        if not self._variable.get():
  
            # As soon as button is pressed it removes this widget
            # but is not destroyed means can be displayed again
            self.frame.grid_forget()
  
            # This will change the text of the checkbutton
            self._button.configure(text = self._collapsed_text)
  
        elif self._variable.get():
            # increasing the frame area so new widgets
            # could reside in this container
            self.frame.grid(row = 1, column = 0, columnspan = 2)
            self._button.configure(text = self._expanded_text)
  
    def toggle(self):
        """Switches the label frame to the opposite state."""
        self._variable.set(not self._variable.get())
        self._activate()
# Defining TextEditor Class
class TextEditor:
  # Defining Constructor
  def __init__(self,root):
    # Assigning root
    self.root = root
    # Title of the window
    self.root.title("TOOL")
    # Window Geometry
    self.root.geometry("1200x700+200+150")
    # Initializing filename
    self.filename = None
    # Declaring Title variable
    self.title = StringVar()
    # Declaring Status variable
    self.status = StringVar()
    # Creating Titlebar

    # Creating Scrollbar
    scrol_y = Scrollbar(self.root,orient=VERTICAL)
    #creating tool options with collapsible pane
    tooloptions = Frame(root,width=500,height=500,bg='green')
    tooloptions.pack(side= LEFT)
    #needs to be rewriten to be usable multiple times
    
    def open_sra_file():
     global inp_address 
     path_inp = filedialog.askopenfile(initialdir="/")
     inp_address = path_inp.name	  
     path.config(text = inp_address)
    
    def open_adp_file():
     global inp_address 
     path_inp = filedialog.askopenfile(initialdir="/")
     adp_address = path_inp.name	  
     adp_path.config(text = adp_address)
   
    #function to run fastqc needs to be moved to better location 
    def  run_fastqc():
    
       for line in open('Project/CODE/fastqc.txt'):
          if 'fastqc ' in line:
            fline = line
            break;
            
       fline = fline.replace('sra_data', inp_address)
       subprocess.run(fline, shell = True, executable = "bash")
       
       self.txtarea.insert(END,fline)
     
    def  run_deinterleave():
    
       codes = open('Project/CODE/deinterleave.sh')     
       codex = codes.read()

       codex = codex.replace('sra_data', inp_address)
       #is opening this twice creating another pipeline?
       subprocess.run(codex, shell=True, executable="bash")
       codes.close()
       
       self.txtarea.insert(END,codex)    
 
    def  run_trim():
    
       codes = open('Project/CODE/trim.txt')     
       codex = codes.read()
       codex = codex.replace('numb',threads)
       #is opening this twice creating another pipeline?
       subprocess.run(codex, shell=True, executable="bash")
       codes.close()
       
       self.txtarea.insert(END,codex)    

     
    
    def sel_typ1_func(event= None):
       
       if event:
          fm = event.widget.get()
          print(fm)
          if fm =='Interleaved':
             Any = Button(PP.frame, text= "Deinterlace", command = run_deinterleave).grid(column = 0, row = 4)
          
    
    
    #selection function to store selected choice
    def create_sel_type1():
       n1 = tk.StringVar()
       file_type1 = Label(PP.frame, text = "Select format :", font = ("Calibri", 15)).grid(column = 0, row = 1)
       file_type_selection1 = ttk.Combobox(PP.frame, width = 27, textvariable= n1)
       file_type_selection1['values'] = ('Interleaved', 'seperate')
       file_type_selection1.grid(column = 1, row = 1)
       file_type_selection1.bind("<<ComboboxSelected>>", sel_typ1_func) 
    
    def sel_typ_func(event= None):
      
       if event:
          typ = event.widget.get()
          print(typ)
          if typ == 'Paired end':
             create_sel_type1()
    global threads         
    def entry_func(event = None):
    	
    	if event:
           threads = event.widget.get()
           print(threads)
           
        
                 
    #PREPROCESSING INPUTS
    PP = CollapsiblePane(tooloptions, expanded_text= "preprocessing", collapsed_text = "preprocessing")
    PP.grid(column = 0, row = 0, sticky = EW)
    file_type = Label(PP.frame, text = "Select file type :", font = ("Calibri", 15)).grid(column = 0, row = 0)
    n = tk.StringVar()
    
    file_type_selection = ttk.Combobox(PP.frame, width = 27, textvariable= n)
    file_type_selection['values'] = ('Single end', 'Paired end')
    file_type_selection.grid(column = 1, row = 0)
    #var = file_type_selection.current()
    file_type_selection.bind("<<ComboboxSelected>>",sel_typ_func)
     
    btn = Button(PP.frame, text ='select file', command= lambda:open_sra_file())
    path = Label(PP.frame, text = "_")
   
    btn.grid(row = 3,column = 0)
    path.grid(row = 3,column = 1)
    

  
    #FASTQC TOOL OPTIONS  
    FASTQC = CollapsiblePane(tooloptions, expanded_text= "FASTQC", collapsed_text= "FASTQC")
    FASTQC.grid(column = 0, row = 1, sticky = EW)
    ANALYSIS = Button(FASTQC.frame, text= "run fasqc", command = run_fastqc).pack()
    
    #TRIMMING TOOL OPTIONS
    TRIM = CollapsiblePane(tooloptions, expanded_text= "TRIMMOMATIC", collapsed_text= "TRIMMOMATIC")
    TRIM.grid(column = 0, row = 2, sticky = EW)
    no_threads = Label(TRIM.frame, text = "No of threads :", font = ("Calibri", 15)).grid(column = 0, row = 0)
    n = tk.StringVar()
    inp_thr = tk.Entry (TRIM.frame)
    inp_thr.grid(column = 1, row = 0)

    
    inp_thr.bind("<Return>",entry_func)
    
    btn = Button(TRIM.frame, text ='adapter file location :', command= lambda:open_adp_file())
    adp_path = Label(TRIM.frame, text = "_")
    trimming = Button(TRIM.frame, text= "run trimmomatic", command = run_trim).grid(row = 4, column = 0)
   
    btn.grid(row = 3,column = 0)
    adp_path.grid(row = 3,column = 1)
    
    #BOWTIE2 AND SAMTOOLS IN CONTAMINATION REMOVAL OPTIONS
    CONT_R = CollapsiblePane(tooloptions, expanded_text= "Removing Host genome contamination ", collapsed_text= "contamination removal")
    CONT_R.grid(column = 0, row = 3, sticky = EW)
    option1 = Button(CONT_R.frame, text= "option1").pack()
    option2 = Button(CONT_R.frame, text= "option2").pack()
    #QUALITY CHECK AFTER REMOVAL FASTQC
    QC = CollapsiblePane(tooloptions, expanded_text= "quality check after removing contamination (FASTQC)", collapsed_text= "quality check")
    QC.grid(column = 0, row = 4, sticky = EW)
    option1 = Button(QC.frame, text= "option1").pack()
    option2 = Button(QC.frame, text= "option2").pack()
    #TAXONOMIC PROFILING OPTIONS
    TAX_P = CollapsiblePane(tooloptions, expanded_text= "Taxonomic Profiling (KAIJU)", collapsed_text= "Profiling")
    TAX_P.grid(column = 0, row = 5, sticky = EW)
    option1 = Button(TAX_P.frame, text= "option1").pack()
    option2 = Button(TAX_P.frame, text= "option2").pack()
    #ASSEMBLY TOOL OPTIONS
    ASS = CollapsiblePane(tooloptions, expanded_text= "Assembly of reads (MetaSpades)", collapsed_text= "Assembly")
    ASS.grid(column = 0, row = 6, sticky = EW)
    option1 = Button(ASS.frame, text= "option1").pack()
    option2 = Button(ASS.frame, text= "option2").pack()
    #ASSEMBLY TOOL OPTIONS
    ASS_Q = CollapsiblePane(tooloptions, expanded_text= "Quality of assembly", collapsed_text= "Assembly quality")
    ASS_Q.grid(column = 0, row = 7, sticky = EW)
    option1 = Button(ASS_Q.frame, text= "option1").pack()
    option2 = Button(ASS_Q.frame, text= "option2").pack()
    #BINNING TOOL OPTIONS
    BIN = CollapsiblePane(tooloptions, expanded_text= "Binning of sequences", collapsed_text= "binning")
    BIN.grid(column = 0, row = 8, sticky = EW)
    option1 = Button(BIN.frame, text= "option1").pack()
    option2 = Button(BIN.frame, text= "option2").pack()
    #ANNOTATION TOOL OPTIONS
    ANN = CollapsiblePane(tooloptions, expanded_text= "Annotation of genes", collapsed_text= "Annotation")
    ANN.grid(column = 0, row = 9, sticky = EW)
    option1 = Button(ANN.frame, text= "option1").pack()
    option2 = Button(ANN.frame, text= "option2").pack()
    # Creating Text Area
    self.txtarea = Text(self.root,yscrollcommand=scrol_y.set,font=("Courier",10,"bold"),state="normal",relief=GROOVE)
    # Packing scrollbar to root window
    scrol_y.pack( side= RIGHT, fill= Y )
    # Adding Scrollbar to text area
    scrol_y.config(command=self.txtarea.yview)
    # Packing Text Area to root window
    self.txtarea.pack(side= BOTTOM, fill=BOTH,expand=1)
    # Calling shortcuts funtion
    self.shortcuts()
  # Defining settitle function
  def settitle(self):
    # Checking if Filename is not None
    if self.filename:
      # Updating Title as filename
      self.title.set(self.filename)
    else:
      # Updating Title as Untitled
      self.title.set("Untitled")
  # Defining New file Function
  def newfile(self,*args):
    # Clearing the Text Area
    self.txtarea.delete("1.0",END)
    # Updating filename as None
    self.filename = None
    # Calling settitle funtion
    self.settitle()
    # updating status
    self.status.set("New File Created")
  # Defining Open File Funtion
  def openfile(self,*args):
    # Exception handling
    try:
      # Asking for file to open
      self.filename = filedialog.askopenfilename(title = "Select file",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
      # checking if filename not none
      if self.filename:
        # opening file in readmode
        infile = open(self.filename,"r")
        # Clearing text area
        self.txtarea.delete("1.0",END)
        # Inserting data Line by line into text area
        for line in infile:
          self.txtarea.insert(END,line)
        # Closing the file  
        infile.close()
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Opened Successfully")
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Save File Funtion
  def savefile(self,*args):
    # Exception handling
    try:
      # checking if filename not none
      if self.filename:
        # Reading the data from text area
        data = self.txtarea.get("1.0",END)
        # opening File in write mode
        outfile = open(self.filename,"w")
        # Writing Data into file
        outfile.write(data)
        # Closing File
        outfile.close()
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Saved Successfully")
      else:
        self.saveasfile()
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Save As File Funtion
  def saveasfile(self,*args):
    # Exception handling
    try:
      # Asking for file name and type to save
      untitledfile = filedialog.asksaveasfilename(title = "Save file As",defaultextension=".txt",initialfile = "Untitled.txt",filetypes = (("All Files","*.*"),("Text Files","*.txt"),("Python Files","*.py")))
      # Reading the data from text area
      data = self.txtarea.get("1.0",END)
      # opening File in write mode
      outfile = open(untitledfile,"w")
      # Writing Data into file
      outfile.write(data)
      # Closing File
      outfile.close()
      # Updating filename as Untitled
      self.filename = untitledfile
      # Calling Set title
      self.settitle()
      # Updating Status
      self.status.set("Saved Successfully")
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining Exit Funtion
  def exit(self,*args):
    op = messagebox.askyesno("WARNING","Your Unsaved Data May be Lost!!")
    if op>0:
      self.root.destroy()
    else:
      return
  # Defining Cut Funtion
  def cut(self,*args):
    self.txtarea.event_generate("<<Cut>>")
  # Defining Copy Funtion
  def copy(self,*args):
          self.txtarea.event_generate("<<Copy>>")
  # Defining Paste Funtion
  def paste(self,*args):
    self.txtarea.event_generate("<<Paste>>")
  # Defining Undo Funtion
  def undo(self,*args):
    # Exception handling
    try:
      # checking if filename not none
      if self.filename:
        # Clearing Text Area
        self.txtarea.delete("1.0",END)
        # opening File in read mode
        infile = open(self.filename,"r")
        # Inserting data Line by line into text area
        for line in infile:
          self.txtarea.insert(END,line)
        # Closing File
        infile.close()
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Undone Successfully")
      else:
        # Clearing Text Area
        self.txtarea.delete("1.0",END)
        # Updating filename as None
        self.filename = None
        # Calling Set title
        self.settitle()
        # Updating Status
        self.status.set("Undone Successfully")
    except Exception as e:
      messagebox.showerror("Exception",e)
  # Defining About Funtion
  def infoabout(self):
    messagebox.showinfo("About Text Editor","A Simple Text Editor\nCreated using Python.")
  # Defining shortcuts Funtion
  def shortcuts(self):
    # Binding Ctrl+n to newfile funtion
    self.txtarea.bind("<Control-n>",self.newfile)
    # Binding Ctrl+o to openfile funtion
    self.txtarea.bind("<Control-o>",self.openfile)
    # Binding Ctrl+s to savefile funtion
    self.txtarea.bind("<Control-s>",self.savefile)
    # Binding Ctrl+a to saveasfile funtion
    self.txtarea.bind("<Control-a>",self.saveasfile)
    # Binding Ctrl+e to exit funtion
    self.txtarea.bind("<Control-e>",self.exit)
    # Binding Ctrl+x to cut funtion
    self.txtarea.bind("<Control-x>",self.cut)
    # Binding Ctrl+c to copy funtion
    self.txtarea.bind("<Control-c>",self.copy)
    # Binding Ctrl+v to paste funtion
    self.txtarea.bind("<Control-v>",self.paste)
    # Binding Ctrl+u to undo funtion
    self.txtarea.bind("<Control-u>",self.undo)
# Creating TK Container
root = Tk()
# Passing Root to TextEditor Class
TextEditor(root)
# Root Window Looping
root.mainloop()
