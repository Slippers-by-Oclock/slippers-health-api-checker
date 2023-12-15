# main.py
import logging
from datetime import datetime
from lib.SlackNotifier import SlackNotifier
from lib.OrganisationHealthChecker import OrganisationHealthChecker

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Slack webhook URL and API URL for organizations
    slack_webhook_url = None
    org_api_url = None

    # Initialize SlackNotifier and OrganisationHealthChecker
    slack_notifier = SlackNotifier(slack_webhook_url)
    health_checker = OrganisationHealthChecker(org_api_url, slack_notifier)

    # Perform health check and log the execution
    logger.info(f"Starting health check of organizations at {datetime.now()}")
    health_checker.perform_health_check()
    logger.info("Health check completed.")

if __name__ == "__main__":
    main()
