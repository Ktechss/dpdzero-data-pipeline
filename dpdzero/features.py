import pandas as pd
import logging
def compute_metrics(df):
    logging.info("Starting feature engineering")

    df['completed'] = df['status'].str.lower().eq('completed')
    df['duration_min'] = df['duration'] / 60.0
    df['presence'] = df['login_time'].notnull().astype(int)

    summary = df.groupby(['agent_id', 'users_first_name', 'users_last_name', 'call_date']).agg(
        total_calls=('call_id', 'count'),
        unique_loans=('installment_id', 'nunique'),
        completed_calls=('completed', 'sum'),
        avg_duration_min=('duration_min', 'mean'),
        presence=('presence', 'max')
    ).reset_index()

    summary['connect_rate'] = (summary['completed_calls'] / summary['total_calls']).round(2)
    summary['avg_duration_min'] = summary['avg_duration_min'].round(2)

    logging.info(f"Computed metrics for {summary.shape[0]} agent-date combinations")

    return summary
