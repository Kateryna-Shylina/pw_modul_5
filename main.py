import sys
import aiohttp
import asyncio
import platform
from datetime import datetime, timedelta


async def get_exchange_rates(session, date):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'
    try:
        async with session.get(url) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                print(f"Error status: {response.status} for {url}")
                return None
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))
        return None


async def main(dates):
    async with aiohttp.ClientSession() as session:
        tasks = list()
        for date in dates:
            tasks.append(get_exchange_rates(session, date)) 
                
        all_exchange_rates = await asyncio.gather(*tasks)

        exchange_rates = list()
        for exchange_rate in all_exchange_rates:
            new_exchange_rate = create_json(exchange_rate)
            exchange_rates.append(new_exchange_rate)
        
        return exchange_rates

                
def create_json(data):
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
            date_list = list()
            for day in range(number_of_days):
                d = datetime.now() - timedelta(days=day)
                shift = d.strftime("%d.%m.%Y")
                date_list.append(shift)
            
            if platform.system() == 'Windows':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())    

            exchange_rates = list()  
            exchange_rates = asyncio.run(main(date_list))

            print(exchange_rates)
    except ValueError as e:
        print(e)
        


    
    
    


    