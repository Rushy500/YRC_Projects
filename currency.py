#This code is about converting money from one currency to another currency
def get_exchange_rates():
  exchange_rates = {
    "USD": {"EUR": 0.917, "JPY": 158.37, "GBP": 0.771, "INR": 83.573, "PHP": 58.32, "THB": 36.248, "CNY": 7.273, "RUB": 87.468, "BHD": 0.376},#United states dollars
    "EUR": {"USD": 1.090, "JPY": 172.65, "GBP": 0.840, "INR": 91.112, "PHP": 63.593, "THB": 39.417, "CNY": 7.911, "RUB": 95.385, "BHD": 0.409},#Euro
    "JPY": {"USD": 0.006, "EUR": 0.005, "GBP": 0.004, "INR": 0.527, "PHP": 0.375, "THB": 0.232, "CNY": 0.046, "RUB": 0.562, "BHD": 0.002},#Japanese yen
    "GBP": {"USD": 1.297, "EUR": 1.189, "JPY": 205.39, "INR": 108.39, "PHP": 75.518, "THB": 46.746, "CNY": 9.395, "RUB": 114.46, "BHD": 0.485},#British pound sterling
    "INR": {"USD": 0.012, "EUR": 0.010, "JPY": 1.894, "GBP": 0.009, "PHP": 0.698, "THB": 0.432, "CNY": 0.086, "RUB": 1.06, "BHD": 0.004},#Indian rupees
    "PHP": {"USD": 0.017, "EUR": 0.015, "JPY": 2.666, "GBP": 0.013, "INR": 1.431, "THB": 0.618, "CNY": 0.123, "RUB": 1.46, "BHD": 0.006},#Philippine Peso
    "THB": {"USD": 0.027, "EUR": 0.025, "JPY": 4.301, "GBP": 0.021, "INR": 2.314, "PHP": 1.617, "CNY": 0.20, "RUB": 2.362, "BHD": 0.01},#Thai Baht
    "CNY": {"USD": 0.137, "EUR": 0.126, "JPY": 21.433, "GBP": 0.106, "INR": 11.504, "PHP": 8.066, "THB": 4.986, "RUB": 11.783, "BHD": 0.051},#Chinese Yuan Renminbi
    "RUB": {"USD": 0.011, "EUR": 0.001, "JPY": 1.778, "GBP": 0.008, "INR": 0.943, "PHP": 0.684, "THB": 0.423, "CNY": 0.084, "BHD": 0.004},#Russian Ruble
    "BHD": {"USD": 2.659, "EUR": 2.441, "JPY": 414.649, "GBP": 2.059, "INR": 222.6, "PHP": 155.43, "THB": 96.078, "CNY": 19.269, "RUB": 227.05},#Bahraini Dinar
  }
  return exchange_rates

def convert_currency(amount, from_currency, to_currency):
  exchange_rates = get_exchange_rates()
  
  if from_currency not in exchange_rates or to_currency not in exchange_rates:
    return "Invalid currency code"
  
  converted_amount = amount * exchange_rates[from_currency][to_currency]
  return converted_amount

def main():
  print("Currency Converter")
  
  amount = float(input("Enter the amount: "))
  from_currency = input("Enter the from currency (e.g., USD, EUR, INR, PHP, THB, CNY, RUB, BHD): ").upper()
  to_currency = input("Enter the to currency (e.g., USD, EUR, INR, PHP, THB, CNY, RUB, BHD): ").upper()
  
  result = convert_currency(amount, from_currency, to_currency)
  
  if isinstance(result, str):
    print(result)
  else:
    print(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}")

if __name__ == "__main__":
  main()
