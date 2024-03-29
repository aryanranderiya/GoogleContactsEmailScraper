import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly"]


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

        # Call the People API
        results = (
            service.people()
            .connections()
            .list(
                resourceName="people/me",
                personFields="names,emailAddresses",
            )
            .execute()
        )

        process_results(results)

        nextPageToken = results.get("nextPageToken", [])

        while (nextPageToken):
            results = (
                service.people()
                .connections()
                .list(
                    resourceName="people/me",
                    personFields="names,emailAddresses",
                    pageToken=nextPageToken,
                )
                .execute()
            )

            nextPageToken = results.get("nextPageToken", [])

            process_results(results)

    except HttpError as err:
        print(err)


def process_results(results):
    connections = results.get("connections", [])

    if not connections:
        print("No Connections")
        return

    for person in connections:
        # print("Person: ", person)
        emailAddresses = person.get("emailAddresses", [])

        if emailAddresses:
            names = person.get("names", [])

            if names:
                displayName = names[0].get("displayName")
                print(displayName, end=": ")

            for email in emailAddresses:
                print(email['value'], end=", ")

            print()

    ...


if __name__ == "__main__":
    main()
