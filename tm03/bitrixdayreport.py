import datetime
import json
import sys

import requests
from selenium import webdriver
import calendar

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC


def add_to_report(now, user, pwd, idbitrix, report):
    res = "000"

    s = Service('C:\\PycharmProjects\\tm03\\tm03\\chromedriver\\chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()

    wait = WebDriverWait(driver, 500)

    url = 'https://bitrix.apx-service.ru/'

    try:
        driver.get(url)
        elem = driver.find_element(by=By.NAME, value="USER_LOGIN")
        elem.clear()
        elem.send_keys(user)
        elem = driver.find_element(by=By.NAME, value="USER_PASSWORD")
        elem.clear()
        elem.send_keys(pwd)

        elem = driver.find_element(By.CLASS_NAME, 'login-btn')
        elem.click()

        wait.until(EC.presence_of_element_located((By.ID, "timeman-container")))

        driver.get('https://bitrix.apx-service.ru/timeman/timeman.php')

        fcn = 'js-' + str(idbitrix) + '_' + str(now.year) + '-' + format(now.month, '02d') + '-' + format(now.day, '02d')

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, fcn)))

        elems = driver.find_elements(By.CLASS_NAME, fcn)
        if elems:
            elems[0].click()

        fcn = 'side-panel-iframe'

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, fcn)))

        spi = driver.find_element(By.CLASS_NAME, fcn)

        driver.switch_to.frame(spi)

        fcn = 'feed-com-add-box-outer'

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, fcn)))

        cur_elem = driver.find_element(By.CLASS_NAME, fcn)

        cur_elem.location_once_scrolled_into_view

        wait.until(EC.element_to_be_clickable(cur_elem))

        cur_elem.click()

        cur_elem.location_once_scrolled_into_view

        fcn = 'bx-editor-iframe'

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, fcn)))

        driver.switch_to.frame(driver.find_element(By.CLASS_NAME, fcn))

        wait.until(EC.element_to_be_clickable((By.TAG_NAME, "body")))

        elem = driver.find_element(By.TAG_NAME, "body")
        elem.send_keys(report)

        driver.switch_to.default_content()

        driver.switch_to.frame(spi)
        send_btns = driver.find_element(By.CLASS_NAME, 'feed-add-post-buttons')
        send_btn = send_btns.find_element(By.XPATH, '//button[contains(@class, "ui-btn ui-btn-sm ui-btn-primary")]')
        send_btn.click()

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    return res


if __name__ == '__main__':

    now = datetime.date.today()

    print(add_to_report(now, "mihail.u", "ZE4pMFr", 313, 'sfgvsthrtjhsdrhwer'))
