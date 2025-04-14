from selenium import webdriver
import threading


class WebDriverSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WebDriverSingleton, cls).__new__(cls)
                cls._instance.driver = webdriver.Chrome()  # 只创建一次 WebDriver
        return cls._instance

    def get_driver(self):
        return self.driver


# 示例
if __name__ == "__main__":
    driver1 = WebDriverSingleton().get_driver()
    driver2 = WebDriverSingleton().get_driver()

    print(driver1 is driver2)  # True，确保只有一个实例