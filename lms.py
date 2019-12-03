# coding: utf-8

import argparse
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

def formatted_output(s):
    print("=== {} ===".format(s))

def click_with_script(driver, element):
    driver.execute_script("arguments[0].click()", element)

def main(subject, file_path, task_name):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://itc-lms.ecc.u-tokyo.ac.jp/login")

    driver.find_element_by_id("com_auth").find_element_by_class_name("square_button").click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "userNameInput")))
    driver.find_element_by_id("userNameInput").send_keys(EMAIL)
    driver.find_element_by_id("passwordInput").send_keys(PASSWORD)
    driver.find_element_by_id("submitButton").click()

    formatted_output("Successfully logged in")

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "timetable")))
    cells = driver.find_elements_by_class_name("divTableCell")
    for cell in cells:
        try:
            cell_link = cell.find_element_by_class_name("divTableCellHeader")
            if cell_link.text == subject:
                cell_link.click()
                break
        except NoSuchElementException:
            continue
    formatted_output("Selected classes")

    convert_table = {chr(0xFF10 + i): chr(0x30 + i) for i in range(10)}

    reports = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "report")))
    assignments = reports.find_elements_by_xpath("//div[@class='result_list_txt break']")
    for assignment in assignments:
        try:
            link = assignment.find_element_by_tag_name("a")
            if task_name.translate(str.maketrans(convert_table)) in link.text.translate(str.maketrans(convert_table)):
                click_with_script(driver, link)
                break
        except NoSuchElementException:
            continue
    formatted_output("Selected task")

    submit_area = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "submissionArea")))
    submit_area.find_element_by_class_name("fileSelectInput").send_keys(os.path.abspath(file_path))
    confirm_btn = driver.find_element_by_id("report_submission_btn")
    click_with_script(driver, confirm_btn)
    formatted_output("Submitting task")

    submit_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "submitButton")))
    click_with_script(driver, submit_btn)
    formatted_output("Submitted!")

if __name__ == "__main__":
    if EMAIL is None or PASSWORD is None:
        print(".envファイルを作成し、.env.sampleを参考にあなたのEMAILとPASSWORDを設定してください。")
        exit()
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subject", help="subject ex) 統計と最適化")
    parser.add_argument("-f", "--file", help="file path to submit.")
    parser.add_argument("-t", "--task", help="task name ex) 第４回")
    args = parser.parse_args()
    if args.subject and args.file and args.task:
        main(args.subject, args.file, args.task)
    else:
        print("python lms.py --file path/to/file --subject 情報数学 --task 第９回\nのように提出するファイル、科目、課題の名前を指定してください。")
