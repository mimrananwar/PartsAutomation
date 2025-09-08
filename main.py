from web_scraper import initialize_browser,  open_login, login, search_product, extract_product_data
from google_sheet_api import get_credentials, get_product_list, add_products, update_product
from change_tracker import ChangeTracker
from email_sender import send_email
from Post_to_slack import Send_Msg as Slack_Msg
from SendEmail import send_csv_to_gsheet as SendEmail
import csv
import os

EMAIL_RECIPIENT = "i.anwar2004@gmail.com ; "

def main():
    print("Starting product monitoring process...")

    # 1. Get credentials from Google Sheet
    credentials = get_credentials()
    if not credentials:
        print("Could not retrieve credentials. Exiting.")
        return
    username = credentials.get("username")
    password = credentials.get("password")
    if not username or not password:
        print("Username or password not found in credentials. Exiting.")
        return

    # 2. Get product list from Google Sheet
    product_list_raw = get_product_list()
    if not product_list_raw:
        print("Could not retrieve product list. Exiting.")
        return
    
    # Assuming the first row is header, skip it
    product_list = []
    if len(product_list_raw) > 1:
        print ("Product List Received")
        for row in product_list_raw:
        
         if len(row) >= 1: # Ensure row has at least Product ID and Product Name
                #print("name", row[0])
                product_list.append({
                    "name": row[0]                                   
                })
                

    if not product_list:
        print("No products found in the Google Sheet. Exiting.")
        return

    driver = None
    #change_tracker = ChangeTracker()

    try:
        driver = initialize_browser("https://partscounter.kenworth.com/")
        #navigate_to_website(driv*er, "https://partscounter.kenworth.com/")
        if open_login(driver):
            print("Successfully opened login page.")
            if not login(driver, username, password):
                print("Failed to log in to Kenworth website. Exiting.")
                Slack_Msg(False,"Login")
                return
        Slack_Msg(True,"Login")
        for product in product_list:
            #product_id = product["id"]
            product_name = product["name"]
            #db_quantity = product["quantity"]
            #db_price = product["price"]
            #db_status = product["status"]

            print(f"Processing product: {product_name}")

            if search_product(driver, product_name):
                scraped_data = extract_product_data(driver)
                if scraped_data:
                    current_quantity = scraped_data.get("quantity")
                    current_price = scraped_data.get("price")
                    listprice = scraped_data.get("listprice")
                    #current_status = "In Stock" # Assuming if data is scraped, it's in stock

                    current_product_info = {
                        "quantity": current_quantity,
                        "price": current_price,
                        "listprice": listprice
                    }
                    
                    csv_file = "product_info.csv"
                    write_header = not os.path.exists(csv_file)

                    with open(csv_file, "a", newline="", encoding='utf-8') as file:
                        writer = csv.DictWriter(file, fieldnames=["Product Name", "Quantity", "Price", "ListPrice"])
                        if write_header:
                            writer.writeheader()
                        writer.writerow({
                            "Product Name": product_name,
                            "Quantity": current_product_info["quantity"],
                            "Price": current_product_info["price"],
                            "ListPrice": current_product_info["listprice"]
                        })

    
    except Exception as e:
        print(f"An error occurred during web scraping: {e}")
    finally:
        if  SendEmail(csv_file):
            Slack_Msg(True, "Email")
        else:
            Slack_Msg(False, "Email")

        if driver:
             #driver.quit()
            print("Browser closed.")

    # 3. Email the list of changes
    

if __name__ == "__main__":
    main()


