# ชื่อไฟล์: find_coords.py
# สคริปต์พิเศษสำหรับช่วยหาพิกัด x, y บนหน้าจอ

import time
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- กรอกข้อมูลของคุณตรงนี้ ---
desired_caps = {
    "platformName": "iOS",
    "appium:platformVersion": "18.5",
    "appium:deviceName": "ipad wave",
    "appium:udid": "00008030-001169883CDA202E",
    "appium:automationName": "XCUITest",
    "bundleId": "com.gourmet.superpos",
    "appium:wdaLocalPort": 8101,
    # "xcodeOrgId": "YOUR_TEAM_ID_HERE",
    # "xcodeSigningId": "Apple Developer"
}
USERNAME = "foodcen"
PASSWORD = "foodcen" # <--- แก้ไขรหัสผ่านจริงที่นี่
TARGET_MACHINE_ID = "เครื่องหลัก"
APPIUM_SERVER_URL = "http://127.0.0.1:4728"
# --------------------------------

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinate captured: x={x}, y={y}")

def find_coordinates():
    driver = None
    try:
        options = XCUITestOptions().load_capabilities(desired_caps)
        driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        print("\nAppium session started. Navigating to PIN screen...")
        wait = WebDriverWait(driver, 20)

        # --- รัน Flow เดิมจนถึงก่อนหน้า PIN ---
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "บัญชีผู้ใช้"))).send_keys(USERNAME)
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        password_field = wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "รหัสผ่าน")))
        password_field.clear()
        password_field.send_keys(PASSWORD)
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "เข้าสู่ระบบ"))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, TARGET_MACHINE_ID))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "ถัดไป"))).click()
        print(" > OK: Reached PIN screen.")
        time.sleep(3)

        # --- ถ่ายรูปและแสดงผล ---
        screenshot_png = driver.get_screenshot_as_png()
        image = Image.open(BytesIO(screenshot_png))
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        window_name = "CLICK ON BUTTONS TO GET COORDS (Press any key on keyboard to quit)"
        cv2.imshow(window_name, image_cv)
        cv2.setMouseCallback(window_name, mouse_callback)
        
        print("\n" + "="*60)
        print("A window with your iPad's screenshot has opened.")
        print("Please CLICK on the number buttons (0, 1) and the 'Confirm' button.")
        print("The coordinates will be printed in this terminal below.")
        print("Press any key on the IMAGE WINDOW when you are done.")
        print("="*60 + "\n")
        
        cv2.waitKey(0)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
        cv2.destroyAllWindows()
        print("\nSession closed. Process finished.")

if __name__ == '__main__':
    find_coordinates()