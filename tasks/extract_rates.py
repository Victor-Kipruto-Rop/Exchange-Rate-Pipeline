import requests

def extract_exchange_rates():
    url = "https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "base": data["base_code"],
        "timestamp": data["time_last_update_utc"],
        "rates": data["rates"],
    }

if __name__ == "__main__":
    print(extract_exchange_rates())
