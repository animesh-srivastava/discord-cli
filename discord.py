from discord_cli import DiscordCLI, reconfigure, delete_configuration, setup, uninstall
from discord_cli.database import list_all, fetch_url, fetch_name
from argparse import ArgumentParser
from validators import url as url_validator
from sys import exit

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument("-m", "--message", help="Add a message to send")
    parser.add_argument("-f", "--file", help="File to attach to the webhook")
    parser.add_argument("-n", "--name", help="Name of the webhook to whom you want to send")
    parser.add_argument("--fetch-name", help="Fetch name from webhook")
    parser.add_argument("--fetch-url", help="Fetch webhook from name")
    parser.add_argument("--add", help="Add a new webhook", nargs=2)
    parser.add_argument("--edit", help="Edit the webhook", nargs=2)
    parser.add_argument("--delete", help="Delete a webhook")
    parser.add_argument("--setup", help="Set up the program", action='store_true')
    parser.add_argument("--reconfigure", help="Reconfigure the main webhook", action="store_true")
    parser.add_argument("--list", help="List all named webhooks", action="store_true")
    parser.add_argument("--uninstall", help="Remove all the generated files", action="store_true")

    args = parser.parse_args()

    cli = DiscordCLI()

    # Reconfiguring 
    if args.reconfigure:
        print("This will reset the configuration file.")
        res = input("Continue? (Y/N) [Default N] ")
        if res.lower() == "y":
            delete_configuration()
            reconfigure()
        elif res.lower() == "n" or res.lower() == "":
            exit()
        else:
            print("Could not read input. Exiting")
            exit()
        


    # Setting up for the first time
    elif args.setup:
        print("Attempting to setup will delete everything and start fresh.")
        res = input("Continue? (Y/N) [Default N] ")
        if res.lower() == "y":
            delete_configuration()
            setup()
        elif res.lower() == "n" or res.lower() == "":
            print("Exiting")
            exit()
        else:
            print("Could not read input. Exiting")
            exit()
        

    # Editing / Changing a Webhook
    elif args.edit:
        if url_validator(args.edit[1]):
            if list_all() is None or args.edit[0] in list_all():
                cli.change_url(args.edit[0], args.edit[1])
            else:
                print("Did not find \"{}\" in database, would you like to enter it?".format(args.edit[0]))
                res = input("Enter? (Y/N) [Default N] ")
                if res.lower() == "y" or res.lower() == "":
                    cli.add_names(args.edit[0], args.edit[1])
                else:
                    print("Exiting")
                    exit()
        else:
            print("Invalid webhook URL")
    # Adding a Webhook
    elif args.add:
        if url_validator(args.add[1]):
            if list_all() is not None:
                if args.add[0] not in list_all():
                    cli.add_names(args.add[0], args.add[1])
                else:
                    print("Entry \"{}\" already exists. Would you like to modify it?".format(args.add[0]))
                    res = input("Modify? (Y/N) [Default N] ")
                    if res.lower() == "n" or res.lower() == "":
                        exit()
                    elif res.lower() == "y":
                        cli.change_url(args.add[0], args.add[1])
            else:
                cli.add_names(args.add[0], args.add[1])
        else:
            print("Invalid webhook URL")

    # Deleting webhook
    elif args.delete:
        if list_all() is not None:
            if args.delete in list_all():
                cli.delete_url(args.delete)
            else:
                print("Did not find \"{}\" in database.".format(args.delete))
        else:
            print("Did not find \"{}\" in database.".format(args.delete))


    # Finding webhook name
    elif args.fetch_name:
        res = fetch_name(args.fetch_name)
        if res is not None:
            print(res)
        else:
            print("Did not find any entry for your input.")

    # Finding webhook url
    elif args.fetch_url:
        res = fetch_url(args.fetch_url)
        if res is not None and res != []:
            print(res)
        else:
            print("Did not find any entry")

    # Listing all urls
    elif args.list:
        from pprint import pprint
        pprint(list_all())

    elif args.uninstall:
        print("Attempting to setup will remove all the files.")
        res = input("Continue? (Y/N) [Default N] ")
        if res.lower() == "y":
            uninstall()
        elif res.lower() == "n" or res.lower() == "":
            print("Exiting")
            exit()
        else:
            print("Could not read input. Exiting")
            exit()
        

    # Sending messages
    elif args.message:
        if args.file:
            if args.name:
                cli.send_file_to_name(args.name, args.file, content=args.message)
            else:
                cli.send_file(args.file, content=args.message)
        else:
            if args.name:
                cli.send_message_to_name(args.name, args.message)
            else:
                cli.send_message(args.message)
    else:
        if args.file:
            if args.name:
                cli.send_file_to_name(args.name, args.file)
            else:
                cli.send_file(args.file)
        else:
            print("Need at least a file or some message")
