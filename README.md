> ### **If you find this Repository helpful or interesting, please consider giving it a star! ⭐️**
<br/>

# Google Contacts Email Scraper

- Use the Google People's (Contacts) API to fetch email addresses from a large contacts directory and from personal contacts & write them to txt files.
- Use case: Scrape all emails from a University Contacts directory and export them to a txt file.
- Google Contacts does not have a native Bulk Contact Export feature that exports all contacts at once. This provides a way to do so.
- You can customise this script to store names, phone numbers and more. [Read more.](https://developers.google.com/people/api)

## Screenshots

![2024-03-30_22-39](https://github.com/aryanranderiya/GoogleContactsEmailScraper/assets/64796509/47620478-0ecf-46d8-840b-9a196086458b)
![2024-03-30_22-41](https://github.com/aryanranderiya/GoogleContactsEmailScraper/assets/64796509/521b1fff-fdf7-491b-859e-2a2f598d2cb6)


## Installation

1. Clone the Repository

   ```
   git clone https://github.com/aryanranderiya/GoogleContactsEmailScraper.git
   ```

2. Navigate to the project directory:

   ```
   cd GoogleContactsEmailScraper
   ```

3. Install Dependencies

   ```
   pip install -r requirements.txt
   ```

4. Run the Script

   ```
   python app.py
   ```

## Usage

> Make sure to setup a Project using Google Cloud Console. <br>
> More Information Here: https://developers.google.com/people/v1/getting-started

- The Script should work fine out of the box if a project is setup correctly using OAuth 2.0 with the following scopes: `contacts.readonly` & `directory.readonly` in [Google Cloud Console](https://console.cloud.google.com/)

- After running the script using `python app.py` it will redirect to complete the authentication procses, after which a `token.json` file be created in the same directory.

- After scraping all the emails, the txt files containing the emails will be stored in the same directory in `contacts_emails.txt` and `directory_emails_alphabetic.txt` `directory_emails_domain.txt` if your account is under an organization (such as a University domain: studentusername@university.edu.in)

### Happy Coding!

Thank you for viewing this Repo! A 🌟 would be appreciated if this project was helpful!

[**Get in touch**](https://aryanranderiya.com/contact)
