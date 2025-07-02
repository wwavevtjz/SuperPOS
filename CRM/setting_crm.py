# ชื่อไฟล์: settings_test.py
# Test Case สำหรับทดสอบการตั้งค่าเงื่อนไขการสะสมแต้ม

import unittest
import time
import datetime
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SuperPOS_SettingsTest(unittest.TestCase):

    # ==================================================================
    # ### ข้อมูลสำหรับ Test Case (แก้ไขได้ที่นี่) ###
    USERNAME = "foodcen"
    PASSWORD = "foodcen"
    TARGET_MACHINE_ID = "เครื่องรอง"
    MANUAL_WAIT_TIME = 5
    
    # --- ข้อมูลสำหรับกรอกในเงื่อนไขที่ 1 ---
    REWARD_BAHT_PER_POINT = "100" # จำนวนเงินบาท
    REWARD_POINTS_TO_GIVE = "15"   # จำนวนแต้มที่จะได้

    # --- ข้อมูลสำหรับกรอกในเงื่อนไขที่ 2 (สะสมตามยอดรวม) ---
    REWARD_TIER_1_MIN = "101"
    REWARD_TIER_1_MAX = "150"
    REWARD_TIER_1_PERCENT = "15"
   
    # --- ข้อมูลสำหรับกรอกในเงื่อนไขที่ 3 (สะสมตามจำนวนเมนู) ---
    REWARD_ITEM_COUNT = "2"   # จำนวนเมนู
    REWARD_ITEM_POINTS = "10" # จำนวนแต้มที่จะได้
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
            logout_button_xpath = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeButton"
            logout_button = WebDriverWait(cls.driver, 3).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, logout_button_xpath))
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
        print(" > OK: Reached PIN screen.")
        print("\n" + "="*50)
        print(f">>> SCRIPT PAUSED FOR {cls.MANUAL_WAIT_TIME} SECONDS <<<")
        print(">>> PLEASE ENTER PIN ON THE IPAD NOW. <<<")
        time.sleep(cls.MANUAL_WAIT_TIME)
        print(">>> Time is up. Session setup complete. On main screen. <<<")

    @classmethod
    def tearDownClass(cls):
        """[ทำงานครั้งเดียว] ปิดการเชื่อมต่อหลังเทสทั้งหมดเสร็จสิ้น"""
        if cls.driver:
            print("\n--- [Session Teardown] Closing the application ---")
            cls.driver.quit()

    def _fill_if_different(self, field_element, new_value):
        """
        ฟังก์ชันผู้ช่วย: ตรวจสอบค่าในช่องกรอก ถ้าไม่ตรงให้ลบแล้วพิมพ์ใหม่
        Returns: True ถ้ามีการเปลี่ยนแปลง, False ถ้าค่าถูกต้องอยู่แล้ว
        """
        change_was_made = False
        current_value = field_element.get_attribute("value")
        if str(current_value) != str(new_value):
            print(f" > Value is '{current_value}', changing to '{new_value}'.")
            field_element.clear()
            field_element.send_keys(new_value)
            change_was_made = True
        else:
            print(f" > Value is already correct: '{current_value}'. Skipping.")
        return change_was_made
            
    def _select_if_not_selected(self, element_to_check):
        """
        ฟังก์ชันผู้ช่วย: ตรวจสอบว่าเงื่อนไขถูกเลือกไว้แล้วหรือยัง ถ้ายังให้กดเลือก
        Returns: True ถ้ามีการเปลี่ยนแปลง, False ถ้าเลือกไว้อยู่แล้ว
        """
        change_was_made = False
        if element_to_check.get_attribute("value") != '1':
            print(f" > Condition '{element_to_check.text[:20]}...' is not selected. Clicking to select.")
            element_to_check.click()
            change_was_made = True
        else:
            print(f" > Condition '{element_to_check.text[:20]}...' is already selected. Skipping click.")
        return change_was_made

    def test_all_reward_settings_in_sequence(self):
        """Test Case สำหรับทดสอบการตั้งค่าเงื่อนไขการสะสมแต้มทั้งหมดต่อเนื่องกัน"""
        print("\n--- Running Main Test: All Reward Settings in Sequence ---")
        try:
            # --- Part 1: นำทางไปยังหน้าแก้ไข ---
            print("Part 1: Navigating to Edit Settings page...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "สมาชิก"))).click()
            print(" > Clicked 'สมาชิก'")
            print("\n" + "="*50)
            print(">>> SCRIPT PAUSED FOR 5 SECONDS <<<")
            print(">>> PLEASE CLICK THE 'ตั้งค่า' BUTTON ON THE IPAD NOW. <<<")
            time.sleep(5)
            print(">>> Time is up. Resuming script... <<<")
            edit_button_xpath = "(//XCUIElementTypeStaticText[@name='แก้ไข'])[1]"
            
            # --- Part 2: ทดสอบเงื่อนไขที่ 1 (สะสมตามยอด) ---
            print("\nPart 2: Configuring 'Reward by Amount' (Condition 1)...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, edit_button_xpath))).click()
            print(" > Entered edit mode for Condition 1.")
            time.sleep(1)

            changes_made_cond1 = False
            reward_type_1_id = "สะสมตามยอดทุกๆ...บาท\n(ตัวอย่าง ซื้อครบทุกๆ 100 บาท ได้ 10 แต้ม)\nบาท\n = \nแต้ม"
            reward_type_1_element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, reward_type_1_id)))
            if self._select_if_not_selected(reward_type_1_element):
                changes_made_cond1 = True
            time.sleep(1)
            
            # === จุดที่อัปเดต: ใช้วิธีค้นหาช่องกรอกทั้งหมดแล้วนับลำดับ ===
            all_fields_cond1 = self.driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeTextField")
            self.assertGreaterEqual(len(all_fields_cond1), 2, "FAIL: Could not find at least 2 text fields for Condition 1.")
            
            print(f" > Setting reward rule: every {self.REWARD_BAHT_PER_POINT} Baht = {self.REWARD_POINTS_TO_GIVE} points.")
            if self._fill_if_different(all_fields_cond1[0], self.REWARD_BAHT_PER_POINT):
                changes_made_cond1 = True
            self.driver.hide_keyboard()
            
            if self._fill_if_different(all_fields_cond1[1], self.REWARD_POINTS_TO_GIVE):
                changes_made_cond1 = True
            self.driver.hide_keyboard()
            
            if changes_made_cond1:
                print(" > Changes were made for Condition 1. Clicking 'ยืนยัน'.")
                self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ยืนยัน"))).click()
            else:
                print(" > No changes needed for Condition 1. Clicking 'ยกเลิก'.")
                self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ยกเลิก"))).click()
            print(" > OK: Exited edit mode.")
            time.sleep(2)

            # --- Part 3: ทดสอบเงื่อนไขที่ 2 (สะสมตามยอดรวม) ---
            print("\nPart 3: Configuring 'Reward by Total Amount' (Condition 2)...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, edit_button_xpath))).click()
            print(" > Re-entered edit mode for Condition 2.")
            time.sleep(1)

            changes_made_cond2 = False
            reward_type_2_id = "สะสมตามยอดรวม\n(ตัวอย่าง ซื้อ 0-100 บาท ได้แต้ม 12 % ของยอดซื้อ, ซื้อ 101-1000 บาท ได้แต้ม 20 % ของยอดซื้อ, ซื้อ 1001 ขึ้นไป ได้แต้ม 25% ของยอดซื้อ)\n - \nบาท\n = \n%"
            reward_type_2_element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, reward_type_2_id)))
            if self._select_if_not_selected(reward_type_2_element):
                changes_made_cond2 = True
            time.sleep(1)

            all_fields_cond2 = self.driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeTextField")
            tier1_fields = all_fields_cond2[2:5] # สมมติว่าช่องของเงื่อนไขนี้เริ่มที่ index 2
            
            if self._fill_if_different(tier1_fields[0], self.REWARD_TIER_1_MIN): changes_made_cond2 = True
            if self._fill_if_different(tier1_fields[1], self.REWARD_TIER_1_MAX): changes_made_cond2 = True
            if self._fill_if_different(tier1_fields[2], self.REWARD_TIER_1_PERCENT): changes_made_cond2 = True
            self.driver.hide_keyboard()
            print(" > OK: Tier 1 checked/configured.")
            
            if changes_made_cond2:
                print(" > Changes were made for Condition 2. Clicking 'ยืนยัน'.")
                self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ยืนยัน"))).click()
            else:
                print(" > No changes needed for Condition 2. Clicking 'ยกเลิก'.")
                self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ยกเลิก"))).click()
            print(" > OK: Exited edit mode.")
            time.sleep(2)

            # --- Part 4: ทดสอบเงื่อนไขที่ 3 (สะสมตามจำนวนเมนู) ---
            print("\nPart 4: Configuring 'Reward by Item Count' (Condition 3)...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, edit_button_xpath))).click()
            print(" > Re-entered edit mode for Condition 3.")
            time.sleep(1)

            changes_made_cond3 = False
            reward_type_3_id = "สะสมตามจำนวนเมนูที่สั่งซื้อ\n(ตัวอย่าง ซื้อเมนู 2 แก้ว ใน 1 บิล ได้คะแนน 10 แต้ม)\nรายการ\n = \nแต้ม"
            reward_type_3_element = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, reward_type_3_id)))
            if self._select_if_not_selected(reward_type_3_element):
                changes_made_cond3 = True
            time.sleep(1)

            all_fields_cond3 = self.driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeTextField")
            # สมมติว่าช่องของเงื่อนไขนี้คือ 2 ช่องสุดท้าย
            fields_in_cond3 = all_fields_cond3[-2:]
            self.assertEqual(len(fields_in_cond3), 2, "FAIL: Could not find the last 2 text fields for Condition 3.")
            
            if self._fill_if_different(fields_in_cond3[0], self.REWARD_ITEM_COUNT): changes_made_cond3 = True
            self.driver.hide_keyboard()
            
            if self._fill_if_different(fields_in_cond3[1], self.REWARD_ITEM_POINTS): changes_made_cond3 = True
            self.driver.hide_keyboard()
            
            if changes_made_cond3:
                print(" > Changes were made for Condition 3. Clicking 'ยืนยัน'.")
                self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ยืนยัน"))).click()
            else:
                print(" > No changes needed for Condition 3. Clicking 'ยกเลิก'.")
                self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ยกเลิก"))).click()
            print(" > OK: Exited edit mode.")

        except Exception as e:
            error_screenshot_name = "error_all_settings_test.png"
            self.driver.save_screenshot(error_screenshot_name)
            self.fail(f"An exception occurred during the test: {e}")
            
        print("\n--- All Settings Tests Completed Successfully ---")
        time.sleep(3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
