import os
import shutil
import tkinter as tk
from tkinter import filedialog
import logging
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
import click
from tqdm import tqdm
import yaml
from config import CLICK_CONTEXT_SETTINGS
#from constants import EXTENSION_TO_FOLDER



maps = {}
with open("maps.yaml") as config_file:
    maps = yaml.load(config_file, Loader=yaml.FullLoader)



@dataclass
class FileOperation:
    source: str
    destination: str
    timestamp: datetime
    success: bool


def get_user_input(title: str = "Input") -> str:
    """
    Displays a simple dialog box to get user input.

    Args:
        title (str, optional): The title of the dialog box. Defaults to "Input".

    Returns:
        str: The user's input.
    """
    root = tk.Tk()
    root.withdraw()
    user_input = filedialog.askdirectory(title=title, initialdir=None, mustexist=False)
    return user_input

def extension_mapping(extension: str, maps: dict = maps) -> None:
    """Updates the maps dictionary with new mapping"""
    while True:
        if extension in maps.keys():
            click.echo(click.style(f"{extension} files are saved in {maps[extension]}"), color="yellow")
            if click.confirm("Do you want to change?"):
                folder_name = click.prompt(F"Enter name of folder to store {extension} files")
                maps.update({extension : folder_name})
            else:
                if click.confirm("Do you want to add another mapping?"):
                    continue
                else:
                    break
        else:
            folder_name = click.prompt(F"Enter name of folder to store {extension} files")
            maps.update({extension : folder_name})
        with open("maps.yaml", "a") as config_file:
            maps = yaml.dump(maps, stream=config_file)
            click.echo(click.style(f"Added mapping: .{extension} → {folder_name}", fg="green"))
            break

def terminal_log(msg, error: bool=True) -> None:
    if error == True:
        click.echo(click.style(msg), color="red")
    else:
        click.echo(click.style(msg), color="blue")
        
class FolderOrganizer:
    def __init__(self):
        self.operation_history: List[FileOperation] = []
        
    def move_file(self, source: str, destination: str) -> bool:
        """Moves file and records the operation"""
        try:
            shutil.move(source, destination)
            operation = FileOperation(
                source=source,
                destination=destination,
                timestamp=datetime.now(),
                success=True
            )
            self.operation_history.append(operation)
            return True
        except (PermissionError, OSError) as e:
            logging.error("Failed to move %s: %s", source, str(e))
            operation = FileOperation(
                source=source,
                destination=destination,
                timestamp=datetime.now(),
                success=False
            )
            logging.error("Move operation failed \n %s → %s", source, destination)
            return False
    
    def save_history(self) -> None:
        """Saves the operation history to a file"""
        pass
        
    def view_operation_history(self) -> None:
        """Displays the operation history"""
        if not self.operation_history:
            click.echo("No operations to display")
            return
        for i, operation in enumerate(self.operation_history):
            click.echo(f"{i + 1}. {operation.timestamp}: {operation.source} → {operation.destination}")

    def undo_last_operation(self) -> bool:
        """Undoes the last successful file operation"""
        if not self.operation_history:
            click.echo("No operations to undo")
            return False
        
        try:
            for operation in tqdm(self.operation_history, desc="Undoing operations", colour="yellow"):
                shutil.move(operation.destination, operation.source)
                self.operation_history.pop()
                logging.info(f"Undid move of {os.path.basename(operation.source)}")
            return True
        except (PermissionError, OSError) as e:
            logging.error("Failed to undo operation: %s", str(e))
            return False
        
    def organize_folder(self, input_folder: str) -> None:
        """Modified OrganizeFolder function to use the new move_file method"""
        if input_folder:
            click.echo(click.style(f"Folding {input_folder}", fg="cyan"))
            for filename in tqdm(os.listdir(input_folder), desc="Organizing files", colour="blue"):
                file_path = os.path.join(input_folder, filename)
                if os.path.isfile(file_path):
                    extension = filename.split(".")[-1].lower()
                    folder_name = maps.get(extension, extension)
                    extension_folder = os.path.join(input_folder, folder_name)

                    if not os.path.exists(extension_folder):
                        os.makedirs(extension_folder)

                    destination = os.path.join(extension_folder, filename)
                    self.move_file(file_path, destination)
            with open("history.yaml", "a") as history_file:
                yaml.dump(self.operation_history, history_file)
        else:
            logging.error("Invalid folder path.\nPlease try again!\n")
            return


################################################################################
##                                   CLICK                                    ##
################################################################################


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)

@click.option(
    "-mp", "--map",
    is_flag=True,
    help="Map files to folders they should be stored in."
)

@click.option(
    "-mx", "--mixed",
    is_flag=True,
    help="Specify operation on a mixed folder."
)

@click.option(
    "-u", "--undo",
    is_flag=True,
    help="Undo the last operation."
)

@click.option(
    "-hy", "--history",
    is_flag=True,
    help="View operation history."
)

# Select the type of folder to sort
def start_point(mixed, map, history, undo):
    organizer = FolderOrganizer()
    
    if map:
        extension = click.prompt("Enter file extension (without dot)")
        extension_mapping(extension)
        return
    
    if mixed:
        click.echo(click.style("\nChoose folder to sort...\n", fg="cyan"))
        folder = get_user_input("Select Folder")
        organizer.organize_folder(folder)
        if click.confirm("Do you want to view history?"):
            organizer.view_operation_history()
        if click.confirm("Do you want to undo last operation?"):
            organizer.undo_last_operation()
        return
    
    if undo:
        pass
    
    if history:
        organizer.view_operation_history()
    
    else:
        if click.prompt("No option selected. Press enter to exit", default="") == "":
            exit(1)

def menu():
    pass
            
if __name__ == "__main__":
    start_point()
