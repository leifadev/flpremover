import os, time, sys, shutil
from datetime import datetime
from pathlib import Path

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import END
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkFont
from ttkthemes import ThemedTk

# Pack the GUI at some point please
# https://www.tutorialspoint.com/python/tk_pack.htm


# recycleURLs Method (doesnt work rn) allows you as Finder to delete items
#error = NSError
#urls = [url]
#tashurl = os.path.join('/Users/leif/.Trash/', 'test.txt')
#newurls = {
#    url: NSURL.fileURLWithPath_(os.path.join('/Users/leif/.Trash/', 'test.txt'))
#}
#def completionHandler(newURLs, error):
#    print(error)
#    
#sw = NSWorkspace.sharedWorkspace()
#sw.recycleURLs_completionHandler_(urls, completionHandler(newurls, error))

class GUI:
    def __init__(self, root):
    
        self.recent_keep_amount = str
        self.old_keep_amount = str
    
        # Setting title
        root.title("FLP Remover")
        
        # Setting window size
        width=600
        height=400
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.set_theme("aqua")

        frame = ttk.Frame(root)
        frame.place(x=0, y=0, relwidth=1.0, relheight=1.0)
#        bottomframe = ttk.Frame(root)
#        bottomframe.pack( side = BOTTOM )

        self.recent_keep_amount_entry=ttk.Entry(root)
        self.recent_keep_amount_entry["text"] = ""
        self.recent_keep_amount_entry.place(x=150,y=210,width=70,height=25)
#        self.recent_keep_amount_entry.bind("<FocusOut>", self.recent_keep_amount_entry_update)

        self.old_keep_amount_entry=ttk.Entry(root)
        self.old_keep_amount_entry["text"] = ""
        self.old_keep_amount_entry.place(x=380,y=210,width=70,height=25)
#        self.old_keep_amount_entry.bind("<FocusOut>", self.old_keep_amount_entry_update)

        output_label=ttk.Label(root)
        output_label["text"] = "label"
        output_label.place(x=290,y=210,width=70,height=25)

        quit_button=ttk.Button(root)
        quit_button["text"] = "Quit"
        quit_button.place(x=20,y=365,width=70,height=25)
        quit_button["command"] = self.quit_button_command

        app_title_message=tk.Message(root)
        app_title_message["anchor"] = "center"
        app_title_message["background"] = "#ECECEC"
        app_title_message["text"] = """
        FLP Backup Remover
        
        This app will delete all your unwanted backups in bulk and searches all of your project folders you select no matter how large!
        """
        app_title_message.place(x=65,y=0,width=500,height=180)

        GCheckBox_517=ttk.Checkbutton(root)
        GCheckBox_517["text"] = "CheckBox"
        GCheckBox_517.place(x=270,y=230,width=70,height=25)
        GCheckBox_517["offvalue"] = "0"
        GCheckBox_517["onvalue"] = "1"
        GCheckBox_517["command"] = self.GCheckBox_517_command

        status_label=ttk.Label(root)
        status_label["text"] = "label"
        status_label.place(x=290,y=180,width=70,height=25)

        recent_keep_amount_label=ttk.Label(root)
        recent_keep_amount_label["text"] = """Keep backups\n(from newest)"""
        recent_keep_amount_label.place(x=140,y=170,width=140,height=35)
        

        old_keep_amount_label=ttk.Label(root)
        old_keep_amount_label["text"] = "Keep backups\n(from oldest)"
        old_keep_amount_label.place(x=370,y=170,width=140,height=35)

        help_button=ttk.Button(root)
        help_button["text"] = "Help"
        help_button.place(x=530,y=365,width=60,height=25)
        help_button["command"] = self.help_button_command

        browse_button=ttk.Button(root)
        browse_button["text"] = "Select Files"
        browse_button.place(x=275,y=260,width=70,height=25)
        browse_button["command"] = self.browse_button_command

    def quit_button_command(self):
        sys.exit(1)

    def GCheckBox_517_command(self):
        print("Checkbox command")

    def recent_keep_amount_entry_update(self, text):
        text = self.recent_keep_amount_entry.get()
            
        self.recent_keep_amount = text
        print(f'Recent Keep Amount Selected: {text}')
        
    def old_keep_amount_entry_update(self, text):
        text = self.old_keep_amount_entry.get()

        self.recent_keep_amount = text
        print(f'Old Keep Amount Selected: {text}')
        
    def help_button_command(self):
        import webbrowser
        webbrowser.open("https://github.com/leifadev/flpremover")
        
    def browse_button_command(self):
        """
        
        calls keepOnlyLastBackups method which does the removing of the files
        """
        self.recent_keep_amount = self.recent_keep_amount_entry.get()
        self.old_keep_amount = self.old_keep_amount_entry.get()

        # Give error and stop file browsing if invput is letters
        if not self.recent_keep_amount.isdigit():
            print(f'Entry value was not an whole integer, calling tkinter.messagebox')
            messagebox.showwarning(message='You must enter a number for your selection of files to keep!')
            self.recent_keep_amount_entry.delete(0, tk.END)
            return

        elif not self.old_keep_amount.isdigit():
            print(f'Entry value was not an whole integer, calling tkinter.messagebox')
            messagebox.showwarning(message='You must enter a number for your selection of files to keep!')
            self.old_keep_amount_entry.delete(0, tk.END)
            return

        # Ask for users directory choice
        user = os.path.expanduser('~')
        ask_folder_dir = filedialog.askdirectory(initialdir=f'{user}')

        try:
            self.recent_keep_amount = int(self.recent_keep_amount)
            self.old_keep_amount =  int(self.old_keep_amount)
        except TypeError as e:
            pass
            
        try:
            os.chdir(ask_folder_dir)
        except FileNotFoundError as e:
            print("No Directory found: Canceled")

        self.keepOnlyLastBackups(ask_folder_dir, self.recent_keep_amount, self.old_keep_amount)


    def keepOnlyLastBackups(self, directory, keep_from_recent, keep_from_old):
        backup_total = [] # List for total backups accumlated to keep for logging them later
        music_projects = [] # os.listdir() of all project folders in the projects directory
        
        try:
            music_projects = os.listdir(str(directory))
        except FileNotFoundError as e:
            print(f'No folder was chosen to search through!')

        for folder in music_projects:
        
            # Change Scripts Directory to the selected directory everytime
            os.chdir(directory) # SHOULD NOT DELETE
            
            if os.path.isdir(folder):
                print(f'Trimming up backups in {folder}/Backup')
                
                # Change directory into the backuo folder of the project folder
                try:
                    os.chdir(folder + "/Backup")
                    backup_total = os.listdir()
                except FileNotFoundError as e: # Except if there is none
                    print(f'No backup for found in: {folder}')
                    
