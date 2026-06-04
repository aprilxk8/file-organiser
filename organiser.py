#scan->create folder->move
import os
import shutil
import logging

from config import FILE_TYPES

logging.basicConfig(
    filename="organiser.log",
    level=logging.INFO,
    format="%(asctime)s- %(levelname)s -%(message)s"
)


def get_category(file_name):
    extension= os.path.splitext(file_name)[1].lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category
    return "Others"


def scan_directory(path):
    items=os.listdir(path)
    files=[]
    #folders=[]
    for item in items:
        full_path=os.path.join(path, item)
        if os.path.isfile(full_path):
            files.append(full_path)
    #     else:
    #         folders.append(full_path)
    # return files, folders
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
        destination_folder= os.path.join(os.path.dirname(file_path), category)
        destination = os.path.join (destination_folder, filename)
        destination=get_unique_destination(destination)

        # if file_path == destination:
        #     continue
        if os.path.abspath(file_path) == os.path.abspath(destination): 
            #check if absolute value of path is same 
            continue

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

    logging.info(f"MOVED: {item['file']} | {item['source']} -> {item['destination']}")        
    print(f"Moved: {item['file']} to {item['destination']}")
    logging.info("MOVE OPERATION COMPLETED")


def organise_files(path, dry_run=True):
    files=scan_directory(path)
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
    
    
    if get_user_confirmation():
        execute_move_plan(plan)
        print("\nFiles have been moved successfully.")
    else:
        logging.warning("OPERATION CANCELLED by user")
        print("Operation cancelled. No files were moved.")


def get_user_confirmation():
    choice = input("\nProceed with moving files? (y/n): ").lower()

    return choice == "y"
