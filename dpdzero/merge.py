import pandas as pd
import logging
def merge_data(call_logs, agent_roster, disposition_summary):
    try:
        logging.info("Starting dataset merge process")

        call_logs['call_date'] = pd.to_datetime(call_logs['call_date']).dt.date
        disposition_summary['call_date'] = pd.to_datetime(disposition_summary['call_date']).dt.date

        merged = call_logs.merge(agent_roster, on=['agent_id', 'org_id'], how='left')
        logging.info(f"Merged call_logs with agent_roster: {len(merged)} rows")

        merged = merged.merge(disposition_summary, on=['agent_id', 'org_id', 'call_date'], how='left')
        logging.info(f"Merged with disposition_summary: {len(merged)} rows")

        missing_agents = merged[merged['users_first_name'].isnull()]
        if not missing_agents.empty:
            logging.warning(f"Agents not found in roster: {missing_agents['agent_id'].nunique()} unique agents")

        return merged
    except Exception as e:
        logging.error(f"Error during merge: {e}")
        return pd.DataFrame()
