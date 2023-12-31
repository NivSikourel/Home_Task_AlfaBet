import threading
import unittest
import requests
from main import run


class TestEventAPI(unittest.TestCase):
    server_thread = None
    base_url = 'http://localhost:8080/events'

    @classmethod
    def setUpClass(cls):
        cls.server_thread = threading.Thread(target=run)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        requests.get('http://localhost:8080/shutdown')
        cls.server_thread.join()
        cls.server_thread.terminate()

    def setUp(self):
        data = {
            'name': 'SetUp Event',
            'location': 'SetUp Location',
            'venue': 'SetUp Venue',
            'date': '2023-12-30T22:00:00',
            'popularity': 50
        }
        response = requests.post(self.base_url, json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        self.created_event_id = response.json()['id']

    def tearDown(self):
        requests.delete(f'{self.base_url}/{self.created_event_id}')

    def test_create_event(self):
        headers = {'Content-Type': 'application/json'}
        data = {
            'name': 'New Test Event',
            'location': 'New York City',
            'venue': 'MSG',
            'date': '2024-01-01T12:00:00',
            'popularity': 100
        }
        response = requests.post(self.base_url, json=data, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())

    def test_get_all_events(self):
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        events = response.json()
        self.assertTrue(len(events) > 0)
        self.assertTrue(isinstance(events, list))

    def test_get_specific_event(self):
        response = requests.get(f'{self.base_url}/{self.created_event_id}')
        self.assertEqual(response.status_code, 200)
        event = response.json()
        self.assertEqual(event['id'], self.created_event_id)

    def test_update_event(self):
        updated_data = {
            'name': 'Updated Test Event',
            'location': 'Chicago',
            'venue': 'AllState Arena',
            'date': '2023-12-31T14:00:00',
            'popularity': 150
        }
        response = requests.put(f'{self.base_url}/{self.created_event_id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Event updated successfully')

    def test_delete_event(self):
        response = requests.delete(f'{self.base_url}/{self.created_event_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Event deleted successfully')


if __name__ == '__main__':
    unittest.main(exit=False)
