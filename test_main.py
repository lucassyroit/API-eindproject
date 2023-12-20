import requests
import json

BASE_URL = "http://127.0.0.1:8000"


# test POST endpoints
# Test to create user
def test_create_user():
    data = {"email": "test@test.be", "password": "test"}
    response = requests.post(f"{BASE_URL}/users/", json=data)
    assert response.status_code == 200


# Helper function to get a valid access token
def get_access_token():
    data = {
        "client_id": "",
        "client_secret": "",
        "scope": "",
        "grant_type": "",
        "refresh_token": "",
        "username": "test@test.be",
        "password": "test"
    }
    response = requests.post(f"{BASE_URL}/token", json=data)
    access_token = response.json().get("access_token")
    headers_with_token = {
        "accept": "application/json",
        "Authorization": f'Bearer {access_token}'
    }
    return headers_with_token


# test to create team
def test_create_team():
    headers_with_token = get_access_token()
    data = {
        "name": "Liverpool FC",
        "city": "Liverpool",
        "stadium": "Anfield",
        "founded_year": 1892
    }
    response = requests.post(f"{BASE_URL}/teams/", json=data, headers=headers_with_token)
    assert response.status_code == 200


# test to create player
def test_create_player():
    headers_with_token = get_access_token()
    data = {
        "first_name": "Mohamed",
        "last_name": "Salah",
        "position": "RW",
        "nationality": "Egypt",
        "number": 11,
        "birthdate": "15-06-1992",
    }
    response = requests.post(f"{BASE_URL}/players/1", json=data, headers=headers_with_token)
    assert response.status_code == 200


# test to create coach
def test_create_coach():
    headers_with_token = get_access_token()
    data = {
        "first_name": "Jurgen",
        "last_name": "Klopp",
        "role": "Head Coach"
    }
    response = requests.post(f"{BASE_URL}/coaches/1", json=data, headers=headers_with_token)
    assert response.status_code == 200


# test to get teams
def test_get_all_teams():
    headers_with_token = get_access_token()
    response = requests.get(f"{BASE_URL}/teams/", headers=headers_with_token)
    assert response.status_code == 200


# test to get specific team
def test_get_specific_team():
    headers_with_token = get_access_token()
    response = requests.get(f"{BASE_URL}/teams/1", headers=headers_with_token)
    assert response.status_code == 200

# test GET endpoints
# test to get players
def test_get_all_players():
    headers_with_token = get_access_token()
    response = requests.get(f"{BASE_URL}/players", headers=headers_with_token)
    assert response.status_code == 200


# test to get specific player
def test_get_specific_player():
    headers_with_token = get_access_token()
    response = requests.get(f"{BASE_URL}/players/1", headers=headers_with_token)
    assert response.status_code == 200


# test to get coaches
def test_get_all_coaches():
    headers_with_token = get_access_token()
    response = requests.get(f"{BASE_URL}/coaches", headers=headers_with_token)
    assert response.status_code == 200


# test to get specific coach
def test_get_specific_coaches():
    headers_with_token = get_access_token()
    response = requests.get(f"{BASE_URL}/coaches/1", headers=headers_with_token)
    assert response.status_code == 200



# test PUT endpoint
def test_put_number_player():
    headers_with_token = get_access_token()
    response = requests.put(f"{BASE_URL}/players/1/12", headers=headers_with_token)
    assert response.status_code == 200

# test DELETE endpoints
# test to delete coach
def test_delete_coach():
    headers_with_token = get_access_token()
    response = requests.delete(f"{BASE_URL}/coaches/1", headers=headers_with_token)
    assert response.status_code == 200


# test to delete player
def test_delete_player():
    headers_with_token = get_access_token()
    response = requests.delete(f"{BASE_URL}/players/1", headers=headers_with_token)
    assert response.status_code == 200


# test to delete team
def test_delete_team():
    headers_with_token = get_access_token()
    response = requests.delete(f"{BASE_URL}/teams/1", headers=headers_with_token)
    assert response.status_code == 200
