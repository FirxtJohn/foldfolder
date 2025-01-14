# Folder Organizer

Folder Organizer is a Python program that organizes files in a specified folder by their file extensions. It also includes a file generator to create sample files with random extensions for testing purposes.

## Features

- Organize files in a folder by their extensions.
- Generate sample files with random extensions.

## Requirements

- Python 3.6+
- Click
- TQDM

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