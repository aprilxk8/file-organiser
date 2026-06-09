import logging
import time 
import os

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from organiser import get_category, organise_single_file

class FileHandler(FileSystemEventHandler):

    def on_created(self, event: FileSystemEvent):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)

        current_folder = os.path.basename(
            os.path.dirname(event.src_path)
        )

        category = get_category(filename)

        if current_folder == category:
            return
        
        print(f"\nDetected: {event.src_path}")
        logging.info(
            f"Detected file: {event.src_path}"
        )

        time.sleep(1)  
                                
        try:
            organise_single_file(event.src_path)

        except Exception as e:
            logging.error(
                f"Error processing {event.src_path}: {e}"
            )
            print(f"Error processing file: {e}")


def watch_directory(path, recursive=False):
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=recursive)
    observer.start()
    print(f"Watching directory: {path}")
    logging.info(f"Watching directory: {path}")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()
    observer.join()

