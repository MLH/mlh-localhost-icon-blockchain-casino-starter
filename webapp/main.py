import json

from flask import Flask, render_template, jsonify, request

from repeater import retry
from score_slot_machine import (
    create_transaction,
    get_casino_balance,
    get_player_balance,
    get_transaction,
    get_transactions,
)
import config

application = Flask(__name__)


@application.route("/api/transactions", methods=["GET"])
def get_transactions_route():
    transaction_list = get_transactions()

    score_balance = get_casino_balance()
    account_balance = get_player_balance()

    decending_ordered_transaction = sorted(
        transaction_list, key=lambda val: int(val["timestamp"]), reverse=True
    )

    latest_transaction = (
        decending_ordered_transaction[0]
        if len(decending_ordered_transaction) > 0
        else None
    )

    response = {
        "transaction_list": decending_ordered_transaction,
        "score_balance": score_balance,
        "account_balance": account_balance,
        "latest_transaction": latest_transaction,
    }

    return jsonify(response)


@application.route("/api/transactions", methods=["POST"])
def create_transaction_route():
    json_data = json.loads(request.data)
    multiplier = json_data.get("multiplier") or request.values.get(
        "multiplier", default=1, type=int
    )

    transaction_hash = create_transaction(multiplier=multiplier)

    return jsonify({"transaction": {"txHash": transaction_hash}})


@application.route("/api/transactions/<txhash>", methods=["GET"])
@retry(Exception, tries=10)
def get_transaction_route(txhash):
    trasaction = get_transaction(txhash)

    score_balance = get_casino_balance()
    account_balance = get_player_balance()

    return jsonify(
        {
            "transaction": trasaction,
            "account_balance": account_balance,
            "score_balance": score_balance,
        }
    )


@application.route("/")
def main():
    return render_template("index.html")


if __name__ == "__main__":
    application.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
