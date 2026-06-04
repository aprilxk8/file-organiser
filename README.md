# File Organizer

A Python CLI tool that automatically organizes files into category-based folders.

## Features

- Organize files by extension
- Dry-run mode
- User confirmation before moving files
- Logging support
- CLI interface

## Usage

Preview changes:

python main.py --path <folder_path> --dry-run

Execute changes:

python main.py --path <folder_path> --execute

## Categories

- Images
- Documents
- Audio
- Videos
- Others

## Future Enhancements

- Duplicate file handling
- Recursive scanning
- JSON configuration
- Watch mode