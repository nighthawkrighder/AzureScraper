#!/usr/bin/env python3
import requests
import json
import csv
import os
import time
import sys

def build_pricing_table(json_data, table_data):
    for item in json_data['Items']:
        meter = item['meterName']
        table_data.append([item['armSkuName'], item['retailPrice'], item['unitOfMeasure'], item['armRegionName'], meter, item['productName']])

def main():
    table_data = []
    table_data.append(['SKU', 'Retail Price', 'Unit of Measure', 'Region', 'Meter', 'Product Name'])

    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = ("armRegionName eq 'westus3' and priceType eq 'Consumption' and ("
             #"contains(armSkuName, 'Standard_A') or "
             #"contains(armSkuName, 'Standard_B') or "
             #"contains(armSkuName, 'Standard_C') or "
             #"contains(armSkuName, 'Standard_D') or "
             #"contains(armSkuName, 'Standard_E') or "
             #"contains(armSkuName, 'Standard_F') or "
             #"contains(armSkuName, 'Standard_G') or "
             #"contains(armSkuName, 'Standard_H') or "
             "contains(armSkuName, 'Standard_N'))")

    response = requests.get(api_url, params={'$filter': query})
    json_data = json.loads(response.text)

    build_pricing_table(json_data, table_data)
    nextPage = json_data['NextPageLink']

    while(nextPage):
        response = requests.get(nextPage)
        json_data = json.loads(response.text)
        nextPage = json_data['NextPageLink']
        build_pricing_table(json_data, table_data)

    # Save to CSV
    with open('azure_vm_prices.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table_data)

    print("Data has been saved to azure_vm_prices.csv")

if __name__ == "__main__":
    main()
    #launche excel with csv file
    os.system('start "C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE" azure_vm_prices.csv')
    #sleep 5 seconds
    time.sleep(5)
    #close excel
    os.system('taskkill /IM excel.exe')
    #Use sys.exit() to exit excel
    #gracefully close excel.exe
    sys.exit()
    
