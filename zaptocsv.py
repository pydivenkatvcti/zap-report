from bs4 import BeautifulSoup
import csv

# Read the OWASP ZAP HTML report
with open('2024-04-25-ZAP-REPORT-.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table containing the vulnerabilities
table = soup.find('table', {'id': 'alerts'})

# Extract data from the table
data = []
if table:
    # Get the table headers
    headers = [header.text.strip() for header in table.find_all('th')]
    data.append(headers)

    # Get the table rows
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        row_data = [cell.text.strip() for cell in row.find_all('td')]
        data.append(row_data)

# Write the extracted data to a CSV file
with open('owasp_report.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Conversion complete. CSV file saved as 'owasp_report.csv'")
