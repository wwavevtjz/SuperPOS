# ชื่อไฟล์: login_test.py

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
    # "xcodeOrgId": "XXXXXXXXXX",
    # "xcodeSigningId": "Apple Developer"
}



class SuperPOSTest(unittest.TestCase):

    # ==================================================================
    # ### 2. ตั้งค่า Test Case ตรงนี้ ###
    USERNAME = "foodcen"
    PASSWORD = "foodcen"  # <--- แก้ไขรหัสผ่านจริงที่นี่
    PIN_CODE = "000000"                # <--- แก้ไข PIN 6 หลักจริงที่นี่
    TARGET_MACHINE_ID = "เครื่องหลัก"     # <--- ตัวเลือก: "เครื่องหลัก" หรือ "เครื่องรอง"
    # ==================================================================

    def setUp(self):
        options = XCUITestOptions()
        options.load_capabilities(desired_caps)
        self.driver = webdriver.Remote("http://127.0.0.1:4728", options=options)
        print("\nAppium session started.")

    def test_full_login_and_setup_flow(self):
        print(f"--- Starting Test: Full Login and Setup ('{self.TARGET_MACHINE_ID}') ---")
        wait = WebDriverWait(self.driver, 20)

        try:
            # --- ขั้นตอนที่ 1-6 เหมือนเดิม ---
            print("Step 1: Finding and typing username...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "บัญชีผู้ใช้"))).send_keys(self.USERNAME)
            print(f" > OK: Typed username '{self.USERNAME}'.")

            print("Step 2: Clicking 'Login' to go to password screen...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
            print(" > OK: Clicked 'Login' button.")

            print("Step 3: Finding and typing password...")
            password_field = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "รหัสผ่าน")))
            password_field.clear()
            password_field.send_keys(self.PASSWORD)
            print(" > OK: Typed password.")
            
            print("Step 4: Clicking 'Login' button again to confirm...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
            print(" > OK: Clicked final 'Login' button.")

            print(f"Step 5: Finding and clicking '{self.TARGET_MACHINE_ID}' button...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.TARGET_MACHINE_ID))).click()
            print(f" > OK: Clicked '{self.TARGET_MACHINE_ID}' button.")
            
            print("Step 6: Finding and clicking 'Next' button...")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ถัดไป"))).click()
            print(" > OK: Clicked 'Next' button.")

            # --- ขั้นตอนที่ 7: กรอก PIN (วิธีที่ถูกต้อง: ช่องเดียว) ---
            print("Step 7: Finding the single PIN text field and typing...")
            pin_field_xpath = "//XCUIElementTypeTextField"
            pin_field = wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, pin_field_xpath))
            )
            print(f" > OK: Found the single PIN field.")
            
            # ส่ง PIN ทั้งหมด 6 หลักเข้าไปในครั้งเดียว
            pin_field.send_keys(self.PIN_CODE)
            print(f" > OK: Sent PIN '{self.PIN_CODE}' to the field.")
            
            # --- ขั้นตอนที่ 8: คลิกปุ่ม "ยืนยัน" ---
            print("Step 8: Waiting for 'Confirm' button to be clickable...")
            confirm_button = wait.until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ยืนยัน"))
            )
            confirm_button.click()
            print(" > OK: Clicked 'Confirm' button.")

        except Exception as e:
            error_screenshot_name = "error_screenshot.png"
            self.driver.save_screenshot(error_screenshot_name)
            print(f"\n !!! TEST FAILED with an error: {e}")
            print(f" >>> Screenshot saved as {error_screenshot_name}")
            self.fail(f"An exception occurred during the test: {e}")

        print("\n--- Test Completed Successfully ---")
        print("Waiting 5 seconds to observe the final screen...")
        time.sleep(5) 

    def tearDown(self):
        if self.driver:
            self.driver.quit()
            print("Appium session closed.")

if __name__ == '__main__':
    unittest.main(verbosity=2)