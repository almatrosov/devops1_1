import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Добавляем текущую директорию в пути поиска Python, чтобы импортировать app.py
sys.path.append(os.path.dirname(__file__))
from app import app

class TestNotesApp(unittest.TestCase):
    def setUp(self):
        # Настраиваем тестовый клиент Flask
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_health_endpoint(self):
        """1. Проверка работоспособности эндпоинта /api/health"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    @patch('app.get_db_connection')
    def test_get_notes_mocked(self, mock_get_db_connection):
        """2. Тестирование бизнес-логики получения заметок с заглушкой БД"""
        # Декоратор @patch сам создал мок и передал его в mock_get_db_connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Настраиваем цепочку вызовов: connection.cursor() -> fetchall() -> данные
        mock_cursor.fetchall.return_value = [(1, "Тестовый заголовок", "Тестовый текст")]
        mock_conn.cursor.return_value = mock_cursor
        
        # Заставляем наш перехваченный метод get_db_connection возвращать mock_conn
        mock_get_db_connection.return_value = mock_conn
        
        # Делаем запрос к тестовому клиенту
        response = self.client.get('/api/notes')
        
        # Проверяем утверждения
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['title'], "Тестовый заголовок")

if __name__ == '__main__':
    unittest.main()