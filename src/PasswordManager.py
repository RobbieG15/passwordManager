from pathlib import Path

from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self) -> None:
        self.key = None
        """ The key to encrypt and decrypt with. """

        self.password_dict: dict[str, str] = None
        """ The decrypted password dictionary. """

    def add_password(self, account_name: str, password: str) -> bool:
        if self.password_dict is None:
            self.password_dict = {}
        if account_name in self.password_dict:
            return False
        self.password_dict[account_name] = password
        return True

    def delete_password(self, account_name: str) -> bool:
        if self.password_dict is None or account_name not in self.password_dict:
            return False
        del self.password_dict[account_name]
        return True

    def get_password(self, account_name: str) -> bool | str:
        if self.password_dict is None or account_name not in self.password_dict:
            return False
        return self.password_dict[account_name]

    def create_key(self, file_name: str) -> bool:
        if self.key is not None:
            return False
        self.key = Fernet.generate_key()
        path = Path().joinpath(".keys", f"{file_name}.key").as_posix()
        with open(path, "w") as f:
            f.write(self.key.decode())
        return True

    def load_key(self, file_name: str) -> bool:
        if self.key is not None:
            return False
        try:
            path = Path().joinpath(".keys", f"{file_name}.key")
            with open(path, "r") as f:
                file_content = f.read()
            if not file_content:
                print("File is empty.")
            self.key = file_content
            return True
        except IOError:
            print(f"File {path} was unable to be read from.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return False

    def load_password_file(self, file_name: str) -> bool:
        if self.key is None or self.password_dict is not None:
            return False
        self.password_dict = {}
        try:
            path = Path().joinpath(".passwords", f"{file_name}.txt").as_posix()
            with open(path, "r") as f:
                f.readline()
                for line in f:
                    account_name, encrypted = line.split(":")
                    self.password_dict[account_name] = (
                        Fernet(self.key).decrypt(encrypted.encode()).decode()
                    )
            return True
        except IOError:
            print(f"File {path} was unable to be read from.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return False

    def create_password_file(
        self, file_name: str, password_dict: dict[str, str] = None
    ) -> bool:
        if self.key is None:
            return False
        try:
            path = Path().joinpath(".passwords", f"{file_name}.txt").as_posix()
            with open(path, "w") as f:
                f.write("Password File created by Robert Greenslade\n")
                if password_dict is not None:
                    for key, value in password_dict.items():
                        f.write(
                            f"{key}:{Fernet(self.key).encrypt(value.encode()).decode()}\n"
                        )
            return True
        except IOError:
            print(f"File {path} was unable to be read from.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return False

    def clear_manager(self) -> None:
        self.key = None
        self.password_dict = None
