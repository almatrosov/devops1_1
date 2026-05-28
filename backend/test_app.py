import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Добавляем текущую директорию в пути поиска Python
sys.path.append(os.path.dirname(__file__))
from app import app

class TestNotesApp(unittest.TestCase):
    def setUp(self):
        # Настраиваем тестовый контекст и клиент Flask
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
        # Создаем фейковые объекты соединения и курсора
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Задаем структуру данных, которую якобы вернула реальная база данных
        mock_cursor.fetchall.return_value = [(1, "Тестовый заголовок", "Тестовый текст")]
        mock_conn.cursor.return_value = mock_cursor
        
        # Перехватываем вызов функции подключения и возвращаем наш фейковый мок
        mock_get_db_connection.return_value = mock_conn
        
        # Выполняем запрос к тестовому клиенту API
        response = self.client.get('/api/notes')
        
        # Проверяем утверждения (Assertions)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['title'], "Тестовый заголовок")

if __name__ == '__main__':
    unittest.main()