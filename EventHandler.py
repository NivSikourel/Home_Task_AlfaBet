from http.server import BaseHTTPRequestHandler
import json
from typing import Any, List, Dict, AnyStr, Optional

from DataBase import add_event, get_sorted_events, delete_event, get_last_event_id, update_event

from ReminderUtilities import schedule_reminder


class EventHandler(BaseHTTPRequestHandler):
    def _set_response(self, status_code: int = 200, content_type: str = 'text/html') -> None:
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def do_GET(self) -> None:
        events: List[Dict] = get_sorted_events('created_at')
        if self.path == '/events':
            self._set_response(200, 'application/json')
            self.wfile.write(json.dumps(events).encode())
        elif self.path.startswith('/events/'):
            event_id: str = self.path.split('/')[-1]
            if event_id.isdigit():
                if event_id in [str(event['id']) for event in events]:
                    specific_event: Dict = [event for event in events if str(event['id']) == event_id][0]
                    self._set_response(200, 'application/json')
                    self.wfile.write(json.dumps(specific_event).encode())
                else:
                    self._set_response(404)
                    self.wfile.write(b'Event not found')
            else:
                self._set_response(400)
                self.wfile.write(b'Invalid event ID')
        else:
            self._set_response(404)
            self.wfile.write(b'Not Found')

    def do_POST(self) -> None:
        if self.path == '/events':
            content_length: int = int(self.headers['Content-Length'])
            post_data: AnyStr = self.rfile.read(content_length)
            new_event: Any = json.loads(post_data.decode())

            add_event(new_event)

            schedule_reminder(new_event)

            created_event_id: Optional[int] = get_last_event_id()

            self._set_response(201, 'application/json')
            self.wfile.write(json.dumps({'message': 'Event scheduled successfully', 'id': created_event_id}).encode())
        else:
            self._set_response(404)
            self.wfile.write(b'Not Found')

    def do_PUT(self) -> None:
        if self.path.startswith('/events/'):
            event_id: str = self.path.split('/')[-1]

            if event_id.isdigit():
                events: List[Dict] = get_sorted_events('created_at')
                if event_id in [str(event['id']) for event in events]:
                    existing_event: Optional[Dict] = [event for event in events if str(event['id']) == event_id][0]

                    content_length: int = int(self.headers['Content-Length'])
                    update_data: AnyStr = self.rfile.read(content_length)
                    updated_event: Any = json.loads(update_data.decode())

                    updated_event: Dict = {**existing_event, **updated_event}

                    update_event(int(event_id), updated_event)

                    self._set_response(200, 'application/json')
                    self.wfile.write(json.dumps({'message': 'Event updated successfully'}).encode())
                else:
                    self._set_response(404)
                    self.wfile.write(b'Event not found')
            else:
                self._set_response(400)
                self.wfile.write(b'Invalid event ID')
        else:
            self._set_response(404)
            self.wfile.write(b'Not Found')

    def do_DELETE(self) -> None:
        if self.path.startswith('/events/'):
            event_id: str = self.path.split('/')[-1]

            if event_id.isdigit():
                events: List[Dict] = get_sorted_events('created_at')
                if event_id in [str(event['id']) for event in events]:
                    delete_event(int(event_id))

                    self._set_response(200, 'application/json')
                    self.wfile.write(json.dumps({'message': 'Event deleted successfully'}).encode())
                else:
                    self._set_response(404)
                    self.wfile.write(b'Event not found')
            else:
                self._set_response(400)
                self.wfile.write(b'Invalid event ID')
        else:
            self._set_response(404)
            self.wfile.write(b'Not Found')
