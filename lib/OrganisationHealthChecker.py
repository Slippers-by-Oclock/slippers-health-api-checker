from json import loads
from urllib3 import PoolManager, HTTPError
from typing import List, Dict, Any, Optional
from SlackNotifier import SlackNotifier

class OrganisationHealthChecker:
    """
    A class to check the health of organizations.

    Attributes:
        api_url (str): The API URL to fetch organizations' data.
        notifier (SlackNotifier): An instance of SlackNotifier to send alerts.
        http (PoolManager): An HTTP client for making requests.
    """

    def __init__(self, api_url: str, notifier: SlackNotifier):
        """
        Initialize the OrganisationHealthChecker with the API URL and a SlackNotifier.

        Parameters:
            api_url (str): The API URL to fetch organizations' data.
            notifier (SlackNotifier): An instance of SlackNotifier for alerts.
        """
        self.api_url = api_url
        self.notifier = notifier
        self.http = PoolManager()

    def _get_organisations(self) -> List[Dict[str, Any]]:
        """
        Retrieve the list of organizations from the API.

        Returns:
            A list of organizations.
        """
        try:
            response = self.http.request('GET', self.api_url)
            return loads(response.data.decode('utf-8'))
        except HTTPError as e:
            # Handle the error appropriately, maybe log or send a Slack notification
            print(f"Failed to retrieve organizations: {e}")
            return []

    def _is_disabled(self, organisation: Dict[str, Any]) -> bool:
        """
        Check if the organization is disabled.

        Parameters:
            organisation (Dict[str, Any]): The organization to check.

        Returns:
            True if disabled, False otherwise.
        """
        return "localhost" in organisation.get('orga', '') or organisation.get('statut') == 'disabled'

    def _check_health(self, organisation: Dict[str, Any]) -> Optional[str]:
        """
        Check the health of a given organization.

        Parameters:
            organisation (Dict[str, Any]): The organization to check.

        Returns:
            An error message if any, otherwise None.
        """
        try:
            response = self.http.request('GET', organisation.get("base_url", "") + "/api/health")
            return None if response.status == 200 else f"Status code: {response.status}"
        except HTTPError as e:
            return str(e)

    def perform_health_check(self) -> None:
        """
        Perform a health check on all organizations and send alerts if necessary.
        """
        organisations = self._get_organisations()
        for organisation in organisations:
            if not self._is_disabled(organisation):
                error_message = self._check_health(organisation)
                if error_message:
                    self.notifier.send_message(f"{organisation.get('base_url', 'Unknown URL')} is down: {error_message}")
