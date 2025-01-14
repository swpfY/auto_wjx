import logging
import random
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver import ActionChains
import numpy as np
import time

import conf


def choose_answer():
    try:
        choose_one(1, [0.2, 0.8, 0, 0])  # 各项均为相同概率，可省略不写。
        choose_one(2, [0.5, 0.5])
        choose_one(3)
        choose_one(4, [0.3, 0.5, 0.2, 0])
        choose_one(5, [0.9, 0.1])
        choose_one(6, [0.4, 0.5, 0.1])
        choose_one(7, [0.9, 0.1])
        choose_one(8, [0.6, 0.4])
        choose_one(9, [0.4, 0.6])
        choose_one(10, [1, 0])
        choose_one(11, [0.7, 0.2, 0.1])
        choose_one(12, [0, 0, 0.3, 0.3, 0.2, 0.2])
        choose_one(13, [1, 0])
        choose_one(14, [0.2, 0.8])
        choose_one(15, [0.7, 0.3])
        choose_one(16, [1, 0])
        choose_one(17, [0.5, 0.4, 0, 0.1])
        choose_one(18, [0.1, 0.2, 0.3, 0.2, 0.2])
        choose_one(19, [0.8, 0.2, 0, 0])
        choose_one(20, [0.2, 0.1, 0.3, 0.2, 0.2])
        choose_one(21, [0.3, 0.3, 0.2, 0.2])
        choose_one(22, [0.2, 0.3, 0.3, 0.2])
        choose_one(23, [0.2, 0.2, 0.2, 0.4])
        choose_multiple(24)
        choose_one(25, [0, 0, 0.4, 0.6])
        choose_multiple(26, [0.35, 0.44, 0.2, 0.01])
        choose_multiple(27, exclude=[5])
        choose_multiple(28)
        choose_multiple(29, [0.01, 0.45, 0.54])
        choose_multiple(30)
        choose_multiple(31, [0.01, 0.43, 0.54, 0.02])
        choose_one(32, [0.2, 0.4, 0.3, 0.1])
        choose_one(33, [0.2, 0.7, 0.1])
        choose_multiple(34, [0.01, 0.25, 0.34, 0.4])
        choose_multiple(35, [0.3, 0.1, 0.4, 0.2, 0], 4)
        # driver.find_element(By.XPATH, '//*[@id="tqq35_5"]').send_keys('无')
        choose_one(36, [0.2, 0.35, 0.25, 0.2])
        choose_one(37, [0.3, 0.7])
        choose_one(38, [0.4, 0.6])
        choose_one(39, [0, 1])
        choose_one(40, [1, 0])
        choose_one(41, [0.8, 0.2, 0, 0])
        choose_one(42, [0.4, 0.4, 0.2])
        choose_one(43, [0.3, 0.3, 0.3, 0.1])
        choose_one(44, [0.6, 0.4])
        choose_one(45)
        choose_multiple(46, [0.01, 0.25, 0.34, 0.4])
        choose_one(47, [0.5, 0.2, 0.3, 0])
        choose_multiple(48)
        choose_one(49, [0, 0.5, 0.5, 0])
        choose_multiple(50)
        write_blank()  # 填写无
        # choose_multiple(14, [0.3, 0.3, 0.3, 0.1])
        # choose_multiple(15, [0.2, 0.2, 0.1, 0.2, 0.2, 0.1])
        # choose_multiple(16, [0.1, 0.2, 0.1, 0.3, 0.2, 0.1])
        # choose_multiple(17, [0.25, 0.25, 0.25, 0.25])
        # choose_multiple(18, [0.3, 0.3, 0.3, 0.1])
        # choose_multiple(19, [0.2, 0.1, 0.3, 0, 0.1, 0.2, 0.1], 3)  # 非相同概率时，没必要用 exclude。
        # choose_multiple(20)  # 各项均为相同概率，可省略不写。
        # choose_one(21, [0.2, 0.4, 0.3, 0.1])
    except NoSuchElementException as e:
        logging.error("任务执行失败，请检查配置。")


def probabilities_generator(choices_num, exclude=None):
    if isinstance(exclude, list):
        choices_num -= len(exclude)
    probability = 1 / choices_num
    res = [probability for i in range(choices_num)]
    if exclude:
        for i in exclude:
            res.insert(i, 0)
    return res


