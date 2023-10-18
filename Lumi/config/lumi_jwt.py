import requests

def get_valid_jwt(email: str, password: str):
    """To generate valid JWT to access API endpoints

    Args:
        email (str): valid lumi dashboard email
        password (str): password
    """
    url = f"https://prod-gateway.lumi.systems/account/user/login"

    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(url = url, json= payload)

    if response.status_code == 200:
        jwt_token = response.json().get("authToken")
        print(jwt_token)
    else:
        print("Error:", response.text)
