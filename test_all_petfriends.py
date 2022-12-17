import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


s = Service('/Users/vorrr/chromedriver')

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome(service=s)
   pytest.driver.get('http://petfriends1.herokuapp.com/login')

   yield

   pytest.driver.quit()


def test_show_all_pets():
   pytest.driver.find_element(By.ID, 'email').send_keys('ugugug@mail.ru')
   pytest.driver.find_element(By.ID, 'pass').send_keys('ugugug')
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   pytest.driver.implicitly_wait(5)
   images = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i].text
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0
