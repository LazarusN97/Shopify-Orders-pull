#Shopify Order Processor

This project automates the process of retrieving Shopify orders, classifying delivery regions, and calculating shipping costs using predefined rates (ACS and Box Now).

## Features

- Connects to Shopify API using access token
- Classifies orders based on ZIP code into:
  - City
  - Out of City
  - Island
  - Faraway
- Calculates shipping price based on:
  - Delivery area
  - Shipping provider (ACS, Box Now)
  - Payment method (Cash on Delivery)
- Outputs a clean Excel report with shipping price included

## Tech Stack

- Python
- Pandas
- Requests
- OpenPyXL
- gspread (for optional Google Sheets updates)
- Shopify API

> ⚠️ Note: This public version has all API credentials removed. Use environment variables for production use.

## How to Run

1. Create a `.env` file with your Shopify API credentials.
2. Install required packages:

```bash
pip install -r requirements.txt

