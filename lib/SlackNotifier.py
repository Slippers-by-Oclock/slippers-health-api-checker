from json import dumps
from urllib3 import PoolManager, HTTPError

class SlackNotifier:
    """
    A class to handle Slack notifications.
    
    Attributes:
        webhook_url (str): The URL of the Slack webhook.
        http (PoolManager): An HTTP client for making requests.
    """

    def __init__(self, webhook_url: str):
        """
        Initialize the SlackNotifier with a specific Slack webhook URL.
        
        Parameters:
            webhook_url (str): The Slack webhook URL.
        """
        self.webhook_url = webhook_url
        self.http = PoolManager()

    def send_message(self, message: str) -> None:
        """
        Send a message to the configured Slack webhook.

        Parameters:
            message (str): The message to be sent to Slack.
        """
        headers = {'Content-Type': 'application/json'}
        payload = {"text": message}
        encoded_data = dumps(payload).encode('utf-8')

        try:
            self.http.request('POST', self.webhook_url, body=encoded_data, headers=headers)
        except HTTPError as e:
            # Log or handle the HTTP error accordingly
            print(f"Failed to send message to Slack: {e}")
  
