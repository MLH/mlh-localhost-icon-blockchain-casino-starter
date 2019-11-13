import os
from dotenv import load_dotenv

load_dotenv()

ICON_SERVICE_PROVIDER_URL = os.getenv(
    "ICON_SERVICE_PROVIDER_URL", "https://bicon.net.solidwallet.io/api/v3"
)
CASINO_SCORE_ADDRESS = os.getenv(
    "CASINO_SCORE_ADDRESS", "cx0000000000000000000000000000000000000000"
)
PLAYER_WALLET_PRIVATE_KEY_FILE_PATH = os.getenv(
    "PLAYER_WALLET_PRIVATE_KEY_FILE_PATH", "./keystores/keystore1.json"
)
PLAYER_WALLET_PASSWORD = os.getenv("PLAYER_WALLET_PASSWORD", "test1_Account")
BET_AMOUNT = int(os.getenv("BET_AMOUNT", 1000))
DEBUG = bool(os.getenv("DEBUG", True))
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", "5000")
