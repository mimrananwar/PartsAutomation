import csv
import json
import requests
import os
from Post_to_slack import Send_Msg as Slack_Msg

def send_csv_to_gsheet(csv_filename):
    """
    Reads CSV, converts to JSON, and posts to Google Apps Script webhook.
    """

    webhook_url = "https://script.google.com/macros/s/AKfycby0pK0rn90UpFUYtFCPzmLdVr5fml7NgjEErWnmpgXVv4DQ_TxKLBw4BkugSWWQgWVLBA/exec"

    try:
        # Get file path (same folder as script)
        file_path = os.path.join(os.path.dirname(__file__), csv_filename)
        print("Opening CSV")

        # Read CSV
        with open(file_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            rows = list(reader)
        if not rows:
            print("CSV is empty!")
            return False
        headers = rows[0]      # first row
        data_rows = rows[1:]   # rest

        # Convert to JSON
        payload = {
        "headers": headers,
        "rows": data_rows
        }
        #print(json.dumps(payload, indent=2))
        # Send POST request
        print("Sending request to Google Apps Script")
        response = requests.post(webhook_url, json=payload)

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        # ✅ Check response
        if response.status_code == 200:
            return True
        else:
            return False

    except Exception as e:
        print("Error:", str(e))
        return False


if __name__ == "__main__":
    if send_csv_to_gsheet("product_info.csv"):
        Slack_Msg(True, "Email")
    else:
        Slack_Msg(False, "Email")
