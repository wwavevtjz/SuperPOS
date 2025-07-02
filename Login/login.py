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

class SuperPOS_NewFlowTest(unittest.TestCase):

    # ==================================================================
    # ### ข้อมูลสำหรับ Test Case (แก้ไขได้ที่นี่) ###
    USERNAME = "testwave"
    PASSWORD = "testwave"
    TARGET_MACHINE_ID = "เครื่องรอง"
    #TARGET_MACHINE_ID = "เครื่องหลัก"
    PIN_CODE = "888888" # <--- ใส่รหัส PIN ที่ถูกต้องตรงนี้
    
    # --- ตัวระบุตำแหน่ง (Locators) ---
    LOGOUT_BUTTON_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeButton"
    # ==================================================================

    driver = None
    wait = None

    @classmethod
    def setUpClass(cls):
        """
        [ทำงานครั้งเดียว] ทำการเชื่อมต่อและ Login เพียงครั้งเดียวสำหรับทุก Test Case
        """
        print("\n--- [Session Setup] Starting and Logging In Once ---")
        options = XCUITestOptions()
        options.load_capabilities(config.desired_caps)
        cls.driver = webdriver.Remote("http://127.0.0.1:4728", options=options)
        cls.wait = WebDriverWait(cls.driver, 20)

        try:
            print(" > Checking for an existing logged-in user...")
            logout_button = WebDriverWait(cls.driver, 3).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, cls.LOGOUT_BUTTON_XPATH))
            )
            print(" > Found logged-in user. Clicking logout button...")
            logout_button.click()
            time.sleep(2)
        except TimeoutException:
            print(" > No logged-in user found. Proceeding to login screen.")
            pass
        
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "บัญชีผู้ใช้"))).send_keys(cls.USERNAME)
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        password_field = cls.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "รหัสผ่าน")))
        password_field.clear()
        password_field.send_keys(cls.PASSWORD)
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, cls.TARGET_MACHINE_ID))).click()
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ถัดไป"))).click()
        
        print(" > OK: Reached intermediate screen. Waiting for it to stabilize...")
        time.sleep(2)

        left_button_bar_xpath = "//XCUIElementTypeOther[@name='LeftButtonBar']/XCUIElementTypeOther"
        print(f" > Clicking element with XPath: {left_button_bar_xpath}")
        cls.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, left_button_bar_xpath))
        ).click()
        print(" > OK: Clicked the LeftButtonBar element. Proceeding to PIN screen.")
        
        # === จุดที่อัปเดต: คลิกที่ช่องใส่ PIN ก่อน ===
        print("\n" + "="*50)
        print(">>> Activating PIN entry field...")
        # XPath สำหรับช่องกรอก PIN ที่เป็นจุดๆ
        pin_entry_field_xpath = '//XCUIElementTypeSecureTextField'
        cls.wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, pin_entry_field_xpath))
        ).click()
        print(">>> PIN entry field activated. Entering PIN automatically... <<<")

        for digit in cls.PIN_CODE:
            print(f" > Tapping PIN digit: {digit}")
            pin_button = cls.wait.until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, digit))
            )
            pin_button.click()
            time.sleep(0.2) 
            
        print(">>> PIN entered. Session setup complete. On main screen. <<<")
        time.sleep(3) 

    @classmethod
    def tearDownClass(cls):
        """[ทำงานครั้งเดียว] ปิดการเชื่อมต่อหลังเทสทั้งหมดเสร็จสิ้น"""
        if cls.driver:
            print("\n--- [Session Teardown] Closing the application ---")
            cls.driver.quit()

    def test_new_flow(self):
        """
        Test Case สำหรับ Flow การทำงานใหม่
        """
        print("\n--- Running New Test Flow ---")
        try:
            # หลังจาก Login สำเร็จแล้ว สคริปต์จะอยู่ที่หน้าหลัก
            
            print(" > Starting new test steps from the main screen...")
            
            # คุณสามารถเพิ่มขั้นตอนต่อไปที่ต้องการทดสอบได้ที่นี่
            # ตัวอย่าง:
            # print(" > Now clicking 'สมาชิก' button...")
            # self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "สมาชิก"))).click()
            
            time.sleep(5) 

        except Exception as e:
            error_screenshot_name = "error_new_flow_test.png"
            self.driver.save_screenshot(error_screenshot_name)
            self.fail(f"An exception occurred during the new flow test: {e}")
            
        print("\n--- New Flow Test Completed Successfully ---")


if __name__ == '__main__':
    unittest.main(verbosity=2)
