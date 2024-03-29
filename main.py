from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os.path
import threading
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly",
          "https://www.googleapis.com/auth/directory.readonly"]

data_list = []


def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
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

    try:
        service = build("people", "v1", credentials=creds)
        fetch_contacts(service)

    except HttpError as err:
        print(err)


def fetch_contacts(service):

    finished = False
    next_page_token = None
    data = set()
    count = 0

    while not finished:

        results = service.people().listDirectoryPeople(
            readMask='names,emailAddresses',
            pageSize=1000,
            sources="DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE",
            pageToken=next_page_token,
        ).execute()

        result = results.get('people', [])

        count += len(result)
        print(f"Fetching Contacts {count}...", end='\r')

        if not result:
            finished = True

        for person in result:
            emailAddresses = person.get("emailAddresses", [])

            if emailAddresses:
                for email in emailAddresses:
                    data.add(email['value'].strip())

        next_page_token = results.get('nextPageToken')

        finished = (next_page_token is None)

    write_to_file(data)


def perform_write(list, filename):
    with open(filename, "w") as file:
        for i, data in enumerate(list):
            print(f"Progress (Writing to File): {i}/{len(list)}", end='\r')
            file.write(data + "\n")


def write_to_file(data_set):

    data_list = sorted(data_set)
    data_list_sorted_domain = sorted(data_set, key=sort_by_domain)

    thread1 = threading.Thread(target=perform_write, args=(
        data_list, "emails_alphabetic.txt"))

    thread2 = threading.Thread(target=perform_write, args=(
        data_list_sorted_domain, "emails_domain.txt"))

    thread1.start()
    thread2.start()


def sort_by_domain(email):
    _, domain = email.split('@')
    return domain


if __name__ == "__main__":
    main()
