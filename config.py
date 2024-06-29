print("tryna work")

import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
DATABASE_URL = os.getenv('DATABASE_URL')
DUPLICATE_CHANNEL_ID = int(os.getenv('DUPLICATE_CHANNEL_ID'))

print(f"Database URL: {DATABASE_URL}")  # Print the DATABASE_URL to verify