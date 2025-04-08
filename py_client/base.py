import os

import requests
from auth import SECRET_FILE, authenticate

# Check for the existence of the secret file
if os.path.exists(SECRET_FILE):
    with open(SECRET_FILE, "r") as fp:
        token = fp.read().strip()
else:
    # Authenticate and obtain the token
    token = authenticate()

# Prepare the authorization header
header = {"Authorization": f"Bearer {token}"}


def get_todo_lists(
    endpoint: str,
    json_payload: dict = None,
    data: dict = None,
    params: dict = None,
    headers: dict = header,
):
    print("*" * 4, f" {endpoint} ", "*" * 4)
    response = requests.get(endpoint, params=params, data=data, headers=headers)
    try:
        json_response = response.json()
        print(json_response)
        # print(response.content)
    except requests.ConnectionError:
        raise Exception("Connection Error")
    except requests.JSONDecodeError:
        raise Exception("JSON error")
    except requests.RequestException as err:
        raise Exception(f"Request Error Exception: {err}")
    return json_response


def post_todo_task(
    endpoint: str,
    json_payload: dict = None,
    data: dict = None,
    params: dict = None,
    headers: dict = header,
):
    print("*" * 4, f" {endpoint} ", "*" * 4)
    response = requests.post(
        endpoint, json=json_payload, data=data, params=params, headers=headers
    )
    try:
        json_response = response.json()
        print(json_response)
        # print(response.content)
    except requests.ConnectionError:
        raise Exception("Connection Error")
    except requests.JSONDecodeError:
        raise Exception("JSON error")
    except requests.RequestException as err:
        raise Exception(f"Request Error Exception: {err}")
    return json_response


def update_todo_task(
    endpoint: str,
    json_payload: dict = None,
    headers: dict = header,
):
    print("*" * 4, f" {endpoint} ", "*" * 4)
    response = requests.put(endpoint, json=json_payload, headers=headers)
    try:
        if response.status_code == 200:
            json_response = response.json()
            print("Updated data:", json_response)
            return json_response
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.content.decode())
    except requests.ConnectionError:
        raise Exception("Connection Error")
    except requests.JSONDecodeError:
        raise Exception("JSON error")
    except requests.RequestException as err:
        raise Exception(f"Request Error Exception: {err}")


def delete_todo_task(
    endpoint: str,
    headers: dict = header,
):
    print("*" * 4, f" {endpoint} ", "*" * 4)
    response = requests.delete(endpoint, headers=headers)

    try:
        if response.status_code == 204:
            # 204 No Content - successful deletion
            print("Task deleted successfully (No Content)")
            return response
        elif response.status_code == 200:
            json_response = response.json()
            print("Deleted data:", json_response)
            return response
        else:
            print(f"Error: Status code {response.status_code}")
            try:
                print(response.json())
            except requests.JSONDecodeError:
                print(response.content.decode())
            return response
    except requests.ConnectionError:
        raise Exception("Connection Error")
    except requests.RequestException as err:
        raise Exception(f"Request Error Exception: {err}")


if __name__ == "__main__":
    endpoint = "http://localhost:8000/api/todos/"
    get_todo_lists(endpoint=endpoint)
