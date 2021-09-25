from click.testing import CliRunner
import csv

from click.types import DateTime
from src.sorter import aggregate_tenant_masts, choose_lease_dates, long_tenancies, sort_rent
import ast
import io
from contextlib import redirect_stdout
import pytest
import re

DATA = list(csv.DictReader(open("dataset.csv", "r")))


## The unit tests below can definitely be extended.
## Firstly, they only really test the default cases or the easily testable code paths.
## Would be better to extend them to use mock data and test all cases.
## The unit testing available for click applications also doesn't seem that great or 
## I may have missed built in method in click.testing. So made a couple helper functions 
## to be able to use the stdout that we see in console.

def _convert_stdout_to_list(stdout, get_full_data=False):
    data_list = stdout.rpartition("--")
    tenant_info = data_list[0].rstrip()
    tenant_list = ast.literal_eval(tenant_info)
    if get_full_data:
        return tenant_list, data_list
    else:
        return tenant_list


def test_cli_exec():
    runner = CliRunner()
    result = runner.invoke(sort_rent)
    result = runner.invoke(long_tenancies)
    result = runner.invoke(aggregate_tenant_masts)
    result = runner.invoke(choose_lease_dates)
    assert result.exit_code == 0


def test_rent_sorter():
    runner = CliRunner()
    result = runner.invoke(sort_rent, ["--rent-only"])
    l = result.stdout
    x = ast.literal_eval(l)
    length = len(x)
    assert length == 5  ## Check length
    for i, item in enumerate(x):
        assert all(
            x[i] <= x[i + 1] for i in range(length - 1)
        )  ## Check if always in ascending order


def test_long_tenancies():
    runner = CliRunner()
    result = runner.invoke(long_tenancies, ["--no-table"])
    tenant_list = _convert_stdout_to_list(result.stdout)
    for entry in tenant_list:
        assert int(entry["Lease Years"]) == 25


def test_long_tenancies_total():
    runner = CliRunner()
    result = runner.invoke(long_tenancies, ["--no-table"])
    tenant_list, data_list = _convert_stdout_to_list(result.stdout, get_full_data=True)
    rent = []
    for entry in tenant_list:
        rent.append(int(float(entry["Current Rent"])))
    stdout_total = data_list[2].rstrip()
    total = int("".join(x for x in stdout_total if x.isdigit()))
    assert sum(rent) == total
