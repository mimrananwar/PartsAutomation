import requests
import json

def Send_Msg(success=True, Types="Login"):
    webhook_url = SLACKAPI

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
   Send_Msg()



