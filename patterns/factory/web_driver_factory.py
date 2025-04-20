from selenium import webdriver

from common.log import Logger


logger = Logger().get_logger()

class WebDriverFactory:
    def __init__(self, browser="chrome"):
        """
        Initializes WebDriverFactory with browser type and base URL.

        Args:
            browser (str): Browser type (chrome, firefox, ie).
        """
        logger.info(f"Initializing WebDriverFactory with browser: {browser}")
        self.browser = browser.lower()

    def get_webdriver_instance(self):
        """
        Creates and returns a WebDriver instance based on the browser type.

        Returns:
            WebDriver: The initialized WebDriver instance.
        """
        drivers = {
            "chrome": lambda: webdriver.Chrome(),
            "firefox": lambda: webdriver.Firefox(),
            "edge": lambda: webdriver.Edge()
        }

        driver = drivers.get(self.browser, drivers["chrome"])()
        return driver


# 示例：使用工厂模式创建 WebDriver 实例
if __name__ == "__main__":
    factory = WebDriverFactory(browser="firefox")
    driver = factory.get_webdriver_instance()