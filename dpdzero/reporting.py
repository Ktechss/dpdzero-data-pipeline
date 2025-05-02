import logging

def generate_slack_summary(summary_df, report_date):
    report_df = summary_df[summary_df['call_date'] == report_date]
    if report_df.empty:
        return f"No agent data found for {report_date}"

    top_agent = report_df.sort_values(by='connect_rate', ascending=False).iloc[0]
    top_name = f"{top_agent['users_first_name']} {top_agent['users_last_name']}"
    top_duration = top_agent['connect_rate']
    top_rate = int(top_agent['connect_rate'] * 100)

    avg_duration = round(report_df['avg_duration_min'].mean(), 2)
    active_agents = report_df['presence'].sum()

    return (f"Agent Summary for {report_date}\n"
            f"Top Performer {top_name} ({top_rate}% connect rate)\n"
            f"Total Active Agents: {active_agents}\n"
            f"Average Duration: {avg_duration} min")