from bs4 import BeautifulSoup
import csv
import re


with open('2024-04-25-ZAP-Report-.html', 'r') as file:
    html_content = file.read()


soup = BeautifulSoup(html_content, 'html.parser')


risk_confidence_data = [['Risk', 'Confidence', 'Count']]
site_risk_data = [['Site', 'High', 'Medium', 'Low', 'Informational']]

risk_confidence_section = soup.find('section', {'id': 'summaries'})
if risk_confidence_section:
    
    rows = risk_confidence_section.find('table', class_='risk-confidence-counts-table').find_all('tr')
    for row in rows[2:]:  
        columns = row.find_all('td')
        risk_level = columns[0].text.strip()
        confidence_level = columns[1].text.strip()
        count_text = columns[-1].text.strip()
       
        count = int(re.search(r'\d+', count_text).group())
        risk_confidence_data.append([risk_level, confidence_level, count])


site_risk_section = soup.find('section', {'id': 'site-risk-counts'})
if site_risk_section:
    
    rows = site_risk_section.find('table', class_='site-risk-counts-table').find_all('tr')
    for row in rows[1:]:  
        
        site_name_th = row.find('th', scope='row')
        site_name = site_name_th.text.strip() if site_name_th else 'Unknown'
        
        
        counts = [int(re.search(r'\d+', span.text.strip()).group()) for span in row.find_all('span') if re.search(r'\d+', span.text.strip())]
        
        
        site_risk_data.append([site_name] + counts)


with open('risk_confidence_counts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(risk_confidence_data)

with open('site_risk_counts.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(site_risk_data)

print("Conversion complete. CSV files saved as 'risk_confidence_counts.csv' and 'site_risk_counts.csv'")
