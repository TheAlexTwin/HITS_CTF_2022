import logging

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep


def _await(driver, t):
	sleep(t)
	driver.wait = WebDriverWait(driver, t)


def start_bot(headless=False):
	options = Options()
	options.headless = headless

	logging.info("[bot] starting...")

	driver = webdriver.Firefox(executable_path="./geckodriver", options=options)
	driver.get(r"http://localhost:8000/admin/login")
	_await(driver, 3)

	login_form = driver.find_element_by_id('username')
	login_form.send_keys("secret_admin_username123")
	login_form = driver.find_element_by_id('password')
	login_form.send_keys("secret_admin_password123")
	login_form.submit()

	_await(driver, 3)
	driver.get(r"http://localhost:8000/reports?query=hkeys%20reports")

	i = 0
	while True:
		links = driver.find_elements_by_class_name("link")

		if i >= len(links):
			break

		link = links[i]
		link.click()
		_await(driver, 4)

		try:
			driver.get(r"http://localhost:8000/reports?query=hkeys%20reports")
		except Exception as e:
			logging.error(e)

		i += 1

	logging.info("[bot] finished ok")
	driver.close()


if __name__ == "__main__":
	start_bot(True)
