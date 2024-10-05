from collections import defaultdict
import numpy as np
import numpy_financial as npf  
from datetime import datetime

# FIFO 
def apply_fifo(transactions):
    folio_units = defaultdict(list)
    
    for transaction in transactions:
        scheme = transaction.get('schemeName')
        folio = transaction.get('folio')
        units = float(transaction.get('decimalUnits', 0))  
        price = float(transaction.get('costValue', 0)) 

        
        if units > 0:
            folio_units[(scheme, folio)].append({'units': units, 'price': price})

        
        elif units < 0:
            units_to_sell = abs(units)
            while units_to_sell > 0 and folio_units[(scheme, folio)]:
                available = folio_units[(scheme, folio)][0]
                if available['units'] <= units_to_sell:
                    units_to_sell -= available['units']
                    folio_units[(scheme, folio)].pop(0)  
                else:
                    available['units'] -= units_to_sell  
                    units_to_sell = 0

    return folio_units


def calculate_portfolio_value(folio_units):
    total_value = 0
    total_gain = 0

    for (scheme, folio), unit_list in folio_units.items():
        total_units = sum(item['units'] for item in unit_list)
        
       
        current_nav = 60  

        
        portfolio_value = total_units * current_nav
        total_value += portfolio_value

       
        acquisition_cost = sum(item['units'] * item['price'] for item in unit_list)
        gain = portfolio_value - acquisition_cost
        total_gain += gain

    return total_value, total_gain


def xirr(transactions, current_value):
    cash_flows = []
    for trxn in transactions:
        date = datetime.strptime(trxn.get('lastTrxnDate', '1970-01-01'), '%d-%b-%Y')  
        amount = float(trxn.get('costValue', 0))  
        cash_flows.append((date, -amount))

    today = datetime.today()
    cash_flows.append((today, current_value))

    def xirr_calc(cash_flows):
        amounts = [cf[1] for cf in cash_flows]
       
        return npf.irr(amounts)

    return xirr_calc(cash_flows)
