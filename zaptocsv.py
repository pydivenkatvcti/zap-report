from bs4 import BeautifulSoup
import csv


with open('2024-04-25-ZAP-Report-.html', 'r') as file:
    html_content = file.read()


soup = BeautifulSoup(html_content, 'html.parser')

alerts_section = soup.find('section', {'id': 'alerts'})


data = [['Risk', 'Confidence', 'Count']]


if alerts_section:
    
    items = alerts_section.find_all('li', class_='alerts--site-li')
    for item in items:
        # Extract risk level and confidence level from the <td> elements
        risk_level = item.find_previous('td', class_='risk-level').text.strip() if item.find_previous('td', class_='risk-level') else 'Unknown'
        confidence_level = item.find_previous('td', class_='confidence-level').text.strip() if item.find_previous('td', class_='confidence-level') else 'Unknown'
        
        # Extract count from the <span> element
        count_span = item.find('span')
        count = int(count_span.text.strip()) if count_span and count_span.text.strip().isdigit() else 0
        
        # Append extracted data to the data list
        data.append([risk_level, confidence_level, count])

# Writing the extracted data to the csv file
with open('owasp_alerts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Conversion complete. CSV file saved as 'owasp_alerts.csv'")
