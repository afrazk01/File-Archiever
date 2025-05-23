import FreeSimpleGUI as sg
import zipfile
import os

def zip_files(file_list, destination_folder):
    zip_path = os.path.join(destination_folder, 'archive.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file_path in file_list:
            arcname = os.path.basename(file_path)
            zipf.write(file_path, arcname=arcname)
    return zip_path

def unzip_file(zip_file, destination_folder):
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        zipf.extractall(destination_folder)

# GUI Layout
sg.theme('DarkBlue3')
layout = [
    [sg.Text('📦 Zip & Unzip Utility', font=('Helvetica', 20), justification='center', expand_x=True)],
    [sg.Frame('Create ZIP File', [
        [sg.Text('Select Files:'), sg.Input(key='-FILES-', enable_events=True, expand_x=True), sg.FilesBrowse()],
        [sg.Text('Destination Folder:'), sg.Input(key='-ZIP_DEST-', expand_x=True), sg.FolderBrowse()],
        [sg.Button('Create ZIP', key='-ZIP-')]
    ], expand_x=True)],

    [sg.Frame('Unzip Archive', [
        [sg.Text('Select ZIP File:'), sg.Input(key='-ZIP_FILE-', expand_x=True), sg.FileBrowse(file_types=(("Zip Files", "*.zip"),))],
        [sg.Text('Destination Folder:'), sg.Input(key='-UNZIP_DEST-', expand_x=True), sg.FolderBrowse()],
        [sg.Button('Unzip File', key='-UNZIP-')]
    ], expand_x=True)],

    [sg.Output(size=(100, 10))]
]

window = sg.Window('Zip & Unzip Tool', layout, resizable=True)

# Event Loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == '-ZIP-':
        files = values['-FILES-'].split(';') if values['-FILES-'] else []
        dest = values['-ZIP_DEST-']
        if not files or not dest:
            print("⚠️ Please select files and a destination folder.")
        else:
            try:
                zip_path = zip_files(files, dest)
                print(f"✅ ZIP created: {zip_path}")
            except Exception as e:
                print(f"❌ Error zipping files: {e}")

    elif event == '-UNZIP-':
        zip_file = values['-ZIP_FILE-']
        dest = values['-UNZIP_DEST-']
        if not zip_file or not dest:
            print("⚠️ Please select a ZIP file and a destination folder.")
        else:
            try:
                unzip_file(zip_file, dest)
                print(f"✅ Unzipped to: {dest}")
            except Exception as e:
                print(f"❌ Error unzipping file: {e}")

window.close()
