import requests
import os

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL", "")

def send_slack_alert(message: str):
    if not SLACK_WEBHOOK:
        print("No Slack webhook configured.")
        return
    requests.post(SLACK_WEBHOOK, json={"text": message})

def alert_on_failure(context):
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    send_slack_alert(f":red_circle: DAG *{dag_id}* task *{task_id}* failed.")

def alert_rate_movement(kes_usd_rate: float, previous_rate: float):
    change_pct = abs((kes_usd_rate - previous_rate) / previous_rate * 100)
    if change_pct >= 1.0:
        send_slack_alert(
            f":warning: KES/USD moved {change_pct:.2f}%\n"
            f"Previous: {previous_rate:.4f} | Current: {kes_usd_rate:.4f}"
        )
