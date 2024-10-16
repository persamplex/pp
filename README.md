# pp - Python File Backup and Restore Utility

## Overview

`pp` is a Python-based tool designed to help users manage files and directories by creating backup points and restore points with ease. It provides cross-platform support for both Windows and Linux, allowing you to create system-level aliases for quick access. Whether you're safeguarding important files or tracking changes in your directories, `pp` offers a structured approach with restore points tagged for easy reference.

### Key Features
- **Cross-Platform Compatibility**: Seamless operation on both Windows and Linux systems.
- **Restore Points**: Easily create and manage restore points with unique tags for quick access.
- **Backup Functionality**: Backup files or directories for added security.
- **Alias Installation**: Automatically create an alias (`pp`) in your terminal for easy access to the script.
- **Comment System**: Add comments to restore points for better context and tracking.
- **Tag Management**: Manage your restore points using unique tags—view, restore, or remove points at any time.

## Installation

Ensure you have Python installed on your system. Clone or download this repository and navigate to the directory containing the `pp.py` script.

For easy access to the script, install the alias by running:
```bash
python pp.py --install
```
This will create a system alias `pp` that allows you to run the script from any terminal session.

## Usage

The script comes with several commands to help you manage your backups and restore points. Below are some key commands:

### Basic Commands

```bash
python pp.py --install         # Install an alias for the script (Windows/Linux)
python pp.py --version         # Show the script version
```

### Backup & Restore Operations

```bash
python pp.py --backup <path>           # Create a backup of the specified file or directory
python pp.py --point <path>            # Create a restore point for the specified file
python pp.py --comment <text> --tag <tag>  # Add a comment to a restore point using its tag
python pp.py --print-point <optional_file_name>  # List all restore points or those for a specific file
python pp.py --restore-point <tag>     # Restore the file or directory associated with the specified tag
python pp.py --remove-point <tag>      # Remove the restore point associated with the specified tag
```

## Detailed Command Breakdown

- **Backup a Directory or File**:
    ```bash
    python pp.py --backup /path/to/directory_or_file --comment "Your backup description"
    ```
    This will create a backup point with a unique tag, and you can include an optional comment.

- **Create a Restore Point**:
    ```bash
    python pp.py --point /path/to/file.txt --comment "Initial save"
    ```
    A restore point is created with a tag, storing the current state of the file.

- **Restore a Point**:
    ```bash
    python pp.py --restore-point <tag>
    ```
    Use this command to restore the file or directory to its state from a specific restore point using the unique tag.

- **View All Restore Points**:
    ```bash
    python pp.py --print-point
    ```
    This command will list all the restore points with details like tag, type (file or folder), date, time, and comments.

- **Remove a Restore Point**:
    ```bash
    python pp.py --remove-point <tag>
    ```
    Deletes the restore point associated with the specified tag.

- **Edit Comments**:
    ```bash
    python pp.py --comment "New comment" --tag <tag>
    ```
    Update or edit the comment of a specific restore point.

## Example Workflow

1. **Create a Restore Point**:
    ```bash
    python pp.py --point /path/to/your/file.txt --comment "Initial version"
    ```
   
2. **Create a Backup**:
    ```bash
    python pp.py --backup /path/to/your/directory
    ```

3. **Restore a Previous Point**:
    ```bash
    python pp.py --restore-point 123456  # Replace with your actual tag
    ```

4. **Remove a Point**:
    ```bash
    python pp.py --remove-point 123456  # Replace with your actual tag
    ```

## Under the Hood

### Core Functions
- **Alias Installation**: Adds an alias for `pp` in your terminal (Bash or CMD depending on the system).
- **Backup Creation**: Automatically organizes backups with unique tags and timestamps, storing metadata in a JSON file for easy management.
- **Restore Point Creation**: Saves the state of a file or directory, allowing for later restoration using its unique tag.
- **Restore Functionality**: Fully restores the file or directory to its backed-up state, replacing the original files with the backed-up versions.
- **Remove Points**: Allows you to delete a specific backup or restore point and its metadata.
- **Comment Editing**: Easily update or add comments to existing restore points for better context.

## Notes

- The alias `pp` can be used after installation for easier command execution.
- Ensure the `pp` folder, which stores backups, is not deleted unless intentional.
- The system uses tags to uniquely identify each restore or backup point.
- The `datasheet.json` file holds metadata for each point, including tag, date, time, and any comments.

## Conclusion

The `pp` utility is a reliable, cross-platform solution for managing file backups and restore points. By keeping a structured record of file versions, you can safeguard your work and easily restore previous versions when needed.
