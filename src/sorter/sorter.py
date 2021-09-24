#!/usr/bin/env python3
import csv
from pprint import pprint
from colorama import Fore, Style
from tabulate import tabulate
import click

DATA = list(csv.DictReader(open("dataset.csv", "r")))

@click.group()
def cli():
  pass


@cli.command('sort-by-rent')
@click.option('--rent_only/--details', default='True', help='Sort tenants info with rent: Low to high. Use --details for all available info on tenants')
@click.option('--count', default=5, help='Choose how many of the tenants you want to see the info of')
def sort_rent(rent_only, count):
    tenants = sorted(DATA, key=lambda k: k["Current Rent"])
    if rent_only:
        rent_only_list = [tenant["Current Rent"] for tenant in tenants[:count]]
        click.echo(f'{Fore.RED}{rent_only_list}')
    else:
        print(f'{Fore.GREEN}{tenants[:count]}')


@cli.command('long-tenants')
@click.option('--period', default='25', help='Choose lease period. --period=VALUE')
@click.option('--table/--no-table', default='False', help='Use --table to view in table format')
def long_tenancies(period, table):
    ## Get tenant list for the period specified. Default to 25 years
    long_tenant_list = [
        tenant for tenant in DATA if tenant["Lease Years"] == period
    ]
    pprint(long_tenant_list, sort_dicts=False)

    ## Print as a table if prompted
    if table:
        header = DATA[0].keys()
        rows = [x.values() for x in DATA]
        print(tabulate(rows, header, tablefmt="grid", numalign="center"))

    ## Calculate the total rent for the list of tenants that meet the lease year period
    all_rents = [rent["Current Rent"] for rent in long_tenant_list]
    total_rent = sum([int(float(x)) for x in all_rents])
    print(f"{Fore.RED}TOTAL RENT: {total_rent}{Style.RESET_ALL}")


@cli.command('masts-per-tenant')
def aggregate_tenant_masts():
    tenant_list = [tenant["Tenant Name"] for tenant in DATA]
    aggregated = dict.fromkeys(tenant_list)
    for k in aggregated.keys():
        total_masts = sum(x.get("Tenant Name") == k for x in DATA)
        aggregated.update({k: total_masts})
    pprint(aggregated)


if __name__ == "__main__":
    cli()
