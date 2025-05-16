import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from PIL import Image

# Set up Selenium with headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1280x720")  # Set window size for consistent thumbnails
service = Service('/home/msauer/.local/bin/chromedriver')  # Replace with the path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Folder paths
input_folder = '../out'
output_folder = '../out/thumbs'
os.makedirs(output_folder, exist_ok=True)

# Iterate through HTML files in the "out" folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.html'):
        file_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.png")

        print(f"Processing {file_name}...")
        # Open the HTML file in the browser
        driver.get(f"file://{os.path.abspath(file_path)}")

        # Take a screenshot
        screenshot_path = f"{output_path}.full.png"
        driver.save_screenshot(screenshot_path)

        # Create a thumbnail
        with Image.open(screenshot_path) as img:
            img.thumbnail((300, 200))  # Resize to thumbnail dimensions
            img.save(output_path, "PNG")

        # Remove the full screenshot
        os.remove(screenshot_path)

# Close the browser
driver.quit()

print(f"Thumbnails saved in '{output_folder}'")