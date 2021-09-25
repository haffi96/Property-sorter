#!/usr/bin/env python3
import csv
from pprint import pprint
from colorama import Fore, Style
from tabulate import tabulate
import click
from datetime import datetime


DATA = list(csv.DictReader(open("dataset.csv", "r")))


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(f"Running everything as no subcommands given...")
        do_everything(ctx)
    else:
        click.echo(f"Running {ctx.invoked_subcommand}...")


def do_everything(ctx):
    step_one_result = ctx.invoke(sort_rent)
    step_two_result = ctx.invoke(long_tenancies)
    step_one_result = ctx.invoke(aggregate_tenant_masts)
    step_one_result = ctx.invoke(choose_lease_dates)


def _tabulate_list(data_list):
    for x, tenant in enumerate(data_list):
        ## Printing the this log line acts as a separator between the tables for each tenant
        click.echo(f"{Fore.RED} Tenant No. {x+1}{Style.RESET_ALL}")
        table_fmt = tabulate(tenant.items(), tablefmt="grid")
        click.echo(table_fmt)


def _convert_string_date_to_datetime(string_date):
    return datetime.strptime(string_date, "%d %b %Y")


@cli.command("sort-by-rent")
@click.option(
    "--rent-only/--details",
    default="True",
    help="Sort tenants info with rent: Low to high. Use --details for all available info on tenants",
)
@click.option(
    "--count",
    default=5,
    help="Choose how many of the tenants you want to see the info of",
)
def sort_rent(rent_only, count):
    """Sort by rent from low to high"""
    tenants = sorted(DATA, key=lambda k: k["Current Rent"])

    ## By default, only print the rent info
    if rent_only:
        rent_only_list = [tenant["Current Rent"] for tenant in tenants[:count]]
        click.echo(f"{rent_only_list}")
        return rent_only_list
    else:
        ## If prompted, print out details for all the resultant tenants
        data_list = tenants[:5]
        _tabulate_list(data_list)


@cli.command("long-tenants")
@click.option("--period", default="25", help="Choose lease period. --period=VALUE")
@click.option(
    "--table/--no-table", default="True", help="Use --table to view in table format"
)
def long_tenancies(period, table):
    """Get tenants with a certain lease period i.e 25 years (default)"""
    ## TODO: If period is specified and doesn't exactly match any tenants details. Show the closest ones that match.
    long_tenant_list = [tenant for tenant in DATA if tenant["Lease Years"] == period]

    ## Print as a table by default
    if table:
        _tabulate_list(long_tenant_list)
    else:
        print(long_tenant_list)

    ## Calculate the total rent for the list of tenants that meet the lease year period
    all_rents = [rent["Current Rent"] for rent in long_tenant_list]
    total_rent = sum([int(float(x)) for x in all_rents])
    click.echo(f"--TOTAL RENT: {total_rent}")


@cli.command("masts-per-tenant")
@click.option(
    "--table/--no-table", default="True", help="Use --table to view in table format"
)
def aggregate_tenant_masts(table):
    """View total masts for each tenant"""
    tenant_list = [tenant["Tenant Name"] for tenant in DATA]
    ## Create a new dict where the tenant names are the keys
    aggregated = dict.fromkeys(tenant_list)
    ## Calculate total masts per tenant
    for k in aggregated.keys():
        total_masts = sum(x.get("Tenant Name") == k for x in DATA)
        aggregated.update({k: total_masts})
    ## Give an optional interface to disable tables output
    if table:
        disp_list = aggregated.items()
        click.echo(
            tabulate(disp_list, headers=["TENANT", "TOTAL MASTS"], tablefmt="grid")
        )
    else:
        ## Pretty print to make it more readable on the console
        pprint(aggregated)


@cli.command("lease-dates")
@click.option(
    "--start_date",
    "-s",
    default="01 Jun 1999",
    help="Specify date to filter from. Use format 'dd mon yyy'",
)
@click.option(
    "--end_date",
    "-e",
    default="31 Aug 2007",
    help="Specify date to filter to. Use format 'dd mon yyy'",
)
def choose_lease_dates(start_date=None, end_date=None):
    """View properties with starting lease dates between a certain period"""
    ## Convert date fields to datetime objects. Makes sorting easier
    start = _convert_string_date_to_datetime(start_date)
    end = _convert_string_date_to_datetime(end_date)
    for x in DATA:
        ## Update the tenant dicts datefield format to datetime.
        ## I think ideally probably would be better to avoid
        ## mutating the original dicts but couln't think of a quick
        ## way to do that here
        x.update(
            (k, _convert_string_date_to_datetime(v))
            for k, v in x.items()
            if k == "Lease Start Date"
        )
    ## Initialize a new list to filter out tenants that meet the date requirements
    new_list = []
    for x in DATA:
        if end > x["Lease Start Date"] > start:
            ## Change formate back to readable format for console
            ## TODO: Also change the Lease End Date format
            x.update(
                (k, datetime.strftime(v, "%d/%m/%Y"))
                for k, v in x.items()
                if k == "Lease Start Date"
            )
            new_list.append(x)
    _tabulate_list(new_list)


if __name__ == "__main__":
    cli()
