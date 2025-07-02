# ชื่อไฟล์: login_fail_test.py
# Test Case สำหรับทดสอบกรณี Login ด้วยรหัสผ่านที่ไม่ถูกต้อง

import unittest
import time
import sys
import os

# --- ส่วนของการจัดการ Path เพื่อให้สามารถ import ไฟล์ config ได้ ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import config

from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SuperPOS_LoginFailTest(unittest.TestCase):

    # ==================================================================
    # ### ข้อมูลสำหรับ Test Case (แก้ไขได้ที่นี่) ###
    USERNAME = "testwave"
    INVALID_PASSWORD = "wrongpassword" # รหัสผ่านที่ไม่ถูกต้องสำหรับทดสอบ
    
    # --- ตัวระบุตำแหน่ง (Locators) ---
    USERNAME_FIELD_ID = "บัญชีผู้ใช้"
    LOGIN_BUTTON_ID = "เข้าสู่ระบบ"
    PASSWORD_FIELD_ID = "รหัสผ่าน"
    SHOW_PASSWORD_ICON_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther"
    BACK_BUTTON_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeButton"
    # ==================================================================

    def setUp(self):
        """ทำการเชื่อมต่อกับ Appium Server และไปที่หน้ากรอกรหัสผ่าน"""
        print("\n--- [Test Setup] Starting a new test session ---")
        options = XCUITestOptions()
        options.load_capabilities(config.desired_caps)
        self.driver = webdriver.Remote("http://127.0.0.1:4728", options=options)
        self.wait = WebDriverWait(self.driver, 20)
        
        # นำทางไปยังหน้ากรอกรหัสผ่าน
        print(" > Navigating to password screen for the test...")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID))).send_keys(self.USERNAME)
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.LOGIN_BUTTON_ID))).click()
        self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.PASSWORD_FIELD_ID)))
        print(" > Ready on password screen.")

    def tearDown(self):
        """ปิดการเชื่อมต่อหลังเทสเสร็จ"""
        if self.driver:
            self.driver.quit()
        print("--- [Test Teardown] Session finished ---")

    def test_invalid_password_flow(self):
        """
        Test Case: ตรวจสอบ Flow ทั้งหมดเมื่อใส่รหัสผ่านไม่ถูกต้อง
        """
        print("\n--- Running Test: Invalid Password Flow ---")
        try:
            # --- Part 1: กรอกรหัสผ่านผิดและพยายาม Login ---
            print("Part 1: Entering incorrect password and attempting login...")
            password_field = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.PASSWORD_FIELD_ID)))
            
            print(f" > Entering incorrect password: {self.INVALID_PASSWORD}")
            password_field.clear()
            password_field.send_keys(self.INVALID_PASSWORD)

            print(" > Clicking 'เข้าสู่ระบบ' button...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.LOGIN_BUTTON_ID))).click()
            
            # --- Part 2: ตรวจสอบ Alert ---
            print("\nPart 2: Verifying alert presence...")
            alert_message_id = "username หรือ รหัสผ่านไม่ถูกต้อง"
            alert_message = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, alert_message_id))
            )
            self.assertTrue(alert_message.is_displayed(), "FAIL: Invalid password alert did not appear.")
            print(" > OK: Invalid password alert is displayed correctly.")
            
            # --- Part 3: ทดสอบปุ่มลูกตาในขณะที่ Alert แสดงอยู่ ---
            print("\nPart 3: Testing show/hide icon while alert is present...")
            
            # 3.1 กดปุ่มลูกตาเพื่อแสดงรหัสผ่าน
            print(" > Action: Tapping show password icon...")
            show_password_icon = self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.SHOW_PASSWORD_ICON_XPATH)))
            show_password_icon.click()
            time.sleep(1)
            print(" > OK: Tapped show password icon.")

            # 3.2 กดปุ่มลูกตาอีกครั้งเพื่อซ่อน
            print(" > Action: Tapping hide password icon...")
            hide_password_icon = self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.SHOW_PASSWORD_ICON_XPATH)))
            hide_password_icon.click()
            time.sleep(1)
            print(" > OK: Tapped hide password icon.")
           
            # === จุดที่อัปเดต: ลบขั้นตอนการกดปิด Alert ออก ===
            # --- Part 4: รอให้ Alert หายไปเอง ---
            print("\nPart 4: Waiting for alert to disappear automatically...")
            # รอสักครู่เพื่อให้เราสังเกตว่า Alert หายไปเอง
            time.sleep(3) 
            
            # ตรวจสอบว่า Alert หายไปแล้วจริงๆ
            is_alert_gone = self.wait.until(
                EC.invisibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, alert_message_id))
            )
            self.assertTrue(is_alert_gone, "FAIL: Alert did not disappear as expected.")
            print(" > OK: Alert has disappeared.")


        except Exception as e:
            error_screenshot_name = "error_invalid_password_test.png"
            self.driver.save_screenshot(error_screenshot_name)
            self.fail(f"An exception occurred during the invalid password test: {e}")

        print("\n--- Invalid Password Test Completed Successfully ---")
        time.sleep(3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
