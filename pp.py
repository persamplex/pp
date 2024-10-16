import os
import sys
import platform
import argparse
import shutil
import json
import random
from datetime import datetime

def check_os():
    return platform.system()


def add_alias_to_registry(command, script_path):
    import winreg as reg
    reg_key_path = r'Software\Microsoft\Command Processor'
    try:
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, reg_key_path, 0, reg.KEY_SET_VALUE)
        command_value = f'DOSKEY {command}={sys.executable} "{script_path}" $*'
        reg.SetValueEx(reg_key, 'AutoRun', 0, reg.REG_SZ, command_value)
        print(f"Alias '{command}' added to CMD.")
        reg.CloseKey(reg_key)
    except Exception as e:
        print(f"Error adding alias to registry: {e}")


def add_alias_to_bash(command, script_path):
    try:
        bash_aliases_path = os.path.expanduser('~/.bash_aliases')
        if not os.path.exists(bash_aliases_path):
            with open(bash_aliases_path, 'w') as f:
                f.write('# Aliases\n')
        with open(bash_aliases_path, 'a') as f:
            f.write(f"alias {command}='{sys.executable} \"{script_path}\"'\n")
        print(f"Alias '{command}' added to .bash_aliases.")
    except Exception as e:
        print(f"Error adding alias to .bash_aliases: {e}")


def install_alias():
    script_path = os.path.abspath(__file__)
    os_name = check_os()
    if os_name == "Windows":
        add_alias_to_registry('pp', script_path)
    elif os_name == "Linux":
        add_alias_to_bash('pp', script_path)
    else:
        print(f"Alias installation is not supported on {os_name}.")


