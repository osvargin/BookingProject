import allure
import pytest
import requests


@allure.feature('Test Ping')
@allure.story('Test connection')
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Expexted status 201 but get {status_code}"


@allure.feature('Test Ping')
@allure.story('Test server unavailability')
def test_ping_server_unavailability(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=Exception('Server unavailable'))
    with pytest.raises(Exception, match='Server unavailable'):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test server HTTP method')
def ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 201 but got 405'):
        api_client.ping()


@allure.feature('Test ping')
@allure.story('Test server error')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 201 but got 500'):
        api_client.ping()


@allure.feature('Test ping')
@allure.story('Test wrong url')
def test_ping_wrong_url(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 201 but got 404'):
        api_client.ping()


@allure.feature('Test ping')
@allure.story('Test connection with different success code')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, 'get', return_value=mock_response)
    with pytest.raises(AssertionError, match='Expected status 201 but got 200'):
        api_client.ping()


@allure.feature('Test ping')
@allure.story('Test timeout')
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.ping()

@allure.feature('Test create booking')
@allure.story('Test successful create booking')
def test_create_booking(api_client, generate_random_booking_dates):
    with allure.step('Test create booking'):
        response = api_client.create_booking(generate_random_booking_dates)
        print(response)
    with allure.step('Checking firstname'):
        assert response['firstname'] == generate_random_booking_dates['firstname']
    with allure.step('Checking lastname'):
        assert response['lastname'] == generate_random_booking_dates['lastname']
