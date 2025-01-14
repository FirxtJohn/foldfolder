# 🗂️ Smart Folder Organizer

A powerful Python-based file organization tool that automatically sorts and categorizes files based on their extensions. This intelligent organizer creates a clean, structured directory system with minimal effort.

## ✨ Key Features

- **Smart Categorization**: Automatically organizes files into appropriate folders based on file extensions
- **User-Friendly Interface**: Simple GUI for folder selection using tkinter
- **Multiple Organization Modes**: 
  - Mixed Files (Available)
  - Pictures (Coming Soon)
  - Videos (Coming Soon)
  - Documents (Coming Soon)
- **Progress Tracking**: Visual progress bar shows real-time organization status
- **Error Handling**: Robust error management for file operations
- **Extensible Design**: Easy to add new file types and categories

## 🚀 Perfect For
- Cleaning up download folders
- Organizing media collections
- Managing project assets
- Structuring work directories

Built with Python using modern libraries like Click for CLI, tkinter for GUI, and tqdm for progress visualization. The tool is designed to be both powerful for advanced users and accessible for beginners.

## 🛠️ Technologies
- Python
- Click
- Tkinter
- Logging
- File System Operations

## Installation

1. Clone the repository:
```sh
    git clone https://github.com/yourusername/folder-organizer.git
    cd folder-organizer
```

2. Install the required packages:
```sh
    pip install -r requirements.txt
```

## Usage

### Organize Files

To organize files in a folder by their extensions, run the following command:

```sh
python src/Folder_Organizer.py --folder_type Mixed
```

Generate Sample Files
To generate sample files with random extensions, run the following command:

```sh
python src/file_generator.py --folder sample --num-files 100 --num-extensions 10
```
Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

License
This project is licensed under the MIT License.
