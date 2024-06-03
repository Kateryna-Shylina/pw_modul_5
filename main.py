import sys
import aiohttp
import asyncio
import platform
from datetime import datetime, timedelta


async def main(date):

    async with aiohttp.ClientSession() as session:
        url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
        
        async with session.get(url) as response:
            result = await response.json()
            return result

def transform_data(data):
    date = data['date']
    exchange_rates = data['exchangeRate']
    
    transformed_data = {date: {}}
    
    for rate in exchange_rates:
        currency = rate['currency']
        if currency == 'EUR' or currency == 'USD':
            sale = rate.get('saleRate', rate.get('saleRateNB'))
            purchase = rate.get('purchaseRate', rate.get('purchaseRateNB'))
            
            if sale is not None and purchase is not None:
                transformed_data[date][currency] = {
                    'sale': sale,
                    'purchase': purchase
                }
    
    return transformed_data

if __name__ == "__main__":
    dates = sys.argv[1]
    try:
        number_of_days = int(dates)
        if number_of_days > 10:
            raise ValueError("You can only view data for the last 10 days.")
        else:
            if platform.system() == 'Windows':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())    

            exchange_rates = list()

            for day in range(number_of_days):
                d = datetime.now() - timedelta(days=day)
                shift = d.strftime("%d.%m.%Y")
                exchange_rates_json = asyncio.run(main(shift))
                new_json = transform_data(exchange_rates_json)
                exchange_rates.append(new_json)

            print(exchange_rates)
    except ValueError as e:
        print(e)
        


    
    
    


    