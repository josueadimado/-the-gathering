Quick Navigation
Getting Started
Authentication
Send SMS
Send Customized SMS
Check Message Status
Code Examples
Important Notes
Getting Started
Base URL
All API requests should be made to:

https://pushr.pywe.org/api/client
For local development:

http://localhost:6700/api/client
Response Format
All API responses are in JSON format. Successful SMS sending responses follow this structure:

{
  "id": 123,
  "business": 1,
  "message": "Your message text",
  "status": "sent",
  "created": "2024-01-15T10:30:00Z",
  "cost": "2.50",
  "sender_id": "PYWE",
  "recipients_count": 2
}
Authentication
Push.R SMS API uses API key authentication. This is the simplest and recommended method for sending SMS programmatically.

API Key Authentication
Use your API keys from the dashboard to authenticate your requests.

Where to find your API keys: Log into your dashboard and check the "API Keys" card. You'll see your Public and Secret keys.
API keys are passed directly in the request body - no headers needed:

{
  "api_key_public": "your_public_key",
  "api_key_secret": "your_secret_key",
  ...
}
Security Note: Keep your API keys secure and never expose them in client-side code or public repositories.
Send SMS
Send SMS messages to one or more recipients using your API keys.

POST
/api/client/sms/send-sms
Request Body:
{
  "api_key_public": "your_public_key",
  "api_key_secret": "your_secret_key",
  "message": "Hello! This is a test message.",
  "recipients": ["233558544343", "233548769324"],
  "sender_id": "PYWE",
  "scheduled": false,
  "time_scheduled": null
}
Parameters:
Field	Type	Required	Description
api_key_public	string	Yes	Your public API key from dashboard
api_key_secret	string	Yes	Your secret API key from dashboard
message	string	Yes	Message content (max 500 characters)
recipients	array	Yes	Array of phone numbers in Ghana format (233XXXXXXXXX)
sender_id	string	No	Approved sender ID (max 11 chars). If not provided, first approved sender ID is used.
scheduled	boolean	No	Whether to schedule the message (default: false)
time_scheduled	datetime	Conditional	ISO 8601 datetime (required if scheduled=true). Must be in the future.
Success Response (201 Created):
{
  "id": 123,
  "business": 1,
  "message": "Hello! This is a test message.",
  "status": "sent",
  "created": "2024-01-15T10:30:00Z",
  "cost": "2.50",
  "sender_id": "PYWE",
  "recipients_count": 2
}
Error Response (400 Bad Request):
{
  "detail": "Insufficient balance to send messages."
}
Important: Make sure you have sufficient account balance and an approved sender ID before sending SMS.
Send Customized SMS
Send personalized SMS messages to multiple recipients using a template and CSV file. Each recipient receives a customized message with their specific data.

POST
/api/client/sms/custom
Content-Type: multipart/form-data

Authentication: API keys required (included in form data)

Request Parameters:
Field	Type	Required	Description
business	integer	Yes	Business ID
sender_id	string	Yes	Approved sender ID
template	string	Yes	Message template with variables like {name}, {order_id}
csv_file	file	Yes	CSV file with 'contact' column and columns matching template variables
scheduled	boolean	No	Whether to schedule (default: false)
time_scheduled	datetime	Conditional	ISO 8601 datetime (required if scheduled=true)
CSV Format Example:
Your CSV file must include a contact column plus columns for each variable in your template:

contact,name,order_id,amount
233558544343,John Doe,ORD123,150.00
233548769324,Jane Smith,ORD124,200.00
233559876543,Bob Johnson,ORD125,75.50
Template Example:
Hi {name}, your order {order_id} for GHS {amount} is ready for pickup!
Result:
Each recipient will receive a personalized message:

233558544343: "Hi John Doe, your order ORD123 for GHS 150.00 is ready for pickup!"
233548769324: "Hi Jane Smith, your order ORD124 for GHS 200.00 is ready for pickup!"
233559876543: "Hi Bob Johnson, your order ORD125 for GHS 75.50 is ready for pickup!"
Response:
{
  "recipients_count": 3,
  "status": "PROCESSING"
}
Note: Customized SMS sending happens asynchronously. The response indicates the request was accepted and processing has started.
CSV Requirements:
Must include a contact column
All template variables must have matching CSV columns
File must be UTF-8 encoded
At least one data row required
Check Message Status
Retrieve the status of your sent messages.

GET
/api/client/sms/?business={business_id}
Authentication: JWT token required

Query Parameters:
business (required): Your business ID
Response:
{
  "data": [
    {
      "id": 123,
      "message": "Hello!",
      "status": "delivered",
      "created": "2024-01-15T10:30:00Z",
      "cost": "2.50",
      "sender_id": "PYWE",
      "recipients_count": 2
    },
    {
      "id": 124,
      "message": "Test message",
      "status": "pending",
      "created": "2024-01-15T11:00:00Z",
      "cost": "1.25",
      "sender_id": "PYWE",
      "recipients_count": 1
    }
  ],
  "count": 2,
  "next": null,
  "previous": null
}
Message Status Values:
pending - Message is queued for sending
sent - Message has been sent to the provider
delivered - Message was successfully delivered
failed - Message failed to send
partial_failed - Some recipients failed (bulk messages)
Code Examples
Here are code examples in different programming languages for sending SMS using the API:

Python
JavaScript
Node.js
PHP
cURL
import requests

# Send SMS using API keys
url = "https://pushr.pywe.org/api/client/sms/send-sms"
headers = {"Content-Type": "application/json"}

data = {
    "api_key_public": "your_public_key",
    "api_key_secret": "your_secret_key",
    "message": "Hello from Python! This is a test message.",
    "recipients": ["233558544343", "233548769324"],
    "sender_id": "PYWE"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 201:
    result = response.json()
    print(f"Message sent! ID: {result['id']}, Cost: GHS {result['cost']}")
else:
    print(f"Error: {response.json()}")
Important Notes
Phone Number Format
All phone numbers must be in Ghana format: 233XXXXXXXXX (country code + number without leading zero).

Examples:
233558544343 ✓ Correct
0558544343 ✗ Wrong (missing country code)
+233558544343 ✓ Correct (will be normalized automatically)
SMS Cost Calculation
SMS costs are calculated based on:

Message length: 160 characters = 1 SMS unit
Number of recipients: Each recipient is charged separately
Your pricing plan: Price per SMS unit from your plan
Example: A 320-character message to 10 recipients = 2 SMS units × 10 recipients = 20 SMS units total.

Cost is deducted automatically from your account balance after successful sends. Make sure you have sufficient balance before sending.
Sender IDs
Sender IDs must be:

Maximum 11 characters
Approved by the system before use
Requested through the dashboard or API
If you don't specify a sender_id, the system will use your first approved sender ID automatically.

Scheduled Messages
You can schedule messages to be sent at a future time:

Set scheduled: true
Provide time_scheduled in ISO 8601 format
Scheduled time must be in the future
Example: "2024-01-20T14:30:00Z"

Error Handling
Common errors you might encounter:

400 Bad Request: Invalid parameters, insufficient balance, invalid sender ID
401 Unauthorized: Invalid or missing API keys
404 Not Found: Business or resource not found
Always check the response status code and handle errors appropriately in your code.

Rate Limits
Rate limits may apply to prevent abuse. Contact support if you need higher limits for your use case.

Support
For additional help, questions, or to report issues, please contact support through your dashboard or visit the dashboard for more information.