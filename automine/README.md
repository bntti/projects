# Automine

Python minesweeper with automatic flag adding and tile opening.

## Usage
### Dependencies
- poetry

### Installation
```
poetry install
```

### Running the program
```
poetry run python3 main.py
```

### Using the program
Clicking on an open tile with the same amount of flags as mines will open all unflagged neighboring empty tiles.

| Keybind | Action                                 |
| ------- | -------------------------------------- |
| `q`     | quit                                   |
| `w`     | automatically add flags                |
| `s`     | automatically open tiles               |
| `a`     | automatically add flags and open tiles |

#### Playing with a mouse
| Keybind     | Action      |
| ----------- | ----------- |
| left click  | open tile   |
| right click | flag/unflag |

 
#### Playing with a keyboard
| Keybind       | Action      |
| ------------- | ----------- |
| arrow keys    | move        |
| space         | open tile   |
| shift + space | flag/unflag |
