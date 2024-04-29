from bs4 import BeautifulSoup
import csv
import re

# Read the OWASP ZAP HTML report
with open('2024-04-25-ZAP-Report-.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize data lists to store extracted data
risk_confidence_data = [['Risk', 'Confidence', 'Count']]
site_risk_data = [['Site', 'High', 'Medium', 'Low', 'Informational']]

# Extract data from the "Alert counts by risk and confidence" section
risk_confidence_section = soup.find('section', {'id': 'summaries'})
if risk_confidence_section:
    # Find all rows within the table
    rows = risk_confidence_section.find('table', class_='risk-confidence-counts-table').find_all('tr')
    for row in rows[2:]:  # Skip the first two rows as they contain column headers and subheaders
        # Extract risk level and confidence level from the row
        columns = row.find_all('td')
        risk_level = columns[0].text.strip()
        confidence_level = columns[1].text.strip()
        count_text = columns[-1].text.strip()
        # Extract numerical count value using regular expression
        count = int(re.search(r'\d+', count_text).group())
        risk_confidence_data.append([risk_level, confidence_level, count])

# Extract data from the "Alert counts by site and risk" section
site_risk_section = soup.find('section', {'id': 'site-risk-counts'})
if site_risk_section:
    # Find all rows within the table
    rows = site_risk_section.find('table', class_='site-risk-counts-table').find_all('tr')
    for row in rows[1:]:  # Skip the first row as it contains column headers
        # Extract site name from the first column if available
        site_name_th = row.find('th', scope='row')
        site_name = site_name_th.text.strip() if site_name_th else 'Unknown'
        
        # Extract counts from subsequent columns
        counts = [int(re.search(r'\d+', span.text.strip()).group()) for span in row.find_all('span') if re.search(r'\d+', span.text.strip())]
        
        # Append extracted data to the site risk data list
        site_risk_data.append([site_name] + counts)

# Write the extracted data to CSV files
with open('risk_confidence_counts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(risk_confidence_data)

with open('site_risk_counts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(site_risk_data)

print("Conversion complete. CSV files saved as 'risk_confidence_counts.csv' and 'site_risk_counts.csv'")
