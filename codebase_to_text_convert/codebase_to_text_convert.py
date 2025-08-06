import os
import argparse
import pathlib

def is_binary_file(filepath):
    """
    Check if a file is binary by reading a small chunk and looking for null bytes.
    """
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)  # Read first 1KB
            return b'\0' in chunk
    except:
        return True  # If we can't read it, assume it's binary

def should_skip_path(path, skip_folders):
    """
    Check if the path contains any folder that should be skipped.
    """
    if not skip_folders:
        return False
    
    # Convert path to normalized absolute path
    path_obj = pathlib.Path(path).resolve()
    path_parts = path_obj.parts
    
    # Check if any part of the path matches a folder to skip
    return any(skip_folder in path_parts for skip_folder in skip_folders)

def printFolderStructure(directory, output_file, skip_folders=None, project_root=None):
    # Show relative path from project root instead of absolute path
    if project_root:
        rel_path = os.path.relpath(directory, project_root)
        display_path = rel_path if rel_path != '.' else 'PROJECT_ROOT'
    else:
        display_path = directory
    output_file.write(f"### DIRECTORY {display_path} FOLDER STRUCTURE ###\n")
    
    # Get the absolute path for the directory
    abs_directory = os.path.abspath(directory)
    
    for root, dirs, files in os.walk(directory):
        # Check if the current path should be skipped
        if should_skip_path(root, skip_folders):
            # Remove all directories to prevent further traversal
            dirs.clear()
            continue
        
        # Filter out directories that should be skipped before recursing into them
        i = 0
        while i < len(dirs):
            dir_path = os.path.join(root, dirs[i])
            if should_skip_path(dir_path, skip_folders):
                dirs.pop(i)
            else:
                i += 1
        
        # Calculate indentation level
        rel_path = os.path.relpath(root, directory)
        level = 0 if rel_path == '.' else rel_path.count(os.sep) + 1
        indent = ' ' * 4 * level
        
        # Write directory name
        if level == 0:
            output_file.write('{}{}/\n'.format(indent, os.path.basename(directory)))
        else:
            output_file.write('{}{}/\n'.format(indent, os.path.basename(root)))
        
        # Write file names
        subindent = ' ' * 4 * (level + 1)
        for f in sorted(files):
            output_file.write('{}{}\n'.format(subindent, f))
    
    output_file.write(f"### DIRECTORY {directory} FOLDER STRUCTURE ###\n\n")

def should_skip_file(filepath, skip_files):
    """
    Check if the file should be skipped based on filename patterns.
    """
    if not skip_files:
        return False
    
    filename = os.path.basename(filepath)
    
    # Check if filename matches any skip pattern
    for skip_pattern in skip_files:
        # Support glob-like patterns
        if '*' in skip_pattern:
            import fnmatch
            if fnmatch.fnmatch(filename, skip_pattern):
                return True
        else:
            # Exact match
            if filename == skip_pattern:
                return True
    
    return False

def walkFolderTree(folder, skip_folders=None, skip_files=None):
    for root, dirs, files in os.walk(folder):
        # Check if the current path should be skipped
        if should_skip_path(root, skip_folders):
            # Remove all directories to prevent further traversal
            dirs.clear()
            continue
        
        # Filter out directories that should be skipped before recursing into them
        i = 0
        while i < len(dirs):
            dir_path = os.path.join(root, dirs[i])
            if should_skip_path(dir_path, skip_folders):
                dirs.pop(i)
            else:
                i += 1
        
        # Yield files that should not be skipped
        for filename in files:
            filepath = os.path.join(root, filename)
            if not should_skip_file(filepath, skip_files):
                yield filepath

