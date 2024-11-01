import allure
import pytest
import requests
from pydantic import ValidationError

from core.models.booking import BookingResponse


@allure.feature('Test create booking')
@allure.story('POSITIVE: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        'firstname': 'Ivan',
        'lastname': 'Ivanov',
        'totalprice': 150,
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2018-01-01',
            'checkout': '2019-01-01'
        },
        'additionalneeds': 'Dinner'
    }
    response = api_client.create_booking(booking_data)
    with allure.step('Test checking create booking with custom data'):
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f'Responce validation failed {e}')

    with allure.step('Checking firstname'):
        assert response['booking']['firstname'] == booking_data['firstname']
    with allure.step('Checking lastname'):
        assert response['booking']['lastname'] == booking_data['lastname']
    with allure.step('Checking totalprice'):
        assert response['booking']['totalprice'] == booking_data['totalprice']
    with allure.step('Checking depositpaid'):
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
    with allure.step('Checking bookingdates checkin'):
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    with allure.step('Checking bookingdates checkout'):
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    with allure.step('Checking additionalneeds'):
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test create booking')
@allure.story('POSITIVE: creating booking with random data')
def test_create_booking_with_random_data(api_client, mocker, generate_random_booking_dates):
    with allure.step('Test create booking with random data'):
        response = api_client.create_booking(generate_random_booking_dates)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f'Responce validation failed {e}')

    with allure.step('Checking firstname'):
        assert response['booking']['firstname'] == generate_random_booking_dates['firstname']
    with allure.step('Checking lastname'):
        assert response['booking']['lastname'] == generate_random_booking_dates['lastname']
    with allure.step('Checking totalprice'):
        assert response['booking']['totalprice'] == generate_random_booking_dates['totalprice']
    with allure.step('Checking depositpaid'):
        assert response['booking']['depositpaid'] == generate_random_booking_dates['depositpaid']
    with allure.step('Checking bookingdates checkin'):
        assert response['booking']['bookingdates']['checkin'] == generate_random_booking_dates['bookingdates'][
            'checkin']
    with allure.step('Checking bookingdates checkout'):
        assert response['booking']['bookingdates']['checkout'] == generate_random_booking_dates['bookingdates'][
            'checkout']
    with allure.step('Checking additionalneeds'):
        assert response['booking']['additionalneeds'] == generate_random_booking_dates['additionalneeds']


@allure.feature('Test create booking')
@allure.story('NEGATIVE: Test server unavailable')
def test_create_booking_with_random_data(api_client, mocker, generate_random_booking_dates):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    with allure.step('Test create booking with wrong url'):
        mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match=f'Expected status 200 but got {mock_response.status_code}'):
        api_client.create_booking(generate_random_booking_dates)

@allure.feature('Test create booking')
@allure.story('NEGATIVE: Test timeout')
def test_ping_timeout(api_client, mocker, generate_random_booking_dates):
    mocker.patch.object(api_client.session, 'post', side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.create_booking(generate_random_booking_dates)