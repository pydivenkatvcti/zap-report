from bs4 import BeautifulSoup
import csv


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
    # Find all lists within the alerts section
    alert_lists = alerts_section.find_all('ol')
    for alert_list in alert_lists:
        # Extract the risk level and confidence level from the list heading
        heading = alert_list.find_previous('a')
        risk_level = heading.find(class_='risk-level').text.strip() if heading.find(class_='risk-level') else 'Unknown'
        confidence_level = heading.find(class_='confidence-level').text.strip() if heading.find(class_='confidence-level') else 'Unknown'
        
        # Find all list items within the list
        items = alert_list.find_all('li')
        for item in items:
            # Extract the count from each list item
            count_span = item.find('span')
            count = int(count_span.text.strip('()')) if count_span and count_span.text.strip('()').isdigit() else 0
            
            # Append extracted data to the data list
            data.append([risk_level, confidence_level, count])

# Write the extracted data to a CSV file
with open('owasp_alerts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Conversion complete. CSV file saved as 'owasp_alerts.csv'")
