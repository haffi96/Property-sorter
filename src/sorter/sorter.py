#!/usr/bin/env python3
import csv
from pprint import pprint
from colorama import Fore, Style
from tabulate import tabulate
import click
from datetime import date, datetime


DATA = list(csv.DictReader(open("dataset.csv", "r")))


@click.group()
def cli():
    pass


@cli.command("sort-by-rent")
@click.option(
    "--rent_only/--details",
    default="True",
    help="Sort tenants info with rent: Low to high. Use --details for all available info on tenants",
)
@click.option(
    "--count",
    default=5,
    help="Choose how many of the tenants you want to see the info of",
)
def sort_rent(rent_only, count):
    tenants = sorted(DATA, key=lambda k: k["Current Rent"])
    if rent_only:
        rent_only_list = [tenant["Current Rent"] for tenant in tenants[:count]]
        click.echo(f"{Fore.RED}{rent_only_list}")
    else:
        click.echo(f"{Fore.GREEN}{tenants[:count]}")


@cli.command("long-tenants")
@click.option("--period", default="25", help="Choose lease period. --period=VALUE")
@click.option(
    "--table/--no-table", default="True", help="Use --table to view in table format"
)
def long_tenancies(period, table):
    ## Get tenant list for the period specified. Default to 25 years
    long_tenant_list = [tenant for tenant in DATA if tenant["Lease Years"] == period]

    ## Print as a table if prompted
    if table:
        for x, tenant in enumerate(long_tenant_list):
            click.echo(f"{Fore.RED} Tenant No. {x+1}{Style.RESET_ALL}")
            table_fmt = tabulate(tenant.items(), tablefmt="grid")
            click.echo(table_fmt)
    else:
        pprint(long_tenant_list, sort_dicts=False)

    ## Calculate the total rent for the list of tenants that meet the lease year period
    all_rents = [rent["Current Rent"] for rent in long_tenant_list]
    total_rent = sum([int(float(x)) for x in all_rents])
    click.echo(f"{Fore.RED}TOTAL RENT: {total_rent}{Style.RESET_ALL}")


@cli.command("masts-per-tenant")
@click.option(
    "--table/--no-table", default="False", help="Use --table to view in table format"
)
def aggregate_tenant_masts(table):
    tenant_list = [tenant["Tenant Name"] for tenant in DATA]
    aggregated = dict.fromkeys(tenant_list)
    for k in aggregated.keys():
        total_masts = sum(x.get("Tenant Name") == k for x in DATA)
        aggregated.update({k: total_masts})
    if table:
        disp_list = aggregated.items()
        click.echo(
            tabulate(disp_list, headers=["TENANT", "TOTAL MASTS"], tablefmt="grid")
        )
    else:
        pprint(aggregated)


from datetime import datetime


@cli.command("lease-dates")
@click.option(
    "--start_date",
    default="1 June 1999",
    help="Specify date to filter from. Use format 'd mon yyy'",
)
@click.option(
    "--end_date",
    default="31 August 2007",
    help="Specify date to filter to. Use format 'd mon yyy'",
)
def choose_least_dates(start_date=None, end_date=None):
    start = datetime.strptime(start_date, "%d %B %Y")
    end = datetime.strptime(end_date, "%d %B %Y")
    for x in DATA:
        x.update(
            (k, datetime.strptime(v, "%d %b %Y"))
            for k, v in x.items()
            if k == "Lease Start Date"
        )
    new_list = []
    for x in DATA:
        if end > x["Lease Start Date"] > start:
            x.update(
                (k, datetime.strftime(v, "%d/%m/%Y"))
                for k, v in x.items()
                if k == "Lease Start Date"
            )
            new_list.append(x)
    for x, tenant in enumerate(new_list):
        click.echo(f"{Fore.RED} Tenant No. {x+1}{Style.RESET_ALL}")
        table_fmt = tabulate(tenant.items(), tablefmt="grid")
        click.echo(table_fmt)


if __name__ == "__main__":
    cli()
