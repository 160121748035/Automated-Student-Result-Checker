from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import streamlit as st
from plyer import notification


def check_result(roll,sem):
    chrome_options = Options()
    # chrome_options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    while True:
        roll_password = roll+'P'
        driver.get('https://erp.cbit.org.in/')
        if (driver.title) == 'Bees Erp Login':
            username_id = driver.find_element(By.ID,'txtUserName')
            username_id.send_keys(roll_password)
            next_button = driver.find_element(By.ID,'btnNext')
            next_button.click()
            try:
                password = driver.find_element(By.ID,'txtPassword')
                password.send_keys(roll_password)
                submit = driver.find_element(By.ID,'btnSubmit')
                submit.click()
            except:
                print('username is incorrect')
            try:
                studentDashboard = driver.find_element(By.ID,'ctl00_cpStud_lnkStudentMain')
                studentDashboard.click()
                if driver.title == '504 Gateway Time-out':
                    continue
                else:
                    # notification.notify(
                    #     title = 'hello',
                    #     message = 'It has opened',
                    #     timeout = 150
                    # )
                    actions = ActionChains(driver)
                    examination_cell = driver.find_element(By.XPATH,'//button[@class="btnback btn-block" and contains(text(), "Examination Cell")]')
                    actions.move_to_element(examination_cell).perform()
                    marks_details = driver.find_element(By.XPATH,"//a[@id='ctl00_cpHeader_ucStud_LinkButton2']")
                    actions.move_to_element(marks_details).perform()   
                    overall_result = driver.find_element(By.ID,'ctl00_cpHeader_ucStud_lnkOverallResult')
                    overall_result.click()
                    print(driver.title)
                    table = driver.find_element(By.ID,'ctl00_cpStud_grdOverall')
                    rows = table.find_elements(By.TAG_NAME,'tr')
                    row_info = []
                    for row in rows:
                        columns = row.find_elements(By.TAG_NAME,'td')
                        if columns:
                            row_data = [data.text for data in columns]
                            row_info.append(row_data)
                        else:
                            header = row.find_elements(By.TAG_NAME,'th')
                            header_data = [head.text for head in header]
                            row_info.append(header_data)
                    # result = 'SGPA : '+row_info[int(sem)-1][2]+'\n'+'CGPA : '+row_info[int(sem)-1][3]
                    # print(result)
                    driver.quit()
                    break
            except:
                print('web error')
        else:
            continue
    return row_info
def main():
    st.title("Student Information")

    # Input fields
    roll_number = st.text_input("Enter Roll Number")
    semester = st.text_input("Enter Semester")

    # Button to generate the result
    if st.button("Get Result"):
        if roll_number and semester:
            row_info = check_result(roll_number, semester)
            st.write('SGPA : ', row_info[int(semester)-1][2])
            st.write('CGPA : ', row_info[int(semester)-1][3])

        else:
            st.error("Please enter both Roll Number and Semester.")

if __name__ == "__main__":
    main()











