#scan->create folder->move
import os
import shutil
import logging
import json

from config import load_file_types
from collections import defaultdict

FILE_TYPES = load_file_types()
HISTORY_FILE = "move_history.json"

logging.basicConfig(
    filename="organiser.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def get_category(file_name):
    extension= os.path.splitext(file_name)[1].lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category
    return "Others"


def scan_directory(path, recursive=False):
    
    files=[]
    if(recursive):
        for root, dirs, filenames in os.walk(path):
            dirs[:] = [
                d for d in dirs
                if d not in FILE_TYPES.keys()
            ]
            for filename in filenames:
                full_path=os.path.join(root, filename)
                files.append(full_path)
        
    else:
        items=os.listdir(path)
        for item in items:
            full_path=os.path.join(path, item)
            if os.path.isfile(full_path):
                files.append(full_path)

    return files

def get_unique_destination(destination):
    if not os.path.exists(destination):
        return destination
    
    base_name, extension = os.path.splitext(destination)

    counter =1
    while True:
        new_destination = f"{base_name}({counter}){extension}"

        if not os.path.exists(new_destination):
            return new_destination
        counter +=1

def build_move_plan(files):
    plan=[]
    for file_path in files:
        filename=os.path.basename(file_path)

        category=get_category(filename)

        current_folder=os.path.dirname(file_path)

        if os.path.normpath(current_folder).split(os.sep)[-1] == category:
            continue

        destination_folder= os.path.join(current_folder, category)
        destination = os.path.join (destination_folder, filename)


        destination=get_unique_destination(destination)


        plan.append({
            "file": filename,
            "source": file_path,
            "destination_folder": destination_folder,
            "destination": destination,
            "category": category
        })
    return plan

def show_plan(plan):
    
    print("\n----Move Plan Preview---\n")
    logging.info("PREVIEW CHECKED")
    for item in plan:
        print(f"{item['file']} -> {item['destination']}")


def execute_move_plan(plan):
    print("\n----moving files---\n")

    for item in plan:
        os.makedirs(item["destination_folder"], exist_ok=True)

        shutil.move(item["source"], item["destination"])

        save_move_history(item["source"], item["destination"])

        logging.info(f"MOVED: {item['file']} | {item['source']} -> {item['destination']}")        
        print(f"Moved: {item['file']} to {item['destination']}")


def organise_files(path, dry_run=True, recursive=False, confirm=True):
    files=scan_directory(path, recursive)
    plan=build_move_plan(files)

    if not plan:
        print("\nNo files need to be organized. Everything is already sorted.")
        logging.info("No files to be organised")
        return

    show_plan(plan)
    
    if dry_run:
        logging.info("DRY RUN - No files moved  - Previewed move plan")
        print("\n------DRY RUN---(no files moved)---\n")
        return
    
    if confirm:
        if get_user_confirmation():
            execute_move_plan(plan)
            print("\nFiles have been moved successfully.")
        else:
            logging.warning("OPERATION CANCELLED by user")
            print("Operation cancelled. No files were moved.")
    else:
        execute_move_plan(plan)
        print("\nFiles have been moved successfully.")

def get_user_confirmation():
    choice = input("\nProceed with moving files? (y/n): ").lower()

    return choice == "y"

def get_folder_stats(path, recursive=False):
    files = scan_directory(path, recursive=recursive)

    stats = defaultdict(int)

    for file_path in files:
        filename = os.path.basename(file_path)
        category = get_category(filename)
        stats[category] += 1

    return stats


def build_single_file_plan(file_path):
    filename=os.path.basename(file_path)
    category= get_category(filename)
    current_folder=os.path.dirname(file_path)

    if os.path.basename(current_folder) == category:
        return []

    destination_folder= os.path.join(current_folder, category)
    destination = os.path.join (destination_folder, filename)

    destination=get_unique_destination(destination)
    plan=[
        {
            "file": filename,
            "source": file_path, 
            "destination_folder": destination_folder,
            "destination": destination, 
            "category": category
        }
    ]
    
    return plan


def organise_single_file(file_path):
    plan = build_single_file_plan(file_path)

    if not plan:
        return
    
    execute_move_plan(plan)

def save_move_history(source, destination):
    import os
    import json

    history = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.append({
        "source": source,
        "destination": destination
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def undo_last_move():
    import json
    import os
    import shutil

    if not os.path.exists(HISTORY_FILE):
        print("No history found.")
        return

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    if not history:
        print("Nothing to undo.")
        return

    last_move = history.pop()

    source = last_move["source"]
    destination = last_move["destination"]

    if os.path.exists(destination):
        os.makedirs(os.path.dirname(source), exist_ok=True)
        shutil.move(destination, source)
        print(f"Undone: {destination} → {source}")
    else:
        print("File already missing, cannot undo.")

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

