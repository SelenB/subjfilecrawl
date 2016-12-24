import Tkinter as tk
import tkFileDialog
import tkMessageBox
import csv
import os
import re
import shutil
from pip._vendor.distlib.util import CSVWriter

class crawl_subject_GUI:
    def __init__(self, master):
        self.start = 0
        self.path = "/home/nicky/classes"
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
        self.copy_or_csv = tk.StringVar()
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
        # start process
        self.start_button = tk.Button(master, text="start", command = lambda: self.crawl_files(self.path, True))
        self.start_button.config(state="disable")
        self.start_button.pack(side=tk.BOTTOM, pady=(10,0))
        # next button
        self.next_button = tk.Button(master, text="next", command = self.getCheckboxVals)
        self.next_button.pack(side=tk.BOTTOM, pady=(10,0))
        
    def getCheckboxVals(self):
        self.start = 1
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
            self.start_button.config(state="normal")
            self.getSavePath()
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
        
    def choose_output_directory(self):
        # save the output directory
        self.output_dir =  tkFileDialog.askdirectory(**self.dir_opt)
        # update the GUI to reflect the change
        self.current_output_dir["text"] = self.output_dir
        
    def create_new_window(self, option):
        self.audio_clan_type = tk.StringVar() 
        self.audio_basic_type = False
        self.video_datavyu_type = tk.StringVar()
        self.video_basic_type = False
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
        window.overrideredirect(1)
        label = tk.Label(window, text="Choose which audio clan files you want")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        newclan_merged_button = tk.Radiobutton(window, text="newclan_merged", variable=self.audio_clan_type, value="newclan_merged", command=self.audio_clan_type.set("newclan_merged"))
        final_button = tk.Radiobutton(window, text="final", variable=self.audio_clan_type, value="final", command=self.audio_clan_type.set("final"))
        newclan_merged_final_button = tk.Radiobutton(window, text="newclan_merged_final", variable = self.audio_clan_type, value="newclan_merged_final", command=self.audio_clan_type.set("newclan_merged_final"))
        newclan_merged_final_button.pack(anchor='w')
        final_button.pack(anchor='w')
        newclan_merged_button.pack(anchor='w')
        accept = tk.Button(window, text="accept",command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        
    def audio_basic_window(self):
        window = tk.Toplevel(root)
        window.title("Audio basic options")
        window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="check.csv files are the only option for basic audio files")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        self.audio_basic_type = True
        
    def video_datavyu_window(self):
        window = tk.Toplevel(root)
        window.title("Video datavyu options")
        window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="Choose which datavyu files you want")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        button = tk.StringVar()
        final_button = tk.Radiobutton(window, text="final", variable=self.video_datavyu_type, value="final", command=self.video_datavyu_type.set("final"))
        final_button.pack(anchor='w')
        consensus_button = tk.Radiobutton(window, text="consensus", variable=self.video_datavyu_type, value="consensus", command=self.video_datavyu_type.set("consensus"))
        consensus_button.pack(anchor='w')
        
    def video_basic_window(self):
        window = tk.Toplevel(root)
        window.title("Video basic options")
        window.overrideredirect(1)
        accept = tk.Button(window, text="accept", command=window.destroy)
        accept.pack(side="bottom", pady=(10,0))
        label = tk.Label(window, text="check.csv files are the only option for basic video files")
        label.config(font="bold")
        label.pack(anchor="w", padx=(10,10), pady=(10,10))
        self.video_basic_type = True

    def crawl_files(self, dirname, writeHeader=False):
        if self.copy_or_csv.get() == "copy":
            for sub in os.listdir(dirname):
                path = os.path.join(dirname, sub)
                if os.path.isdir(path):
                    subs = self.crawl_files(path)
                else:
                    if self.video_datavyu_type.get() == "final":
                        if str(path).endswith(".jpg"):
                            shutil.copy(path, self.output_dir)
        else:
            x = self.save_filename
            if not re.match("(.csv)$", self.save_filename):
                x +=".csv"
            with open(self.output_dir+'/'+x, 'a') as f:
                writer = csv.writer(f)
                if writeHeader:
                    writer.writerow(["full path", "file name"])
            tups = []
            for sub in os.listdir(dirname):
                path = os.path.join(dirname, sub)
                if os.path.isdir(path):
                    subs = self.crawl_files(path)
                else:
                    if self.audio_clan_type.get() == "final":
                        if str(path).endswith(".png"):
                            tups.append([str(path), str(sub)])
            with open(self.output_dir+'/'+x, 'a') as f:
                writer = csv.writer(f)
                for tup in tups:
                    writer.writerow(tup)
            
if __name__=="__main__":
    root = tk.Tk()
    my_gui = crawl_subject_GUI(root)
    root.mainloop()