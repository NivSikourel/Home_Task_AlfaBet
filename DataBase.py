import sqlite3
from typing import Dict, Any, List, Optional

DB_FILE = "events.db"


def create_table() -> None:
    conn: Any = sqlite3.connect(DB_FILE)
    cursor: Any = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            venue TEXT,
            date TEXT,
            popularity INTEGER,
            created_at TEXT
        )
    ''')

    conn.commit()
    conn.close()


def add_event(event: Dict) -> None:
    conn: Any = sqlite3.connect(DB_FILE)
    cursor: Any = conn.cursor()

    cursor.execute('''
            INSERT INTO events (name, location, venue, date, popularity, created_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        ''', (
        event.get('name'), event.get('location'), event.get('venue'), event.get('date'), event.get('popularity', 0)))

    conn.commit()
    conn.close()


def get_sorted_events(sort_by: str = 'created_at') -> List[Dict]:
    conn: Any = sqlite3.connect(DB_FILE)
    cursor: Any = conn.cursor()

    cursor.execute(f'SELECT * FROM events ORDER BY {sort_by}')

    events: List[Dict] = []
    for row in cursor.fetchall():
        event: Dict = {
            'id': row[0],
            'name': row[1],
            'location': row[2],
            'venue': row[3],
            'date': row[4],
            'popularity': row[5],
            'created_at': row[6]
        }
        events.append(event)

    conn.close()
    return events


def delete_event(event_id: int) -> None:
    conn: Any = sqlite3.connect(DB_FILE)
    cursor: Any = conn.cursor()

    cursor.execute('''
            DELETE FROM events
            WHERE id = ?
        ''', (event_id,))

    conn.commit()
    conn.close()


def get_last_event_id() -> Optional[int]:
    conn: Any = sqlite3.connect(DB_FILE)
    cursor: Any = conn.cursor()

    cursor.execute('''
            SELECT id FROM events
            ORDER BY id DESC
            LIMIT 1
        ''')

    last_event_id: Dict = cursor.fetchone()

    conn.close()

    if last_event_id:
        return last_event_id[0]
    else:
        return None


def update_event(event_id: int, updated_event: Dict) -> None:
    conn: Any = sqlite3.connect(DB_FILE)
    cursor: Any = conn.cursor()

    cursor.execute(
        'UPDATE events SET name=?, location=?, venue=?, date=?, popularity=? WHERE id=?',
        (
            updated_event['name'],
            updated_event['location'],
            updated_event['venue'],
            updated_event['date'],
            updated_event['popularity'],
            event_id
        )
    )

    conn.commit()
    conn.close()
