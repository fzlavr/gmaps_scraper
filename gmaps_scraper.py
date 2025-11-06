import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIG ===
# INPUT_FILE = "outlet_nolatlong.csv"
INPUT_FILE = "mini_outlet_loc.csv"
OUTPUT_FILE = "mini_outlet_loc_SLM.csv"
CHROMEDRIVER_PATH = "chromedriver.exe"  # adjust path if needed
SAVE_INTERVAL = 50  # save progress every 50 rows
WAIT_LOAD = 5  # seconds to wait after search

# === SETUP SELENIUM ===
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument("--headless")  # comment this out if you want to see browser
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# === LOAD INPUT DATA ===
df = pd.read_csv(INPUT_FILE)

# === RESUME MODE (if output exists) ===
if os.path.exists(OUTPUT_FILE):
    print(f"Found existing output file: {OUTPUT_FILE}")
    saved_df = pd.read_csv(OUTPUT_FILE)
    completed = saved_df["LATITUDE"].notna().sum()
    print(f"Resuming from row {completed}...")
    df = df.iloc[completed:].copy()
    latitudes = list(saved_df["LATITUDE"])
    longitudes = list(saved_df["LONGITUDE"])
else:
    latitudes = []
    longitudes = []

# === MAIN LOOP ===
for i, row in df.iterrows():
    index = len(latitudes) + 1
    name = str(row["NAMAOUTLET"])
    address = str(row["ALAMAT"])
    query = f"{name}, {address}"
    # query = f"{name}"

    print(f"\nSearching {index}/{len(df)}: {query}")
    driver.get("https://www.google.com/maps")
    time.sleep(3)

    try:
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)
        time.sleep(WAIT_LOAD)

        # === HANDLE MULTIPLE RESULTS ===
        try:
            first_result = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href^="https://www.google.com/maps/place"]'))
            )
            first_result.click()
            time.sleep(WAIT_LOAD)
        except TimeoutException:
            pass  # no multiple result list, continue

        current_url = driver.current_url
        lat, lng = None, None      
        if "!3d" in current_url and "!4d" in current_url:
            try:
                lat = float(current_url.split("!3d")[1].split("!4d")[0])
                lng = float(current_url.split("!4d")[1].split("!")[0])
            except:
                pass

        print(f"Found: ({lat}, {lng})")
        latitudes.append(lat)
        longitudes.append(lng)

    except Exception as e:
        print(f"Error on {query}: {e}")
        latitudes.append(None)
        longitudes.append(None)

    # Auto-save progress
    if index % SAVE_INTERVAL == 0 or index == len(df):
        temp_df = pd.read_csv(INPUT_FILE)
        temp_df["LATITUDE"] = pd.Series(latitudes + [None] * (len(temp_df) - len(latitudes)))
        temp_df["LONGITUDE"] = pd.Series(longitudes + [None] * (len(temp_df) - len(longitudes)))
        temp_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
        print(f"Progress saved ({index}/{len(df)})")

    time.sleep(2)

# === FINAL SAVE ===
final_df = pd.read_csv(INPUT_FILE)
final_df["LATITUDE"] = latitudes
final_df["LONGITUDE"] = longitudes
final_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
print("\nDone! All results saved to:", OUTPUT_FILE)

driver.quit()

