import os
import unittest

from backend.database import Database


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = os.path.join(os.getcwd(), "test_images.db")
        cls.db = Database(cls.test_db_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_path):
            os.remove(cls.test_db_path)

    def setUp(self):
        self.db._create_tables()  # Ensure tables are created before each test

    def tearDown(self):
        with self.db._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM images')  # Clear the table after each test
            conn.commit()

    def test_save_label_and_string(self):
        self.db.save_label_and_string(1, "image_data_cat")
        with self.db._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM images WHERE label = ?', (1,))
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[1], 1)
            self.assertEqual(result[2], "image_data_cat")

    def test_search_images_by_label(self):
        self.db.save_label_and_string(2, "image_data_dog1")
        self.db.save_label_and_string(2, "image_data_dog2")
        result = self.db.search_images_by_label(2)
        self.assertEqual(len(result), 2)
        self.assertIn("image_data_dog1", result)
        self.assertIn("image_data_dog2", result)

    def test_get_all_labels(self):
        self.db.save_label_and_string(3, "image_data_bird")
        self.db.save_label_and_string(4, "image_data_fish")
        result = self.db.get_all_labels()
        self.assertIn(3, result)
        self.assertIn(4, result)

    def test_delete_image_by_string(self):
        self.db.save_label_and_string(5, "image_data_rabbit")
        self.db.delete_image_by_string("image_data_rabbit")
        with self.db._create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM images WHERE image_str = ?', ("image_data_rabbit",))
            result = cursor.fetchone()
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
