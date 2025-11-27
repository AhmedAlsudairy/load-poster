
import os
from html2image import Html2Image
from pathlib import Path

# Define paths
BASE_DIR = Path(os.getcwd())
HTML_FILE = BASE_DIR / 'index.html'
OUTPUT_FILE = 'poster_highres.png'

# Initialize Html2Image
# We try to find Chrome/Edge automatically. 
# If this fails, we might need to specify the path.
hti = Html2Image()

# Set size for high resolution
# A0 size at 72 DPI is roughly 2384 x 3370 pixels
# Let's go for a good width like 2400px
width = 2400
# Height will be determined by the content, but we can set a large enough value
# or let it capture the full page.
# html2image usually captures the specified size.
# Let's try to capture the full page by setting a large height.
height = 4000 

print(f"Generating high-resolution poster image from {HTML_FILE}...")

try:
    # Read the HTML content to pass it directly or use the file path
    # Using file path with file:// protocol is safer for local resources
    file_url = f"file:///{HTML_FILE.absolute().as_posix()}"
    
    hti.screenshot(
        url=file_url,
        save_as=OUTPUT_FILE,
        size=(width, height)
    )
    
    print(f"Successfully created {OUTPUT_FILE}")
    
except Exception as e:
    print(f"Error generating image with html2image: {e}")
    print("Trying alternative method with Selenium...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        import time

        options = Options()
        options.add_argument('--headless')
        options.add_argument(f'--window-size={width},{height}')
        options.add_argument('--hide-scrollbars')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        driver.get(file_url)
        time.sleep(2) # Wait for animations
        
        # Get full height of the page
        required_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        driver.set_window_size(width, required_height + 100)
        
        driver.save_screenshot(OUTPUT_FILE)
        driver.quit()
        
        print(f"Successfully created {OUTPUT_FILE} using Selenium")
        
    except Exception as e2:
        print(f"Error generating image with Selenium: {e2}")
