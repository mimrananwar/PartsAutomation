import re
import time
import random
import datetime
import threading
import os
import psutil
import subprocess
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
#from selenium_stealth import stealth

def initialize_browser(url=None, profile=None):
        """Initialize Chrome browser with specified profile"""
        temp_dir = tempfile.mkdtemp(prefix="chrome_session_")

        # Setup Chrome options with temporary directory
        options = webdriver.ChromeOptions()
        #options.add_argument(f"--user-data-dir={temp_dir}") # isolated profile
        #options.add_argument(f"--profile-directory={temp_profile_name}")
        
        # Add stability and compatibility flags
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--use-gl=swiftshader")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-accelerated-2d-canvas")
        options.add_argument("--disable-accelerated-jpeg-decoding")
        options.add_argument("--disable-gpu-compositing")
        options.add_argument("--disable-gpu-driver-bug-workarounds")
        options.add_argument("--use-gl=swiftshader")
        options.add_argument("--disable-webgl")
        options.add_argument("--disable-dawn-features=disallow_unsafe_apis")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--disable-cloud-import")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-background-networking")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-background-timer-throttling")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--enable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--disable-ipc-flooding-protection")
        options.add_argument("--disable-backgrounding-occluded-windows")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-hang-monitor")
        options.add_argument(
            "--disable-features=NetworkService,NetworkServiceInProcess"
        )
        options.add_argument("--disable-background-task-scheduler")

        # Initialize the driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Store temp directory reference for cleanup
        driver._temp_dir = temp_dir
        
        print(f"Chrome browser initialized with temporary copy of {profile}")
        
        # Navigate to URL if provided
        if url:
            print(f"Navigating to {url}")
            driver.get(url)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("return navigator.language")
            time.sleep(3)  # Wait for page to load
            print(f"Successfully navigated to {url}")
        
        return driver
        
       

def login(driver, username, password):
    try:
        # Wait for the username and password fields to be visible and fill them
        driver.execute_script("return navigator.language")
        username_field = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@name="username"]'))
        )
        print("Username field found")
        username_field.send_keys(username)
        password_field = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@type="password"]'))
        )
        print("Password field found")      
        password_field.send_keys(password)
       
        time.sleep(10)
        human = True

        while not human:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "success"))
                )
                human = True
                print("Element found, human =", human)
            except TimeoutException:
                print("Element not found. Retrying in 30 seconds...")
                time.sleep(30)

        # Click the continue button
        submit_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))
        )
        submit_button.click()
        print("Clicked continue button")

        # Wait for some element that indicates successful login, e.g., a dashboard element
        # This will need to be updated after successful login to the actual dashboard element
        WebDriverWait(driver, 10).until(
             EC.presence_of_element_located((By.ID, 'search_panel_mini_form')) # Placeholder
        )
        print("Login successful")
        return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False
    
def open_login(driver):
    try:
        # Try to dismiss cookie popup
        try:
            cookie_accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'CybotCookiebotDialogBodyButtonAccept'))
            )
            cookie_accept.click()
            print("Accepted cookies")
        except:
            print("No cookie popup found")

        # Find and scroll to login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@name="websso-login-button"]'))
        )
        print("login button Found")
        driver.execute_script("arguments[0].scrollIntoView(true);", login_button)

        # Click using JS if normal click fails
        try:
            login_button.click()
        except:
            driver.execute_script("arguments[0].click();", login_button)

        print("Clicked login button")
        return True

    except Exception as e:
        print(f"Login failed: {e}")
        return False

def search_product(driver, product_name):
    try:
        search_field = WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.ID, 'search')) # Placeholder for search input field ID
        )
        search_field.clear()
        search_field.send_keys(product_name)

        search_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Search"]'))
        )
        search_button.click()
        #search_field.submit()
        

        print(f"Searched for {product_name}")
        
        time.sleep(1)
        try:
            first_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.item.product:first-of-type a"))
            )
        except Exception as e:
            print(f"single product found")
            first_link = False

        # Click the element
        if first_link:
            first_link.click()
            time.sleep(1)

        WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.CLASS_NAME, 'm-stock__current-stock-qty')) # Placeholder for product list ID
        )
        print(f"Found {product_name}")
            
        return True
    except Exception as e:
        print(f"Search failed: {e}")
        return False

def extract_product_data(driver):
    quantity = "N/A"
    price = "N/A"
    listprice = "N/A"
    try:
        # Wait for all elements to be present using a single WebDriverWait call
        print("Searching for product Qty...")
        quantity_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'm-stock__current-stock-qty'))
        )
        if quantity_element:
            quantity = quantity_element.text.strip()
            #print(f"Quantity: {quantity}")

        print("Searching for product Price...")
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'm-price-box__price--special'))
        )
        if price_element:
            # Correct the syntax from .text,strip() to .text.strip()
            price = price_element.text.strip()
            #print(f"Price: {price}")

        print("Searching for product List Price...")
        listprice_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'm-price-box__price--list-price'))
        )
        if listprice_element:
            # Correct the syntax from .text,strip() to .text.strip()
            listprice = listprice_element.text.strip()
            #print(f"List Price: {listprice}")

        # Return the collected data
        return {"quantity": quantity, "price": price, "listprice": listprice}

    except TimeoutException:
        print("A specified element was not found within the timeout period.")
        return {"quantity": quantity, "price": price, "listprice": listprice}
    except Exception as e:
        # This will now catch any other errors, like the AttributeError
        print(f"Data extraction failed: {e}")
        return None

def cleanup_browser(driver):
    """Clean up browser and temporary files"""
    try:
        if driver:
            # Clean up temporary directory if it exists
            if hasattr(driver, '_temp_dir') and driver._temp_dir and os.path.exists(driver._temp_dir):
                temp_dir = driver._temp_dir
                driver.quit()
                time.sleep(1)  # Wait for browser to fully close
                shutil.rmtree(temp_dir)
                print(f"Cleaned up temporary directory: {temp_dir}")
            else:
                driver.quit()
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    url = "https://partscounter.kenworth.com/"
    driver = initialize_browser(url, profile="Profile 2")  # You can change the profile here
    
    if driver:
        # Placeholder for actual username and password retrieval
        test_username = "freshandretroresale@gmail.com"
        test_password = "Chelc1985!!!"
        
        try:
            if open_login(driver):
                print("Successfully opened login page.")
            
                if login(driver, test_username, test_password):
                    print("Successfully logged in.")
                    # Example usage of search and extract
                    # search_product(driver, "some_product_name")
                    # product_data = extract_product_data(driver)
                    # if product_data:
                    #     print(product_data)
                else:
                    print("Failed to log in.")
            else:
                print("Failed to open login page.")
            
            # Don't quit immediately, let user interact
            input("Press Enter to close the browser...")
            
        finally:
            # Always clean up, even if an error occurs
            cleanup_browser(driver)
    else:

        print("Failed to initialize browser.")












