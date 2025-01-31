def receive(self, recv):
    match self.cmd:
        case "quitter":
            if recv=="1":
                self.quit()
            else:
                print("Il y a eu une erreur lors de la déconnexion")
        case "aide":
            print("""aide: affiche ce message
solde: affiche ton solde
quitter: permet de quitter
nettoyer: efface l'écran""")
        case "nettoyer":
            print("\n"*50)
        case _:
            print(recv)