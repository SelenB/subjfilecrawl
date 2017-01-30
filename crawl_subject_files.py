try:
    import Tkinter as tk  # for python2
    import tkFileDialog as tkfiledialog
    import tkMessageBox
except ImportError:
    import tkinter as tk  # for python3
    import tkinter.filedialog as tkfiledialog
    import tkinter.messagebox as tkMessageBox
import csv
import os
import re
import shutil
from pip._vendor.distlib.util import CSVWriter

class crawl_subject_GUI(object):
    def __init__(self, master):
        self.start = 0
        # list of tups that holds the path -> file structure
        self.tups = []
        self.init_gui(master)
    
    def init_gui(self, master):  
        self.master = master
        master.title("Get subject files")
        # close button
        self.close_button = tk.Button(master, text="close", command = master.quit)
        self.close_button.pack(side=tk.BOTTOM)
        # label for crawl directory
        self.crawl_dir = os.getcwd()
        crawlDirLabel = tk.Label(master, text="Crawl directory:")
        crawlDirLabel.pack(anchor="w")
        self.current_crawl_dir = tk.Label(master, bg="white", text = self.crawl_dir)
        self.current_crawl_dir.pack(anchor="w", padx=5)  
        #browser to choose crawl directory
        self.choose_crawl_directory_button = tk.Button(master, text="Browse", command=lambda: self.choose_directory("crawl"))
        self.choose_crawl_directory_button.pack(anchor="center", pady=(0,10))
        self.crawl_dir_opt = options = {}
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
        self.audio_clan = tk.BooleanVar()
        self.clan_file_option = tk.Checkbutton(master, variable = self.audio_clan, text="Audio clan files")
        self.clan_file_option.pack(anchor='w')
        self.audio_basic = tk.BooleanVar()
        self.audio_basic_option = tk.Checkbutton(master, variable = self.audio_basic, text="Basic audio files")
        self.audio_basic_option.pack(anchor='w')
        self.video_datavyu = tk.BooleanVar()
        self.datavyu_file_option = tk.Checkbutton(master, variable = self.video_datavyu,text="Video datavyu files")
        self.datavyu_file_option.pack(anchor='w')
        self.video_basic = tk.BooleanVar()
        self.video_basic_option = tk.Checkbutton(master, variable = self.video_basic, text="Basic video files")
        self.video_basic_option.pack(anchor='w')
        # month ranges
        startMonthLabel = tk.Label(master, text="Start Month:")
        startMonthLabel.pack(anchor="w")
        self.start_month_var = tk.StringVar()
        self.start_month = tk.Spinbox(master, from_=6, to=18, textvariable=self.start_month_var, command=self.updateSpinbox)
        self.start_month_var.set(6)
        self.start_month.pack(anchor='w')
        endMonthLabel = tk.Label(master, text="End Month:")
        endMonthLabel.pack(anchor="w")
        self.end_month_var = tk.StringVar()
        self.end_month = tk.Spinbox(master, from_=6, to=18, textvariable=self.end_month_var, command=self.updateSpinbox)
        self.end_month_var.set(18)
        self.end_month.pack(anchor="w")
        # start process
        self.start_button = tk.Button(master, text="start", command = lambda: self.crawl_files(self.crawl_dir))
        self.start_button.config(state="disable")
        self.start_button.pack(side=tk.BOTTOM, pady=(10,0))
        # next button
        self.next_button = tk.Button(master, text="next", command = self.getCheckboxVals)
        self.next_button.pack(side=tk.BOTTOM, pady=(10,0))
        
    def getCheckboxVals(self):
        self.start = 1
        self.checked_boxes = []
        if (self.audio_clan.get()):
            self.checked_boxes.append("audio_clan")
        if (self.audio_basic.get()):
            self.checked_boxes.append("audio_basic")
        if (self.video_datavyu.get()):
            self.checked_boxes.append("video_datavyu")
        if (self.video_basic.get()):
            self.checked_boxes.append("video_basic")
        self.file_types = self.checked_boxes
        if len(self.checked_boxes) == 0:
            tkMessageBox.showinfo("Error", "You must select at least one type of file")
        else:
            for item in self.checked_boxes:
                self.create_new_window(item)
            self.start_button.config(state="normal")
            self.getSavePath()
            #self.close_button.invoke()
            
    def updateSpinbox(self):
        start=6
        end=18
        if int(self.start_month.get()) > int(self.end_month.get()):
            self.end_month_var.set(self.start_month_var.get())
            
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
        
    def choose_directory(self, dir_type):
        if dir_type=="output":
            # save the output directory
            self.output_dir =  tkfiledialog.askdirectory(**self.output_dir_opt)
            # update the GUI to reflect the change
            self.current_output_dir["text"] = self.output_dir
        else:
            # save the crawl directory
            self.crawl_dir = tkfiledialog.askdirectory(**self.crawl_dir_opt)
            # update the GUI to reflect the change
            self.current_crawl_dir["text"] = self.crawl_dir
        
    def create_new_window(self, option):
        self.audio_clan_type = tk.StringVar() 
        self.audio_clan_type.set("None")
        self.audio_basic_type = False
        self.video_datavyu_type = tk.StringVar()
        self.video_datavyu_type.set("None")
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
    
    def crawl_files(self, dirname):
        # if the save file name is empty and you want a csv
        if not self.filename.get() and self.copy_or_csv.get()=="csv":
            tkMessageBox.showinfo("Error", "You must provide a name for your file!")
            return
        # for each item in this directory
        try:
            for sub in os.listdir(dirname):
                path = os.path.join(dirname, sub)
                # if the current item is a directory, recurse
                if os.path.isdir(path):
                    # only recurse into dirs that lie within specified month ranges
                    if re.match("[0-9]{2}_[0-9]{2}$", sub):
                        splt = sub.split("_")
                        month = int(splt[1])
                        print(sub, month)
                        if month > int(self.end_month_var.get()) or month < int(self.start_month_var.get()):
                            #print("MONTH: ", month, "START: ", self.start_month_var.get(), "END: ", self.end_month_var.get())
                            continue
                    self.crawl_files(path)
                # else, here's a file to check
                else:
                    self.tups.append((str(path), str(sub)))
                    # add file paths to tups if it fits criteria
                    if "audio_basic" in self.checked_boxes:
                        pass
                    if "video_basic" in self.checked_boxes:
                        pass
                    if "audio_clan" in self.checked_boxes:
                        pass
                    if "video_datavyu" in self.checked_boxes:
                        pass
        # this only happens if we don't have permissions to files
        except OSError as e:
            print(e)
        # once all of the items in the top level directory have been searched, we're done
        if dirname==self.crawl_dir:
            if self.copy_or_csv.get()=="copy":
                self.copy_files(self.tups)
            else:
                self.copy_to_csv(self.tups)
    
    def copy_to_csv(self, lst):
        x = self.save_filename
        if not re.match("(.csv)$", self.save_filename):
            x+=".csv"
        with open(self.output_dir+'/'+x, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(["full path", "file name"])
            for item in lst:
                writer.writerow(item)
                
    def copy_files(self, lst):
        for tup in lst:
            filepath = tup[0]
            localdir = os.path.dirname(filepath)
            savepath = self.output_dir+localdir
            try:
                with open(savepath) as f: pass
            except IOError as e:
                if not os.path.exists(savepath):
                    os.makedirs(savepath)
                shutil.copy(filepath, savepath)
            
if __name__=="__main__":
    root = tk.Tk()
    my_gui = crawl_subject_GUI(root)
    root.mainloop()