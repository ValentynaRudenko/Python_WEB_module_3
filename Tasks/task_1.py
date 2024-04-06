import shutil
from pathlib import Path
from threading import Thread
import logging


def process_directory(source_directory, destination_directory):
    source_path = Path(source_directory)
    destination_path = Path(destination_directory)

    for item in source_path.glob('**/*'):
        if item.is_dir():

            # logging.basicConfig(level=logging.DEBUG,
            #                     format='%(threadName)s %(message)s')
            thread = Thread(target=process_directory,
                            args=(item, destination_directory))
            thread.start()

            # process_directory(item, destination_directory)
            logging.debug("is_dir")
        else:
            extension = item.suffix.lower()
            extension_folder = destination_path / extension[1:]
            extension_folder.mkdir(parents=True, exist_ok=True)

            destination_file = extension_folder / item.name
            shutil.copy2(item, destination_file)
            logging.debug("file")

    destination_folders = sorted(destination_path.glob('*'))

    for i, folder in enumerate(destination_folders):
        if folder.is_dir():
            # logging.basicConfig(level=logging.DEBUG,
            #                     format='%(threadName)s %(message)s')
            # thread = Thread(target=process_directory,
            #                 args=(source_directory, destination_directory))
            # thread.start()
            new_folder_name = destination_path / folder.name
            folder.rename(new_folder_name)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(threadName)s %(message)s')
    # thread = Thread(target=process_directory,
    #                 args=("Python_WEB_module_3/source_dir",
    #                       "Python_WEB_module_3/dest_dir"))
    # thread.start()
    process_directory("Python_WEB_module_3/source_dir",
                      "Python_WEB_module_3/dest_dir")
