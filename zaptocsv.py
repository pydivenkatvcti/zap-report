from bs4 import BeautifulSoup
import csv

# Read the OWASP ZAP HTML report
with open('owasp_report.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the section containing the site risk counts
site_risk_counts_section = soup.find('section', {'id': 'site-risk-counts'})

# Initialize data list to store extracted data
data = [['Site', 'High', 'Medium', 'Low', 'Informational']]

# Extract data from the site risk counts section
if site_risk_counts_section:
    # Find all rows within the table
    rows = site_risk_counts_section.find_all('tr')
    for row in rows[1:]:  # Skip the first row as it contains column headers
        # Extract site name from the first column
        site_name = row.find('th', scope='row').text.strip()
        
        # Extract counts from subsequent columns
        counts = [span.text.strip() for span in row.find_all('span')]
        
        # Append extracted data to the data list
        data.append([site_name] + counts)

# Write the extracted data to a CSV file
with open('site_risk_counts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Conversion complete. CSV file saved as 'site_risk_counts.csv'")
