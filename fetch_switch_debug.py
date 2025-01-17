import requests
import pandas as pd
import time

# Initialization of Variables
inventory = []
backup_path = "C:/Backups/SwitchConfigBackup/" + pd.Timestamp.now().strftime("%Y%m%d")
user = "switch_backup"
password = "JkkTxw7Pv9K5AsRbnFGAb5UuBVZgzBuAcmxRRUBhmLb5VeLPvbg6nh8XY9hyt3qw"
email_title = "Switch Backup Configuration Failed!"

# Function to get device list from ISE Server
def get_device_list(user, password):
    session = requests.Session()
    session.headers.update({
        "Cache-Control": "max-age=0",
        "Origin": "https://mtlhksvrpise.macroviewhk.com",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Referer": "https://mtlhksvrpise.macroviewhk.com/admin/login.jsp",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6"
    })

    print("Starting device list retrieval...")

    try:
        print("Sending initial GET request to login page...")
        session.get("https://mtlhksvrpise.macroviewhk.com/admin/login.jsp?mid=external_auth_msg#administration/administration_networkresources/administration_networkresources_devices/networkdevices", verify=False)

        login_data = {
            'username': user,
            'password': password,
            'authType': 'Internal',
            'rememberme': 'on',
            'name': user,
            'password': password,
            'authType': '',
            'newPassword': '',
            'destinationURL': '',
            'xeniaUrl': '',
            'locale': 'en',
            'hasSelectedLocale': 'false'
        }

        print("Sending POST request to login...")
        login_response = session.post("https://mtlhksvrpise.macroviewhk.com/admin/LoginAction.do", data=login_data, verify=False)
        print("Login response status code:", login_response.status_code)
        print("Login response content:", login_response.text)
        print("Cookies after login:", session.cookies)

        # Adding a delay to avoid rate limiting
        time.sleep(2)

        print("Sending GET request to retrieve device list...")
        response = session.get("https://mtlhksvrpise.macroviewhk.com/admin/NetworkDevicesLPInputAction.do?command=restjson&start=0&count=1000&sort=name", verify=False)
        print("Device list response status code:", response.status_code)
        print("Device list response headers:", response.headers)
        print("Device list response content:", response.text)

        try:
            devices = response.json()
            print("API Response:", devices)
        except ValueError as e:
            print("Failed to parse JSON response:", e)
            return

        print("Extracting Objects")

        for item in devices['items']:
            if "Switch" in item['deviceType']:
                inventory.append({
                    'Hostname': item['name'],
                    'IP': item['deviceIpMask'].split("/")[0],
                    'DeviceType': item['deviceType']
                })

        print("Inventory:", inventory)
        print("Device list retrieval completed.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Call the function
get_device_list(user, password)

# Create a DataFrame with the inventory data
df = pd.DataFrame(inventory)

# Export the inventory to a CSV file
df.to_csv("C:/Users/matthewchs/Downloads/SwitchInventory.csv", index=False)

print("Inventory exported to CSV file.")
