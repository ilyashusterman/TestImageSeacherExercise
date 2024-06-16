import os
import sqlite3
from typing import List

class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.getcwd(), "images.db")
        self.db_path = db_path
        self._create_tables()

    def _create_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_tables(self) -> None:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label INTEGER NOT NULL,
                    image_str TEXT NOT NULL
                )
            ''')
            conn.commit()

    def save_label_and_string(self, label: int, image_str: str) -> None:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO images (label, image_str) VALUES (?, ?)
            ''', (label, image_str))
            conn.commit()

    def search_images_by_label(self, label: int) -> List[str]:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT image_str, label FROM images WHERE label = ?
            ''', (label,))
            results = cursor.fetchall()
            return [[row[0], row[1]] for row in results]

    def get_all_labels(self) -> List[int]:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT DISTINCT label FROM images
            ''')
            results = cursor.fetchall()
            return [row[0] for row in results]

    def delete_image_by_string(self, image_str: str) -> None:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM images WHERE image_str = ?
            ''', (image_str,))
            conn.commit()
