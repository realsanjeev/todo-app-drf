from getpass import getpass

import requests

SECRET_FILE = "SECRET"
AUTH_ENDPOINT = "http://localhost:8000/api/todos/auth/"


def authenticate(endpoint=AUTH_ENDPOINT, save=True):
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    try:
        get_auth_response = requests.post(
            url=endpoint, data={"username": username, "password": password}
        )
        token = get_auth_response.json()["token"]
        print(f"Auth response: {token}")
        if save:
            with open(SECRET_FILE, "w") as fp:
                fp.write(token)
        return token
    except requests.JSONDecodeError:
        raise Exception("JSON response invalid")
    # print(get_auth_response.json())


if __name__ == "__main__":
    token = authenticate()
    headers = {"Authorization": f"Bearer {token}"}
    sample_endpoint = "http://127.0.0.1:8000/api/todos"
    try:
        request = requests.get(sample_endpoint, headers=headers)
        print(request.json())
    except requests.RequestException as err:
        print(f"Some problem occured: {err}")
        exit()