def main(project_folder=None, exclude_dirs=None, exclude_files=None, output_folder=None):
    if exclude_dirs is None:
        exclude_dirs = []
    if exclude_files is None:
        exclude_files = []
    
    # Set default output file path
    default_output = 'codebase.md'
    if output_folder:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        default_output = os.path.join(output_folder, 'codebase.md')
    
    parser = argparse.ArgumentParser(description='Flattens a codebase.')
    parser.add_argument('--folders', nargs='*', default=[project_folder] if project_folder else None, help='Base folders to process')
    parser.add_argument('--skip-folders', nargs='*', default=exclude_dirs, help='Folders to skip during processing')
    parser.add_argument('--skip-files', nargs='*', default=exclude_files, help='Files to skip during processing (supports patterns like *.log)')
    parser.add_argument('--system_instructions', action='store_true', help='Print system instructions')
    parser.add_argument('--output', default=default_output, help='Output file name (default: codebase.md)')
    
    system_instructions = """## System Instructions for Language Model Assistance in Code Debugging
### Codebase Markdown File Structure:
- The codebase markdown file represents the actual codebase structure and content.
- It begins with a directory tree representation:
  ```
  ### DIRECTORY path/to/file/tree FOLDER STRUCTURE ###
  (file tree representation)
  ### DIRECTORY path/to/file/tree FOLDER STRUCTURE ###
  ```
- Following the directory tree, the contents of each file are displayed:
  ```
  ### path/to/file1 BEGIN ###
  (content of file1)
  ### path/to/file1 END ###
  
  ### path/to/file2 BEGIN ###
  (content of file2)
  ### path/to/file2 END ###
  ```
### Guidelines for Interaction:
- Respond to queries based on the explicit content provided within the markdown file.
- Avoid making assumptions about the code without clear evidence presented in the file content.
- When seeking specific implementation details, refer to the corresponding section in the markdown file, for example:
  ```
  ### folder1/folder2/myfile.ts BEGIN ###
  (specific implementation details)
  ### folder1/folder2/myfile.ts END ###
  ```
### Objective:
- The primary objective is to facilitate understanding of codebase by providing accurate information and guidance strictly adhering to the content available in the markdown file."""

    args = parser.parse_args()
    
    if args.system_instructions:
        print(system_instructions)
        if not args.folders:
            return
    
    if args.folders:
        base_folders = args.folders
        skip_folders = args.skip_folders
        skip_files = args.skip_files
        
        with open(args.output, 'w', encoding='utf-8') as output_file:
            for base_folder in base_folders:
                printFolderStructure(base_folder, output_file, skip_folders, base_folder)
                
                # Show relative path from project root instead of absolute path
                rel_path = os.path.relpath(base_folder, base_folder)
                display_path = rel_path if rel_path != '.' else 'PROJECT_ROOT'
                output_file.write(f"### DIRECTORY {display_path} FLATTENED CONTENT ###\n")
                for filepath in walkFolderTree(base_folder, skip_folders, skip_files):
                    # Show relative path from project root instead of absolute path
                    rel_filepath = os.path.relpath(filepath, base_folder)
                    
                    # Skip binary files
                    if is_binary_file(filepath):
                        content = f"### {rel_filepath} BEGIN ###\n"
                        content += "[Binary file - content skipped]\n"
                        content += f"### {rel_filepath} END ###\n\n"
                        output_file.write(content)
                        continue
                    
                    content = f"### {rel_filepath} BEGIN ###\n"
                    
                    try:
                        with open(filepath, "r", encoding='utf-8', errors='replace') as f:
                            content += f.read()
                        content += f"\n### {rel_filepath} END ###\n\n"
                    except Exception as e:
                        # Better error handling
                        content += f"[Error reading file: {str(e)}]\n"
                        content += f"### {rel_filepath} END ###\n\n"
                    
                    output_file.write(content)
                output_file.write(f"### DIRECTORY {display_path} FLATTENED CONTENT ###\n")
    else:
        print("usage: main.py [-h] --folders FOLDERS [FOLDERS ...] [--skip-folders SKIP_FOLDERS [SKIP_FOLDERS ...]] [--skip-files SKIP_FILES [SKIP_FILES ...]] [--system_instructions] [--output OUTPUT]")
        print("Error: the following arguments are required: --folders")

if __name__ == "__main__":
    project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if not os.path.exists(project_folder):
        raise FileNotFoundError(f"Project folder not found: {project_folder}")

    exclude_dirs = ['__pycache__', '.git', '.vscode', 'env', 'data', '.venv', 'node_modules', 'logs', 'codebase_to_text_convert', 'migrations']
    exclude_files = ['*.pyc', '*.log', '*.tmp', '.DS_Store', 'Thumbs.db', '*.swp', '*.swo', '.env', 'pnpm-lock.yaml', 'poetry.lock', 'yarn.lock', 'webpack-stats.json']
    output_folder = os.path.join(project_folder, 'codebase_to_text_convert', 'output')
    main(project_folder, exclude_dirs, exclude_files, output_folder)
