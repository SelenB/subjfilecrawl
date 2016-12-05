import Tkinter as tk
import tkFileDialog
import tkMessageBox
import csv
import os
import re
import shutil

class crawl_subject_GUI:
    def __init__(self, master):
        self.init_gui(master)
    
    def init_gui(self, master):  
        self.master = master
        master.title("Get subject files")
        # close button
        self.close_button = tk.Button(master, text="close", command = master.quit)
        self.close_button.pack(side=tk.BOTTOM)
        # label for output directory
        self.output_dir = os.getcwd()
        outputDirLabel = tk.Label(master, text="Output directory:")
        outputDirLabel.pack(anchor="w")
        self.current_output_dir = tk.Label(master, bg="white", text=self.output_dir)
        self.current_output_dir.pack(anchor="w", padx=5)
        # browser to choose output directory
        self.choose_directory_button = tk.Button(master, text="Browse", command=self.choose_output_directory)
        self.choose_directory_button.pack(anchor='center', pady=(0,10))
        self.dir_opt = options = {}
        options['initialdir'] = os.getcwd()
        options['mustexist'] = True
        # choose to save as csv or copy files to directory
        self.copy_or_csv = tk.IntVar()
        self.saveLabel = tk.Label(master, text="What do you want to do with these files?")
        self.saveLabel.pack(anchor='w')
        self.filename = tk.Entry(master)
        self.copy_files_radio = tk.Radiobutton(master, text="copy files to output directory", variable=self.copy_or_csv, value="copy", command=self.disableEntry)
        self.copy_files_radio.pack(anchor="w", padx=(20, 0))
        self.save_as_CSV_radio = tk.Radiobutton(master, text="save as CSV of all filepaths in output directory.\n File name:", variable=self.copy_or_csv,value="csv", command=self.enableEntry, justify="left")
        self.save_as_CSV_radio.pack(anchor="w", padx=(20,0))
        self.filename.pack(anchor="w", padx=(48, 0), pady=(0,10))
        self.copy_files_radio.invoke()
        # options for audio annotations
        self.file_options_label = tk.Label(master, text="What kinds of files do you want?")
        self.file_options_label.pack(anchor='w')
        self.audio_clan = tk.IntVar()
        self.clan_file_option = tk.Checkbutton(master, variable = self.audio_clan, text="Audio clan files")
        self.clan_file_option.pack(anchor='w')
        self.audio_basic = tk.IntVar()
        self.audio_basic_option = tk.Checkbutton(master, variable = self.audio_basic, text="Basic audio files")
        self.audio_basic_option.pack(anchor='w')
        self.video_datavyu = tk.IntVar()
        self.datavyu_file_option = tk.Checkbutton(master, variable = self.video_datavyu,text="Video datavyu files")
        self.datavyu_file_option.pack(anchor='w')
        self.video_basic = tk.IntVar()
        self.video_basic_option = tk.Checkbutton(master, variable = self.video_basic, text="Basic video files")
        self.video_basic_option.pack(anchor='w')
        # next button
        self.next_button = tk.Button(master, text="next", command = self.getCheckboxVals)
        self.next_button.pack(side=tk.BOTTOM, pady=(10,0))
        
    def getCheckboxVals(self):
        checked = []
        if (self.audio_clan.get()):
            checked.append("audio_clan")
        if (self.audio_basic.get()):
            checked.append("audio_basic")
        if (self.video_datavyu.get()):
            checked.append("video_datavyu")
        if (self.video_basic.get()):
            checked.append("video_basic")
        self.file_types = checked
        if len(checked) == 0:
            tkMessageBox.showinfo("Error", "You must select at least one type of file")
        else:
            for item in checked:
                self.create_new_window(item)
            #self.close_button.invoke()
        
    def enableEntry(self):
        self.copy_or_csv.set("csv")
        self.filename.configure(state="normal")
        self.filename.update()
        
    def disableEntry(self):
        self.copy_or_csv.set("copy")
        self.filename.configure(state="disabled")
        self.filename.update()
    
    def getSavePath(self):
        self.save_filename = self.filename.get()
        print self.save_filename
        
    def choose_output_directory(self):
        # save the output directory
        self.output_dir =  tkFileDialog.askdirectory(**self.dir_opt)
        print self.output_dir
        # update the GUI to reflect the change
        self.current_output_dir["text"] = self.output_dir
        
    def create_new_window(self, option):
        if option == "audio_clan":
            self.audio_clan_window()
        if option == "audio_basic":
            self.audio_basic_window()
        if option == "video_datavyu":
            self.video_datavyu_window()
        if option == "video_basic":
            self.video_basic_window()
    
    def audio_clan_window(self):
        window = tk.Toplevel(root)
        window.title("Audio clan options")
        close_window = tk.Button(window, text="close", command=window.destroy)
        close_window.pack(side="bottom")
        label = tk.Label(window, text="Choose which files you want")
        label.pack(anchor="w")
        
       
    def audio_basic_window(self):
        window = tk.Toplevel(root)
        window.title("Audio basic options")
        close_window = tk.Button(window, text="close", command=window.destroy)
        close_window.pack(side="bottom")
        label = tk.Label(window, text="Choose which files you want")
        label.pack(anchor="w")
        
        
    def video_datavyu_window(self):
        window = tk.Toplevel(root)
        window.title("Video datavyu options")
        close_window = tk.Button(window, text="close", command=window.destroy)
        close_window.pack(side="bottom")
        label = tk.Label(window, text="Choose which files you want")
        label.pack(anchor="w")
        
    def video_basic_window(self):
        window = tk.Toplevel(root)
        window.title("Video basic options")
        close_window = tk.Button(window, text="close", command=window.destroy)
        close_window.pack(side="bottom")
        label = tk.Label(window, text="Choose which files you want")
        label.pack(anchor="w")

if __name__=="__main__":
    root = tk.Tk()
    my_gui = crawl_subject_GUI(root)
    root.mainloop()