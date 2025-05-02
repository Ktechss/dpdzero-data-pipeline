# main.py
import argparse
import logging
import os

from dpdzero.ingestion import read_csv_with_validation
from dpdzero.merge import merge_data
from dpdzero.features import compute_metrics
from dpdzero.reporting import generate_slack_summary

# Setup logging
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main(call_logs_path, agent_roster_path, disposition_summary_path):
    expected_call_logs_cols = [
        'call_id', 'agent_id', 'org_id', 'installment_id', 
        'status', 'duration', 'created_ts', 'call_date'
    ]
    expected_agent_roster_cols = [
        'agent_id', 'users_first_name', 'users_last_name', 
        'users_office_location', 'org_id'
    ]
    expected_disposition_cols = [
        'agent_id', 'org_id', 'call_date', 'login_time'
    ]

    # Ingest with validation
    call_logs = read_csv_with_validation(call_logs_path, expected_call_logs_cols, ['agent_id', 'org_id', 'call_date'])
    agent_roster = read_csv_with_validation(agent_roster_path, expected_agent_roster_cols, ['agent_id', 'org_id'])
    disposition_summary = read_csv_with_validation(disposition_summary_path, expected_disposition_cols, ['agent_id', 'org_id', 'call_date'])

    if call_logs.empty:
        logging.error("Call logs data is empty. Exiting.")
        return

    # Merge data
    merged_df = merge_data(call_logs, agent_roster, disposition_summary)
    if merged_df.empty:
        logging.error("Merged dataset is empty. Exiting.")
        return

    # Feature Engineering
    summary_df = compute_metrics(merged_df)

    # Save output
    os.makedirs("output", exist_ok=True)
    summary_path = "output/agent_performance_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    logging.info(f"Saved report to {summary_path}")

    # Generate Slack-style summary
    latest_date = summary_df['call_date'].max()
    summary_message = generate_slack_summary(summary_df, latest_date)
    print(summary_message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run DPDzero data pipeline.")
    parser.add_argument("--call_logs", required=True, help="Path to call_logs.csv")
    parser.add_argument("--agent_roster", required=True, help="Path to agent_roster.csv")
    parser.add_argument("--disposition_summary", required=True, help="Path to disposition_summary.csv")
    args = parser.parse_args()

    main(args.call_logs, args.agent_roster, args.disposition_summary)
