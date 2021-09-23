#!/usr/bin/env python3
import csv

data = list(csv.DictReader(open('dataset.csv', 'r')))
# data = list(csv.reader(open('dataset.csv', 'r')))

# def open_file():
#     with open('dataset.csv') as csvfile:
#         csv_reader = csv.reader(csvfile, delimiter=',')
#     return csv_reader


# def sort_rent(data):
#     rent_list = []
#     for row in data[1:]:
#         rent_list.append(row[-1])
#     rent_list.sort()
#     print(rent_list[:5])

def sort_rent_dict(data, rent_only=True):
    tenants = sorted(data, key=lambda k: k['Current Rent'])
    if rent_only:
        rent_only_list = [tenant['Current Rent'] for tenant in tenants[:5]]
        print(rent_only_list)
    else:
        print(tenants[:5])
    

if __name__ == "__main__":
    # sort_rent(data)
    sort_rent_dict(data)