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
from config import CLICK_CONTEXT_SETTINGS
from constants import EXTENSION_TO_FOLDER



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

def add_extension_mapping() -> tuple[str, str]:
    """Gets user input for new extension mapping"""
    root = tk.Tk()
    root.withdraw()
    
    # Create a simple dialog window
    dialog = tk.Toplevel()
    dialog.title("Add New Extension Mapping")
    
    extension_var = tk.StringVar()
    folder_var = tk.StringVar()
    
    # Create and pack widgets
    tk.Label(dialog, text="Enter file extension (without dot):").pack()
    tk.Entry(dialog, textvariable=extension_var).pack()
    
    tk.Label(dialog, text="Enter folder name:").pack()
    tk.Entry(dialog, textvariable=folder_var).pack()
    
    result = [None, None]
    
    def on_submit():
        result[0] = extension_var.get().lower()
        result[1] = folder_var.get()
        dialog.destroy()
    
    tk.Button(dialog, text="Submit", command=on_submit).pack()
    
    # Wait for user input
    dialog.wait_window()
    return result[0], result[1]

def update_extension_mapping(extension: str, folder_name: str) -> None:
    """Updates the EXTENSION_TO_FOLDER dictionary with new mapping"""
    if extension and folder_name:
        EXTENSION_TO_FOLDER[extension] = folder_name
        click.echo(click.style(f"Added mapping: .{extension} → {folder_name}", fg="green"))


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
            self.operation_history.append(operation)
            return False

    def undo_last_operation(self) -> bool:
        """Undoes the last successful file operation"""
        if not self.operation_history:
            click.echo("No operations to undo")
            return False

        last_op = self.operation_history[-1]
        if last_op.success:
            try:
                shutil.move(last_op.destination, last_op.source)
                self.operation_history.pop()
                click.echo(f"Undid move of {os.path.basename(last_op.source)}")
                return True
            except (PermissionError, OSError) as e:
                logging.error("Failed to undo operation: %s", str(e))
                return False
        return False

    def organize_folder(self, input_folder: str) -> None:
        """Modified OrganizeFolder function to use the new move_file method"""
        if input_folder:
            click.echo(click.style(f"Folding {input_folder}", fg="cyan"))
            for filename in tqdm(os.listdir(input_folder), desc="Organizing files", colour="blue"):
                file_path = os.path.join(input_folder, filename)
                if os.path.isfile(file_path):
                    extension = filename.split(".")[-1].lower()
                    folder_name = EXTENSION_TO_FOLDER.get(extension, extension)
                    extension_folder = os.path.join(input_folder, folder_name)

                    if not os.path.exists(extension_folder):
                        os.makedirs(extension_folder)

                    destination = os.path.join(extension_folder, filename)
                    self.move_file(file_path, destination)
        else:
            logging.error("Invalid folder path.\nPlease try again!\n")
            return
                    
################################################################################
##                                   CLICK                                    ##
################################################################################


@click.command(context_settings=CLICK_CONTEXT_SETTINGS)
@click.option(
    "--folder_type",
    type=click.Choice(["Mixed", "Pictures", "Videos", "Documents"], case_sensitive=False),
    prompt="Type of folder to organize",
    help="""Select the type of folder content to organize:\n
        - Mixed: Organizes folders containing various file types into categorized subfolders\n
        - Pictures: Specialized sorting for image files and photo collections (Coming soon)\n
        - Videos: Specialized sorting for video files and media content (Coming soon)\n
        - Documents: Specialized sorting for document files and archives (Coming soon)"""
    )

# Select the type of folder to sort
def start_point(folder_type):
    organizer = FolderOrganizer()
    
    if folder_type == "Pictures":
        click.echo(click.style("Coming soon...\nCheck back later!\nTry available features!", fg="cyan"))
        if click.confirm('Would you like to explore available features?', default=True):
            start_point.main(standalone_mode=False)
        else:
            return
        
    elif folder_type == "Videos":
        click.echo(click.style("Coming soon...\nCheck back later!\nTry available features!", fg="cyan"))
        if click.confirm('Would you like to explore available features?', default=True):
            start_point.main(standalone_mode=False)
        else:
            return
        
    elif folder_type == "Documents":
        click.echo(click.style("Coming soon...\nCheck back later!\nTry available features!", fg="cyan"))
        if click.confirm('Would you like to explore available features?', default=True):
            start_point.main(standalone_mode=False)
        else:
            return
        
    elif folder_type == "Mixed":
        while True:
            choice = click.prompt(
                "Choose an action",
                type=click.Choice(['organize', 'add_mapping', 'exit'], case_sensitive=False)
            )
            
            if choice == 'organize':
                click.echo(click.style("\nChoose folder to sort...\n", fg="cyan"))
                folder = get_user_input("Select Folder")
                organizer.organize_folder(folder)
            elif choice == 'add_mapping':
                extension, folder_name = add_extension_mapping()
                update_extension_mapping(extension, folder_name)
            else:
                if click.confirm('Would you like to try something else?', default=True):
                    start_point.main(standalone_mode=True)
                else:
                    return
                    
            if click.confirm('Would you like to continue?', default=True):
                continue
            else:
                return

            
if __name__ == "__main__":
    start_point()
