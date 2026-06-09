# File Organizer

A Python command-line application that automatically organizes files into category-based folders using file extensions. The tool supports recursive organization, real-time directory monitoring, undo functionality, logging, and configurable file categories.

---

## Features

### File Organization

* Organizes files into category folders based on file extension
* Automatically creates category folders when needed
* Supports duplicate filename handling
* Prevents re-organizing already sorted files

### Dry Run Mode

* Preview all planned file movements before making changes
* Safe way to verify organization rules

### Recursive Scanning

* Optionally scan subdirectories
* Preserves folder structure while organizing files

### Real-Time Watch Mode

* Monitor a directory for newly created files
* Automatically organize files as they appear
* Optional recursive monitoring of subdirectories

### Undo Support

* Stores move history in JSON format
* Undo the most recent file move operation

### Statistics

* View file counts grouped by category

### Logging

* Records previews, moves, cancellations, watch events, and errors
* Logs stored in `organiser.log`

### Testing

* Unit tests implemented using `pytest`
* Tests cover categorization and move-planning logic

### Configurable Categories

* File categories and extensions stored in `config.json`
* Easy to customize without modifying source code

---

## Supported Categories

Example categories:

* Images
* Documents
* Audio
* Videos
* Scripts
* Others

Categories can be customized in `config.json`.

---

## Project Structure

```text
file_organiser/
│
├── main.py
├── organiser.py
├── watch.py
├── config.py
├── config.json
├── README.md
│
├── tests/
│   ├── conftest.py
│   └── test_organiser.py
│
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd file_organiser
```

Install dependencies:

```bash
pip install watchdog pytest
```

---

## Usage

### Organize Files

Preview planned changes:

```bash
python main.py organise --path <folder_path> --dry-run
```

Organize files:

```bash
python main.py organise --path <folder_path>
```

---

### Recursive Organization

```bash
python main.py organise --path <folder_path> --recursive
```

---

### View Statistics

```bash
python main.py stats --path <folder_path>
```

Example output:

```text
Images: 12
Documents: 5
Audio: 3
Videos: 2
Others: 1
```

---

### Watch Mode

Monitor a directory and automatically organize newly created files:

```bash
python main.py watch --path <folder_path>
```

Watch subdirectories recursively:

```bash
python main.py watch --path <folder_path> --recursive
```

Example:

```text
Detected: photo.jpg
Moved: photo.jpg -> Images/photo.jpg
```

---

### Undo Last Move

Undo the most recent move operation:

```bash
python main.py undo
```

Example:

```text
Undone: Images/photo.jpg -> photo.jpg
```

---

## Running Tests

Run all tests:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

---

## Technologies Used

* Python
* argparse
* watchdog
* pytest
* logging
* json
* shutil
* os

---

## Example Workflow

1. Preview file organization

```bash
python main.py organise --path Downloads --dry-run
```

2. Organize files

```bash
python main.py organise --path Downloads
```

3. Monitor Downloads folder continuously

```bash
python main.py watch --path Downloads
```

4. Undo a move if needed

```bash
python main.py undo
```

---

## Future Improvements

* Batch undo support
* View move history
* Ignore rules and exclusion patterns
* Scheduled organization
* GUI version
* File size based organization
* Advanced conflict resolution
* Packaging and PyPI distribution

---

## Learning Outcomes

This project demonstrates:

* File system operations
* Command-line interface development
* Recursive directory traversal
* Event-driven programming
* Logging and monitoring
* JSON configuration management
* Unit testing with pytest
* Error handling
* Software architecture and modular design
* State persistence and undo functionality
