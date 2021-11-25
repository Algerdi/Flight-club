import requests

SHEETY_PRICES_ENDPOINT = 'https://api.sheety.co/bb88d1f903af5db2b8c236edfde94c48/flightDeals/prices'
SHEETY_USERS_ENDPOINT = 'https://api.sheety.co/bb88d1f903af5db2b8c236edfde94c48/flightDeals/users'


class Destination:

    def __init__(self):
        self.destination_data = {}
        self.city_codes = []

    # We determine the list of cities that we would like to visit.

    def get_destination_data(self):
        response = requests.get(url=SHEETY_PRICES_ENDPOINT)
        data = response.json()
        self.destination_data = data['prices']
        print(data)
        return self.destination_data

    # We supplement the list of flights with previously defined codes.

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data
            )
            print(response.text)

    # Collect emails and names of those who want to receive an alert via email.

    def get_customer_emails(self):
        customers_endpoint = SHEETY_USERS_ENDPOINT
        response = requests.get(url=customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
