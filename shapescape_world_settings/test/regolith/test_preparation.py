'''
A quick script that sets up the level.dat file for testing.
'''
from pathlib import Path
import sys
import shutil
import os

def main():
    test_path = Path(os.environ['ROOT_DIR']).parent
    original = (test_path / 'level.dat.original')
    updated = (test_path / 'level.dat')
    if updated.exists():
        updated.unlink()
    shutil.copy(original, updated)

if __name__ == "__main__":
    main()