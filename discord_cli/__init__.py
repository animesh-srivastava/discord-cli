from discord_webhook import DiscordWebhook, DiscordEmbed
from os.path import expanduser
from os.path import isdir, join, isfile, isabs, abspath
from os import remove, mkdir, rmdir
from validators import url as url_validator
from .misc import message

home = expanduser("~")

foldername = ".discordcli" # Configure the name of the folder here
folderpath = join(home, foldername) # Default path for folder

filename = "config.ini" # Configure the name of the config file here
filepath = join(folderpath, filename) # Configure the path for the config file here

dbname = "hooks.db" # Configure the name of the database here
dbpath = join(folderpath, dbname) # Configure the path of the database here

from .database import create_database, checking_if_table_exists
from .database import add_url, delete_url, change_url, fetch_url, fetch_name, list_all

# Setup

def reconfigure():
    """
    This function will restart the configuration
    """
    with open(filepath, "w+") as f:
        f.write("[CONFIGURATION]\n")
        while True:
            webhook = input("Enter the webhook: ")
            if url_validator(webhook):
                f.write("webhook = {}\n".format(webhook))
                break
            else:
                print("Invalid URL")


def setup():
    """
    This function will set up the configuration.
    """

    # Checking if folderpath exists
    if not isdir(folderpath):
        mkdir(folderpath)

    # Checking if config path exists
    if not isfile(filepath):
        print(message)
        reconfigure()

    # Checking if database exists
    if not isfile(dbpath):
        create_database()
    
    # If it exists and doesn't have that table
    elif not checking_if_table_exists():
        create_database()

# setup()


def delete_configuration():
    """
    This function will delete the configuration
    """
    if isfile(filepath):
        print("Removing {}".format(filepath))
        remove(filepath)


def uninstall():
    """
    This will remove all the created files
    """
    print("Uninstalling...")
    if isfile(filepath):
        print("Removing config files")
        remove(filepath)
    if isfile(dbpath):
        print("Removing database")
        remove(dbpath)
    if isdir(folderpath):
        print("Removing other files")
        rmdir(folderpath)


from configparser import ConfigParser

config = ConfigParser()

config.read(filepath)

try:
    main_webhook = config["CONFIGURATION"]["webhook"]
except KeyError:
    main_webhook = None



class DiscordCLI(object):
    def __init__(self):
        """
        Instantiating the CLI
        """
        self.main_webhook = main_webhook

    def send_message_to_url(self, url, message):
        """
        Sending provided message to a provided URL
        """
        hook = DiscordWebhook(url, content=message)
        resp = hook.execute()
        if resp[0].status_code == 200:
            print("Successfully sent!")
        return resp[0]
    
    def send_file_to_url(self, url, file_to_be_sent, file_name = None, content = None):
        """
        Sending provided file to a provided URL, with optional file_name and content
        """
        if content is not None and isinstance(content, str):
            hook = DiscordWebhook(url, content=content)
        else:
            hook = DiscordWebhook(url)
        if file_name is None:
            if isabs(file_to_be_sent):
                # For windows machines
                if '\\' in file_to_be_sent:
                    file_name = file_to_be_sent.split("\\")[-1]
                elif "/" in file_to_be_sent:
                    file_name = file_to_be_sent.split("/")[-1]
            else:
                file_name = file_to_be_sent
        if isfile(file_to_be_sent):
            with open(file_to_be_sent, "rb") as f:
                hook.add_file(file=f.read(), filename=file_name)
        else:
            print("Invalid filepath")
        resp = hook.execute()
        if resp[0].status_code == 200:
            print("Successfully sent!")
            return resp[0]

    def send_message_to_name(self, name, message):
        """
        Sending provided message to a provided name in contacts
        """
        if name in list_all():
            url = fetch_url(name)
            if url is not None:
                return self.send_message_to_url(url, message)
        else:
            print("Did not find \"{}\" in webhooks".format(name))

    def send_file_to_name(self, name, file_to_be_sent, file_name = None, content = None):
        """
        Sending provided file to a provided name in contacts, with optional file_name and content
        """
        url = fetch_url(name)
        if url is not None:
            return self.send_file_to_url(url, file_to_be_sent, file_name, content)

    def send_message(self, message):
        """
        Sending provided message to primary URL
        """
        if self.main_webhook is not None:
            return self.send_message_to_url(self.main_webhook, message)
        else:
            print("Setup is incomplete. Please run the setup first.")

    def send_file(self, file_to_be_sent, file_name = None, content = None):
        """
        Sending provided file to primary URL with optional filename and content
        """
        if self.main_webhook is not None:
            return self.send_file_to_url(self.main_webhook, file_to_be_sent, file_name, content)
        else:
            print("Setup is incomplete. Please run the setup first.")

    def list_names(self):
        """
        Listing all the available names in contacts
        """
        print(list_all())

    def add_names(self, name, url):
        """
        Adding provided name and provided URL in contacts
        """
        add_url(name, url)

    def delete_url(self, name):
        """
        Deleting provided name from contacts
        """
        delete_url(name)

    def change_url(self, name, url):
        """
        Changing URL to the given URL for a given name
        """
        change_url(name, url)
