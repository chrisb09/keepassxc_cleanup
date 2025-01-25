import argparse
from pykeepass import PyKeePass
from getpass import getpass

def find_duplicates(kp):
    """Find duplicates based on URL/app ID, username, and password."""
    entries = kp.entries
    duplicates = {}
    
    for entry in entries:
        # Construct the key from URL/app ID, username, and password

        urlAppIds = []
        if entry.url:
            urlAppIds.append(entry.url)
        for key in entry.custom_properties.keys():
            if 'app' in key.lower() or 'ssid' in key.lower():
                urlAppIds.append(entry.custom_properties[key])

        urlAppId = filter(lambda x: x is not None, urlAppIds)

        for urlAppId in urlAppIds:
            key = (urlAppId, entry.username, entry.password)
            
            if key not in duplicates:
                duplicates[key] = []
            duplicates[key].append(entry)
    
    return duplicates

def print_duplicates(duplicates):
    """Print out duplicates in the specified format."""
    duplicate_count = 0
    dupliocate_entries_count = 0
    for key, entries in duplicates.items():
        if len(entries) > 1:
            duplicate_count += 1
            dupliocate_entries_count += len(entries)
            print(f"Duplicate #{duplicate_count} found with URL/AppID: {key[0]}, Username: {key[1]}, Password: {(key[2][0]+'*'*(len(key[2])-2)+key[2][-1]) if key[1] is not None else 'None'}")
            print("Entries:")
            for i, entry in enumerate(entries, start=1):
                print(f"  {i}. Name: {entry.title}, URL/AppID: {entry.url or entry.custom_properties.get('app_id')}, Username: {entry.username}")
                print(f"     Internal path: {entry.path}")
            print("\n---\n")
    
    print()
    print(f"Found {duplicate_count} duplicates in total with {dupliocate_entries_count} entries.")

def deduplicate(kp, duplicates):
    """Ask the user which entry to keep for each set of duplicates."""
    for key, entries in duplicates.items():
        if len(entries) > 1:
            print(f"Duplicates for URL/AppID: {key[0]}, Username: {key[1]}")
            for i, entry in enumerate(entries, start=1):
                print(f"  {i}. Name: {entry.title}, URL/AppID: {entry.url or entry.custom_properties.get('app_id')}, Username: {entry.username}")
                print(f"     Internal path: {entry.path}")
            
            # Ask the user which entry to keep
            while True:
                try:
                    choice = int(input(f"Choose which entry to keep (1-{len(entries)}) (0 for keep all): "))
                    if 0 <= choice <= len(entries):
                        break
                    else:
                        print(f"Please choose a valid number between 1 and {len(entries)}, or 0.")
                except ValueError:
                    print("Please enter a valid number.")
            
            if choice != 0:
                # Get the selected entry
                selected_entry = entries[choice - 1]
                print(f"Keeping: {selected_entry.title}")
                
                # Remove the unselected entries
                for entry in entries:
                    if entry != selected_entry:
                        print(f"Removing: {entry.title}")
                        kp.entries.remove(entry)
            else:
                print("Keeping all entries.")
    
    # Save the database after modifications
    try:
        kp.save()
        print("Database saved successfully.")
    except Exception as e:
        print(f"Error saving database: {e}")

def print_custom_properties(kp):
    """Print out custom properties that exist."""
    custom_properties = {}
    for entry in kp.entries:
        for key in entry.custom_properties.keys():
            if key not in custom_properties:
                custom_properties[key] = 0
            custom_properties[key] += 1
    
    print("Custom properties found:")
    for key in sorted(custom_properties.keys(), key=lambda x: custom_properties[x]):
        print(f"  {key}: {custom_properties[key]} entries")

def main():
    parser = argparse.ArgumentParser(description="KeePassXC Database Deduplication Script")
    parser.add_argument('db', help="Path to the KeePassXC database file")
    
    # Create subparsers for subcommands
    subparsers = parser.add_subparsers(dest="command", required=True)  # Make 'command' required

    # Subcommand for listing duplicates
    subparsers.add_parser('list_duplicates', help="Find duplicate entries")

    # Subcommand for deduplication
    subparsers.add_parser('dedup', help="Remove duplicate entries after user selection")

    # Subcommand for listing custom properties
    subparsers.add_parser('list_custom_properties', help="List custom properties of all entries")

    # Parse arguments
    args = parser.parse_args()

    # Prompt for the master password
    password = getpass(f"Master Password for KeePassXC Database located at {args.db}: ")

    # Load the KeePass database
    try:
        kp = PyKeePass(args.db, password=password)
    except Exception as e:
        print(f"Error opening database: {e}")
        return
    
    # Execute the corresponding subcommand
    if args.command == 'list_duplicates':
        # Find duplicates and print them
        duplicates = find_duplicates(kp)
        print_duplicates(duplicates)
    
    if args.command == 'dedup':
        # Find duplicates and let user deduplicate
        duplicates = find_duplicates(kp)
        deduplicate(kp, duplicates)

    if args.command == 'list_custom_properties':
        # List custom properties of all entries
        print_custom_properties(kp)

if __name__ == "__main__":
    main()
