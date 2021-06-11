# Chess matcher

Chess tournament organizer with a curses TUI

Made for Linux.\
Works on Windows, but with display glitches (menus not refreshing, input field boxes glitching after refresh)

## setup

First clone the repo :
```bash
git clone https://github.com/BNNJ/Project4.git
```
or with gh CLI:
```bash
gh repo clone BNNJ/Project4
```

Then go into the directory and make a virtual environment:
```bash
cd Project4
python3 -m venv .
```

Source the environment script:
| Platform    | Shell             | Command to activate virtual environment |
| ------------|-------------------|---------------------------------------- |
| POSIX       | bash/zsh          | `$ source ./bin/activate`               |
|             | fish              | `$ source ./bin/activate.fish`          |
|             | csh/tcsh          | `$ source ./bin/activate.csh`           |
|             | PowerShell Core   | `$ ./bin/Activate.ps1`                  |
| Windows     | cmd.exe           | `C:\> .\Scripts\activate.bat`           |
|             | PowerShell        | `PS C:\> .\Scripts\Activate.ps1`        |

now install required modules:\
for Linux/macOs:
```bash
pip install -r requirements.txt
```
for Windows:
```bash
pip install -r requirements-windows.txt
```

## usage

```bash
./chess.py [-p/--players player_database] [-t/--tournaments tournament_database]
```
or for windows:
```bash
python ./chess.py [-p/--players player_database] [-t/--tournaments tournament_database]
```

## arguments

argument            | effect
--------------------|-------
-h, --help          | show help message and exit
-t, --tournaments T | specify tournaments database
-p, --players P     | specify players database
