import requests
from datetime import datetime

class IPInfoClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.requests_made = 0
        self.last_reset = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def get_location(self, ip_address):
        # Check if rate limit is reached for the current month
        if self.requests_made >= 49998:
            print("Rate limit reached for IPinfo API.")
            return None

        # Check if the current month has changed since the last request
        now = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if now > self.last_reset:
            self.requests_made = 0
            self.last_reset = now

        # Construct the API request URL
        api_url = f'https://ipinfo.io/{ip_address}/json?token={self.api_token}'

        # Make a GET request to the IPinfo API
        response = requests.get(api_url)

        # Increment the number of requests made
        self.requests_made += 1

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract geolocation data
            country = data.get('country')
            city = data.get('city')
            region = data.get('region')
            # Other relevant information

            # Return the location data
            return {
                'country': country,
                'city': city,
                'region':region,
                # Other location data fields
            }
        else:
            # Request failed
            print("Failed to retrieve location data from IPinfo API.")
            return None

# Example usage:
# api_token = "your_api_token"
# client = IPInfoClient(api_token)
# location_data = client.get_location("8.8.8.8")
# print(location_data)