# Buysol - Lysol Miner
Buys lysol for you as it comes back in stock on Amazon

## PreRecs
- Python 3.6.5+
- Chromium Driver Executable 

## Installation
```bash
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
source ./env/bin/activate
python3 ITEM={URL_OF_AMAZON_ITEM} UUID={AMZN_USER_ID} PASS={AMZN_USER_PASSWORD} main.py
```