# KeePassXC Cleanup

KeePassXC Cleanup is a tool designed to help you manage and clean up your KeePassXC database. It provides features to remove unused entries, organize your database, and ensure that your passwords are secure.

## Installation

To install the required dependencies, run:
```bash
python install_requirements.py
```

## Usage

The script provides three main functionalities: listing duplicates, deduplication, and listing custom properties.

### List Duplicates

To find and list duplicate entries in your KeePassXC database, run:
```bash
python main.py list_duplicates <path_to_database>
```

### Deduplicate

To remove duplicate entries after user selection, run:
```bash
python main.py dedup <path_to_database>
```

### List Custom Properties

To list custom properties of all entries in your KeePassXC database, run:
```bash
python main.py list_custom_properties <path_to_database>
```

## Example

```bash
python main.py list_duplicates mydatabase.kdbx
python main.py dedup mydatabase.kdbx
python main.py list_custom_properties mydatabase.kdbx
```

Replace `<path_to_database>` with the path to your KeePassXC database file.


