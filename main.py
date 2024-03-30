from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os.path
import threading

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly",
          "https://www.googleapis.com/auth/directory.readonly"]

data: list = []


def wrap_error(func):
    """
    Used to ensure other function execution doesnt stop due to occurence of an exception
    Thanks a lot: https://stackoverflow.com/a/40102885/21615084
    """
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
    return func_wrapper


def authenticate() -> None:
    """
    Authenticate user using Google OAuth
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print("User not authenticated... Authentication flow Started...")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    if creds.valid:
        print("User authenticated")

    try:
        service = build("people", "v1", credentials=creds)

        fetch_contacts(service)
        fetch_directory_contacts(service)

    except Exception as err:
        print("Error: ", err)


@wrap_error
def fetch_contacts(service):

    finished: bool = False
    next_page_token: str = None
    data: set = set()
    count: int = 0

    print("Fetching Contacts...", end="\r")

    while not finished:

        results = service.people().connections().list(
            resourceName='people/me',
            personFields='names,emailAddresses',
            pageSize=1000,
        ).execute()

        connections = results.get("connections", [])

        count += len(connections)  # Increment the count of records fetched
        print(f"Fetching Contacts {count}...", end='\r')

        for person in connections:
            # Store email addresses (if multiple) in a list after fetching from dict
            emailAddresses: list = person.get("emailAddresses", [])

            # Check if the value exists
            if emailAddresses:
                for email in emailAddresses:  # Iterate over lists
                    data.add(email['value'].strip())

        # Fetch the next page of results (1k)
        next_page_token = results.get('nextPageToken')

        # If no more results then exit the while loop
        finished = not next_page_token

    write_contacts_file(data)


@wrap_error
def fetch_directory_contacts(service) -> None:
    """
    Fetch all the contacts from Directory
    """
    finished: bool = False
    next_page_token: str = None
    data: set = set()
    count: int = 0

    print("Fetching Directory Contacts...", end='\r')

    while not finished:

        # Fetch results of listing directory
        results = service.people().listDirectoryPeople(
            readMask='names,emailAddresses',
            pageSize=1000,
            sources="DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE",
            pageToken=next_page_token,
        ).execute()

        result = results.get('people', [])

        count += len(result)  # Increment the count of records fetched
        print(f"Fetching Directory Contacts {count}...", end='\r')

        for person in result:
            # Store email addresses (if multiple) in a list after fetching from dict
            emailAddresses: list = person.get("emailAddresses", [])

            # Check if the value exists
            if emailAddresses:
                for email in emailAddresses:  # Iterate over lists
                    data.add(email['value'].strip())

        # Fetch the next page of results (1k)
        next_page_token = results.get('nextPageToken')

        # If no more results then exit the while loop
        finished = not next_page_token

    write_directory_file(data)


def perform_write(list: list, filename: str) -> None:
    """
    Write the contents of a list to the specified filename
    """

    if list:
        with open(filename, "w") as file:
            for i, data in enumerate(list):
                print(f"Progress (Writing to File): {i}/{len(list)}", end='\r')
                file.write(data + "\n")

        print(f"{filename} Successfully Written!")

    else:
        print(f"{list} is Empty! No Records found!")


def write_contacts_file(data_set: set) -> None:
    """
    """
    data: list = sorted(data_set)

    threading.Thread(target=perform_write, args=(
        data, "contacts_emails.txt")).start()


def write_directory_file(data_set: set) -> None:
    """
    Create 2 threads to write to 2 files.
    File 1 (directory_emails_alphabetic.txt) contains emails sorted by their name.
    File 2 (directory_emails_domain.txt) contains emails sorted by the domain
    """

    if not data_set:
        print("No Directory Exists!")
        return

    data: list = sorted(data_set)
    data_sortby_domain: list = sorted(data_set, key=domain)

    thread1 = threading.Thread(target=perform_write, args=(
        data, "directory_emails_alphabetic.txt"))

    thread2 = threading.Thread(target=perform_write, args=(
        data_sortby_domain, "directory_emails_domain.txt"))

    thread1.start()
    thread2.start()


def domain(email) -> str:
    """
    Return the domains of the specified email
    """
    _, domain = email.split('@')
    return domain


if __name__ == "__main__":
    authenticate()
