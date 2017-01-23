'''
Created on Jan 20, 2017

@author: nicky
'''
import Tkinter as tk
import os
import tkFileDialog
import subprocess

class mirror_directory(object):
    '''
    classdocs
    '''
    def __init__(self, master):
        '''
        Constructor
        '''
        self.start=0
        self.lst = []
        self.init_gui(master)
        
    def init_gui(self, master):
        self.master = master
        master.title("Mirror directory")
        # close button
        self.close_button = tk.Button(master, text="close", command = master.quit)
        self.close_button.pack(side=tk.BOTTOM)
        # label for mirror directory
        self.mirror_dir = os.getcwd()
        mirrorDirLabel = tk.Label(master, text="Mirror this directory:")
        mirrorDirLabel.pack(anchor="w")
        self.current_mirror_dir = tk.Label(master, bg="white", text = self.mirror_dir)
        self.current_mirror_dir.pack(anchor="w", padx=5)  
        #browser to choose mirror directory
        self.choose_mirror_directory_button = tk.Button(master, text="Browse", command=lambda: self.choose_directory("mirror"))
        self.choose_mirror_directory_button.pack(anchor="center", pady=(0,10))
        self.mirror_dir_opt = options = {}
        options["initialdir"] = os.getcwd()
        options["mustexist"] = True
        # label for output directory
        self.output_dir = os.getcwd()
        outputDirLabel = tk.Label(master, text="Output directory:")
        outputDirLabel.pack(anchor="w")
        self.current_output_dir = tk.Label(master, bg="white", text=self.output_dir)
        self.current_output_dir.pack(anchor="w", padx=5)
        # browser to choose output directory
        self.choose_output_directory_button = tk.Button(master, text="Browse", command=lambda: self.choose_directory("output"))
        self.choose_output_directory_button.pack(anchor='center', pady=(0,10))
        self.output_dir_opt = options
        # start process
        self.start_button = tk.Button(master, text="start", command = lambda: self.mirror(self.mirror_dir))
        self.start_button.pack(side=tk.BOTTOM, pady=(10,0))
        
    def mirror(self, dirname):
        try:
            for sub in os.listdir(dirname):
                path = os.path.join(dirname, sub)
                # if the current item is a directory, recurse
                if os.path.isdir(path):
                    self.mirror(path)
                # else, here's a file to check
                else:
                    self.lst.append(path)
        # this only happens if we don't have permissions to files
        except OSError as e:
            print(e)
        if dirname==self.mirror_dir:
            self.mirror_files(self.lst)
            
    def mirror_files(self, lst):
        for tup in lst:
            filepath = tup
            base_name = os.path.basename(filepath)
            localdir = os.path.dirname(filepath)
            #print(self.output_dir, localdir[1:])
            savepath = os.path.join(self.output_dir,localdir[1:])
            try:
                with open(savepath): pass
            except IOError:
                if not os.path.exists(savepath):
                    os.makedirs(savepath)
                pathBefore = os.getcwd()
                os.chdir(savepath)
                subprocess.call(['touch', base_name])
                os.chdir(pathBefore)
                
        
    def choose_directory(self, dir_type):
        if dir_type=="output":
            # save the output directory
            self.output_dir =  tkFileDialog.askdirectory(**self.output_dir_opt)
            # update the GUI to reflect the change
            self.current_output_dir["text"] = self.output_dir
        else:
            # save the mirror directory
            self.mirror_dir = tkFileDialog.askdirectory(**self.mirror_dir_opt)
            # update the GUI to reflect the change
            self.current_mirror_dir["text"] = self.mirror_dir
        
        
if __name__=="__main__":
    root = tk.Tk()
    my_gui = mirror_directory(root)
    root.mainloop()
