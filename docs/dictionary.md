# Data Dictionary — RetailIQ

## Table: transactions (SQLite → retail.db)
Source: UCI Online Retail II dataset (2009-12-01 to 2011-12-09)
Rows: 1,067,371 | Columns: 8

| Column       | Type     | Nullable | Description                                      |
|-------------|----------|----------|--------------------------------------------------|
| invoice      | TEXT     | No       | Invoice number. Prefix 'C' = cancellation/return |
| stockcode    | TEXT     | No       | Product code. 5-digit + optional letter          |
| description  | TEXT     | Yes      | Product name. 4,382 nulls                        |
| quantity     | INTEGER  | No       | Units per transaction. Negative = return         |
| invoicedate  | DATETIME | No       | Transaction timestamp. Range: 2009-12 to 2011-12 |
| price        | FLOAT    | No       | Unit price in GBP (£)                            |
| customer_id  | FLOAT    | Yes      | Unique customer ID. 243,007 nulls = guest orders |
| country      | TEXT     | No       | Customer country. 43 unique values               |

## Known Data Quality Issues
| Issue                          | Count     | Action (Weekend 2)              |
|-------------------------------|-----------|----------------------------------|
| Missing customer_id            | 243,007   | Drop for customer-level analysis |
| Missing description            | 4,382     | Fill with stockcode or drop      |
| Negative quantity (returns)    | ~20,000+  | Separate into returns table      |
| Zero/negative price            | TBD       | Drop — likely data entry errors  |
| Duplicate invoices             | TBD       | Investigate in EDA               |

## Derived columns (added in cleaning pipeline)
| Column       | Description                              |
|-------------|------------------------------------------|
| revenue      | quantity × price per line item           |
| is_return    | 1 if quantity < 0 or invoice starts 'C'  |
| year_month   | YYYY-MM extracted from invoicedate       |