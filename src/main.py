from PasswordManager import PasswordManager

menu = """
Select an option.
1. Load a password file
2. Create a password file
3. Add a password
4. Delete a password
5. Get a password
6. Clear password manager
7. Create an encryption key
8. Load an encryption key
9. Exit
"""

if __name__ == "__main__":
    pm = PasswordManager()

    while True:
        print(menu)
        user_choice = input("Option: ")

        try:
            user_choice = int(user_choice)
        except Exception:
            print("Invalid choice specified, try again\n")
            continue

        match user_choice:
            case 1:
                file_name = input("Specify the name of the password file to load: ")
                success = pm.load_password_file(file_name=file_name)
                if success:
                    print("Password file loaded successfully.")
                else:
                    print("Unable to load password file")
                continue
            case 2:
                print(
                    "Creating a password file will use the current passwords within the manager."
                )
                file_name = input("Specify the name of this password list: ")
                success = pm.create_password_file(
                    file_name=file_name, password_dict=pm.password_dict
                )
                if success:
                    print("Password file created successfully.")
                else:
                    print("Unable to create password file.")
                continue
            case 3:
                account_name = input("Specify a name for the password: ")
                password = input("Input the password: ")
                success = pm.add_password(account_name=account_name, password=password)
                if success:
                    print("Password was added to manager successfully.")
                else:
                    print(
                        "Password could not be added to manager.\n"
                        "Password under that name already exists.\n"
                        "To override, delete the old password first."
                    )
                    continue
            case 4:
                account_name = input("Specify the name the password is under: ")
                success = pm.delete_password(account_name=account_name)
                if success:
                    print("Password was deleted from manager successfully.")
                else:
                    print(
                        "Password could not be deleted.\n"
                        "Password did not exist in the manager."
                    )
                    continue
            case 5:
                account_name = input("Specify a name the password is under: ")
                password = pm.get_password(account_name=account_name)
                if isinstance(password, bool):
                    print("Could not get password.")
                else:
                    print(f"Password for {account_name}: {password}")
                continue
            case 6:
                pm.clear_manager()
                print("Password manager has been cleared.")
                continue
            case 7:
                file_name = input("Specify a name for this key: ")
                success = pm.create_key(file_name=file_name)
                if success:
                    print("Key was created successfully.")
                else:
                    print(
                        "Key is already loaded into the manager.\n"
                        "Clear or exit manager to create new key."
                    )
                continue
            case 8:
                file_name = input("Specify a name for this key: ")
                success = pm.load_key(file_name=file_name)
                if success:
                    print("Key was loaded successfully.")
                else:
                    print("Key Could not be loaded.")
                continue
            case 9:
                print("Exiting the password manager command line interface.")
                exit()
            case _:
                print(f"Choice {user_choice} is not an option, try again")
                continue
