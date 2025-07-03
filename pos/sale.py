# -*- coding: utf-8 -*-
# ชื่อไฟล์: sale.py
# Test Case สำหรับทดสอบ Flow การขายหน้าร้าน (เวอร์ชันดึงข้อมูลจากฐานข้อมูล)

import unittest
import time
import sys
import os

# --- ส่วนของการจัดการ Path เพื่อให้สามารถ import ไฟล์อื่นๆ ได้ ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# --- Import ที่จำเป็น ---
import config
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- Import ฐานข้อมูลและลิสต์เมนูที่จะสั่ง ---
from menu_data import MENU_DATABASE

class SuperPOS_SaleTest(unittest.TestCase):

    # ==================================================================
    # ### ข้อมูลสำหรับ Test Case และ Locators ###
    # ==================================================================
    USERNAME = "foodcen"
    PASSWORD = "foodcen"
    TARGET_MACHINE_ID = "เครื่องรอง"
    PIN_CODE = "000000"
    TARGET_TABLE_NAME = "A12"
    TARGET_ORDER_TYPE = "ทั่วไป" 
    TARGET_PHONE_NUMBER = "0987654321"
    FINAL_ACTION = "สั่งอาหารทันที"

    # ใส่แค่ "ชื่อ" ของเมนูที่ต้องการสั่งในรอบนี้
    MENUS_TO_ORDER = [
        "ยำปลาป๋อง",
        "a ri ka to",
        "ต้มยำกุ้ง",
    ]

    # --- Locators ---
    LEFT_MENU_BUTTON_ID = "LeftButtonBar"
    CLOSE_POPUP_BUTTON_ID = "Close"
    BACK_BUTTON_ID = "Back"
    LOGOUT_BUTTON_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeButton"
    MAIN_WINDOW_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]"
    SELL_AT_STORE_BUTTON_ID = "ขายหน้าร้าน"
    FLOOR_PLAN_ID = "nidchin\nTab 1 of 6"
    PHONE_NUMBER_FIELD_XPATH = '//XCUIElementTypeApplication[@name="Super POS"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeTextField[1]'
    ORDER_NOW_BUTTON_ID = "สั่งอาหารทันที"
    MENU_SCROLL_VIEW_XPATH = "//XCUIElementTypeApplication[@name='Super POS']/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther[2]/XCUIElementTypeScrollView"
    ADD_TO_CART_BUTTON_ID = "ใส่ตะกร้า"
    # ==================================================================

    driver = None
    wait = None

    @classmethod
    def setUpClass(cls):
        print("\n--- [Session Setup] Starting Test Suite ---")
        options = XCUITestOptions()
        options.load_capabilities(config.desired_caps)
        cls.driver = webdriver.Remote("http://127.0.0.1:4728", options=options)
        cls.wait = WebDriverWait(cls.driver, 20)
        cls._perform_initial_login()

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            print("\n--- [Session Teardown] Closing the application ---")
            cls.driver.quit()

    @classmethod
    def _perform_initial_login(cls):
        print("\n--- Performing Initial Login ---")
        try:
            logout_button = WebDriverWait(cls.driver, 3).until(EC.element_to_be_clickable((AppiumBy.XPATH, cls.LOGOUT_BUTTON_XPATH)))
            logout_button.click()
        except TimeoutException: pass
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "บัญชีผู้ใช้"))).send_keys(cls.USERNAME)
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        password_field = cls.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "รหัสผ่าน")))
        password_field.clear()
        password_field.send_keys(cls.PASSWORD)
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, cls.TARGET_MACHINE_ID))).click()
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ถัดไป"))).click()
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, cls.LEFT_MENU_BUTTON_ID))).click()
        cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "0")))
        for digit in cls.PIN_CODE:
            cls.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, digit))).click()
        time.sleep(3)

    def _return_to_main_screen(self):
        for _ in range(5):
            try:
                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, self.SELL_AT_STORE_BUTTON_ID)))
                return
            except TimeoutException:
                try: self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.BACK_BUTTON_ID).click(); time.sleep(1.5)
                except Exception: self.fail("Could not find back button.")
        self.fail("Failed to return to the main screen.")

    def _handle_optional_popup(self):
        try:
            close_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.CLOSE_POPUP_BUTTON_ID)))
            close_button.click()
        except TimeoutException: pass

    def _select_table(self, table_name):
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.SELL_AT_STORE_BUTTON_ID))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.FLOOR_PLAN_ID))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, f'//XCUIElementTypeImage[@name="{table_name}"]'))).click()

    def _select_order_type(self, order_type):
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, order_type))).click()

    def _click_menu_by_position(self, menu_name, position):
        print(f"\n--- Clicking menu '{menu_name}' at Row: {position['row']}, Col: {position['col']} ---")
        try:
            menu_container = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH, self.MENU_SCROLL_VIEW_XPATH)))
            print(" > Menu container found.")
        except TimeoutException: 
            self.fail("Could not find menu scroll view.")
        
        location = menu_container.location
        size = menu_container.size
        
        # สมมติว่ามี 4 คอลัมน์
        col_width = size['width'] / 4
        
        # <<< แก้ไข >>>: ใช้ค่า Y-coordinate และ row_height ที่ได้จากการวิเคราะห์
        # เพื่อความแม่นยำสูงสุด
        start_y = 181  # Y-coordinate ของแถวแรก
        row_height = 220 # ความสูงของแต่ละแถว (คำนวณจาก 401 - 181)

        tap_x = location['x'] + (col_width * (position['col'] - 0.5))
        # คำนวณ Y-coordinate ของแถวเป้าหมาย
        tap_y = start_y + (row_height * (position['row'] - 1))
        
        print(f" > Using fixed Start Y: {start_y}, Row Height: {row_height}")
        print(f" > Tapping at calculated coordinates: X={int(tap_x)}, Y={int(tap_y)}")
        
        try:
            self.driver.execute_script('mobile: tap', {'x': int(tap_x), 'y': int(tap_y)})
            print(f" > OK: Tap action performed for '{menu_name}'.")
        except Exception as e: 
            self.fail(f"Failed to tap for '{menu_name}'. Error: {e}")

    def _add_item_to_cart(self):
        print(" > Checking for 'ใส่ตะกร้า' button...")
        try:
            short_wait = WebDriverWait(self.driver, 3)
            add_to_cart_button = short_wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.ADD_TO_CART_BUTTON_ID)))
            add_to_cart_button.click()
            print(" > OK: Found and clicked 'ใส่ตะกร้า'.")
            time.sleep(1.5) 
        except TimeoutException:
            print(" > INFO: 'ใส่ตะกร้า' button not found. Assuming item was added directly.")
            
    def _handle_general_order_flow(self, phone_number, final_action, menus_to_order):
        print("\n--- Handling 'General' order flow ---")
        print("\n" + "="*50)
        print(">>> SCRIPT PAUSED FOR 5 SECONDS <<<")
        print(">>> PLEASE SELECT THE NUMBER OF PEOPLE ON THE IPAD NOW. <<<")
        time.sleep(5)
        print(">>> Time is up. Resuming script... <<<")

        if phone_number:
            print(f"\n > Entering phone number: {phone_number}")
            phone_field = self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.PHONE_NUMBER_FIELD_XPATH)))
            phone_field.send_keys(phone_number)
            self.wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, self.MAIN_WINDOW_XPATH))).click()
            time.sleep(0.5)
        
        if final_action == "สั่งอาหารทันที":
            print(" > Finding and clicking 'สั่งอาหารทันที' button...")
            self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.ORDER_NOW_BUTTON_ID))).click()
            print(" > OK: Clicked 'สั่งอาหารทันที'.")
            
            print("\n--- Starting to order multiple items ---")
            for menu_name in menus_to_order:
                menu_position = MENU_DATABASE.get(menu_name)
                if not menu_position:
                    self.fail(f"Menu name '{menu_name}' not found in MENU_DATABASE.")
                
                self._click_menu_by_position(menu_name, menu_position)
                self._add_item_to_cart()
            
            print("\n--- All items have been added to the cart. ---")

    def test_order_flow(self):
        print("\n" + "="*50)
        print("### Running Test: Multiple Items Order Flow ###")
        print("="*50)
        try:
            self._return_to_main_screen()
            self._handle_optional_popup()
            self._select_table(self.TARGET_TABLE_NAME)
            
            if self.TARGET_ORDER_TYPE:
                self._select_order_type(self.TARGET_ORDER_TYPE)
                if self.TARGET_ORDER_TYPE == "ทั่วไป":
                    self._handle_general_order_flow(
                        self.TARGET_PHONE_NUMBER, 
                        self.FINAL_ACTION, 
                        self.MENUS_TO_ORDER
                    )
            
            print("\n--- Test Completed Successfully ---")
            time.sleep(5)

        except Exception as e:
            error_screenshot_name = f"error_test_{int(time.time())}.png"
            self.driver.save_screenshot(error_screenshot_name)
            self.fail(f"An exception occurred during the test: {e}")

if __name__ == '__main__':
    unittest.main(verbosity=2)
