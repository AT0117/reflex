import requests
EXTERNAL_API_URL = 'http://127.0.0.1:8001/v1/get-user'


def fetch_user_data(user_id):
    """Fetches user data from the external API."""
    payload = {'account_id': user_id}
    response = requests.post(EXTERNAL_API_URL, json=payload, timeout=5)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'API Error: {response.status_code} - {response.text}')