def make_backup(point, comment=None):
    if comment is None:
        comment = "No Message"
        
    current_dir = os.getcwd()
    pp_folder = os.path.join(current_dir, 'pp')
    os.makedirs(pp_folder, exist_ok=True)

    if point == "None":
        point = os.getcwd()
        
    if os.path.exists(point):
        tag = random.randint(100000, 999999)
        file_name = os.path.basename(point)

        tagged_folder = os.path.join(pp_folder, f"backup_{tag}")
        while os.path.exists(tagged_folder):
            tag = random.randint(100000, 999999)
            tagged_folder = os.path.join(pp_folder, f"backup_{tag}")

        os.makedirs(tagged_folder)

        if os.path.isfile(point):
            shutil.copy2(point, os.path.join(tagged_folder, file_name))
            print(f"Backup of file '{point}' created in '{tagged_folder}'.")
        
        elif os.path.isdir(point):
            for item in os.listdir(point):
                s = os.path.join(point, item)
                d = os.path.join(tagged_folder, item)
                if os.path.isdir(s) and s != tagged_folder and os.path.basename(s) != 'pp':
                    shutil.copytree(s, d, dirs_exist_ok=True)
                elif os.path.basename(s) != 'pp':
                    shutil.copy2(s, d)
            print(f"Backup of directory '{point}' created in '{tagged_folder}'.")
        else:
            print("The provided path is neither a file nor a directory.")
        
        # Update the datasheet
        datasheet_path = os.path.join(pp_folder, 'datasheet.json')
        if not os.path.exists(datasheet_path):
            with open(datasheet_path, 'w') as f:
                json.dump({}, f)

        metadata = {
            "file_name": file_name,
            "date": datetime.now().strftime("%Y/%m/%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "comment": comment,
            "tag": tag,
            "file_path": tagged_folder,
            "source_path": os.path.abspath(point)
        }

        with open(datasheet_path, 'r+') as f:
            datasheet = json.load(f)
            datasheet[tag] = metadata
            f.seek(0)
            json.dump(datasheet, f, indent=4)
            f.truncate()

        print(f"Updated '{datasheet_path}' with new backup metadata.")
    else:
        print(f"The path '{point}' does not exist.")


def edit_comment(new_comment, tag):
    pp_folder = os.path.join(os.getcwd(), 'pp')
    
    if not os.path.exists(pp_folder):
        print("There is no point here.")
        return

    datasheet_path = os.path.join(pp_folder, 'datasheet.json')
    
    if not os.path.exists(datasheet_path):
        print("There is no datasheet available.")
        return

    with open(datasheet_path, 'r+') as f:
        datasheet = json.load(f)

        if str(tag) not in datasheet:
            print(f"No point found with tag {tag}.")
            return

        datasheet[str(tag)]['comment'] = new_comment
        print(f"Comment for tag {tag} updated to: {new_comment}")

        f.seek(0)
        json.dump(datasheet, f, indent=4)
        f.truncate()


def print_point(file_name):
    if file_name == "None":
        file_name = None
    pp_folder = os.path.join(os.getcwd(), 'pp')
    
    if not os.path.exists(pp_folder):
        print("There is no point here.")
        return

    datasheet_path = os.path.join(pp_folder, 'datasheet.json')
    
    if not os.path.exists(datasheet_path):
        print("There is no datasheet available.")
        return

    with open(datasheet_path, 'r') as f:
        datasheet = json.load(f)

    # Header for the table with fixed widths for alignment
    header = f"{'tag':<8} | {'[type] name':<20} | {'date time':<25} | comment"
    print(header)
    print('-' * len(header))  # separator line

    if file_name is None:
        sorted_entries = sorted(datasheet.values(), key=lambda x: (x["date"], x["time"]))
        
        for entry in sorted_entries:
            item_type = '[folder]' if os.path.isdir(entry['source_path']) else '[file]'
            tag_str = f"{entry['tag']:<8}"  # 8 character width for tag
            name_str = f"{item_type} {entry['file_name']}".ljust(20)  # 20 character width for name
            date_str = f"{entry['date']} {entry['time']}".ljust(25)  # 25 character width for date and time
            comment_str = entry['comment']  # comment field

            # Print the formatted row
            print(f"{tag_str} | {name_str} | {date_str} | {comment_str}")
    else:
        matched_entries = [entry for entry in datasheet.values() if entry['file_name'] == file_name]

        if not matched_entries:
            print(f"There is no point for {file_name}.")
        else:
            for entry in matched_entries:
                item_type = '[folder]' if os.path.isdir(entry['source_path']) else '[file]'
                tag_str = f"{entry['tag']:<8}"  # 8 character width for tag
                name_str = f"{item_type} {entry['file_name']}".ljust(20)  # 20 character width for name
                date_str = f"{entry['date']} {entry['time']}".ljust(25)  # 25 character width for date and time
                comment_str = entry['comment']  # comment field

                # Print the formatted row
                print(f"{tag_str} | {name_str} | {date_str} >> | {comment_str}")


def make_point(file_path, comment=None):
    if comment is None:
        comment = "No Message"
    current_dir = os.getcwd()

    pp_folder = os.path.join(current_dir, 'pp')
    os.makedirs(pp_folder, exist_ok=True)

    file_name = os.path.basename(file_path)
    tag = random.randint(100000, 999999)

    tagged_folder = os.path.join(pp_folder, f"{file_name}_{tag}")
    while os.path.exists(tagged_folder):
        tag = random.randint(100000, 999999)
        tagged_folder = os.path.join(pp_folder, f"{file_name}_{tag}")

    os.makedirs(tagged_folder)
    
    shutil.copy2(file_path, os.path.join(tagged_folder, file_name))
    print(f"Copied '{file_name}' to '{tagged_folder}'.")

    datasheet_path = os.path.join(pp_folder, 'datasheet.json')
    if not os.path.exists(datasheet_path):
        with open(datasheet_path, 'w') as f:
            json.dump({}, f)

    metadata = {
        "file_name": file_name,
        "date": datetime.now().strftime("%Y/%m/%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "comment": comment,
        "tag": tag,
        "file_path": os.path.join(tagged_folder, file_name),
        "source_path": os.path.abspath(file_path)
    }

    with open(datasheet_path, 'r+') as f:
        datasheet = json.load(f)
        
        datasheet[tag] = metadata
        
        f.seek(0)
        json.dump(datasheet, f, indent=4)
        f.truncate()

    print(f"Updated '{datasheet_path}' with new metadata.")


def remove_point(tag):
    pp_folder = os.path.join(os.getcwd(), 'pp')

    if not os.path.exists(pp_folder):
        print("There is no point here.")
        return

    datasheet_path = os.path.join(pp_folder, 'datasheet.json')

    if not os.path.exists(datasheet_path):
        print("There is no datasheet available.")
        return

    with open(datasheet_path, 'r') as f:
        datasheet = json.load(f)

    if str(tag) not in datasheet:
        print(f"No point found with tag {tag}.")
        return

    # Get the file path associated with the tag
    file_path = datasheet[str(tag)]['file_path']
    
    if os.path.isdir(file_path):
        tagged_folder = file_path
    else:
        tagged_folder = os.path.dirname(file_path)

    try:
        shutil.rmtree(tagged_folder)
        print(f"Folder '{tagged_folder}' has been removed.")
    except Exception as e:
        print(f"Error while removing folder: {e}")
        return

    # Remove the entry from the datasheet
    del datasheet[str(tag)]

    # Write the updated datasheet back to the file
    with open(datasheet_path, 'w') as f:
        json.dump(datasheet, f, indent=4)

    print(f"The {tag} point was removed successfully.")



def restore_point(tag):
    pp_folder = os.path.join(os.getcwd(), 'pp')   
    if not os.path.exists(pp_folder):
        print("There is no point here.")
        return

    datasheet_path = os.path.join(pp_folder, 'datasheet.json')
    
    if not os.path.exists(datasheet_path):
        print("There is no datasheet available.")
        return

    with open(datasheet_path, 'r') as f:
        datasheet = json.load(f)

    matched_entry = None
    for entry in datasheet.values():
        if entry['tag'] == tag:
            matched_entry = entry
            break

    if not matched_entry:
        print(f"No point found with tag {tag}.")
        return

    source_path = matched_entry['source_path']
    file_path = matched_entry['file_path']

    # Check if the file_path is a directory
    if os.path.isdir(file_path):
        if os.path.exists(source_path):
            for item in os.listdir(source_path):
                item_path = os.path.join(source_path, item)
                if item_path != pp_folder:  # Avoid deleting the pp folder
                    try:
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    except PermissionError:
                        print(f"PermissionError: pp can not access to the {item_path}.")
                        print("Found the app that still in use by another process and will kill it.")
                        return

        shutil.copytree(file_path, source_path, dirs_exist_ok=True)
        print(f"Restored directory from '{file_path}' to '{source_path}'.")
    else:
        if not os.path.exists(source_path):
            with open(source_path, 'w') as f:
                pass
            print(f"File '{source_path}' created as it did not exist.")
        
        try:
            shutil.copy2(file_path, source_path)
            print(f"Restored file from '{file_path}' to '{source_path}'")
        except PermissionError:
            print(f"PermissionError: pp can not access to the {source_path}.")
            print("Found the app that still in use by another process and will kill it.")
            return

def main():
    parser = argparse.ArgumentParser(description="IMPORTANT: Please use --install to make Bash Alias or Registry for windows")
    parser.add_argument('--install', '-i', action='store_true', help='Install the alias for the script.')
    parser.add_argument('--version', '-v', action='store_true', help='Show the version of the script.')
    parser.add_argument('--backup', '-b', type=str, nargs='?', const='None', help='Make a backup point from a file or directory.')
    parser.add_argument('--point', '-p', type=str, help='Specify a file path to make a point of the file.')
    parser.add_argument('--comment', '-c', type=str, help='Textual content to comment (must be used with --point or --backup).')
    parser.add_argument('--print-point', '-pr','-ls', type=str, nargs='?', const='None', help='Print points from datasheet (optional file name).')
    parser.add_argument('--restore-point', '-re', type=int, help='Restore file using the specified tag.')
    parser.add_argument('--remove-point', '-rm', type=int, help='Remove restore point using the specified tag.')
    parser.add_argument('--tag', '-t', type=int, help='Use to specify a tag.')

    args = parser.parse_args()

    if args.install:
        install_alias()
    elif args.version:
        print("Script version: 1.0.2")
    elif args.point:
        make_point(args.point, args.comment)
    elif args.backup:
        make_backup(args.backup, args.comment)
    elif args.comment and args.tag:
        edit_comment(args.comment, args.tag)
    elif args.comment:
        print('You can only use --comment with --point, --backup, or --tag.')
    elif args.tag:
        print('The --tag or -t is used to specify a tag number.')
    elif args.print_point:
        print_point(args.print_point)
    elif args.restore_point:
        restore_point(args.restore_point)
    elif args.remove_point:
        remove_point(args.remove_point)
    else:
        print("Use pp --help to see Manual")

if __name__ == "__main__":
    main()
