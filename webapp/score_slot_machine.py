import ast

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import CallTransactionBuilder
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet

import config

CASINO_SCORE_ADDRESS = config.CASINO_SCORE_ADDRESS
BET_AMOUNT = config.BET_AMOUNT

icon_service = IconService(HTTPProvider(config.ICON_SERVICE_PROVIDER_URL))

player_wallet = KeyWallet.load(
    config.PLAYER_WALLET_PRIVATE_KEY_FILE_PATH, config.PLAYER_WALLET_PASSWORD
)

def get_wallet_balance(wallet_address):
    return icon_service.get_balance(wallet_address)


def get_casino_balance():
    return get_wallet_balance(CASINO_SCORE_ADDRESS)


def get_player_balance():
    return get_wallet_balance(player_wallet.get_address())


# Returns a list of recent transactions
def get_transactions():
    call = (
        CallBuilder()
        .from_(player_wallet.get_address())
        .to(CASINO_SCORE_ADDRESS)
        .method("get_results")
        .params({})
        .build()
    )
    result = icon_service.call(call)

    transaction_list = []
    for resultVal in result["result"]:
        transaction_list.append(ast.literal_eval(resultVal))

    return transaction_list


# Create a new transaction and returns its hash
def create_transaction(multiplier=1):
    transaction = (
        CallTransactionBuilder()
        .from_(player_wallet.get_address())
        .to(CASINO_SCORE_ADDRESS)
        .method("play")
        .value(BET_AMOUNT * multiplier)
        .step_limit(2000000)
        .nid(3)
        .nonce(100)
        .params({})
        .build()
    )

    signed_transaction = SignedTransaction(transaction, player_wallet)
    signed_transaction_hash = icon_service.send_transaction(signed_transaction)
    print('Transaction hash: {} '.format(signed_transaction_hash))
    return signed_transaction_hash


# Find a transaction by its hash in the list of recent transactions
def get_transaction(txhash):
    transaction_list = get_transactions()

    transaction = next(
        (
            tx
            for tx in transaction_list
            if (tx["txHash"] in (txhash) or txhash in tx["txHash"])
        ),
        None,
    )

    if not transaction:
        raise Exception("Transaction not ready yet!")

    return transaction
