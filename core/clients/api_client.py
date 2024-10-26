import os

import allure
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
from core.settings.environments import Environments

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environments[environment_str]
        except KeyError:
            raise ValueError(f'Unsupported environment value: {environment_str}')

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {'Content-Type': 'application/json'}

    def get_base_url(self, environment: Environments) -> str:
        if environment == Environments.test:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environments.prod:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f'Unsupported environment value: {environment}')

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step('Ping API client'):
            url = f"{self.base_url}{Endpoints.ping_endpoint}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 201, f"Expected status 201 but get {response.status_code}"
        return response.status_code

    def auth(self):
        with allure.step('Getting authentificate'):
            url = f"{self.base_url}{Endpoints.auth_endpoint}"
            payload = {"username": Users.username, "password": Users.password}
            response = self.session.post(url, json=payload, timeout=Timeouts.timeout)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but get {response.status_code}"
        token = response.json()['token']
        with allure.step('Updating header with autorization'):
            self.session.headers.update({'Authorization': f'Bearer {token}'})

    def get_booking_by_id(self, booking_id):
        with allure.step(f'Getting booking by id'):
            url = f"{self.base_url}{Endpoints.booking_endpoint.value}/{booking_id}"
            response = self.session.get(url, timeout=Timeouts.timeout)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected status 200 but get {response.status_code}"
        return response.json()

    def delete_booking(self, booking_id):
        with allure.step('Deleting booking'):
            url = f"{self.base_url}{Endpoints.booking_endpoint}/{booking_id}"
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.username, Users.password),
                                           timeout=Timeouts.timeout)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 201, f"Expexted status 201 but get {response.status_code}"
        return response.status_code

    def create_booking(self, booking_data):
        with allure.step('Creating booking'):
            url = f"{self.base_url}{Endpoints.booking_endpoint}"
            response = self.session.post(url, json=booking_data, timeout=Timeouts.timeout)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expexted status 200 but get {response.status_code}"
        return response.json()

    def get_booking_ids(self, params=None):
        with allure.step('Getting booking ids'):
            url = f"{self.base_url}{Endpoints.booking_endpoint}"
            response = self.session.get(url, params=params, timeout=Timeouts.timeout)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expexted status 200 but get {response.status_code}"
        return response.json()

    def update_booking(self, booking_id, booking_data):
        with allure.step('Updating booking'):
            url = f"{self.base_url}{Endpoints.booking_endpoint}/{booking_id}"
            response = self.session.put(url, json=booking_data, timeout=Timeouts.timeout)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expexted status 200 but get {response.status_code}"
        return response.json()

    def partial_update_booking(self, booking_id, booking_data):
        with allure.step('Partial updating booking'):
            url = f"{self.base_url}{Endpoints.booking_endpoint}/{booking_id}"
            response = self.session.put(url, json=booking_data, timeout=Timeouts.timeout)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expexted status 200 but get {response.status_code}"
        return response.json()
