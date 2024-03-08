"""This module contains the definition for `password_manager()`."""

from src.create_secret import create_secret
from src.delete_secret import delete_secret
from src.get_secret import get_secret
from src.list_secrets import list_secrets
from src.write_secret import write_secret


def password_manager():
    """
    A function to manage user_names and passwords in AWS Secrets Manager.


    """
    print("\n\nWelome to Password Manager 🕵️")
    print("-----------------------------")

    while True:
        print("\nPlease specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:")

        choice = input("Enter your choice: ")

        if choice == "e":
            try:
                secret_id = input("Enter a Secret Identifier: ")
                user_id = input("Enter a UserID: ")
                password = input("Enter a Password: ")

                response = create_secret(
                    secret_id,
                    user_id,
                    password,
                )
                if response == 200:
                    print("✅ Secret saved.")

            except Exception:
                print("❌ Secret not saved.")

        elif choice == "r":
            try:
                secret_id = input("Specify secret to retrieve: ")
                secret_string = get_secret(secret_id)
                write_secret(secret_id, secret_string)
                print(f"✅ Secret stored in local file {secret_id}.txt")

            except Exception:
                print("❌ Secret not retrieved.")

        elif choice == "d":
            try:
                secret_id = input("Specify secret to delete: ")
                response = delete_secret(secret_id)
                if response == 200:
                    print("✅ Deleted")

            except Exception:
                print("❌ Unable to delete.")

        elif choice == "l":
            secret_list = list_secrets()
            if len(secret_list) > 0:
                print(f"{len(secret_list)} secret(s) available: ")
                for secret in secret_list:
                    print(f"> {secret}")
            else:
                print("0 secrets available.")

        elif choice == "x":
            print("\nThankyou for using Password Manager. Goodbye. 🕵️")
            print("------------------------------------------------")
            break

        else:
            print(
                "❌ Invalid input. Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:"
            )


if __name__ == "__main__":
    password_manager()