#                For loop that gets a list of all file's creation dates in a list
#                dont need it any more
#                for backup_file in os.listdir():
#                    if os.path.isdir(backup_file):
#                        if Path(backup_file).suffix == ".flp":
#                            # Get creation date of single file
#                            creation_date = time.ctime(
#                            os.path.getctime(backup_file)
#                            )
#                            backups.append(creation_date)
#                        print(backups)

                # Sort all file names of .FLP's with sorted() and iterdir(), with lamdba key by creation time (getctime)
                try:
                    sorted_backups = sorted(Path(f'{directory}/{folder}/Backup').iterdir(), key=os.path.getctime)
                except FileNotFoundError as e:
                    print(f'Could not find a backup folder for {folder}', e)
                    continue # Skip this folder in the loop, since there is no backup folder to sort through
                    
                # Check for over or under calculations of users parameters to actual FLP count
#                if len(sorted_backups) < keep_from_recent:
#                    # This means there are less backups than
#                    # what the person already wanted to keep
#                    print(f"Didn't have to delete anything because you already have {len(sorted_backups)} backups and chose to keep (from newest) {keep_from_recent} backups!")
#                    print("Try again!")
##                    sys.exit(1)
#                    
#                elif len(sorted_backups) < keep_from_old:
#                    # Remove certain amount of most recently created files from list so we delete all the other ones
#                    print(f"Didn't have to delete anything because you already have {len(sorted_backups)} backups and chose to keep (from oldest) {keep_from_old} backups!")
#                    print("Try again!")
#                    sys.exit(1)


                # Index sorted backups for recently kept amount
                keep_files_index = sorted_backups[0:keep_from_recent]
                print(f'Attempting to delete {len(keep_files_index)} backups from the most recent...')
#                print(keep_files_index)
                
                # Index sorted backups for recently kept amount (uses slice operator to gather from the negative
                # indexing that gives me multiple of the last items rather than just the last using -1
                # https://stackoverflow.com/questions/646644/how-to-get-last-items-of-a-list-in-python
                # Index sorted backups for earliest kept amount
                
                keep_files_old_index = sorted_backups[-keep_from_old:]
                print(f'Attempting to delete {len(keep_files_old_index)} backups from the most old...')
#                print(keep_files_old_index)
                
                
                # Using MacOS to delete files from system instead of python
                # via NSFileManager for more secure and legitimate outcomes (depedent on MacOS more)
                
                user = os.path.expanduser('~')

                from Foundation import NSURL, NSFileManager
                
                # Make MacOS File Manager url and manager to use real trash methods
#                fm = NSFileManager.defaultManager()

#                try:
                for file in keep_files_index:
#                    print(file)
                    user_trash_path = os.path.join('/Users/{user}/.Trash', file)
                    fileurl = os.path.join(directory, file)
                                            
#                    trashurl = NSURL.fileURLWithPath_(user_trash_path) # Path for where file will be in trash directory
#                    url = NSURL.fileURLWithPath_(fileurl) # Path for the file being deleted
#                    print(trashurl, url)

#                    fm.trashItemAtURL_resultingItemURL_error_(url, trashurl, None) # Mac instance method
                    shutil.move(str(fileurl), str(user_trash_path))

                for file in keep_files_old_index:
#                    print(file)
                    user_trash_path = os.path.join('/Users/{user}/.Trash', file) # Make system path from string
                    fileurl = os.path.join(directory, file) # Make system path as well for the fiule
                                            
#                    trashurl = NSURL.fileURLWithPath_(user_trash_path)
#                    url = NSURL.fileURLWithPath_(fileurl)
#                    print(url, trashurl)

#                    fm.trashItemAtURL_resultingItemURL_error_(url, trashurl, None)
                    shutil.move(str(fileurl), str(user_trash_path))


#                except Exception as e:
#                    print(e)


if __name__ == "__main__":
    root = ThemedTk(themebg=True)
    app = GUI(root)
    root.mainloop()
