import requests
import json

WEB_APP_URL_READ = "https://script.google.com/macros/s/AKfycbw_ZwzFTNbykypgDYwvpM6DQxcnu5QONqzgn4uKML3UWUceVi-HWJ7JxNtnStYM3uU/exec" # Original URL for read operations (get credentials, get product list)
WEB_APP_URL_WRITE = "https://script.google.com/macros/s/AKfycbzrMszsxfls00o8V7HdZcY9cExlz78TiuRULTkhHHuPhGW8bYrYFEunA10zksSg4Ota/exec" # New URL for write operations (update product)

def send_request(sheet_name, action, data, use_write_url=False):
    url = WEB_APP_URL_WRITE if use_write_url else WEB_APP_URL_READ
    payload = {
        "sheet": sheet_name,
        "action": action,
        "data": json.dumps(data)
    }
    print(f"Connecting with Google Sheets...")
    ##print(f"Sending request to {url}")
     
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.get(url, params=payload)
    ##print(f"Response Status Code: {response.status_code}")
    #print(f"Response Text: {response.text}")
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Response Content: {response.text}")
        return None

def get_credentials():
    response = send_request("Credentials", "getCredentials", {})
    if response.get("status") == "success":
        print("Credentials retrieved successfully.")
        return response.get("data")
        

    else:
        print(f"Error getting credentials: {response.get('message')}")
        return None

def get_product_list():
    response = send_request("Product_Data", "getProducts", {})
    if response.get("status") == "success":
        print("Product list retrieved successfully.")
        return response.get("data")
    else:
        print(f"Error getting product list: {response.get("message")}")
        return None

def add_products(products):
    # products should be a list of lists, e.g., [[id, name, qty, price, last_updated, status]]
    response = send_request("Product_Data", "addProducts", {"products": products}, use_write_url=True)
    if response.get("status") == "success":
        print("Products added successfully.")
        return True
    else:
        print(f"Error adding products: {response.get("message")}")
        return False

def update_product(product_id, new_qty=None, new_price=None, new_status=None):
    data = {"productId": product_id}
    if new_qty is not None:
        data["newQty"] = new_qty
    if new_price is not None:
        data["newPrice"] = new_price
    if new_status is not None:
        data["newStatus"] = new_status

    response = send_request("Product_Data", "updateProduct", data, use_write_url=True)
    if response.get("status") == "success":
        print(f"Product {product_id} updated successfully.")
        return True
    else:
        print(f"Error updating product {product_id}: {response.get("message")}")
        return False

if __name__ == "__main__":
    # Example Usage:
    # credentials = get_credentials()
    # if credentials:
    #     print("Credentials:", credentials)

    # product_list = get_product_list()
    # if product_list:
    #     print("Product List:", product_list)

    # new_products = [["PROD001", "Test Product 1", 10, 9.99, "2025-08-10 10:00:00", "In Stock"]]
    # add_products(new_products)

    # update_product("PROD001", 12, 10.50)
    pass

