import requests
import json

def Send_Msg(success=True, Types="Login"):
    webhook_url = "https://hooks.slack.com/services/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"

    if Types.lower() == "login":
        if success:
            text = "✅ Login complete"
        else:
            text = "❌ Login failed. Please try manually."

    elif Types.lower() == "email":
        if success:
            text = "📧 Data processed and email sent"
        else:
            text = "⚠️ Failed to process data, check manually."

    else:
        text = f"ℹ️ Unknown type: {Types}"

    message = {"text": text}

    response = requests.post(
        webhook_url,
        data=json.dumps(message),
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        print("Message posted successfully!")
    else:
        print("Failed to post message, error:", response.status_code, response.text)
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

