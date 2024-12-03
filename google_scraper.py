from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from typing import List, Dict


class GoogleScraper:
    """
    Класс для парсинга результатов поиска Google.

    Этот класс использует Selenium для автоматизации браузера и извлечения заголовков и ссылок из результатов поиска.
    """

    def __init__(self) -> None:
        """
        Инициализация экземпляра GoogleScraper.

        Запускает браузер Chrome с помощью ChromeDriver.
        """
        self.driver: webdriver.Chrome = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def perform_search(self, query: str) -> None:
        """
        Выполняет поиск в Google по заданному запросу.

        :param query: Строка, содержащая поисковый запрос.
        """
        self.driver.get("https://www.google.com")  # Открытие главной страницы Google
        search_box = self.driver.find_element(By.NAME, "q")  # Поиск поля ввода
        search_box.send_keys(query + Keys.RETURN)  # Ввод запроса и нажатие Enter
        time.sleep(2)  # Ожидание загрузки результатов

    def extract_results(self) -> List[Dict[str, str]]:
        """
        Извлекает заголовки и ссылки из результатов поиска.

        :return: Список словарей с заголовками и ссылками на результаты.
        """
        results: List[Dict[str, str]] = []  # Список для хранения результатов поиска
        result_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.g')  # Поиск контейнеров результатов

        for result in result_elements:
            # Извлечение заголовка
            title_element = result.find_element(By.TAG_NAME, 'h3') if result.find_elements(By.TAG_NAME, 'h3') else None
            title = title_element.text if title_element else 'Нет заголовка'

            # Извлечение ссылки
            link_element = result.find_element(By.TAG_NAME, 'a') if result.find_elements(By.TAG_NAME, 'a') else None
            link = link_element.get_attribute('href') if link_element else 'Нет URL'

            # Добавление результата в список
            results.append({'title': title, 'link': link})

        return results

    def close(self) -> None:
        """
        Закрывает браузер.

        Этот метод необходимо вызывать после завершения работы с экземпляром GoogleScraper,
        чтобы освободить ресурсы.
        """
        self.driver.quit()


if __name__ == "__main__":
    query: str = "Python Selenium tutorial"  # Задайте поисковый запрос
    scraper = GoogleScraper()  # Создание экземпляра парсера

    try:
        scraper.perform_search(query)  # Выполнение поиска по запросу
        search_results: List[Dict[str, str]] = scraper.extract_results()  # Извлечение результатов

        # Вывод результатов на экран
        for result in search_results:
            print(f"Заголовок: {result['title']}\nСсылка: {result['link']}\n")
    finally:
        scraper.close()  # Закрытие браузера в любом случае