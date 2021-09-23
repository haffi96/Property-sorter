#!/usr/bin/env python3
import csv

data = list(csv.DictReader(open('dataset.csv', 'r')))
# data = list(csv.reader(open('dataset.csv', 'r')))

# def open_file():
#     with open('dataset.csv') as csvfile:
#         csv_reader = csv.reader(csvfile, delimiter=',')
#     return csv_reader

def sort_rent_dict(data, rent_only=True):
    tenants = sorted(data, key=lambda k: k['Current Rent'])
    if rent_only:
        rent_only_list = [tenant['Current Rent'] for tenant in tenants[:5]]
        print(rent_only_list)
    else:
        print(tenants[:5])
    
def long_tenancies(data, tenancy_time='25'):
    long_tenant_list = [tenant for tenant in data if tenant['Lease Years'] == tenancy_time]
    print(long_tenant_list)
    all_rents = [rent['Current Rent'] for rent in long_tenant_list]
    total_rent = sum([int(float(x)) for x in all_rents])
    print(total_rent)


if __name__ == "__main__":
    sort_rent_dict(data)
    long_tenancies(data)