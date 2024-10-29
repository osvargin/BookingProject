import allure
from pydantic import ValidationError

from core.models.booking import BookingResponse


@allure.feature('Test create booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanov",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Dinner"
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
