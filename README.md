# Send discord messages from your terminal


## Setup

```python discord.py --setup```


## Usage

```python discord.py -m <message>```

```python discord.py -f /path/to/your/image/file.png```

## Other usage

1. Adding webhooks to the database

    ```python discord.py --add <name> <url>```

2. Editing webhooks in the database

    ```python discord.py --edit <name> <new_url>```

3. Deleting webhooks in the database

    ```python discord.py --delete <name>```

4. Sending to someone in your "contacts"

    ```python discord.py -m <message> -n <name>```

5. Listing your contacts

    ```python discord.py --list```

6. Finding webhook URL for a name

    ```python discord.py --fetch-url <name>```

7. Finding name for a URL

    ```python discord.py --fetch-name <url>```

8. Reconfiguring

    ```python discord.py --reconfigure```

9. Uninstalling 

    ```python discord.py --uninstall```


## Tweaks

This script creates two files in ~/.discordcli/
1. config.ini 
2. hooks.db

Both these files are important for usage

## Requirements

- ```pip install discord_webhook```
- ```pip install validators```
- ```pip install pyinstaller (only for compilation)```

## Compiling into binaries

- Run ```pyinstaller --onefile discord.py``` in the folder directory
- Copy dist/discord (dist\discord.exe in Windows) into a folder which is in your $PATH (```/usr/local/bin```)
- Restart the terminal
- Run setup if you needed

## Things to do

1. Integrate with Vim to write messages instead of one liners
