#!/usr/bin/env python3
import csv
from pprint import pprint
from colorama import Fore, Style
from tabulate import tabulate

data = list(csv.DictReader(open('dataset.csv', 'r')))


def sort_rent(data, rent_only=True):
    tenants = sorted(data, key=lambda k: k['Current Rent'])
    if rent_only:
        rent_only_list = [tenant['Current Rent'] for tenant in tenants[:5]]
        print(rent_only_list)
    else:
        print(tenants[:5])
    
def long_tenancies(data, tenancy_time='25', print_table=False):
    long_tenant_list = [tenant for tenant in data if tenant['Lease Years'] == tenancy_time]
    if print_table:
        header = data[0].keys()
        rows = [x.values() for x in data]
        print(tabulate(rows, header, tablefmt='grid', numalign='center'))
    pprint(long_tenant_list, sort_dicts=False)
    all_rents = [rent['Current Rent'] for rent in long_tenant_list]
    total_rent = sum([int(float(x)) for x in all_rents])
    print(f"{Fore.RED}TOTAL RENT: {total_rent}{Style.RESET_ALL}")


def aggregate_tenant_masts(data):
    tenant_list = [tenant['Tenant Name'] for tenant in data]
    aggregated = dict.fromkeys(tenant_list)
    for k in aggregated.keys():
        total_masts = sum(x.get('Tenant Name') == k for x in data)
        aggregated.update({k: total_masts})
    pprint(aggregated)


if __name__ == "__main__":
    sort_rent(data)
    long_tenancies(data)
    aggregate_tenant_masts(data)