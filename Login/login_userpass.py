# ชื่อไฟล์: login_test.py
# Test Case สำหรับทดสอบฟังก์ชันการทำงานของหน้า Login โดยเฉพาะ

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

class SuperPOS_LoginFunctionalityTest(unittest.TestCase):

    # ==================================================================
    # ### ข้อมูลสำหรับ Test Case (แก้ไขได้ที่นี่) ###
    USERNAME = "testwave"
    PASSWORD = "testwave"
    TARGET_MACHINE_ID = "เครื่องรอง"
    
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
    NEXT_BUTTON_ID = "ถัดไป"
    # ==================================================================

    driver = None
    wait = None

    @classmethod
    def setUpClass(cls):
        """[ทำงานครั้งเดียว] ทำการเชื่อมต่อกับ Appium Server เพียงครั้งเดียว"""
        print("\n--- [Session Setup] Starting Appium Session for Login Tests ---")
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

    def test_01_username_field_typing(self):
        """Test Case: ตรวจสอบการพิมพ์ในช่อง 'บัญชีผู้ใช้'"""
        print("\n--- Running Test 01: Username Field Typing ---")
        try:
            username_field = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID)))
            
            print(" > Verifying keyboard appearance...")
            username_field.click()
            self.assertTrue(self.driver.is_keyboard_shown(), "FAIL: Keyboard did not appear.")
            print(" > OK: Keyboard is shown.")
            
            test_inputs = {"Numbers Only": self.NUMBERS_ONLY, "Special Chars": self.SPECIAL_CHARS}
            for description, test_value in test_inputs.items():
                print(f" > Testing input: {description}...")
                username_field.clear()
                username_field.send_keys(test_value)
                self.assertEqual(username_field.get_attribute("value"), test_value)
                print(f" > OK: Field correctly accepts '{description}'.")
            
            self.driver.hide_keyboard()
        except Exception as e:
            self.fail(f"An exception occurred during username typing test: {e}")

    def test_02_username_field_copy_paste_clear(self):
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

    def test_03_navigate_to_password_screen(self):
        """Test Case: ตรวจสอบการไปหน้ากรอกรหัสผ่านด้วย Username ที่ถูกต้อง"""
        print("\n--- Running Test 03: Navigate to Password Screen ---")
        try:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID))).send_keys(self.USERNAME)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.LOGIN_BUTTON_ID))).click()
            
            password_field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.PASSWORD_FIELD_ID)))
            self.assertTrue(password_field.is_displayed(), "FAIL: Did not navigate to password screen.")
            print(" > OK: Successfully navigated to password screen.")
        except Exception as e:
            self.fail(f"An exception occurred during navigation to password screen: {e}")

    def test_04_password_field_functionality(self):
        """Test Case: ตรวจสอบฟังก์ชันของช่อง 'รหัสผ่าน'"""
        print("\n--- Running Test 04: Password Field Functionality ---")
        try:
            # ไปที่หน้ากรอกรหัสผ่านก่อน
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID))).send_keys(self.USERNAME)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.LOGIN_BUTTON_ID))).click()
            
            password_field = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.PASSWORD_FIELD_ID)))
            
            print(" > Verifying secure text entry...")
            password_field.send_keys("test")
            self.assertNotEqual(password_field.get_attribute("value"), "test")
            print(" > OK: Password text is obscured.")
            
            print(" > Testing Paste & Clear functionality...")
            self.driver.set_clipboard_text(self.PASTE_STRING)
            password_field.clear()
            password_field.send_keys(self.PASTE_STRING)
            self.assertTrue(password_field.get_attribute("value"))
            print(" > OK: Paste works correctly.")
            
            password_field.clear()
            self.assertFalse(password_field.get_attribute("value"))
            print(" > OK: Clear works correctly.")
            self.driver.hide_keyboard()
        except Exception as e:
            self.fail(f"An exception occurred during password field test: {e}")

    def test_05_full_login_flow(self):
        """Test Case: ทดสอบ Flow การ Login ที่ถูกต้องทั้งหมด"""
        print("\n--- Running Test 05: Full Successful Login Flow ---")
        try:
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.USERNAME_FIELD_ID))).send_keys(self.USERNAME)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.LOGIN_BUTTON_ID))).click()
            
            password_field = self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.PASSWORD_FIELD_ID)))
            password_field.send_keys(self.PASSWORD)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.LOGIN_BUTTON_ID))).click()
            
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.TARGET_MACHINE_ID))).click()
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.NEXT_BUTTON_ID))).click()
            
            pin_pad_element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "1")))
            self.assertTrue(pin_pad_element.is_displayed(), "FAIL: Did not navigate to PIN screen.")
            print(" > OK: Successfully navigated to PIN screen.")
        except Exception as e:
            self.fail(f"An exception occurred during the full login flow test: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
