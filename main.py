from dotenv import load_dotenv
import os
import asyncio
from denotify.client import DenotifyClient

load_dotenv()


async def main():
    # Staging Credentials
    PROJECT_ID = 'xfxplbmdcoukaitzxzei'
    ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhmeHBsYm1kY291a2FpdHp4emVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzgwMDg4NzMsImV4cCI6MTk5MzU4NDg3M30.WLk7bR5syQ4YJ8_jNOAuaT1UMvl7E2MS_VYMs7sN56c'

    api = DenotifyClient(key=ANON_KEY, project_id=PROJECT_ID)
    await api.login(os.getenv('EMAIL'), os.getenv('PASSWORD'))

    # Get the abi hash
    network = 'optimism'
    contract = '0x92024c4bda9da602b711b9abb610d072018eb58b'
    hash = (await api.get_abi(network, contract))['hash']

    # Create a new alert
    webhook = "https://discord.com/api/webhooks/webhookski"
    trigger = {
        "alertType": "event",
        "network": "optimism",
        "nickname": "Sonne TimelockController CallScheduled",
        "type": "handler_onchain_event_v2",
        "handler": {
            "triggerOn": "always",
            "event": "CallScheduled",
            "abiHash": hash,
            "addresses": [contract]
        }
    }

    # TODO - Add support for raw webhooks
    notification = {
        "notify_type": "notify_discord_webhook",
        "notify": {
            "embed": {
                "title": "TODO - use standard webhook",
            },
            "message": "Call Scheduled",
            "url": webhook
        }
    }

    # Create an alert
    print(f'Creating a new alert')
    alertId = await api.create_alert(trigger, notification)
    alert = await api.read_alert(alertId)
    print(f'Created alert {alertId}')

    # read the alert
    print('Reading alerts')
    alerts = await api.read_alerts(alertId)
    print(f'You have {len(alerts)} alerts')

    # Delete an alert
    print(f'Deleting alert {alertId}')
    deleted = await api.delete_alert(alertId)
    print(f'Alert {deleted} deleted')

    # Note - update not yet supported

asyncio.run(main())
