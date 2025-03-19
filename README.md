# Xero API Integration for Account Chart in Django

This document explains the steps involved in integrating the Xero API to fetch and display account chart data in a Django application. It covers the setup process, the flow of data, and the interaction between the Django backend and Xero API.


## Table of Contents

- [Overview](#overview)
- [Setup and Installation](#setup-and-installation)
- [Code Flow](#code-flow)
  - [Fetching Data from Xero API](#fetching-data-from-xero-api)
  - [Processing the Data](#processing-the-data)
  - [Rendering the Data in the Template](#rendering-the-data-in-the-template)
- [Instructions](#instructions)
- [Troubleshooting](#troubleshooting)

---

## Overview

This project demonstrates how to integrate the Xero API into a Django application and display account charts. The Xero API provides access to accounting data, and we fetch account data from the API, process it, and render it on a webpage. This guide outlines how the data flows in the application.

---

## Setup and Installation

### Prerequisites

- Python 3.8+
- Django 5.x or higher
- A valid [Xero Developer Account](https://developer.xero.com/) with API access
- Xero OAuth credentials (client ID, client secret, and API scopes)

### Install Dependencies

Ensure all the necessary dependencies are installed by running the command to install requirements from the `requirements.txt` file.

### Configure Xero Credentials

Add your Xero credentials (client ID, client secret, and other necessary configurations) in the `settings.py` file. These credentials are used to authenticate requests to the Xero API.

---

## Code Flow

### Fetching Data from Xero API

1. **OAuth Token Validation:**
   - The application checks if a valid OAuth token exists in the database. If the token is expired, it refreshes the token using the stored refresh token.
   - A helper function verifies the token's expiration and handles the token refresh process by making a request to the Xero OAuth token endpoint.

2. **Making the Request:**
   - With a valid OAuth token, the application makes a GET request to the Xero API endpoint for accounts.
   - The request includes the access token in the `Authorization` header to ensure the request is authenticated.

### Processing the Data

1. **Parsing the Response:**
   - The response from Xero is a JSON object containing an array of accounts under the `"Accounts"` key. Each account includes fields like `AccountID`, `Code`, `Name`, and `Type`.
   - The relevant data is extracted and formatted into a list of dictionaries for easier handling.

2. **Handling Missing or Empty Accounts:**
   - If the `"Accounts"` field is empty or missing, the application gracefully handles this by passing an empty list or a relevant message to the template.

### Rendering the Data in the Template

- The processed account data is passed to the `account_chart.html` template for rendering.
- The template displays the account data in a table format, with each row showing the account code, name, and type.
- If no accounts are available, a message is displayed indicating that no data was found.

---

## Instructions

1. **Clone the Repository**
   - Clone the repository from GitHub by running the following command:
     ```
     git clone https://github.com/anjeelupreti/xero_oauth_integration.git
     cd xero_oauth_integration
     ```

2. **Set Up a Virtual Environment**
   - It is recommended to use a virtual environment to manage your dependencies. To set it up, run:
     - On macOS/Linux:
       ```
       python -m venv venv
       source venv/bin/activate
       ```
     - On Windows:
       ```
       python -m venv venv
       venv\Scripts\activate
       ```

3. **Install Required Dependencies**
   - Install the necessary dependencies by running:
     ```
     pip install -r requirements.txt
     ```

4. **Configure Xero API Credentials**
   - Create an account on the [Xero Developer Portal](https://developer.xero.com/) and create a new OAuth application.
   - Obtain the **client ID**, **client secret**, and **redirect URI**.
   - In the `settings.py` file of your Django project, add your Xero credentials.

5. **Set Up the Database**
   - Run the following command to set up your database and apply migrations:
     ```
     python manage.py migrate
     ```

6. **Run the Development Server**
   - Start the development server by running:
     ```
     python manage.py runserver
     ```
   - The server will run at `http://127.0.0.1:8000/`.

7. **Authenticate with Xero**
   - Navigate to `http://127.0.0.1:8000/login/` in your browser.
   - Log in and authenticate with Xero by granting permissions for your application.
   - After successful authentication, you will be redirected back to the application.

8. **Fetch Account Information**
   - Once authenticated, you will be redirected to a page where you can fetch account details from Xero.
   - Click the **Fetch Accounts** link or visit `http://127.0.0.1:8000/xero/fetch_accounts/` to make the API request to Xero and retrieve account data.

9. **View Account Data**
   - After fetching the data, visit `http://127.0.0.1:8000/xero/accounts/` to view the list of Xero accounts.
   - The page will display the accounts in a table format. If no accounts are available, a message will be shown indicating "No accounts available."

10. **Troubleshooting**
    - If you encounter any issues, check the server logs for error messages.
    - Ensure your Xero credentials and redirect URI are correctly configured in `settings.py`.
    - If the access token is expired, the application should automatically refresh it. If needed, manually refresh the token in the Xero Developer Portal.




## Troubleshooting

1. **Invalid or Expired Token:**
   - Ensure that the OAuth token is correctly refreshed when expired. Verify the token's validity in the database.

2. **API Request Issues:**
   - If the API request fails, check the response status code and error message for details.
   - Ensure that your Xero credentials are correct and that you have the necessary permissions/scopes for the requested data.

3. **No Data:**
   - If no accounts are returned, verify that the API response contains valid account data under the `"Accounts"` key.