import json
import requests


def send_request(line):
    """Sends a request to the URL with the given line."""
    url = "http://127.0.0.1:8000/predict"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = json.dumps(line)
    response = requests.post(url, headers=headers, data=data)
    return response


if __name__ == "__main__":
    with open("data/requests.json") as f:
        for line in f:
            response = send_request(line)
            print(response)