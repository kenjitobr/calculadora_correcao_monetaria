import requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal, getcontext
import ipeadatapy as ipea

app = Flask(__name__)

# Set precision for Decimal calculations to avoid floating point issues
getcontext().prec = 5 # Sufficient for currency, adjust if needed for more precision

igpm_series_code = 'IGP12_IGPMG12' # IGP-M - Índice Geral de Preços - Mercado (Variação Mensal)
ipca_series_code = 'PRECOS12_IPCAG12' # IPCA - Índice Nacional de Preços ao Consumidor Amplo (Variação Mensal)
igpm_all = ipea.timeseries(igpm_series_code) # Uses ipeadatapy to fetch entire IGP-M data once
igpm_all_last_3_columns = igpm_all.iloc[:, -3:] # Trim the DataFrame to provide only MONTH, YEAR, VALUE columns
ipca_all = ipea.timeseries(ipca_series_code) # Uses ipeadatapy to fetch entire IPCA data once
ipca_all_last_3_columns = ipca_all.iloc[:, -3:] # Trim the DataFrame to provide only MONTH, YEAR, VALUE columns

# Fetch IPCA data using ipeadatapy (PRECOS12_IPCAG12)
def fetch_ipca_data():
    print(f"Fetching IPCA from Ipeadata (PRECOS12_IPCAG12)")
    
    try:
        ipca_rates = {}
        for index, row in ipca_all_last_3_columns.iterrows():
            month_key = index.strftime('%Y-%m')
            rate = Decimal(str(row.iloc[2])) / 100 
            ipca_rates[month_key] = rate
            
        return ipca_rates
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching IPCA data from Ipeadata: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching IPCA data from Ipeadata: {e}")
        return None

# Fetch IGP-M data using ipeadatapy (IGP12_IGPMG12)
def fetch_igpm_data():
    print(f"Fetching IGP-M from Ipeadata (IGP12_IGPMG12)")

    try:
        igpm_rates = {}
        for index, row in igpm_all_last_3_columns.iterrows():
            month_key = index.strftime('%Y-%m')
            rate = Decimal(str(row.iloc[2])) / 100 
            igpm_rates[month_key] = rate
            
        return igpm_rates
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching IGP-M data from Ipeadata: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching IGP-M data from Ipeadata: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    initial_date_str = data.get('initialDate')
    final_date_str = data.get('finalDate')
    index_type = data.get('indexType')
    final_monetary_value_str = data.get('finalMonetaryValue')

    try:
        initial_date = datetime.strptime(initial_date_str, '%Y-%m-%d').date()
        final_date = datetime.strptime(final_date_str, '%Y-%m-%d').date()
        final_monetary_value = Decimal(final_monetary_value_str)

        if initial_date >= final_date:
            return jsonify({"error": "Initial date must be before final date."}), 400

        if index_type == 'IPCA':
            index_data = fetch_ipca_data()
        elif index_type == 'IGPM':
            index_data = fetch_igpm_data()
        else:
            return jsonify({"error": "Invalid economic index type."}), 400

        if index_data is None:
            return jsonify({"error": f"Could not retrieve {index_type} data for the specified period. Please check dates or try again later."}), 500

        current_value = final_monetary_value
        calculation_steps = []
        
        current_month_to_correct = final_date.replace(day=1)

        while current_month_to_correct >= initial_date.replace(day=1):
            
            month_key = current_month_to_correct.strftime('%Y-%m')
            
            monthly_rate = index_data.get(month_key)

            if monthly_rate is None:
                print(f"Missing {index_type} data for {month_key}.")
                return jsonify({"error": f"Missing {index_type} data for {month_key}. Calculation aborted. Data might not be available for the entire period."}), 500
            
            current_value = current_value / (Decimal('1') + monthly_rate)
            
            calculation_steps.append({
                "month": month_key,
                "rate": f"{(monthly_rate * 100):.2f}",
                "value": f"{current_value:.2f}"
            })

            current_month_to_correct -= relativedelta(months=1)
            
        initial_monetary_value = current_value
        
        return jsonify({
            "initialMonetaryValue": f"{initial_monetary_value:.2f}",
            "calculationSteps": calculation_steps
        })

    except ValueError:
        return jsonify({"error": "Invalid date or monetary value format. Please use YYYY-MM-DD for dates and a valid number for monetary value."}), 400
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": f"An unexpected server error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
