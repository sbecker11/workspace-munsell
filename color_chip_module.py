from pathlib import Path
from hashlib import sha256

# Maintain a set of unique line hashes
line_hashes = set()

def createFile(filename):
    global file_path
    file_path = Path(filename)
    
    # Check if file exists, and delete if it does
    if file_path.exists():
        file_path.unlink()

    # Create a new file
    file_path.touch()

def addLine(line):
    # Compute the hash of the line
    line_hash = sha256(line.encode()).hexdigest()

    # If the hash is in the set of hashes, the line is a duplicate
    if line_hash in line_hashes:
        return

    # If the hash is not in the set, add it and write the line to the file
    line_hashes.add(line_hash)
    with file_path.open('a') as file:
        file.write(line + '\n')
