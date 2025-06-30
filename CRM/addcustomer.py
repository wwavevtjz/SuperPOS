# ชื่อไฟล์: full_happy_path_test_updated.py

import unittest
import time
import datetime
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- 1. ตั้งค่าการเชื่อมต่อ (Desired Capabilities) ---
desired_caps = {
    "platformName": "iOS",
    "appium:platformVersion": "18.5",
    "appium:deviceName": "ipad wave",
    "appium:udid": "00008030-001169883CDA202E",
    "appium:automationName": "XCUITest",
    "bundleId": "com.gourmet.superpos",
    "appium:wdaLocalPort": 8101,
    "appium:newCommandTimeout": 180,
    # "xcodeOrgId": "YOUR_TEAM_ID_HERE",
    # "xcodeSigningId": "Apple Developer"
}

class SuperPOS_FullFlowTest(unittest.TestCase):

    # ==================================================================
    # ### 2. ตั้งค่า Test Case ของคุณตรงนี้ ###
    #
    USERNAME = "foodcen"
    PASSWORD = "foodcen"
    TARGET_MACHINE_ID = "เครื่องรอง"
    MANUAL_WAIT_TIME = 10

    # --- ข้อมูลสำหรับกรอกฟอร์มสมาชิก ---
    NEW_MEMBER_FULLNAME = "สมชาย ใจดี ทดสอบ"
    NEW_MEMBER_NICKNAME = "ชาย"
    # อัปเดตข้อมูลให้ตรงกับการทดสอบล่าสุด
    BIRTH_YEAR = "2005" 
    BIRTH_MONTH = "Jun" 
    BIRTH_DAY = "19" 
    # ==================================================================

    def setUp(self):
        """ทำการเชื่อมต่อกับ Appium Server"""
        options = XCUITestOptions()
        options.load_capabilities(desired_caps)
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
            nickname_predicate = "type == 'XCUIElementTypeTextField' AND (name CONTAINS 'ชื่อเล่น' OR label CONTAINS 'ชื่อเล่น')"
            nickname_field = wait.until(EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, nickname_predicate)))
            nickname_field.click(); time.sleep(0.5); nickname_field.send_keys(self.NEW_MEMBER_NICKNAME)
            print(f" > OK: Typed Nickname '{self.NEW_MEMBER_NICKNAME}'.")

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

            # === จุดที่อัปเดต: ใช้ Predicate ที่ถูกต้องในการเลือกวัน ===
            print(f" > Selecting StaticText element that starts with: '{self.BIRTH_DAY},'")
            # Predicate นี้จะหา element ที่เป็น StaticText, และมี name (accessibility id) ที่ขึ้นต้นด้วยเลขวันตามด้วยคอมม่า
            day_predicate = f"type == 'XCUIElementTypeStaticText' AND name BEGINSWITH '{self.BIRTH_DAY},'"
            wait.until(EC.element_to_be_clickable((AppiumBy.IOS_PREDICATE, day_predicate))).click()
            print(" > OK: Birthday selected.")

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
