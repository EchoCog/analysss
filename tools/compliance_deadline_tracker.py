#!/usr/bin/env python3

"""
Track and manage legal compliance deadlines based on the South African AI legislation compliance framework.
"""

import json
import pandas as pd
from datetime import datetime, timedelta

def get_compliance_deadlines(compliance_file):
    """Load compliance deadlines from a JSON file."""
    with open(compliance_file, 'r') as f:
        data = json.load(f)
    return data.get('timeline', {}).get('compliance_deadlines', [])

def check_upcoming_deadlines(deadlines, days_ahead=30):
    """Check for upcoming deadlines within a specified number of days."""
    upcoming_deadlines = []
    today = datetime.now()
    for deadline in deadlines:
        timeframe = deadline.get('timeframe', '')
        if 'hours' in timeframe:
            hours = int(timeframe.split(' ')[0])
            deadline_date = today + timedelta(hours=hours)
        elif 'days' in timeframe:
            days = int(timeframe.split(' ')[0])
            deadline_date = today + timedelta(days=days)
        else:
            continue

        if deadline_date <= today + timedelta(days=days_ahead):
            upcoming_deadlines.append({
                'requirement': deadline['requirement'],
                'legislation': deadline['legislation'],
                'due_date': deadline_date.strftime('%Y-%m-%d %H:%M:%S'),
                'severity': deadline['severity']
            })
    return upcoming_deadlines

def generate_compliance_report(upcoming_deadlines):
    """Generate a report of upcoming compliance deadlines."""
    if not upcoming_deadlines:
        return "No upcoming compliance deadlines."

    report = "## Upcoming Compliance Deadlines\n\n"
    report += "| Requirement | Legislation | Due Date | Severity |\n"
    report += "|---|---|---|---|\n"
    for deadline in upcoming_deadlines:
        report += f"| {deadline['requirement']} | {deadline['legislation']} | {deadline['due_date']} | {deadline['severity']} |\n"
    return report

if __name__ == '__main__':
    compliance_file = 'evidence/sa_ai_legislation_compliance/entities_and_timeline.json'
    deadlines = get_compliance_deadlines(compliance_file)
    upcoming_deadlines = check_upcoming_deadlines(deadlines)
    report = generate_compliance_report(upcoming_deadlines)
    print(report)

