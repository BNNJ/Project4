# Chess matcher

Chess tournament organizer with a curses TUI

## todo

Make windows req.txt, make sure everything works there
	- display bugs all over the place
	- match bug : all matches are player1 vs player1

fix empty date bug

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

now install required modules:
```bash
pip install -r requirement.txt
```

## usage


## arguments

argument            | effect
--------------------|-------
-h, --help          | show help message and exit
-t, --tournaments T | specify tournaments database
-p, --players P     | specify players database

## examples
