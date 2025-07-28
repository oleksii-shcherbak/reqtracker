"""Simple test application."""

from datetime import datetime

import requests


def fetch_data(url):
    """Fetch data from URL."""
    response = requests.get(url)
    return response.json()


def main():
    """Main function."""
    data = fetch_data("https://api.example.com/data")
    print(f"Fetched {len(data)} items at {datetime.now()}")


if __name__ == "__main__":
    main()
