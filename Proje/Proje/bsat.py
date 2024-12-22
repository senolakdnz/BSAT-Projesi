import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

class MyEventHandler(FileSystemEventHandler):
    def __init__(self, log_file, directory_to_watch):
        self.log_file = log_file
        self.directory_to_watch = directory_to_watch

    def on_any_event(self, event):
        if event.is_directory:
            return None

        change_type = ""
        if event.event_type == "created":
            change_type = "created"
        elif event.event_type == "deleted":
            change_type = "deleted"
        elif event.event_type == "modified":
            change_type = "modified"
        elif event.event_type == "moved":
            change_type = "moved"

        data = {
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "file": event.src_path,
                "change_type": change_type,
                }
        self.write_to_log(data)

    def write_to_log(self, data):
        try:
            with open(self.log_file, 'r') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        existing_data.append(data)
        with open(self.log_file, 'w') as f:
            json.dump(existing_data, f, indent=4)

if __name__ == "__main__":

    log_file = "/home/ubuntu/bsm/logs/changes.json"
    directory_to_watch = "/home/ubuntu/bsm/test" #Takip edilecek dizin

    event_handler = MyEventHandler(log_file, directory_to_watch)
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
