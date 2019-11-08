from iconservice import *

TAG = "SLOT_MACHINE"
PAYOUT_MULTIPLIER = 10


class SlotMachine(IconScoreBase):
    _PLAY_RESULT = "PLAY_RESULT"

    @eventlog(indexed=1)
    def SlotMachine(self, _by: Address, amount: int, result: str):
        pass

    @eventlog(indexed=3)
    def FundTransfer(self, backer: Address, amount: int, is_contribution: bool):
        pass

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._play_results_array = ArrayDB(self._PLAY_RESULT, db, value_type=str)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    @external
    @payable
    def set_treasury(self) -> None:
        Logger.info(
            f"{self.msg.value} was added to the treasury from address {self.msg.sender}",
            TAG,
        )

    @external(readonly=True)
    def get_treasury(self) -> int:
        Logger.info(
            f"Amount in the treasury is {self.icx.get_balance(self.address)}", TAG
        )
        return self.icx.get_balance(self.address)

    @payable
    @external
    def play(self):
        # Write code here!

    @external(readonly=True)
    def get_results(self) -> dict:
        valueArray = []
        for value in self._play_results_array:
            valueArray.append(value)

        Logger.info(f"{self.msg.sender} is getting results", TAG)
        return {"result": valueArray}