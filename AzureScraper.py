#!/usr/bin/env python3
import requests
import json
import csv

def build_pricing_table(json_data, table_data):
    for item in json_data['Items']:
        meter = item['meterName']
        table_data.append([item['armSkuName'], item['retailPrice'], item['unitOfMeasure'], item['armRegionName'], meter, item['productName']])

def save_to_html(table_data, filename):
    with open(filename, 'w') as htmlfile:
        htmlfile.write("<!DOCTYPE html>\n")
        htmlfile.write("<html lang='en'>\n")
        htmlfile.write("<head>\n")
        htmlfile.write("  <meta charset='UTF-8'>\n")
        htmlfile.write("  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
        htmlfile.write("  <title>Azure VM Prices</title>\n")
        htmlfile.write("  <style>\n")
        htmlfile.write("    table { width: 100%; border-collapse: collapse; margin: 20px 0; }\n")
        htmlfile.write("    th, td { border: 1px solid #ddd; padding: 8px; }\n")
        htmlfile.write("    th { background-color: #f2f2f2; }\n")
        htmlfile.write("    tr:hover { background-color: #f5f5f5; }\n")
        htmlfile.write("  </style>\n")
        htmlfile.write("</head>\n")
        htmlfile.write("<body>\n")
        htmlfile.write("  <table>\n")
        headers = table_data[0]
        htmlfile.write("    <thead>\n")
        htmlfile.write("      <tr>\n")
        for header in headers:
            htmlfile.write(f"        <th>{header}</th>\n")
        htmlfile.write("      </tr>\n")
        htmlfile.write("    </thead>\n")
        htmlfile.write("    <tbody>\n")
        for row in table_data[1:]:
            htmlfile.write("      <tr>\n")
            for cell in row:
                htmlfile.write(f"        <td>{cell}</td>\n")
            htmlfile.write("      </tr>\n")
        htmlfile.write("    </tbody>\n")
        htmlfile.write("  </table>\n")
        htmlfile.write("</body>\n")
        htmlfile.write("</html>\n")

def main():
    table_data = []
    table_data.append(['SKU', 'Retail Price', 'Unit of Measure', 'Region', 'Meter', 'Product Name'])

    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = ("armRegionName eq 'westus3' and priceType eq 'Consumption' and ("
             "contains(armSkuName, 'Standard_A') or "
             "contains(armSkuName, 'Standard_B') or "
             "contains(armSkuName, 'Standard_C') or "
             "contains(armSkuName, 'Standard_D') or "
             "contains(armSkuName, 'Standard_E') or "
             "contains(armSkuName, 'Standard_F') or "
             "contains(armSkuName, 'Standard_G') or "
             "contains(armSkuName, 'Standard_H') or "
             "contains(armSkuName, 'Standard_L') or "
             "contains(armSkuName, 'Standard_M') or "
             "contains(armSkuName, 'Standard_M') or "
             "contains(armSkuName, 'Standard_T'))")
                    
             
             

    response = requests.get(api_url, params={'$filter': query})
    json_data = json.loads(response.text)

    build_pricing_table(json_data, table_data)
    nextPage = json_data['NextPageLink']

    while(nextPage):
        response = requests.get(nextPage)
        json_data = json.loads(response.text)
        nextPage = json_data['NextPageLink']
        build_pricing_table(json_data, table_data)

    # Sort the table data by SKU (VM series)
    table_data = [table_data[0]] + sorted(table_data[1:], key=lambda x: x[0])

    # Save to CSV
    with open('azure_vm_prices.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table_data)
    print("Data has been saved to azure_vm_prices.csv")

    # Save to HTML
    save_to_html(table_data, 'azure_vm_prices.html')
    print("Data has been saved to azure_vm_prices.html")

if __name__ == "__main__":
    main()
