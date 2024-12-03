import unittest
from google_scraper import GoogleScraper


class TestGoogleScraper(unittest.TestCase):
    def setUp(self):
        """Настройка тестового окружения перед каждым тестом."""
        self.scraper = GoogleScraper()

    def tearDown(self):
        """Закрытие браузера после каждого теста."""
        self.scraper.close()

    def test_perform_search(self):
        """Тестирование выполнения поиска."""
        query = "Python"
        self.scraper.perform_search(query)

        # Проверяем, что заголовки результатов не пустые
        results = self.scraper.extract_results()
        self.assertGreater(len(results), 0, "Результаты поиска должны быть найдены.")

    def test_extract_results(self):
        """Тестирование извлечения результатов."""
        query = "Python programming"
        self.scraper.perform_search(query)

        results = self.scraper.extract_results()

        # Проверяем, что хотя бы один результат содержит заголовок и ссылку
        self.assertTrue(all('title' in result and 'link' in result for result in results),
                        "Каждый результат должен содержать заголовок и ссылку.")

        # Проверяем, что заголовки не пустые
        for result in results:
            self.assertNotEqual(result['title'], 'Нет заголовка', "Заголовок не должен быть пустым.")
            self.assertNotEqual(result['link'], 'Нет URL', "Ссылка не должна быть пустой.")


if __name__ == "__main__":
    unittest.main()