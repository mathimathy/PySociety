def receive(self, recv):
    match recv:
        case "solde":
            self.cryptedSend(f"Solde: {self.amount}")
        case "quitter":
            try:
                self.cryptedSend("1")
                self.quit()
            except:
                self.cryptedSend("0")
        case _:
            self.cryptedSend("Cette commande n'existe pas")