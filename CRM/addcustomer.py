import unittest
import time
import datetime
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import config

from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class SuperPOS_FullFlowTest(unittest.TestCase):

    USERNAME = "testwave"
    PASSWORD = "testwave"
    TARGET_MACHINE_ID = "เครื่องรอง"
    MANUAL_WAIT_TIME = 5

    # --- ข้อมูลสำหรับกรอกฟอร์มสมาชิก ---
    NEW_MEMBER_FULLNAME = "สมชาย ทดสอบ"
    NEW_MEMBER_NICKNAME = "คิม"
    BIRTH_YEAR = "2003" 
    BIRTH_MONTH = "Jun" 
    BIRTH_DAY = "21" 
    GENDER_SELECTION = "ชาย" # ตัวเลือก: "ชาย", "หญิง", "ไม่ระบุ"
    NEW_MEMBER_EMAIL = "somchai.test@gmail.com" # เพิ่มข้อมูลอีเมล
    NEW_MEMBER_ADDRESS = "365/2 นนทบุรี 1120"
    NEW_MEMBER_PHONE = "0998285433"
    # ==================================================================

    def setUp(self):
        """ทำการเชื่อมต่อกับ Appium Server"""
        options = XCUITestOptions()
        options.load_capabilities(config.desired_caps)
        self.driver = webdriver.Remote("http://127.0.0.1:4728", options=options)
        print("\n--- Starting Full Flow Test ---")

    def tearDown(self):
        """ปิดการเชื่อมต่อหลังเทสเสร็จ"""
        if self.driver:
            self.driver.quit()
        print("--- Test Finished ---\n")

    def _scroll_to_element(self, accessibility_id, direction='up', container_element=None, max_swipes=25):
        """
        ฟังก์ชันสำหรับเลื่อนหน้าจอ โดยจะเลื่อนบน container ที่ระบุเพื่อความแม่นยำ
        """
        for i in range(max_swipes):
            try:
                # ลองหา element ก่อน ถ้าเจอให้ return เลย
                element = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, accessibility_id))
                )
                print(f" > Found element '{accessibility_id}' after {i+1} swipes.")
                return element
            except TimeoutException:
                
                swipe_args = {'direction': direction}
                if container_element:
                    print(f" > Element '{accessibility_id}' not visible, swiping on specific container (direction: {direction})... (Attempt {i+1}/{max_swipes})")
                    swipe_args['elementId'] = container_element.id
                else:
                    print(f" > Element '{accessibility_id}' not visible, swiping on whole screen (direction: {direction})... (Attempt {i+1}/{max_swipes})")

                try:
                    self.driver.execute_script("mobile: swipe", swipe_args)
                    time.sleep(0.5)
                except Exception as e:
                    print(f" > ERROR during swipe: {e}")
                    raise e

        raise TimeoutException(f"Element with ID '{accessibility_id}' not found after {max_swipes} swipes.")


    def test_full_process_from_login_to_add_member_form(self):
        """Test Case สำหรับ Flow การทำงานที่ถูกต้องทั้งหมด"""
        wait = WebDriverWait(self.driver, 20)

        try:
            # --- ส่วนที่ 1, 2, 3 (Login และการนำทาง) ---
            print("Part 1: Performing login and setup...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "บัญชีผู้ใช้"))).send_keys(self.USERNAME)
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
            password_field = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "รหัสผ่าน")))
            password_field.clear()
            password_field.send_keys(self.PASSWORD)
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.TARGET_MACHINE_ID))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ถัดไป"))).click()
            print(" > OK: Reached PIN screen.")
            print("\n" + "="*50)
            print(f">>> SCRIPT PAUSED FOR {self.MANUAL_WAIT_TIME} SECONDS <<<")
            print(">>> PLEASE ENTER PIN ON THE IPAD NOW. <<<")
            time.sleep(self.MANUAL_WAIT_TIME)
            print(">>> Time is up. Resuming script... <<<")
            print("Part 3: Navigating to Add Member form...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "สมาชิก"))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เพิ่มสมาชิก"))).click()
            print(" > OK: Reached Add Member form.")
            time.sleep(1)

            # --- ส่วนที่ 4: กรอกข้อมูล ---
            print("Part 4: Filling out new member details...")
            full_name_predicate = "type == 'XCUIElementTypeTextField' AND (name CONTAINS 'ชื่อ - นามสกุล' OR label CONTAINS 'ชื่อ - นามสกุล')"
            full_name_field = wait.until(EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, full_name_predicate)))
            full_name_field.click(); time.sleep(0.5); full_name_field.send_keys(self.NEW_MEMBER_FULLNAME)
            print(f" > OK: Typed Full Name '{self.NEW_MEMBER_FULLNAME}'.")
            self.driver.hide_keyboard()
            time.sleep(1)

            nickname_predicate = "type == 'XCUIElementTypeTextField' AND (name CONTAINS 'ชื่อเล่น' OR label CONTAINS 'ชื่อเล่น')"
            nickname_field = wait.until(EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, nickname_predicate)))
            nickname_field.click(); time.sleep(0.5); nickname_field.send_keys(self.NEW_MEMBER_NICKNAME)
            print(f" > OK: Typed Nickname '{self.NEW_MEMBER_NICKNAME}'.")
            self.driver.hide_keyboard()
            time.sleep(1)

            # --- เลือกวันเกิด ---
            print(" > Attempting to select birthday by swiping on the CORRECT container...")
            birthday_field_id = "วันเกิด\n*"
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, birthday_field_id))).click()
            time.sleep(1)
            print(f" > Setting Date to: {self.BIRTH_DAY} {self.BIRTH_MONTH} {self.BIRTH_YEAR}")

            # --- คลิกปุ่มเลือกปี ---
            year_selector_xpath = "(//XCUIElementTypeButton[@name='Select year'])[2]"
            wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, year_selector_xpath))).click()
            time.sleep(1)

            # --- ตรรกะการตัดสินใจเลื่อนหน้าจอ ---
            target_year_int = int(self.BIRTH_YEAR)
            current_year = datetime.datetime.now().year
            scroll_direction = 'down' if target_year_int < current_year else 'up'
            print(f" > System's current year is {current_year}. Target year is {target_year_int}. Swiping '{scroll_direction}' to find it.")

            # --- หา Container ที่จะใช้เลื่อน ---
            year_container_xpath = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]"
            year_container = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, year_container_xpath)))
            
            # เรียกใช้ฟังก์ชันเลื่อนหน้าจอพร้อมส่ง container ไปด้วย
            year_element = self._scroll_to_element(self.BIRTH_YEAR, direction=scroll_direction, container_element=year_container)
            year_element.click()

            # --- คลิกปุ่มเลือกเดือน และเลือกเดือนที่ต้องการ ---
            month_selector_xpath = "(//XCUIElementTypeButton[@name='Select year'])[1]"
            wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, month_selector_xpath))).click()
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.BIRTH_MONTH))).click()
            
            print(" > Waiting for calendar to re-render...")
            time.sleep(2)

            # --- เลือกวัน ---
            print(f" > Selecting StaticText element that starts with: '{self.BIRTH_DAY},'")
            day_predicate = f"type == 'XCUIElementTypeStaticText' AND name BEGINSWITH '{self.BIRTH_DAY},'"
            day_element = wait.until(EC.presence_of_element_located((AppiumBy.IOS_PREDICATE, day_predicate)))
            
            location = day_element.location
            size = day_element.size
            tap_x = location['x'] + (size['width'] / 2)
            tap_y = location['y'] + (size['height'] / 2)

            print(f" > Tapping on the found element's center coordinates ({int(tap_x)}, {int(tap_y)}) with 'mobile: tap'")
            self.driver.execute_script("mobile: tap", {"x": int(tap_x), "y": int(tap_y)})
            
            print(" > OK: Birthday selected.")

            print(" > Clicking OK button to close the date picker...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "OK"))).click()
            print(" > OK: Closed date picker.")
            time.sleep(1)

            # --- เลือกเพศ ---
            print(f" > Selecting gender: '{self.GENDER_SELECTION}'")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.GENDER_SELECTION))).click()
            print(" > OK: Gender selected.")

            # --- กรอก E-mail ---
            print(f" > Typing email: '{self.NEW_MEMBER_EMAIL}'")
            email_predicate = "type == 'XCUIElementTypeTextField' AND (name CONTAINS 'E-mail' OR label CONTAINS 'E-mail')"
            email_field = wait.until(EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, email_predicate)))
            email_field.click(); time.sleep(0.5)
            email_field.send_keys(self.NEW_MEMBER_EMAIL)
            print(" > OK: Email typed.")
            self.driver.hide_keyboard()
            time.sleep(1)

            # --- กรอกที่อยู่ ---
            print(f" > Typing Address: '{self.NEW_MEMBER_ADDRESS}'")
            address_predicate = "type == 'XCUIElementTypeTextField' AND (name CONTAINS 'ที่อยู่' OR label CONTAINS 'ที่อยู่')"
            address_field = wait.until(EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, address_predicate)))
            address_field.click(); time.sleep(0.5)
            address_field.send_keys(self.NEW_MEMBER_ADDRESS)
            print(" > OK: Address typed.")
            self.driver.hide_keyboard()
            time.sleep(1)

            # --- กรอกเบอร์โทรศัพท์ ---
            print(f" > Typing Phone: '{self.NEW_MEMBER_PHONE}'")
            phone_predicate = "type == 'XCUIElementTypeTextField' AND (name CONTAINS 'เบอร์โทรศัพท์' OR label CONTAINS 'เบอร์โทรศัพท์')"
            phone_field = wait.until(EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, phone_predicate)))
            phone_field.click(); time.sleep(0.5)
            phone_field.send_keys(self.NEW_MEMBER_PHONE)
            print(" > OK: Phone Typed.")
            self.driver.hide_keyboard()
            time.sleep(1)

            # === จุดที่อัปเดต: กดปุ่มบันทึก ===
            print(" > Clicking Save button...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "บันทึก"))).click()
            print(" > OK: Save button clicked.")


        except TimeoutException as e:
            error_screenshot_name = "error_timeout_screenshot.png"
            self.driver.save_screenshot(error_screenshot_name)
            print(f"\n !!! TEST FAILED: {e.msg}")
            print(f" >>> Screenshot saved as {error_screenshot_name}")
            self.fail(f"A TimeoutException occurred: {e.msg}")
        except Exception as e:
            error_screenshot_name = "error_exception_screenshot.png"
            self.driver.save_screenshot(error_screenshot_name)
            print(f"\n !!! TEST FAILED with an unexpected error: {e}")
            print(f" >>> Screenshot saved as {error_screenshot_name}")
            self.fail(f"An exception occurred during the test: {e}")

        print("\n--- Test Flow Completed Successfully ---")
        time.sleep(5)

if __name__ == '__main__':
    unittest.main(verbosity=2)
