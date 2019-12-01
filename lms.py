import argparse
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

def click_with_script(driver, element):
    driver.execute_script("arguments[0].click()", element)

def main(subject, file_path, task_name):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://itc-lms.ecc.u-tokyo.ac.jp/login")

    driver.find_element_by_id("com_auth").find_element_by_class_name("square_button").click()
    time.sleep(2)
    driver.find_element_by_id("userNameInput").send_keys(EMAIL)
    driver.find_element_by_id("passwordInput").send_keys(PASSWORD)
    driver.find_element_by_id("submitButton").click()

    time.sleep(5)
    print("=======Successfully logged in=======")

    cells = driver.find_elements_by_class_name("divTableCell")
    for cell in cells:
        try:
            cell_link = cell.find_element_by_class_name("divTableCellHeader")
            if cell_link.text == subject:
                cell_link.click()
                break
        except NoSuchElementException:
            continue
    print("=======Selected classes=======")

    time.sleep(1)

    convert_table = {chr(0xFF10 + i): chr(0x30 + i) for i in range(10)}

    reports = driver.find_element_by_id("report")
    assignments = reports.find_elements_by_xpath("//div[@class='result_list_txt break']")
    for assignment in assignments:
        try:
            link = assignment.find_element_by_tag_name("a")
            if link.text.translate(str.maketrans(convert_table)) == task_name.translate(str.maketrans(convert_table)):
                click_with_script(driver, link)
                break
        except NoSuchElementException:
            continue
    print("=======Selected task=======")

    time.sleep(2)

    submit_area = driver.find_element_by_id("submissionArea")
    submit_area.find_element_by_class_name("fileSelectInput").send_keys(os.path.abspath(file_path))
    confirm_btn = driver.find_element_by_id("report_submission_btn")
    click_with_script(driver, confirm_btn)
    print("=======Submitting task=======")

    time.sleep(3)
    submit_btn = driver.find_element_by_id("submitButton")
    click_with_script(driver, submit_btn)
    print("=======Submitted!=======")

if __name__ == "__main__":
    print(EMAIL)
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
