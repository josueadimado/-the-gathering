"""
SMS API Client - Handles communication with the SMS API service.
"""
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SMSAPIClient:
    """Client for interacting with the SMS API."""
    
    def __init__(self):
        self.base_url = getattr(settings, 'SMS_API_BASE_URL', 'https://pushr.pywe.org/api/client')
        self.public_key = getattr(settings, 'SMS_API_PUBLIC_KEY', '')
        self.secret_key = getattr(settings, 'SMS_API_SECRET_KEY', '')
        self.sender_id = getattr(settings, 'SMS_SENDER_ID', 'TheGathering')
        
        if not self.public_key or not self.secret_key:
            logger.warning("SMS API keys not configured. SMS sending will fail.")
    
    def _get_headers(self):
        """Get request headers."""
        return {
            'Content-Type': 'application/json',
        }
    
    def _format_phone_number(self, phone_number):
        """
        Convert phone number to Ghana format (233XXXXXXXXX).
        Accepts E.164 format (+233XXXXXXXXX, +228XXXXXXXXX, etc.) or Ghana format (233XXXXXXXXX).
        Note: API requires Ghana format, but we'll convert other formats if possible.
        """
        # Remove any spaces, dashes, or parentheses
        phone = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        # If it starts with +, remove it
        if phone.startswith('+'):
            phone = phone[1:]
        
        # If it starts with 233, it's already in Ghana format
        if phone.startswith('233'):
            return phone
        
        # If it starts with 0, replace with 233 (local Ghana format)
        if phone.startswith('0'):
            return '233' + phone[1:]
        
        # If it's a different country code (like 228 for Togo), we need to handle it
        # For now, log a warning and return as-is - the API will reject it with a proper error
        if phone.isdigit() and len(phone) >= 9:
            # If it's 12 digits and starts with a country code other than 233, log it
            if len(phone) == 12 and not phone.startswith('233'):
                logger.warning(f"Phone number {phone_number} is not Ghana format. API requires 233XXXXXXXXX format.")
                # Try to convert if it's a known format, otherwise return as-is
                # This will let the API return a proper error message
                return phone
        
        # If it's already a number without country code, assume it's Ghana and add 233
        if phone.isdigit() and len(phone) == 9:
            return '233' + phone
        
        # Return as-is if we can't determine - API will return proper error
        logger.warning(f"Could not format phone number {phone_number} to Ghana format. Returning as-is.")
        return phone
    
    def send_sms(self, to, body, sender_id=None):
        """
        Send a single SMS message.
        
        Args:
            to: Recipient phone number (will be converted to Ghana format: 233XXXXXXXXX)
            body: Message content (max 500 characters)
            sender_id: Optional sender ID (defaults to settings value, max 11 chars)
        
        Returns:
            dict with 'success' (bool), 'message_id' (str), 'cost' (float), 
            'currency' (str), 'segments' (int), and optional 'error' (str)
        """
        if not self.public_key or not self.secret_key:
            return {
                'success': False,
                'error': 'SMS API keys not configured. Please add SMS_API_PUBLIC_KEY and SMS_API_SECRET_KEY to your .env file.'
            }
        
        # Validate message length (API limit is 500 characters)
        if len(body) > 500:
            return {
                'success': False,
                'error': f'Message is too long ({len(body)} characters). Maximum is 500 characters.'
            }
        
        # API endpoint according to documentation: /api/client/sms/send-sms
        url = f"{self.base_url}/sms/send-sms"
        headers = self._get_headers()
        
        # Format phone number to Ghana format (233XXXXXXXXX)
        formatted_phone = self._format_phone_number(to)
        
        # Validate phone number format (must be Ghana: 233XXXXXXXXX, 12 digits total)
        if not formatted_phone.startswith('233') or len(formatted_phone) != 12 or not formatted_phone.isdigit():
            return {
                'success': False,
                'error': f'Invalid phone number format. API requires Ghana format (233XXXXXXXXX, 12 digits). Got: {formatted_phone}. Original: {to}'
            }
        
        # According to API docs: API keys go in the request body, not headers
        # recipients must be an array
        # Include scheduled fields as per API documentation
        payload = {
            'api_key_public': self.public_key,
            'api_key_secret': self.secret_key,
            'message': body,
            'recipients': [formatted_phone],  # Must be an array
            'scheduled': False,  # Explicitly set as per API docs
            'time_scheduled': None,  # Explicitly set as per API docs
        }
        
        # Add sender_id if provided (optional field, but API might require it)
        # According to docs: "If not provided, first approved sender ID is used"
        # So we can omit it, but let's include it if we have one
        if sender_id:
            payload['sender_id'] = sender_id[:11]  # Max 11 characters
        elif self.sender_id:
            payload['sender_id'] = self.sender_id[:11]  # Max 11 characters
        # If no sender_id, API will use first approved one automatically
        
        try:
            logger.info(f"Sending SMS to {to} via {url}")
            logger.debug(f"Payload: {payload}")
            logger.debug(f"Headers: {dict(headers)}")
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            logger.info(f"API Response Status: {response.status_code}")
            logger.info(f"API Response Headers: {dict(response.headers)}")
            logger.info(f"API Response Text (first 500 chars): {response.text[:500]}")
            
            # Try to parse JSON response
            response_data = {}
            try:
                if response.content:
                    response_data = response.json()
            except ValueError as json_error:
                logger.error(f"Failed to parse JSON response: {str(json_error)}")
                logger.error(f"Response content type: {response.headers.get('Content-Type', 'unknown')}")
                logger.error(f"Response text: {response.text[:1000]}")
                # If it's not JSON, return a helpful error
                return {
                    'success': False,
                    'error': f'API returned non-JSON response (Status {response.status_code}). Response: {response.text[:200]}',
                    'status_code': response.status_code,
                    'response': response.text[:500],
                }
            
            if response.status_code == 201 or response.status_code == 200:
                # According to API docs, response structure is:
                # {
                #   "id": 123,
                #   "status": "sent",
                #   "cost": "2.50",
                #   "sender_id": "PYWE",
                #   "recipients_count": 2
                # }
                return {
                    'success': True,
                    'message_id': response_data.get('id'),
                    'cost': float(response_data.get('cost', 0)) if response_data.get('cost') else 0,
                    'currency': 'GHS',  # Ghana Cedis according to API
                    'segments': 1,  # API doesn't return segments, defaulting to 1
                }
            else:
                # According to API docs, error responses have a "detail" field
                # Example: {"detail": "Insufficient balance to send messages."}
                # But 400 errors might have different structure, so check all possibilities
                error_message = None
                
                # Try different error field names
                # The API might return errors in different formats:
                # - {"detail": "message"}
                # - {"api_key": ["message"]}
                # - {"message": "text"}
                # - {"error": "text"}
                if 'detail' in response_data:
                    error_message = response_data['detail']
                elif 'api_key' in response_data:
                    # Handle array of errors: {"api_key": ["Invalid or inactive API keys."]}
                    api_key_errors = response_data['api_key']
                    if isinstance(api_key_errors, list):
                        error_message = api_key_errors[0] if api_key_errors else 'Invalid API keys'
                    else:
                        error_message = str(api_key_errors)
                elif 'message' in response_data:
                    error_message = response_data['message']
                elif 'error' in response_data:
                    error_message = response_data['error']
                elif isinstance(response_data, dict) and len(response_data) > 0:
                    # If it's a dict with content, try to get the first value
                    first_key = list(response_data.keys())[0]
                    first_value = response_data[first_key]
                    if isinstance(first_value, list) and len(first_value) > 0:
                        error_message = first_value[0]
                    else:
                        error_message = str(first_value)
                elif response_data:
                    error_message = str(response_data)
                else:
                    error_message = f'API returned status {response.status_code}'
                
                errors = response_data.get('errors', []) if isinstance(response_data, dict) else []
                
                # Log full error details for debugging
                logger.error(f"SMS API Error (Status {response.status_code}): {error_message}")
                logger.error(f"Full response data: {response_data}")
                logger.error(f"Full response text: {response.text}")
                logger.error(f"Request URL: {url}")
                logger.error(f"Request payload: {payload}")
                logger.error(f"Formatted phone: {formatted_phone} (from {to})")
                
                # Include more details in the error message for user
                detailed_error = error_message
                if response.status_code == 400:
                    # Add helpful hints based on common 400 errors
                    if 'balance' in error_message.lower():
                        detailed_error += " - Check your account balance in the dashboard"
                    elif 'phone' in error_message.lower() or 'recipient' in error_message.lower():
                        detailed_error += " - Phone number must be in Ghana format (233XXXXXXXXX, 12 digits)"
                    elif 'sender' in error_message.lower():
                        detailed_error += " - Check if sender_id is approved in your dashboard"
                    elif 'key' in error_message.lower() or 'auth' in error_message.lower():
                        detailed_error += " - Verify your API keys are correct"
                    else:
                        detailed_error += " - Check phone number format (must be Ghana: 233XXXXXXXXX), sender_id approval, account balance, or API keys"
                
                return {
                    'success': False,
                    'error': detailed_error,
                    'errors': errors,
                    'status_code': response.status_code,
                    'response': response.text[:500],  # First 500 chars of response
                    'response_data': response_data,  # Full parsed response
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"SMS API request error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to connect to SMS API: {str(e)}'
            }
        except Exception as e:
            logger.error(f"SMS API error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def send_customized_sms(self, template_id, csv_file, event_id=None):
        """
        Send customized SMS messages to multiple recipients using a template and CSV.
        
        Args:
            template_id: ID of the message template to use
            csv_file: File object containing recipient data
            event_id: Optional event ID to link messages
        
        Returns:
            dict with 'success' (bool), 'total_messages_sent' (int), 
            'failed_messages' (int), and optional 'error' (str)
        """
        if not self.public_key or not self.secret_key:
            return {
                'success': False,
                'error': 'SMS API keys not configured. Please add SMS_API_PUBLIC_KEY and SMS_API_SECRET_KEY to your .env file.'
            }
        
        url = f"{self.base_url}/sms/send/custom/"
        headers = {
            'X-API-Key': self.public_key,
            'X-API-Secret': self.secret_key,
        }
        
        files = {
            'csv_file': csv_file,
        }
        
        data = {
            'template_id': template_id,
        }
        
        if event_id:
            data['event_id'] = event_id
        
        try:
            response = requests.post(url, files=files, data=data, headers=headers, timeout=60)
            
            if response.status_code == 200 or response.status_code == 201:
                response_data = response.json()
                return {
                    'success': True,
                    'total_messages_sent': response_data.get('data', {}).get('total_messages_sent', 0),
                    'failed_messages': response_data.get('data', {}).get('failed_messages', 0),
                }
            else:
                error_data = response.json() if response.content else {}
                error_message = error_data.get('message', f'API returned status {response.status_code}')
                
                return {
                    'success': False,
                    'error': error_message,
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"SMS API request error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to connect to SMS API: {str(e)}'
            }
        except Exception as e:
            logger.error(f"SMS API error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_message_status(self, message_id):
        """
        Check the status of a sent message.
        
        Args:
            message_id: The ID of the message to check
        
        Returns:
            dict with 'success' (bool), 'status' (str), 'recipient' (str),
            'cost' (float), 'sent_at' (str), 'delivered_at' (str), 
            and optional 'error' (str)
        """
        if not self.public_key or not self.secret_key:
            return {
                'success': False,
                'error': 'SMS API keys not configured.'
            }
        
        url = f"{self.base_url}/sms/status/{message_id}/"
        headers = self._get_headers()
        
        try:
            # Use a small timeout so status checks don't block the UI for long
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                try:
                    json_data = response.json()
                except ValueError:
                    logger.error(f"SMS status API returned non-JSON response: {response.text[:200]}")
                    return {
                        'success': False,
                        'error': 'Status API returned invalid response',
                    }
                
                data = json_data.get('data', {}) if isinstance(json_data, dict) else {}
                return {
                    'success': True,
                    'status': data.get('status', 'unknown'),
                    'recipient': data.get('recipient'),
                    'cost': data.get('cost', 0),
                    'currency': data.get('currency', 'USD'),
                    'sent_at': data.get('sent_at'),
                    'delivered_at': data.get('delivered_at'),
                    'error_code': data.get('error_code'),
                }
            else:
                # Try to parse error response, but don't crash if it's not JSON
                error_message = f'API returned status {response.status_code}'
                try:
                    error_data = response.json() if response.content else {}
                    if isinstance(error_data, dict):
                        error_message = error_data.get('message', error_message)
                except ValueError:
                    logger.error(f"SMS status API error (non-JSON): {response.text[:200]}")
                
                return {
                    'success': False,
                    'error': error_message,
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"SMS API request error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to connect to SMS API: {str(e)}'
            }
        except Exception as e:
            logger.error(f"SMS API error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

