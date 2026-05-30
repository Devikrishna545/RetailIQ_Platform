# RetailIQ — Customer Intelligence Platform

End-to-end ML capstone project covering EDA, segmentation, churn 
prediction, forecasting, recommenders, NLP, and AI assistant.

## Stack
Python 3.11 · scikit-learn · XGBoost · LightGBM · PyTorch · 
HuggingFace · FastAPI · Streamlit · MLflow · Docker · LangChain

## Dataset
UCI Online Retail II (~1M transactions) + Amazon Fine Food Reviews

## Setup
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Data + Run Order
1. Place the dataset at `data/online_retail_II.xlsx`.
2. Run ingestion: `python src/data/load_retail.py`
3. Run cleaning: `python src/data/clean.py`
4. Run SQL exploration: `python src/data/explore_sql.py`

## Results
_(to be filled as weekends progress)_

## Architecture
_(diagram to be added Weekend 10)_