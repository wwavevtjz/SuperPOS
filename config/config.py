# ชื่อไฟล์: config.py
# ไฟล์สำหรับเก็บค่าการตั้งค่าการเชื่อมต่อ Appium
# แก้ไขค่าเหล่านี้ให้ตรงกับเครื่องและอุปกรณ์ของคุณ

# --- ตั้งค่าการเชื่อมต่อ Appium (Desired Capabilities) ---
desired_caps = {
    "platformName": "iOS",
    "appium:platformVersion": "18.5",
    "appium:deviceName": "ipad wave",
    "appium:udid": "00008030-001169883CDA202E",
    "appium:automationName": "XCUITest",
    "bundleId": "com.gourmet.superpos",
    "appium:wdaLocalPort": 8101,
    "appium:newCommandTimeout": 180,
    # ### สำคัญ! เอา # ออกแล้วใส่ Team ID 10 หลักของคุณ ###
    # "xcodeOrgId": "YOUR_TEAM_ID_HERE",
    # "xcodeSigningId": "Apple Developer"
}
