# ชื่อไฟล์: full_test_suite.py

import unittest
import time
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 1. ตั้งค่าการเชื่อมต่อ (Desired Capabilities) ---
desired_caps = {
    "platformName": "iOS",
    "appium:platformVersion": "18.5",
    "appium:deviceName": "ipad wave",
    "appium:udid": "00008030-001169883CDA202E",
    "appium:automationName": "XCUITest",
    "bundleId": "com.gourmet.superpos",
    "appium:wdaLocalPort": 8101,
    "appium:newCommandTimeout": 180, # ขยายเวลา Timeout เป็น 3 นาที
    # ### สำคัญ! เอา # ออกแล้วใส่ Team ID 10 หลักของคุณ ###
    # "xcodeOrgId": "YOUR_TEAM_ID_HERE",
    # "xcodeSigningId": "Apple Developer"
}

class SuperPOSLoginTestSuite(unittest.TestCase):

    # ==================================================================
    # ### 2. ตั้งค่าข้อมูลสำหรับ Test Cases ทั้งหมด ###
    #
    VALID_USERNAME = "foodcen"
    VALID_PASSWORD = "foodcen"  # <--- แก้ไขรหัสผ่านจริงที่นี่
    INVALID_PASSWORD = "wrong_password_1234"
    TARGET_MACHINE_ID = "เครื่องหลัก"
    MANUAL_WAIT_TIME = 10
    # ข้อมูลสำหรับ Error Message (จากที่คุณเคยหามา)
    LOGIN_ERROR_ID = "username หรือ รหัสผ่านไม่ถูกต้อง"
    EXPECTED_LOGIN_ERROR_TEXT = "username หรือ รหัสผ่านไม่ถูกต้อง"
    # ==================================================================

    def setUp(self):
        """ฟังก์ชันนี้จะทำงาน 'ก่อน' ทุกๆ test_..."""
        options = XCUITestOptions()
        options.load_capabilities(desired_caps)
        self.driver = webdriver.Remote("http://127.0.0.1:4728", options=options)
        print(f"\n--- Starting Test: {self._testMethodName} ---")
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """ฟังก์ชันนี้จะทำงาน 'หลัง' ทุกๆ test_..."""
        if self.driver:
            self.driver.quit()
        print(f"--- Finished Test: {self._testMethodName} ---\n")

    def _perform_login_actions(self, username, password):
        """ฟังก์ชันช่วย: ทำขั้นตอนการกรอกข้อมูลและกด Login"""
        print(" > Performing login actions...")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "บัญชีผู้ใช้"))).send_keys(username)
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        password_field = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "รหัสผ่าน")))
        password_field.clear()
        if password:
            password_field.send_keys(password)
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        print(" > Login attempt submitted.")


    def test_A_login_failed_with_wrong_password(self):
        """Test Case 'ไม่ผ่าน': ทดสอบการ Login ด้วยรหัสผ่านที่ผิด (Automated 100%)"""
        print("Objective: Login with invalid password should show an error message.")
        self._perform_login_actions(self.VALID_USERNAME, self.INVALID_PASSWORD)
        
        print("Verifying that an error message is displayed...")
        error_element = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.LOGIN_ERROR_ID))
        )
        self.assertTrue(error_element.is_displayed(), "Error message did not appear for wrong password.")
        self.assertEqual(error_element.text, self.EXPECTED_LOGIN_ERROR_TEXT)
        print(f" > OK: Test Passed. Correct error message was shown.")


    def test_B_login_successful_with_manual_pin(self):
        """Test Case 'ผ่าน': ทดสอบการ Login สำเร็จ โดยมีคนช่วยกด PIN"""
        print("Objective: Successfully log in and get to the post-login screen.")
        
        # ขั้นตอนการ Login ที่ควรจะผ่าน
        self._perform_login_actions(self.VALID_USERNAME, self.VALID_PASSWORD)
        
        # ขั้นตอนที่เหลือ
        print("Continuing with post-login steps...")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.TARGET_MACHINE_ID))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ถัดไป"))).click()
        print(" > OK: Reached PIN screen.")
        
        # หยุดรอให้คนกด PIN
        print("\n" + "="*50)
        print(f">>> SCRIPT PAUSED FOR {self.MANUAL_WAIT_TIME} SECONDS <<<")
        print(">>> PLEASE ENTER PIN AND CONFIRM ON THE IPAD NOW. <<<")
        time.sleep(self.MANUAL_WAIT_TIME)
        print(">>> Time is up. Resuming to end the test. <<<")
        print("="*50 + "\n")
        

if __name__ == '__main__':
    unittest.main(verbosity=2)