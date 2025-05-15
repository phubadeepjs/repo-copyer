import os
import fnmatch
from pathlib import Path
from typing import List, Tuple
import aiofiles
from aiofiles.os import wrap

# Wrap os functions for async use
os_listdir = wrap(os.listdir)
os_path_exists = wrap(os.path.exists)
os_makedirs = wrap(os.makedirs)
os_path_join = os.path.join
os_path_relpath = os.path.relpath
os_path_basename = os.path.basename
os_path_abspath = os.path.abspath
os_path_dirname = os.path.dirname

async def get_file_tree(startpath: str, exclude_patterns: Tuple[str, ...] = None) -> str:
    """Generate a tree representation of the directory structure.
    
    Args:
        startpath: Root directory path
        exclude_patterns: Patterns to exclude from the tree
        
    Returns:
        String representation of the directory tree
    """
    if exclude_patterns is None:
        from src.config.settings import EXCLUDE_PATTERNS
        exclude_patterns = EXCLUDE_PATTERNS

    tree_lines = []

    async def tree(dir_path: str, prefix: str = "") -> None:
        try:
            entries = []
            for entry in await os_listdir(dir_path):
                if any(fnmatch.fnmatch(entry, pattern) for pattern in exclude_patterns):
                    continue
                entries.append(entry)
            for idx, entry in enumerate(sorted(entries)):
                full_path = os_path_join(dir_path, entry)
                connector = "+-- " if idx == len(entries) - 1 else "|-- "
                tree_lines.append(f"{prefix}{connector}{entry}")
                if await os_path_exists(full_path) and os.path.isdir(full_path):
                    extension = "    " if idx == len(entries) - 1 else "|   "
                    await tree(full_path, prefix + extension)
        except PermissionError:
            tree_lines.append(f"{prefix}[Permission Denied]")

    tree_lines.append(os_path_basename(os_path_abspath(startpath)) + "/")
    await tree(startpath)
    return "\n".join(tree_lines)

def wrap_text(text: str, width: int) -> str:
    """Wrap text to a specified width.
    
    Args:
        text: The text to wrap
        width: Maximum width of each line
        
    Returns:
        Wrapped text with line breaks
    """
    lines = text.split('\n')
    wrapped_lines = []
    
    for line in lines:
        if len(line) <= width:
            wrapped_lines.append(line)
            continue
            
        current_line = ''
        words = line.split(' ')
        
        for word in words:
            if len(current_line) + len(word) + 1 <= width:
                if current_line:
                    current_line += ' ' + word
                else:
                    current_line = word
            else:
                if current_line:
                    wrapped_lines.append(current_line)
                current_line = word
                
        if current_line:
            wrapped_lines.append(current_line)
            
    return '\n'.join(wrapped_lines)

async def get_files_to_process(repo_path: str) -> List[str]:
    """Get list of files to process from repository.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        List of file paths to process
    """
    from src.config.settings import EXCLUDE_PATTERNS
    
    files_to_process = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            file_path = os_path_join(root, file)
            rel_path = os_path_relpath(file_path, repo_path)
            if not any(fnmatch.fnmatch(rel_path, pattern) for pattern in EXCLUDE_PATTERNS):
                files_to_process.append(file_path)
    return files_to_process
