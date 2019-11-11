(() => {
  const CREDIT_IN_ICX = 10 ** 10;
  const parseJson = data => data.json();

  const SlotMachineAPI = {
    async getTransactions() {
      return fetch("/api/transactions").then(parseJson);
    },
    async createTransaction(multiplier = 1) {
      const { transaction: { txHash } = {} } = await fetch(
        "/api/transactions",
        { method: "POST", body: JSON.stringify({ multiplier }) }
      ).then(parseJson);

      return fetch(`/api/transactions/${txHash}`).then(parseJson);
    }
  };

  const SlotMachineUI = {
    getSlots: () => $(".slot-machine--slots .slot-machine--slot--container"),
    getPlayButton: () => $("#button--play"),
    getIncreaseMultiplierButton: () => $("#button--increase-multiplier"),
    getDecreaseMultiplierButton: () => $("#button--decrease-multiplier"),
    getStatusDisplay: () => $("#slot-machine--result"),
    getCreditsDisplay: () => $("#slot-machine--credits"),
    getPrizeDisplay: () => $("#slot-machine--prize"),
    getBetValueDisplay: () => $("#slot-machine--bet-value"),
    getBetValue() {
      return parseInt(this.getBetValueDisplay().text());
    },

    enablePlayButton() {
      this.getPlayButton().attr("disabled", false);
    },
    disablePlayButton() {
      this.getPlayButton().attr("disabled", true);
    },

    initSlots() {
      this.getSlots().each(function() {
        const $slot = $(this);
        const slotMachineController = $slot.slotMachine();
        $slot.data("slot-machine", slotMachineController);
      });
    },
    runSlots() {
      this.getSlots().each(function() {
        const $slot = $(this);
        const slotMachineController = $slot.data("slot-machine");
        slotMachineController.shuffle(99999);
      });
    },
    stopSlots(slots) {
      this.getSlots().each(function(index) {
        const $slot = $(this);
        const slotMachineController = $slot.data("slot-machine");

        slotMachineController.changeSettings({
          randomize: () => slots[index]
        });

        slotMachineController.stop();
      });
    },

    updateBalance(balance = 0, { animate = false, hasWon = false } = {}) {
      const credits = Math.floor(balance / CREDIT_IN_ICX);
      if (animate) {
        this.getCreditsDisplay().addClass(
          `updating ${hasWon ? "win" : "loss"}`
        );
      }

      setTimeout(() => {
        this.getCreditsDisplay().html(credits);

        if (animate) {
          this.getCreditsDisplay().removeClass("updating win loss");
        }
      }, 1000);
    },
    updateBetValue(betValue = 1) {
      this.getBetValueDisplay().html(betValue);
    },
    updateDisplay(text, type = "default") {
      const $display = this.getStatusDisplay();
      const classes = `slot-machine--result-display slot-machine--result-display-${type}`;

      $display.html(text).attr("class", classes);
    },
    updatePrize(balance = 0, { animate = false, hasWon = false } = {}) {
      const multiplier = this.getBetValue();
      const creditsPrize = Math.floor(balance / CREDIT_IN_ICX);

      if (animate) {
        this.getPrizeDisplay().addClass(`updating ${hasWon ? "win" : "loss"}`);
      }

      setTimeout(() => {
        this.getPrizeDisplay().html(creditsPrize);

        if (animate) {
          this.getPrizeDisplay().removeClass("updating win loss");
        }
      }, 1000);
    },

    async placeBet() {
      const multiplier = this.getBetValue();

      this.disablePlayButton();
      this.updateDisplay($("<marquee>Good Luck!</marquee>"));
      this.runSlots();

      try {
        const {
          transaction,
          account_balance: balance,
          score_balance: slotMachineBalance
        } = await SlotMachineAPI.createTransaction(multiplier);
        const hasWon = transaction && transaction.result;
        if (hasWon) {
          var s = Math.floor(Math.random() * 4); 
          var slots = [s,s,s];
        } else {
          var slots = [Math.floor(Math.random() * 4) + 2, Math.floor(Math.random() * 2), Math.floor(Math.random() * 4)];
          
        }
        this.stopSlots(slots);
        this.updateDisplay(hasWon ? "WON" : "LOST", hasWon ? "win" : "loss");
        this.updateBalance(balance, { animate: true });
        this.updatePrize(slotMachineBalance, { animate: true });
      } catch (error) {
        this.stopSlots([0, 0, 0]);
        this.updateDisplay("Sorry, an error happened. Try again!", "error");

        console.error("Error placing the bet", error);
      }

      this.enablePlayButton();
    },

    async init() {
      const {
        account_balance: balance,
        score_balance: slotMachineBalance
      } = await SlotMachineAPI.getTransactions();

      this.initSlots();
      this.enablePlayButton();
      this.updateBalance(balance);
      this.updatePrize(slotMachineBalance);

      const $buttonPlay = this.getPlayButton();

      this.getDecreaseMultiplierButton()
        .unbind("click")
        .on("click", () => {
          this.updateBetValue(
            Math.max(1, this.getBetValueDisplay().text() / 10)
          );
        });
      this.getIncreaseMultiplierButton()
        .unbind("click")
        .on("click", () => {
          this.updateBetValue(
            Math.min(1000, this.getBetValueDisplay().text() * 10)
          );
        });
      $buttonPlay.unbind("click").on("click", () => this.placeBet());
    }
  };

  $(document).ready(() => {
    SlotMachineUI.init();
  });
})();
