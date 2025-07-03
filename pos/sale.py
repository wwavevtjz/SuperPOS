# -*- coding: utf-8 -*-
# ชื่อไฟล์: sale.py
# Test Case สำหรับทดสอบ Flow การขายหน้าร้าน (Flow ใหม่สำหรับออเดอร์ทั่วไป)

import unittest
import time
import sys
import os

# --- ส่วนของการจัดการ Path เพื่อให้สามารถ import ไฟล์ config ได้ ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import config  # สมมติว่ามีไฟล์ config.py ที่เก็บ desired_caps

from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class SuperPOS_SaleTest(unittest.TestCase):

    # ==================================================================
    # ### ข้อมูลสำหรับ Test Case (แก้ไขได้ที่นี่) ###
    # ==================================================================
    USERNAME = "foodcen"
    PASSWORD = "foodcen"
    TARGET_MACHINE_ID = "เครื่องรอง"
    PIN_CODE = "000000"
    TARGET_TABLE_NAME = "A1"
    
    # กำหนดประเภทออเดอร์ที่ต้องการทดสอบที่นี่ ("ทั่วไป", "บุฟเฟ่ต์", หรือ "")
    TARGET_ORDER_TYPE = "ทั่วไป" 
    
    # กำหนดเบอร์โทรที่สคริปต์จะกรอกให้
    TARGET_PHONE_NUMBER = "0900000000"

    # กำหนด Action สุดท้ายเป็น "สั่งอาหารทันที"
    FINAL_ACTION = "สั่งอาหารทันที"
    
    # กำหนดชื่อเมนูที่ต้องการค้นหา
    TARGET_MENU_NAME = "เมนูที่ 1"

    # --- ตัวระบุตำแหน่ง (Locators) ---
    LEFT_MENU_BUTTON_ID = "LeftButtonBar"
    CLOSE_POPUP_BUTTON_ID = "Close"
    BACK_BUTTON_ID = "Back"
    LOGOUT_BUTTON_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeButton"
    MAIN_WINDOW_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]"
    PHONE_NUMBER_FIELD_XPATH = '//XCUIElementTypeApplication[@name="Super POS"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeTextField[1]'
    
    # Locators สำหรับปุ่มใหม่
    MOBILE_QR_BUTTON_ID = "Mobile QR"
    ORDER_NOW_BUTTON_ID = "สั่งอาหารทันที"
    QR_CLOSE_BUTTON_ID = "ปิด"
    
    # XPath ของพื้นที่เลื่อนเมนูอาหาร
    MENU_SCROLL_VIEW_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeScrollView"
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
        cls._perform_initial_login()

    @classmethod
    def tearDownClass(cls):
        """[ทำงานครั้งเดียว] ปิดการเชื่อมต่อหลังเทสทั้งหมดเสร็จสิ้น"""
        if cls.driver:
            print("\n--- [Session Teardown] Closing the application ---")
            cls.driver.quit()

    # ==================================================================
    # ### ฟังก์ชันผู้ช่วย (HELPER FUNCTIONS) ###
    # ==================================================================

    @classmethod
    def _perform_initial_login(cls):
        """ฟังก์ชันสำหรับจัดการการ Login และใส่ PIN ทั้งหมด"""
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

        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "บัญชีผู้ใช้"))).send_keys(cls.USERNAME)
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        password_field = cls.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "รหัสผ่าน")))
        password_field.clear()
        password_field.send_keys(cls.PASSWORD)
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, cls.TARGET_MACHINE_ID))).click()
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ถัดไป"))).click()

        print(" > Reached intermediate screen. Finding Left Menu Button...")
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, cls.LEFT_MENU_BUTTON_ID))).click()
        print(f" > OK: Clicked '{cls.LEFT_MENU_BUTTON_ID}'.")

        print(" > Waiting for PIN pad to be ready...")
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "0")))
        print(" > PIN pad is ready. Entering PIN automatically...")
        for digit in cls.PIN_CODE:
            cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, digit))).click()

        print(" > OK: PIN entered. Session setup complete. On main screen.")
        time.sleep(3)

    def _return_to_main_screen(self):
        """
        ฟังก์ชันสำหรับกลับไปยังหน้าจอหลัก (ที่มีปุ่ม 'ขายหน้าร้าน')
        """
        print("\n--- Returning to Main Screen ---")
        for i in range(5):
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "ขายหน้าร้าน"))
                )
                print(f" > Successfully returned to main screen.")
                return
            except TimeoutException:
                try:
                    print(f" > Not on main screen, attempting to go back... (Attempt {i+1})")
                    self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.BACK_BUTTON_ID).click()
                    time.sleep(1.5)
                except Exception:
                    print(f" > '{self.BACK_BUTTON_ID}' button not found, cannot return automatically.")
                    self.fail(f"Could not find '{self.BACK_BUTTON_ID}' button to return to main screen.")
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "ขายหน้าร้าน")))
        except TimeoutException:
            self.fail("Failed to return to the main screen after multiple attempts.")

    def _handle_optional_popup(self):
        """ฟังก์ชันสำหรับตรวจสอบและปิด Pop-up ที่อาจจะขึ้นมา"""
        try:
            print(" > Checking for potential pop-up window...")
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.CLOSE_POPUP_BUTTON_ID))
            )
            print(" > Pop-up found. Clicking close button.")
            close_button.click()
            time.sleep(1)
        except TimeoutException:
            print(" > No pop-up found. Continuing...")

    def _select_table(self, table_name):
        """
        ฟังก์ชันสำหรับเดินทางไปที่โต๊ะ และเลือกโต๊ะเป้าหมาย
        """
        print(f"\n--- Navigating and selecting table '{table_name}' ---")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ขายหน้าร้าน"))).click()
        
        # --- แก้ไข Tab ผังร้านได้ที่นี่ ---
        floor_plan_id = "nidchin\nTab 1 of 6" 
        print(f" > Selecting floor plan '{floor_plan_id.replace('\n', ' ')}'")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, floor_plan_id))).click()
        
        table_xpath = f'//XCUIElementTypeImage[@name="{table_name}"]'
        print(f" > Selecting table '{table_name}'")
        self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, table_xpath))).click()
        print(f" > OK: Selected table '{table_name}'.")

    def _select_order_type(self, order_type):
        """
        ฟังก์ชันสำหรับเลือกประเภทการสั่งอาหาร (ทั่วไป หรือ บุฟเฟ่ต์)
        """
        print(f"\n--- Selecting order type: '{order_type}' ---")
        try:
            order_button = self.wait.until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, order_type))
            )
            order_button.click()
            print(f" > OK: Clicked order type '{order_type}'.")
        except TimeoutException:
            self.fail(f"Could not find the order type button '{order_type}' after selecting the table.")

    def _select_menu_item(self, menu_name):
        """
        <<< แก้ไขแล้ว >>>: ฟังก์ชันสำหรับค้นหาและคลิกเมนูอาหารโดยใช้ "XPath Scanner"
        """
        print(f"\n--- Selecting menu item: '{menu_name}' ---")
        time.sleep(2) # รอให้หน้าเมนูโหลดสมบูรณ์

        try:
            menu_container = self.wait.until(
                EC.presence_of_element_located((AppiumBy.XPATH, self.MENU_SCROLL_VIEW_XPATH))
            )
            print(" > Menu container found. Starting scan...")
        except TimeoutException:
            self.fail("Could not find the menu scroll view.")

        for i in range(15):
            try:
                # <<< แก้ไข >>>: ใช้ XPath เพื่อสแกนหา "ทุกอย่าง" (`*`) ที่อยู่ข้างใน container
                elements = menu_container.find_elements(AppiumBy.XPATH, ".//*")
                print(f" > [Attempt {i+1}] Found {len(elements)} potential elements. Scanning text...")

                for el in elements:
                    # ดึงข้อความจากทุก attribute ที่เป็นไปได้
                    full_text = f"{el.get_attribute('name') or ''} {el.get_attribute('label') or ''} {el.get_attribute('value') or ''}"
                    
                    # ถ้าเจอข้อความที่ต้องการ และ Element นั้นแสดงบนหน้าจอ
                    if menu_name in full_text and el.is_displayed():
                        print(f" > SUCCESS: Found visible menu item with text: '{full_text.strip()}'")
                        el.click()
                        print(f" > OK: Clicked menu item '{menu_name}'.")
                        return # ออกจากฟังก์ชันเมื่อเจอและคลิกแล้ว
                
                print(f" > Menu item not found on this screen. Swiping up...")
                self.driver.execute_script('mobile: swipe', {'elementId': menu_container.id, 'direction': 'up', 'percent': 0.8})
                time.sleep(1.5)

            except Exception as e:
                print(f" > An error occurred during scan: {e}. Swiping to refresh...")
                self.driver.execute_script('mobile: swipe', {'elementId': menu_container.id, 'direction': 'up', 'percent': 0.8})
                time.sleep(1.5)
        
        self.fail(f"Could not find menu item '{menu_name}' after multiple swipes.")

    def _handle_general_order_flow(self, phone_number, final_action, menu_name):
        """
        <<< แก้ไขแล้ว >>>: ฟังก์ชันสำหรับ Flow 'ทั่วไป' โดยเฉพาะ และเลือก Action สุดท้ายได้
        """
        print("\n--- Handling 'General' order flow ---")
        try:
            # 1. หยุดรอให้ผู้ใช้กดจำนวนคนเอง
            print("\n" + "="*50)
            print(">>> SCRIPT PAUSED FOR 5 SECONDS <<<")
            print(">>> PLEASE SELECT THE NUMBER OF PEOPLE ON THE IPAD NOW. <<<")
            time.sleep(5)
            print(">>> Time is up. Resuming script... <<<")

            # 2. กรอกเบอร์โทร (ถ้ามี)
            if phone_number:
                print(f"\n > Entering phone number: {phone_number}")
                phone_field = self.wait.until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, self.PHONE_NUMBER_FIELD_XPATH))
                )
                phone_field.send_keys(phone_number)
                print(f" > OK: Entered phone number '{phone_number}'.")
                
                # 3. คลิกที่หน้าจอเพื่อซ่อนคีย์บอร์ด
                print(" > Clicking main window to dismiss keyboard...")
                main_window = self.wait.until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, self.MAIN_WINDOW_XPATH))
                )
                main_window.click()
                print(" > OK: Clicked main window.")
                time.sleep(0.5)
            else:
                print("\n > Skipping phone number entry (no number provided).")

            # 4. กดปุ่มสุดท้ายตามที่เลือก
            if final_action == "Mobile QR":
                print(" > Finding and clicking 'Mobile QR' button...")
                self.wait.until(
                    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.MOBILE_QR_BUTTON_ID))
                ).click()
                print(" > OK: Clicked 'Mobile QR'.")
                
                print("\n" + "="*50)
                print(">>> SCRIPT PAUSED FOR 15 SECONDS (Displaying QR Code) <<<")
                time.sleep(15)
                print(">>> Time is up. Closing QR Code screen... <<<")

                print(" > Finding and clicking 'Close' button...")
                self.wait.until(
                    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.QR_CLOSE_BUTTON_ID))
                ).click()
                print(" > OK: Clicked 'Close'.")

            elif final_action == "สั่งอาหารทันที":
                print(" > Finding and clicking 'สั่งอาหารทันที' button...")
                self.wait.until(
                    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.ORDER_NOW_BUTTON_ID))
                ).click()
                print(" > OK: Clicked 'สั่งอาหารทันที'.")
                
                # <<< เพิ่มเติม >>>: เรียกใช้ฟังก์ชันเลือกเมนู
                self._select_menu_item(menu_name)

            else:
                print(f" > No final action specified or action '{final_action}' is unknown. Ending flow here.")
            
            time.sleep(1)

        except Exception as e:
            self.fail(f"An error occurred during the 'General' order flow: {e}")

    # ==================================================================
    # ### TEST CASES ###
    # ==================================================================
    
    def test_full_order_flow(self):
        """
        *** แก้ไขแล้ว: ทดสอบ Flow โดยให้ผู้ใช้กดจำนวนคนเอง ***
        """
        print("\n" + "="*50)
        print("### Running Test: Full Order Flow ###")
        print("="*50)
        try:
            self._return_to_main_screen()
            self._handle_optional_popup()
            
            # 1. เดินทางไปเลือกโต๊ะ
            self._select_table(self.TARGET_TABLE_NAME)
            
            if self.TARGET_ORDER_TYPE:
                # 2. ถ้ากำหนดไว้ ให้เลือกประเภทการสั่งอาหาร
                self._select_order_type(self.TARGET_ORDER_TYPE)

                # 3. แยก Flow การทำงานตามประเภทออเดอร์
                if self.TARGET_ORDER_TYPE == "ทั่วไป":
                    # <<< แก้ไข >>>: ส่ง FINAL_ACTION และ TARGET_MENU_NAME เข้าไปในฟังก์ชันด้วย
                    self._handle_general_order_flow(self.TARGET_PHONE_NUMBER, self.FINAL_ACTION, self.TARGET_MENU_NAME)
                # (ส่วนของบุฟเฟ่ต์ยังไม่ได้ใช้งานใน Test Case นี้)

            else:
                print("\n--- Skipping order type selection (no type provided) ---")

            
            print("\n--- Test Completed Successfully ---")
            time.sleep(3) # หยุดรอให้เห็นผลลัพธ์สุดท้าย

        except Exception as e:
            error_screenshot_name = f"error_full_flow_test_{int(time.time())}.png"
            self.driver.save_screenshot(error_screenshot_name)
            print(f" !!! An error occurred. Screenshot saved as {error_screenshot_name} !!!")
            self.fail(f"An exception occurred during the test: {e}")


# --- ส่วนที่ทำให้สามารถรันไฟล์นี้ได้โดยตรง ---
if __name__ == '__main__':
    unittest.main(verbosity=2)
