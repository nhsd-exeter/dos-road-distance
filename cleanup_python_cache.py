#!/usr/bin/env python3
"""
Cleanup script to remove Python cache files and directories safely.
This script handles permission issues that can occur with __pycache__ directories.
"""

import os
import shutil
import stat
import sys
from pathlib import Path


def make_writable(func, path, exc_info):
    """
    Error handler for shutil.rmtree to make files writable before deletion.
    """
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR | stat.S_IWRITE)
        func(path)
    else:
        raise


def cleanup_python_cache(root_dir='.'):
    """
    Clean up Python cache files and directories.

    Args:
        root_dir (str): Root directory to start cleanup from. Defaults to current directory.
    """
    root_path = Path(root_dir).resolve()

    print(f"Starting Python cache cleanup from: {root_path}")

    # Patterns to clean
    patterns = [
        '**/__pycache__',
        '**/*.pyc',
        '**/*.pyo',
        '**/*$py.class',
        '**/*.so'
    ]

    cleaned_files = 0
    cleaned_dirs = 0

    for pattern in patterns:
        for path in root_path.glob(pattern):
            try:
                if path.is_dir():
                    # Remove __pycache__ directories
                    print(f"Removing directory: {path}")
                    shutil.rmtree(path, onerror=make_writable)
                    cleaned_dirs += 1
                elif path.is_file():
                    # Remove cache files
                    print(f"Removing file: {path}")
                    # Make sure file is writable before deletion
                    if not os.access(path, os.W_OK):
                        os.chmod(path, stat.S_IWUSR | stat.S_IWRITE)
                    path.unlink()
                    cleaned_files += 1
            except (OSError, PermissionError) as e:
                print(f"Warning: Could not remove {path}: {e}")
                continue

    print(f"Cleanup complete. Removed {cleaned_dirs} directories and {cleaned_files} files.")
    return cleaned_dirs + cleaned_files > 0


if __name__ == '__main__':
    # Allow specifying root directory as command line argument
    root_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

    try:
        success = cleanup_python_cache(root_dir)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error during cleanup: {e}")
        sys.exit(1)
