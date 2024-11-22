import pandas as pd
import sys

def parse_and_convert_to_csv(content):
    # Split the content into lines for processing
    lines = content.split('\n')
    # Initialize variables to hold parsed data
    data = []
    all_fields = set(['timestamp', 'report_id', 'type'])  # Common fields
    current_report = {}

    for line in lines:
        if line.startswith('172'):  # Identifies the start of a new report
            # Save current report if it exists
            if current_report:
                data.append(current_report)
                current_report = {}
            # Extract timestamp and report_id
            parts = line.split(' - Stats report id: ')
            current_report['timestamp'] = parts[0].strip()
            current_report['report_id'] = parts[1].strip()
            current_report['type'] = parts[1].split('_')[0]  # Derive type from report_id
        elif line.strip():
            # Process report fields
            key, value = line.split(': ')
            current_report[key] = value
            all_fields.add(key)

    # Don't forget to add the last report
    if current_report:
        data.append(current_report)

    # Create DataFrame
    df = pd.DataFrame(data)
    # Ensure all columns are present, fill missing with NaN
    for field in all_fields:
        if field not in df.columns:
            df[field] = pd.NA

    # Reorder columns and sort by timestamp and report_id
    ordered_columns = ['timestamp', 'report_id', 'type'] + sorted(list(all_fields - {'timestamp', 'report_id', 'type'}))
    df = df[ordered_columns].sort_values(by=['timestamp', 'report_id'])

    return df

txt_file = sys.argv[1]
csv_file = sys.argv[2]

# Assuming 'content' is your file content read from 'example_gazelle_legacy_output_stats.txt'
content = open(txt_file, 'r').read()

# Use the function to parse and convert
df = parse_and_convert_to_csv(content)

# Save the DataFrame to a CSV file
df.to_csv(csv_file, index=False)
