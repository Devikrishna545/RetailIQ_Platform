# Learnings Log

## Weekend 1
Set up the full project scaffold with reproducible tooling (black, 
ruff, pre-commit)Learned about the config file pyproject.toml. Loaded 1M+ real 
retail transactions into SQLite and discovered that 22% of rows have no customer ID (guest checkouts), 
the UK accounts for 96% of revenue, and one-time buyers represent 27% 
of the customer base — all of which will drive modelling decisions ahead.

## Weekend 2
Cleaned 1M rows down to 779K valid purchase transactions with zero 
missing values by separating returns, dropping guest checkouts, and 
capping outliers using domain thresholds rather than blindly applying 
IQR. Discovered two statistically significant findings: non-UK customers 
spend nearly double per order (£875 vs £489, p≈0), and return rates 
differ significantly by region (Chi2=593, p≈0) — both will become 
features in the churn model.