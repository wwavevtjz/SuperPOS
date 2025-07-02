# ชื่อไฟล์: login_user.py
# Test Case สำหรับทดสอบฟังก์ชันการทำงานของช่อง "บัญชีผู้ใช้" (Username)

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

class SuperPOS_UsernameFieldTest(unittest.TestCase):

    # ==================================================================
    # ### ข้อมูลสำหรับ Test Case (แก้ไขได้ที่นี่) ###
    INVALID_USERNAME = "invalid_user_for_testing"
    
    # --- ข้อมูลสำหรับทดสอบช่องกรอก ---
    TEXT_ONLY = "testuser"
    NUMBERS_ONLY = "1234567890"
    SPECIAL_CHARS = "!@#$%^&*()"
    PASTE_STRING = "textToPaste"
    
    # --- ตัวระบุตำแหน่ง (Locators) ---
    LOGOUT_BUTTON_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeButton"
    USERNAME_FIELD_ID = "บัญชีผู้ใช้"
    LOGIN_BUTTON_ID = "เข้าสู่ระบบ"
    PASSWORD_FIELD_ID = "รหัสผ่าน"
    # ==================================================================

    driver = None
    wait = None

    @classmethod
    def setUpClass(cls):
        """[ทำงานครั้งเดียว] ทำการเชื่อมต่อกับ Appium Server เพียงครั้งเดียว"""
        print("\n--- [Session Setup] Starting Appium Session for Username Field Tests ---")
        options = XCUITestOptions()
        options.load_capabilities(config.desired_caps)
        cls.driver = webdriver.Remote("http://127.0.0.1:4728", options=options)
        cls.wait = WebDriverWait(cls.driver, 20)

    @classmethod
    def tearDownClass(cls):
        """[ทำงานครั้งเดียว] ปิดการเชื่อมต่อหลังเทสทั้งหมดเสร็จสิ้น"""
        if cls.driver:
            print("\n--- [Session Teardown] Closing the application ---")
            cls.driver.quit()

    def setUp(self):
        """[ก่อนแต่ละเทส] ตรวจสอบและกลับไปที่หน้า Login เสมอ"""
        print(f"\n--- [Test Setup] Preparing for {self._testMethodName} ---")
        try:
            logout_button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, self.LOGOUT_BUTTON_XPATH))
            )
            print(" > Found logged-in user. Clicking logout button...")
            logout_button.click()
            self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID)))
        except TimeoutException:
            print(" > No logged-in user found. Already on login screen.")
            pass
        
        # ตรวจสอบให้แน่ใจว่าเห็นช่อง "บัญชีผู้ใช้" ก่อนเริ่มเทส
        self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID)))
        print(" > Ready on login screen.")

    def tearDown(self):
        """[หลังแต่ละเทส] ไม่ต้องทำอะไรเป็นพิเศษ"""
        print(f"--- [Test Teardown] Finished {self._testMethodName} ---")
        pass

    def test_01_field_interaction(self):
        """Test Case: ตรวจสอบการพิมพ์ในช่อง 'บัญชีผู้ใช้'"""
        print("\n--- Running Test 01: Username Field Typing and Keyboard ---")
        try:
            username_field = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID)))
            
            print(" > Verifying keyboard appearance...")
            username_field.click()
            self.assertTrue(self.driver.is_keyboard_shown(), "FAIL: Keyboard did not appear.")
            print(" > OK: Keyboard is shown.")
            
            test_inputs = {"Text Only": self.TEXT_ONLY, "Numbers Only": self.NUMBERS_ONLY, "Special Chars": self.SPECIAL_CHARS}
            for description, test_value in test_inputs.items():
                print(f" > Testing input: {description}...")
                username_field.clear()
                username_field.send_keys(test_value)
                self.assertEqual(username_field.get_attribute("value"), test_value)
                print(f" > OK: Field correctly accepts '{description}'.")
            
            self.driver.hide_keyboard()
        except Exception as e:
            self.fail(f"An exception occurred during username typing test: {e}")

    def test_02_copy_paste_clear(self):
        """Test Case: ตรวจสอบการคัดลอก, วาง, และลบในช่อง 'บัญชีผู้ใช้'"""
        print("\n--- Running Test 02: Username Field Copy-Paste-Clear ---")
        try:
            username_field = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID)))
            
            print(" > Testing Copy & Paste functionality...")
            self.driver.set_clipboard_text(self.PASTE_STRING)
            username_field.clear()
            username_field.send_keys(self.PASTE_STRING)
            self.assertEqual(username_field.get_attribute("value"), self.PASTE_STRING)
            print(" > OK: Paste works correctly.")

            print(" > Testing Clear functionality...")
            username_field.clear()
            self.assertFalse(username_field.get_attribute("value"))
            print(" > OK: Clear works correctly.")
        except Exception as e:
            self.fail(f"An exception occurred during username copy-paste test: {e}")

    def test_03_navigate_with_invalid_username(self):
        """Test Case: ตรวจสอบว่าเมื่อใส่ username ผิด ก็ยังไปหน้ากรอกรหัสผ่าน"""
        print("\n--- Running Test 03: Navigate to Password with Invalid Username ---")
        try:
            print(f" > Entering incorrect username: {self.INVALID_USERNAME}")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID))).send_keys(self.INVALID_USERNAME)
            
            print(" > Clicking 'เข้าสู่ระบบ' button...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.LOGIN_BUTTON_ID))).click()

            print(" > Verifying navigation to password screen...")
            password_field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.PASSWORD_FIELD_ID)))
            self.assertTrue(password_field.is_displayed(), "FAIL: Password field is not visible after entering invalid username.")
            print(" > OK: Correctly navigated to the password screen even with invalid username.")
        except Exception as e:
            self.fail(f"An exception occurred during navigation with invalid username test: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
