![test-badge](https://github.com/danielschweigert/pypgsync/actions/workflows/lint-and-test.yml/badge.svg)

[//]: # (![coverage-badge]&#40;https://raw.githubusercontent.com/danielschweigert/pypgsync/main/coverage-manual.svg&#41;)

# pypgsync
Python utility to sync two postgresql databases


## Installation

```bash
pip install pypgsync
```

## Usage
Given two databases, pypgsync can determine which records differ. In the `primarykey` use case, 
records are identified by their primary key.
```python
import psycopg
from pypgsync.mode.primarykey import delta_by_primary_key, apply_delta_by_primary_key

con_source = psycopg.connect(host="host_source", dbname="db_source", user="user_source", 
                             password="secret_source")
con_destination = psycopg.connect(host="host_destination", dbname="db_destination", 
                                  user="user_destination", password="secret_destination")

cur_source = con_source.cursor()
cur_destination = con_destination.cursor()

delta = delta_by_primary_key(cur_source=cur_source, cur_destination=cur_destination,
                                 table_name="products", primary_key="id",
                                 columns=["name", "count", "price"], pk_values=[1, 2, 3, 4, 5],)
```
`delta` provides an overview of the differences between the two database tables, in terms of which 
database operations (`delete`, `insert`, `update`) have to be applied to the destination database 
in order to match the source database. The primary key identifies the rows that have to be modified.
```console
{
    "table_name": "products",
    "primary_key": "id",
    "intersection": set([1, 2]),
    "delete": set([3, ]),
    "insert": [{"id": 5, "name": "bread", "count": 5, "price": 3.2}],
    "update": [{"id": 2, "count": 20}, ]
}
```
`delta` can then be used to apply the necessary changes to the destination database.
```python
from pypgsync.mode.primarykey import apply_delta_by_primary_key

apply_delta_by_primary_key(con_destination, delta)
```
After which the two database tables are identical within the column and primary key range specified.

To accomplish the sync in one step, use the `sync_by_primary_key` function.
```python
from pypgsync.mode.primarykey import sync_by_primary_key
sync_by_primary_key(cur_source, con_destination, table_name="products", primary_key="id")
```
