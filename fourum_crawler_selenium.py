import time, requests, re
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

# Initialization
start_time = time.time()
driver = webdriver.Chrome()
driver.get('')
driver.maximize_window()
login_element = driver.find_element_by_name('username')
passW_element = driver.find_element_by_name('password')
login_button_element = driver.find_element_by_name('loginsubmit')
sec_quest_element = driver.find_element_by_name('questionid')
sec_quest_element_select = Select(sec_quest_element)  # drop down menu element
sec_ans_element = driver.find_element_by_name('answer')
login_element.clear()
login_element.send_keys('dbg3177')
passW_element.clear()
passW_element.send_keys('Aa000000-')
sec_quest_element_select.select_by_value('5')  # selecting drop down menu options
sec_ans_element.send_keys('sah')
login_button_element.click()
time.sleep(5)

# Global variables
main_tab = driver.current_window_handle
attachment_xpath_1 = '/html/body/center/p[1]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr[2]/td/p[2]/a[2]'
attachment_xpath_2 = '/html/body/center/p[1]/table[2]/tbody/tr[5]/td[2]/table/tbody/tr[2]/td/p[2]/a[2]'
attachment_xpath_3 = '/html/body/center/p[1]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr[2]/td/p[2]/b/a[2]'
attachment_xpath_4 = '/html/body/center/p[1]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr[2]/td/p[3]/a[2]'
attachment_xpath_list = [attachment_xpath_1, attachment_xpath_2, attachment_xpath_3, attachment_xpath_4]
page_number = 1
filter_list = []
end_date = '2016-10-22'


def main():
    url_link = ''

    for i in range(1, 10):  # loop to which page
        print('page', i)
        driver.get(url_link + str(i))
        time.sleep(3)
        if i == 1:
            xpath_list = []
            for row in range(43, 45):  # 21,45
                xpath_list_item = '/html/body/center/table[7]/tbody/tr[' + str(row) + ']/td[2]/a'
                xpath_list.append(xpath_list_item)
            get_attachments_or_links(xpath_list)
        else:
            xpath_list_2 = []
            for row in range(40, 43):  # threads number in one page 3, 43
                xpath_list_item = '/html/body/center/table[7]/tbody/tr[' + str(row) + ']/td[2]/a'
                xpath_list_2.append(xpath_list_item)
            # for i in xpath_list_2: print(i)
            get_attachments_or_links(xpath_list_2)


def get_attachments_or_links(xpath_list):
    global page_number
    for item in xpath_list:
        # get the post date
        a = driver.find_element_by_xpath(item).text
        b = str(int(item[-4]) + 1) + ']'
        c = item
        xpath_date = c.replace(c[-4:], b)
        d = driver.find_element_by_xpath(xpath_date).text

        filter_flag = 0

        for i in filter_list:
            if i.lower() in a.lower():
                filter_flag = 1
                break

        if d[-10:] not in end_date:
            if filter_flag == 0:
                print(page_number, a)
                page_number += 1
                driver.find_element_by_xpath(item).send_keys(Keys.CONTROL + Keys.ENTER)
                print(item)
                driver.switch_to_window(driver.window_handles[1])  # switch to new tab
                time.sleep(2)
                attachment_counter = 0
                for att_xpath in attachment_xpath_list:
                    try:
                        driver.find_element_by_xpath(att_xpath).click()  # may add a loop here
                        time.sleep(2)
                        driver.close()
                        driver.switch_to_window(main_tab)  # Switch focus back to main tab
                        break
                    except NoSuchElementException:
                        print('attachment_xpath', attachment_counter, 'not found', att_xpath)
                        attachment_counter += 1
                        pass
                if attachment_counter == len(attachment_xpath_list):
                    print('thank op')
                    thank_op()
        else:
            total_time = time.time() - start_time
            print('total time is', total_time)
            quit()


def thank_op():  # too many nested try except
    thanks_button_xpath = '/html/body/center/p[1]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr[2]/td/blockquote/font/a/img'
    hidden_link_xpath_list = []
    for i in range(1, 10):
        hidden_link_xpath = '/html/body/center/p[1]/table[2]/tbody/tr[4]/td[2]/table/tbody/tr[2]/td/blockquote/a[' + str(i) + ']'
        hidden_link_xpath_list.append(hidden_link_xpath)

    try:
        driver.find_element_by_xpath(thanks_button_xpath).click()
        print('found thank you button and click')
        time.sleep(3)
        driver.find_element_by_name('submitpass').click()
        print('found submit button and click')
        time.sleep(3)
        print(driver.current_url)
        save_hidden_links(hidden_link_xpath_list)

    except NoSuchElementException:  # bug: if post never thanked, the hidden links while be looped twice
        print('already thanked', '\n', driver.current_url)
        save_hidden_links(hidden_link_xpath_list)


def save_hidden_links(hidden_link_xpath_list):
    file = open('C:/Users/dbg316/Downloads/hiddenlink.txt', 'a')
    for i in hidden_link_xpath_list:
        try:
            a = driver.find_element_by_xpath(i)
            file.writelines(a.get_attribute('href') + '\n')
            print(a.get_attribute('href'))
        except NoSuchElementException:
            print('No more hidden links')
            break
    file.close()
    print('wrote to hiddenlink.txt')
    driver.close()
    driver.switch_to_window(main_tab)

main()