def choose_one(question_number, question_probability=None, exclude=None):
    """
    :param question_number: int
    :param question_probability: [] # If you set it None, It will auto generate an averages list.
    :param exclude: [] # A list which question index you want to exclude.
    """
    el_choices = driver.find_elements(By.XPATH, f"//*[@id=\"div{question_number}\"]/div[2]/div")
    choices_num = len(el_choices)
    if not question_probability:
        question_probability = probabilities_generator(choices_num, exclude=exclude)
    chosen_number = np.random.choice(
        a=list(range(1, choices_num + 1)),
        p=question_probability
    )
    el_checked = driver.find_element(By.XPATH, f"//*[@id=\"div{question_number}\"]/div[2]/div[{chosen_number}]")
    el_checked.click()
    # 随机停顿
    # rt = random.randint(10, 100)
    # time.sleep(rt / 100)


def choose_multiple(question_number, question_probability=None, restrict=10000, exclude=None):
    el_options = driver.find_elements(By.XPATH, f"//*[@id=\"div{question_number}\"]/div[2]/div")
    choices_num = len(el_options)
    if not question_number:
        question_probability = probabilities_generator(choices_num, exclude=exclude)
    chosen_number = np.random.choice(
        a=list(range(1, choices_num + 1)),
        p=question_probability,
        size=random.randint(1, min(restrict, choices_num)),
        replace=False
    )
    for i in chosen_number:
        driver.find_element(By.XPATH, f"//*[@id=\"div{question_number}\"]/div[2]/div[{i}]").click()
    # 随机停顿
    # rt = random.randint(10, 100)
    # time.sleep(rt / 100)


def write_blank():
    """填写内容"""
    driver.find_element(By.XPATH, '//*[@id="q51"]').send_keys('无')
    # 随机停顿
    # rt = random.randint(10, 100)
    # time.sleep(rt / 100)


def slider_move(loop_index, dest=380):
    """
    :param loop_index: int
    :param dest: int # A position where you want to move.
    """
    try:
        el_slider = WebDriverWait(driver, 10).until(
            presence_of_element_located(
                (By.XPATH, "//*[@id='nc_1__scale_text']/span"))
        )
        ActionChains(driver).click_and_hold(el_slider).perform()
        ActionChains(driver).move_by_offset(xoffset=dest, yoffset=0).perform()
        ActionChains(driver).release().perform()
    except (TimeoutException, ElementClickInterceptedException):
        logging.error(f"第 {loop_index} 次请求执行失败！")


def check_element_exists(element: str) -> bool:
    """ 检查元素是否存在，若不存在会抛出异常

    :param element: id
    :return: Boolean
    """
    try:
        driver.find_element(By.XPATH, element)
        return True
    except Exception as e:
        return False


def main():
    try:
        for i in range(loop_count):
            driver.get(question_url)
            try:
                driver.find_element(By.XPATH, '//*[@id="confirm_box"]/div[2]/div[3]/button[1]').click()  # 取消提示
            except NoSuchElementException:
                pass
            choose_answer()
            driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
            time.sleep(0.5)
            if check_element_exists('//*[@id="alert_box"]/div[2]/div[2]/button'):
                driver.find_element(By.XPATH, '//*[@id="alert_box"]/div[2]/div[2]/button').click()
                driver.find_element(By.XPATH, '//*[@id="rectMask"]').click()
            print(f"第 {i} 次任务执行成功。")
            try:
                WebDriverWait(driver, 15).until(
                    ec.url_changes(question_url)
                )
            except TimeoutException:
                slider_move(i, dest=380)  # 若验证码逃逸失败，请自行调教参数 dest
    except Exception as e:
        print('error: ', e)
        logging.error("任务执行错误，正在退出任务: ")
    finally:
        driver.close()
        input()


if __name__ == '__main__':
    question_url = conf.QUESTION_URL or input("请输入问卷地址：")
    loop_count = conf.LOOP_COUNT or int(input("请输入填写次数："))
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    opt.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=opt)
    # driver = webdriver.Safari(options=opt)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                           {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
    np.random.seed(int(time.time()))
    main()
