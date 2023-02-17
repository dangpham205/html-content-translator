from translator import translate_worker
import sys
import multiprocessing
import os


def translate_all():
    html_folder = r"../web/"  
    html_files = os.listdir(html_folder)
    # since I'm having an images folder inside web folder so I'll will need to filter, only using html files
    html_files = [f"../web/{html_file}" for html_file in html_files if html_file[-5:] == ".html"]
    # not forget the index.html file that is not inside the web folder
    html_files.append('../index.html')

    processes = []
    arg_list = [(html_files, i, i+4) for i in range(0, len(html_files)+1, 4)]
    for args in arg_list:
        process = multiprocessing.Process(target=translate_worker, args=args)
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

def translate_again(path):
    html_files = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            html_files.append(line)
    processes = []
    batch_size = 2
    arg_list = [(html_files, i, i+batch_size) for i in range(0, len(html_files) + 1, batch_size)]
    for args in arg_list:
        process = multiprocessing.Process(target=translate_worker, args=args)
        processes.append(process)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

if __name__ == '__main__':
    # translate_again('failed_files.txt')

    translate_all()

