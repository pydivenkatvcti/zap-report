from bs4 import BeautifulSoup
import csv

# Read the OWASP ZAP HTML report
with open('2024-04-25-ZAP-Report-.html', 'r') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the section containing the alerts
alerts_section = soup.find('section', {'id': 'alerts'})

# Initialize data list to store extracted data
data = [['Risk', 'Confidence', 'Count']]

# Extract data from the alerts section
if alerts_section:
    # Find all anchor tags within the alerts section
    alert_links = alerts_section.find_all('a')
    for link in alert_links:
        try:
            # Extract risk level, confidence level, and count from the anchor tag text
            risk_level = link.find(class_='risk-level').text.strip()
            confidence_level = link.find(class_='confidence-level').text.strip()
            count = int(link.find('span').text.strip('()'))
            
            # Append extracted data to the data list
            data.append([risk_level, confidence_level, count])
        except AttributeError:
            # Handle cases where one of the elements is missing
            pass

# Write the extracted data to a CSV file
with open('owasp_alerts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Conversion complete. CSV file saved as 'owasp_alerts.csv'")
