# Nokia Snake 3310

A classic Snake game inspired by the Nokia 3310, built with Python and Pygame.

## Run from source

```powershell
py -m pip install pygame-ce
py snake_3310.py
```

## Build a Windows executable

Install PyInstaller:

```powershell
py -m pip install pyinstaller
```

Build:

```powershell
py -m PyInstaller --clean --noconfirm --onefile --windowed --name "Nokia Snake 3310" snake_3310.py
```

The executable will be created in the `dist` folder.

## Controls

- Arrow keys, WASD, or 2/4/6/8: move
- Enter or Space: start / restart
- P or Escape: pause
- Mouse/touch-style on-screen keypad: use the phone controls
