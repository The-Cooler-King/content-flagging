# File Interaction

## Overview
This application will be interacting with PDF's and CSV's and will be built on a Windows machine, but likely used on a
macOS machine. It needs to read/write to files and navigate the local file system in a robust manner. I will document
what I learn in this domain here.

### Python's `pathlib` module
A part of the standard python library, `pathlib` is a powerful module that provides the `Path` class which will be used
to create robust file path objects instead of raw strings that are commonly used with the more familiar `os.path`.

#### Strengths
1. Cleaner syntax
```python
from pathlib import Path

p = Path("../lists") / "file.csv"
print(p)  # "../lists/file.csv"

# versus

import os.path

p = os.path.join("../lists", "file.csv")
print(p) # "../lists/file.csv"
```

2. Cross-platform safe
The notorious backslash `(\)` for Windows vs. foward slash `(/)` for Linux/macOS is handled automatically

3. Useful built-in methods
```python
from pathlib import Path

p = Path("../lists") / "file.csv"

print(p.stem)   # "file" (filename without extension)
print(p.suffix) # ".csv"
print(p.name)   # "file.csv"
print(p.parent) # "..\lists"
```
4. Built-in operations
```python
from pathlib import Path

p = Path("../lists") / "file.csv"
d = Path("../lists")

def test_operations(path_object):
    if path_object.exists():
        print("Yes!")
    if path_object.is_file():
        print("It’s a file")
    if path_object.is_dir():
        print("It’s a directory")
        
test_operations(p)
# "Yes!"
# "It’s a file"
test_operations(d)

```