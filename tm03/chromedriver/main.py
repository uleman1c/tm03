import calendar
import datetime
import json
import sys

import requests
from selenium import webdriver
import time
import calendar

# from selenium.webdriver import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from back_server import AUTH_DATA

def get_month():

    s = Service('C:\\Users\\Mihail\\PycharmProjects\\FileServer\\chromedriver\\chromedriver')
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()


    wait = WebDriverWait(driver, 500)

    url = 'https://hermes.growfood.pro/login'

    try:
        driver.get(url)
        elem = driver.find_element(value="login")
        elem.clear()
        elem.send_keys("enikafood")
        elem = driver.find_element(value="password")
        elem.clear()
        elem.send_keys("QTXVkvQn")

        elem = driver.find_elements(By.XPATH, '//button')[2]
        elem.click()

        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Прогноз")))

        elem = driver.find_element(By.LINK_TEXT, 'Прогноз')
        elem.click()

        wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="btn btn-lg btn-secondary"]')))

        now = datetime.date.today()
        to = now + datetime.timedelta(days=25)

        m_rows = list()

        if now.month == to.month:
            read_month(driver, now.day, now.month, now.year, to.day, wait, m_rows)
        else:
            read_month(driver, now.day, now.month, now.year, calendar.monthrange(now.year, now.month)[1], wait, m_rows)
            read_month(driver, 1, to.month, to.year, to.day, wait, m_rows)

        res = dict()
        res['plans_from_hermes'] = dict()
        res['plans_from_hermes']['rows'] = m_rows

        try:
            req = requests.post(AUTH_DATA['efr_upp_addr'] + '/hs/exch/gf', data=json.dumps(res), auth=(AUTH_DATA['user'], AUTH_DATA['pwd']))
        except Exception:
            res['exeption'] = str(sys.exc_info())
            print(res['exeption'])


        try:
            data_dict = json.loads(req.content)
        except:
            data_dict = {}

        # if data_dict['success'] == True:
        #     res['success'] = True
        #     for cco in co:
        #         cco.delivered1c = True
        #         cco.save()

        res['req'] = data_dict


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def read_month(driver, f_day, f_month, f_year, t_day, wait, m_rows):

    period = driver.find_element(By.XPATH, '//div[@class="form-control reportrange-text"]')
    period.click()

    wait.until(EC.element_to_be_clickable((By.XPATH, '//th[@class="prev available"]')))

    daterangepicker = driver.find_element(By.XPATH, '//div[contains(@class, "daterangepicker")]')

    selperiod = daterangepicker.find_element(By.XPATH, '//span[@class="drp-selected"]')

    m_months = ['янв.', 'февр.', 'март', 'апр.', 'май', 'июнь', 'июль', 'авг.', 'сент.', 'окт.', 'нояб.', 'дек.']
    prevs = daterangepicker.find_elements(By.XPATH, '//th[@class="prev available"]')
    nexts = daterangepicker.find_elements(By.XPATH, '//th[@class="next available"]')

    months = daterangepicker.find_elements(By.XPATH, '//th[@class="month"]')
    start_period = months[0].text.split(' ')
    start_year = int(start_period[1])
    while f_year != start_year:
        if f_year > start_year:
            nexts[0].click()
        else:
            prevs[0].click()

        months = daterangepicker.find_elements(By.XPATH, '//th[@class="month"]')
        start_period = months[0].text.split(' ')
        start_year = int(start_period[1])
    while f_month != m_months.index(start_period[0]) + 1:
        if f_month > m_months.index(start_period[0]) + 1:
            nexts[0].click()
        else:
            prevs[0].click()

        months = daterangepicker.find_elements(By.XPATH, '//th[@class="month"]')
        start_period = months[0].text.split(' ')
    days = daterangepicker.find_element(By.XPATH,
                                        '//td[@data-date="' + str(datetime.date(f_year, f_month, f_day)) + '"]')
    days.click()
    end_day = t_day
    cur_day = f_day
    while cur_day <= end_day:

        cur_date = datetime.date(f_year, f_month, cur_day)
        next_date = datetime.date(f_year, f_month, cur_day) + datetime.timedelta(days=7)

        if cur_date.month == next_date.month:

            cur_day = cur_day + 7

            days = daterangepicker.find_element(By.XPATH, '//td[@data-date="' + str(
                datetime.date(f_year, f_month, cur_day)) + '"]')
            ActionChains(driver).move_to_element(days).perform()

        else:
            break
    while cur_day + 7 > end_day and cur_day != end_day:
        cur_day = cur_day - 1

        days = daterangepicker.find_element(By.XPATH,
                                            '//td[@data-date="' + str(datetime.date(f_year, f_month, cur_day)) + '"]')
        ActionChains(driver).move_to_element(days).perform()
    if cur_day + 7 == end_day:
        cur_day += 7
        days = daterangepicker.find_element(By.XPATH,
                                            '//td[@data-date="' + str(datetime.date(f_year, f_month, cur_day)) + '"]')
        ActionChains(driver).move_to_element(days).perform()
    days.click()
    driver.find_element(By.XPATH, '//button[contains(@class, "applyBtn")]').click()
    elems = driver.find_elements(By.XPATH, '//button[@class="btn btn-lg btn-secondary"]')
    elems[0].click()
    wait.until(EC.presence_of_element_located(
        (By.XPATH, '//table[contains(@class, "table table-sm table-bordered table-striped mb-0")]')))
    table = driver.find_element(By.XPATH,
                                '//table[contains(@class, "table table-sm table-bordered table-striped mb-0")]')
    if table:
        tbody = table.find_element(By.XPATH, '//tbody')
        rows = tbody.find_elements(By.XPATH, '//tr')

        for cur_row in rows:
            cur_row_cells = cur_row.get_property('children')
            # cur_row.find_elements(By.XPATH, '//td')

            row = dict()

            row['date'] = cur_row_cells[0].text
            row['name_1c'] = cur_row_cells[1].text
            row['name'] = cur_row_cells[2].text
            row['uid'] = cur_row_cells[3].text
            row['code'] = cur_row_cells[4].text
            row['rc'] = cur_row_cells[5].text
            row['will'] = cur_row_cells[6].text
            row['fact'] = cur_row_cells[7].text

            m_rows.append(row)

    return True


def main():

    get_month()

if __name__ == '__main__':
    main()




