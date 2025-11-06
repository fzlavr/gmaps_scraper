# 🗺️ Google Maps Latitude & Longitude Scraper

This Python script automates the process of retrieving latitude and longitude coordinates from Google Maps for a list of outlet names. It uses **Selenium WebDriver** to simulate browser interaction and **Pandas** to manage input and output CSV data.  

---

## 📋 Features
- Automatically searches outlet names on Google Maps.  
- Extracts latitude and longitude directly from the URL.  
- Handles multiple search results by clicking the first item.  
- Supports resume mode (continues from where the last run stopped).  
- Periodically saves progress to prevent data loss.  

---

## ⚙️ Requirements

Before running this script, ensure that you have the following installed:

### 1. Python
Ensure Python 3.8 or higher is installed on your system.  
You can verify this by running:
```bash
python --version
```

### 2. Python Libraries
Install the required dependencies using:
```bash
pip install pandas selenium
```

### 3. Google Chrome & ChromeDriver
The script requires **Google Chrome** and **ChromeDriver**.  

#### • Check your Chrome version
Open Chrome and visit:
```
chrome://settings/help
```

#### • Download matching ChromeDriver
Visit the [official ChromeDriver page](https://chromedriver.chromium.org/downloads) and download the version corresponding to your Chrome browser.  

Place the `chromedriver.exe` file in the same directory as the script, or specify its path in:
```python
CHROMEDRIVER_PATH = "chromedriver.exe"
```

---

## 🧾 Input and Output Files

- **Input file**:  
  A CSV file containing outlet names.  
  Default:
  ```
  INPUT_FILE = "unfinished_outlets.csv"
  ```
  The CSV must include a column named `NAMAOUTLET`.

- **Output file**:  
  The resulting CSV file with latitude and longitude columns added.  
  Default:
  ```
  OUTPUT_FILE = "unfinished_outlets_SLM.csv"
  ```

---

## ▶️ How to Run

1. Place your input CSV file in the same folder as the script.  
2. Open a terminal or command prompt in the directory containing `gmaps_scraper.py`.  
3. Run the script:
   ```bash
   python gmaps_scraper.py
   ```
4. The browser will open and start processing each outlet.  
5. The script will save progress every 50 rows (default) and create the output CSV file.

---

## ⚠️ Notes
- The script uses Selenium automation and may be slowed by Google Maps’ dynamic loading.  
- You can enable **headless mode** (to run without opening a browser window) by uncommenting this line:
  ```python
  # chrome_options.add_argument("--headless")
  ```
- Avoid performing excessive queries in a short time to prevent temporary blocking by Google.

---

## ✅ Example Output
The resulting CSV file will include two new columns:
| NAMAOUTLET | ADDRESS | LATITUDE | LONGITUDE |
|-------------|-------------|-----------|-----------|
| Contoh Outlet | jl.contoh | -6.21462 | 106.84513 |
