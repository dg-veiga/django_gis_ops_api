import django
django.setup()

from django.test import TestCase
from rest_framework.test import APIClient
from base.models.user_area import UserArea
from django.contrib.auth.models import User


class UserAreaViewsTests(TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.client = APIClient()

    @property
    def default_user(self):
        return User(email='test@test.com', is_staff=False, is_active=True, password='')

    def test_health(self):
        response = self.client.get('/api/v1/health/', data={'format': 'json'})
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual('Ok', json_response['health'])

    def test_user_area__add_geometry_with_polygon_coordinates__expected_success(self):
        payload = {
            "user": 1,
            "geometry": {
                "coordinates": [
                    [
                        [
                            -38.31999477608238,
                            -12.899555673542778
                        ],
                        [
                            -38.347184235020336,
                            -12.904922667790004
                        ],
                        [
                            -38.346900420209494,
                            -12.921520889862478
                        ],
                        [
                            -38.3347531462781,
                            -12.923346626969973
                        ],
                        [
                            -38.32340055381948,
                            -12.912281348939914
                        ],
                        [
                            -38.30483906515025,
                            -12.908076414805137
                        ],
                        [
                            -38.30608785032018,
                            -12.902764817966329
                        ],
                        [
                            -38.31556726502345,
                            -12.90436937473784
                        ],
                        [
                            -38.31999477608238,
                            -12.899555673542778
                        ]
                    ]
                ],
                "type": "Polygon"
            }
        }
        response = self.client.post('/api/v1/user_area/', payload, format='json')
        self.assertEqual(201, response.status_code)

    def test_user_area__add_geometry_as_point__expected_success(self):
        payload = {
            "user": 1,
            "geometry": {
                "coordinates": [-38.332766442598256, -12.90968093749268],
                "type": "Point"
            }
        }
        response = self.client.post('/api/v1/user_area/', payload, format='json')
        self.assertEqual(201, response.status_code)

    def test_user_area__add_geometry_as_point__expected_area_on_get_list_request(self):
        payload = {
            "user": 1,
            "geometry": {
                "coordinates": [-38.332766442598256, -12.90968093749268],
                "type": "Point"
            }
        }
        response = self.client.post('/api/v1/user_area/', payload, format='json')
        self.assertEqual(201, response.status_code)

        response = self.client.get('/api/v1/user_area/', format='json')
        json_response = response.json()
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(json_response))

    def test_user_area__add_geometry_as_point__expected_to_update_area_from_point_to_polygon(self):
        payload = {
            "user": 1,
            "code": "123",
            "description": "x" * 1010,
            "geometry": {
                "coordinates": [-38.332766442598256, -12.90968093749268],
                "type": "Point"
            }
        }
        response = self.client.post('/api/v1/user_area/', payload, format='json')
        self.assertEqual(201, response.status_code)

        response = self.client.get('/api/v1/user_area/', format='json')
        json_response = response.json()
        self.assertEqual(200, response.status_code)

        _id = json_response[0]['id']
        user_area_1 = UserArea.objects.get(id=_id)
        self.assertEqual('123', user_area_1.code)
        self.assertEqual('x'*997 + '...', user_area_1.description)
