import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEX_SCREENER_API = "https://api.dexscreener.com/latest/dex/tokens/"

def get_token_info(address):
    response = requests.get(f"{DEX_SCREENER_API}{address}")
    if response.status_code == 200:
        data = response.json()
        if 'pairs' in data and data['pairs']:
            pair = data['pairs'][0]
            return {
                'address': address,
                'name': pair['baseToken']['name'],
                'symbol': pair['baseToken']['symbol'],
                'chain': pair.get('chainId', 'Unknown'),  # Use 'chainId' instead of 'chain'
                'price': float(pair['priceUsd']),
                'fdv': float(pair.get('fdv', 0)),  # Use .get() with a default value
                'volume24h': float(pair['volume'].get('h24', 0)),  # Use .get() with a default value
                'priceChange24h': float(pair['priceChange'].get('h24', 0))  # Use .get() with a default value
            }
    return None

__all__ = ['get_token_info']