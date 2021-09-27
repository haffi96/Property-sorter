# Property-sorter

## A small project to help visualize info from a csv dataset about properties in an area of UK.

## Install

- You need atleast python3.8 for this project. Python3.9 recommended.
- In a virtualenv and from the root of the repository:
  Run `pip install -r requirements.txt`
- This will install the required libraries for running the main application and also the unit tests.

## Usuage

Commands to use:
From within `property-sorter/src`, run:

- `python sorter.py` to run all available commands
- `python sorter.py --help` to see all available commands
- `python sorter.py <command> --help` to see options for each command

To sort rent in ascending order:

- `python sorter.py sort-by-rent`
- Can also use `--count` to choose how many tenants to get info of. Default is 5.

To see tenants with a given lease period:

- `python sorter.py long-tenants`.
- Can set the period amount by using `--period` arguement. Default is 25 years.
- Can also use `--no-table` option to view info without tabulating. Default is to show in table.

To see how many masts each tenant has:

- `python sorter.py masts-per-tenant`
- Can use `--no-table` to view without tabulating. Default is to show in table.
- To see which tenants' contract lease start date fits between a certain period:
- `python sorter.py lease-dates`
- Can use `--start-date` or `s` to input a start date.
- Can use `--end-date` or `e` to input an end date.
  i.e
  `python sorter.py lease-dates -s '01 Aug 2007' -e '31 Aug 2007'`
  Note: Need to use dates with the same format as example.

## Unit test

Run unit tests with pytest from within the property-sorter/test directory

- `python -m pytest`
