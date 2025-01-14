import os
import shutil
import tkinter as tk
from tkinter import filedialog
import logging
import click
from tqdm import tqdm
from config import CLICK_CONTEXT_SETTINGS
from constants import EXTENSION_TO_FOLDER



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


def OrganizeFolder(input_folder: str) -> None:
    """Organizes files in the specified input folder by their file extension. 
    For each file in the folder, it creates a subfolder with the same name as the file extension 
    or a predefined folder name, and moves the file into that subfolder."""
    if input_folder:
        click.echo(click.style(f"Folding {input_folder}", fg="cyan"))
        for filename in tqdm(os.listdir(input_folder), desc="Organizing files", colour="blue"):
            if os.path.isfile(os.path.join(input_folder, filename)):
                extension = filename.split(".")[-1].lower()
                # Get the folder name from the dictionary or use the extension as the folder name
                folder_name = EXTENSION_TO_FOLDER.get(extension, extension)
                extension_folder = os.path.join(input_folder, folder_name)

                if not os.path.exists(extension_folder):
                    os.makedirs(extension_folder)

                try:
                    shutil.move(
                        os.path.join(input_folder, filename),
                        os.path.join(extension_folder, filename),
                    )
                except (PermissionError, OSError) as e:
                    logging.error("Failed to move %s: %s", filename, str(e))
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
        click.echo(click.style("\nChoose folder to sort...\n", fg="cyan"))
        folder = get_user_input("Select Folder")
        OrganizeFolder(folder)
        if click.confirm('Would you like to organize another folder?', default=True):
            start_point.main(standalone_mode=False)
        else:
            if click.confirm('Would you like to try something else?', default=True):
                start_point.main(standalone_mode=True)
            else:
                return

            
if __name__ == "__main__":
    start_point()
