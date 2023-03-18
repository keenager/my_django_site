from django.shortcuts import render, redirect
from config import settings
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
import re
from pprint import pprint

CHROME_DRIVER_PATH = f'{settings.BASE_DIR}/chromedriver'


class LoginError(Exception):
    def __str__(self) -> str:
        return '로그인 실패... 아이디나 비밀번호를 다시 입력하세요!'


def getData(id: str, password: str, howManyWeeks: int) -> list[dict]:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=options)

    driver.get('https://case.publicdef.net')
    time.sleep(1)

    # 로그인
    login_button = driver.find_element(By.LINK_TEXT, '로그인')
    login_button.click()

    time.sleep(1)
    input_id = driver.find_element(By.ID, 'id_username')
    input_id.send_keys(id)
    input_password = driver.find_element(By.ID, 'id_password')
    input_password.send_keys(password)
    login_button2 = driver.find_element(By.ID, 'loginbutton')
    login_button2.click()
    time.sleep(1)

    if 'login' in driver.current_url:
        print('로그인 실패')
        driver.quit()
        raise LoginError()

    print('로그인 성공')

    # 일정으로 진입
    driver.find_element(By.LINK_TEXT, '일정').click()

    # 주간 일정으로 진입
    driver.find_element(By.CLASS_NAME, 'fc-listWeek-button').click()
    time.sleep(1)

    # 스케줄 긁어오기
    schedules = getSchedules(driver)
    for i in range(howManyWeeks):
        driver.find_element(By.CLASS_NAME, 'fc-next-button').click()
        time.sleep(1)
        schedules += getSchedules(driver)

    # 매 사건 법정 위치 가져오기
    for i in range(len(schedules)):
        if schedules[i]['link'] == None:
            continue
        # 링크 페이지로 이동
        driver.get(schedules[i]['link'])

        case_detail_text = driver.find_element(
            By.CSS_SELECTOR, 'tbody.casedetail_td').text

        pattern = re.compile('제?\d+호 ?법정')
        result = pattern.findall(case_detail_text)
        pattern = re.compile('\d+호')
        result = pattern.search(result[-1])
        courtroom = '[{}]'.format(result.group() if result else '?')
        schedules[i]['courtroom'] = courtroom

    # pprint(schedules)

    return schedules

    # while (True):
    #     pass

#   (headless: true)


# 현재 페이지의 스케줄 긁어오기
def getSchedules(driver: WebDriver) -> list:
    date = ''
    schedule_list = []

    tr_elements = driver.find_elements(
        By.CSS_SELECTOR, '.fc-list-table > tbody > tr')

    for tr in tr_elements:

        if tr.get_attribute('class') == 'fc-list-heading':
            date = tr.get_attribute('data-date')
            continue

        content = tr.find_element(
            By.CSS_SELECTOR, 'td.fc-list-item-title').text

        if '기일표' in content:
            continue

        time = tr.find_element(By.CSS_SELECTOR, 'td.fc-list-item-time').text

        link = None if '의견서' in content else tr.find_element(
            By.TAG_NAME, 'a').get_attribute('href')

        schedule_list.append(   # 기일표 제외
            {'date': date,
             'time': time,
             'content': content,
             'link': link}      # 의견서 제외
        )
    return schedule_list
