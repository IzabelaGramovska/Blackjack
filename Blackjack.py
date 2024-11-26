import random 

suites = ["Hearts", "Spades", "Diamonds", "Clubs"] 
values = {"Two":2, "Three":3, "Four":4, "Five":5, "Six":6, "Seven":7, "Eight":8, "Nine":9, "Ten":10, "Jack":10, "Queen":10, "King":10, "Ace":1} 
ranks = list(values.keys()) 

class Card: 
    def __init__(self, rank, suite): 
        self.rank = rank 
        self.suite = suite 
        self.value = values[rank] 
        
    def __str__(self): 
        return f"{self.rank} of {self.suite}" 

class Deck: 
    @classmethod 
    def create_deck(cls): 
        return [Card(rank, suite) for rank in ranks for suite in suites] 
        
class Box: 
    def __init__(self, position, wager, cards): 
        self.position = position 
        self.wager = wager 
        self.cards = cards 
        self.result = 0 
        self.blackjack = False 
        self.profit = 0 
        self.insurance = False 
        self.busted = False 
        self.surrender = False
        self.splitted = False
        self.addedten = False
        
class Player: 
    def __init__(self, name): 
        self.name = name 
        self.balance = 0 
        self.boxespositions = [] 
        self.boxes = [] 
        
    @classmethod 
    def take_player_balance(cls): 
        balance = input("Enter your balance, ranging from 1 to 100 000 inclusive: ") 
        
        while (not balance.isdigit()) or (not int(balance) in range(5, 100001)): 
            balance = input("Enter your balance, ranging from 1 to 100 000 inclusive: ") 
            
        return int(balance) 
        
    @classmethod 
    def take_player_wager(cls, self): 
        wager = input(f"Choose how much you want to wager in your box, ranging from 10 to 10 000 inclusive: ") 
        
        while (not wager.isdigit()) or (not int(wager) in range(10, 10001) or (int(wager) > self.balance)): 
            wager = input("Incorrect input! Please try again: ") 
            
        self.balance -= int(wager) 
        
        return int(wager) 
        
    def __str__(self): 
        return f"My name is {self.name} and I have {self.balance} balance." 

class Dealer: 
    def __init__(self): 
        self.name = "Layo" 
        self.cards = [] 
        self.result = 0 
        self.insurance = False 
        
    def __str__(self): 
        return f"My name is {self.name} and I will be your dealer in the next games!" 

class Game: 
    freeboxes = [1, 2, 3, 4, 5, 6, 7] 
    
    def pick_num_of_boxes(): 
        num = input("Choose how many boxes you want to play with, ranging from 1 to 7, inclusive: ") 
        
        while (not num.isdigit()) or (not int(num) in range(1, 8)): 
            num = input("Incorrect input. Please try again: ") 
        
        return int(num) 
        
    def __init__(self): 
        self.deck = Deck.create_deck() 
        random.shuffle(self.deck) 
        self.numofboxes = Game.pick_num_of_boxes() 
        self.player = Player("Bella") 
        self.dealer = Dealer() 
        
    def deal_player_first_card_per_box(self): 
        cards = [] 
        card = self.deck.pop() 
        print(f"The first card for this box is {Card.__str__(card)}") 
        cards.append(card.value) 
        
        return cards 
        
    def pick_player_box(self, freeboxes, numofboxes): 
        for box in range(0, numofboxes): 
            chosedboxpos = input(f"The free boxes you can choose from are at positions {freeboxes}. Choose your preferred one: ") 
            
            while (not chosedboxpos.isdigit()) or (not int(chosedboxpos) in range(1, 8)): chosedboxpos = input("Invalid input! Please try again: ") 
        
            boxposition = int(chosedboxpos) 
            freeboxes.remove(boxposition) 
        
            wager = Player.take_player_wager() 
            cards = Game.deal_player_first_card_per_box()
            self.player.boxes.append(Box(boxposition,wager,cards)) 
            
        return self.player.boxes 
            
    def deal_dealer_first_card(self): 
        card = self.deck.pop() 
        self.dealer.cards.append(card.value) 
        self.dealer.result += card.value 
        
        if card.value == 1: 
            self.dealer.insurance = True 
            for box in self.player.boxes:
                playerchoice = input("It is insurance time. Would you like to insure your bets? If yes, please enter Y otherwise enter N: ") 
                
                while (not playerchoice.isalpha()) or (not playerchoice == "Y") or (not playerchoice == "N"): 
                    playerchoice = input("Wrong input. Please try again. If you want to make an insurance enter Y otherwise enter N: ") 
                    
                if playerchoice == "Y": 
                    box.wager += box.wager / 2 
                    box.insurance = True 
                    print("You just made an insurance. If the dealer has a blackjack, you will lose your original wager but the insurance bet will be paid 2 to 1.") 
                    
            return self.dealer.cards 
            
    def deal_player_second_card_per_box(self, cards): 
        card = self.deck.pop() 
        print(f"The second card for this box is {Card.__str__(card)}") 
        cards.append(card.value) 
        
        return cards 
    
    def deal_other_dealer_cards(self):
        self.dealer.result = sum(self.dealer.cards)
        card = self.deck.pop()
        self.dealer.cards.append(card.value)
        self.dealer.result += card.value

        if 1 in self.dealer.cards and 10 in self.dealer.cards:
            self.dealer.insurance = True

            for box in self.player.boxes:
                if box.insurance == True:
                    box.profit = box.wager / 2
                    print(f"Insurance win! Your addtional insuarnce bet is paid 2:1 and your profit is {box.profit}")
                elif box.insurance == False:
                    box.profit = 0
                    print(f"Insurance win! Unfortunately you loose all your wager. Your profit is 0.")

        
        while self.dealer.result < 18:
            card = self.deck.pop()
            self.dealer.result += card.value
            self.dealer.cards.append(card.value)

            print(f"The card the dealer has just drawn is {Card.__str__(card)}")
            print(f"The dealer's result till now is {self.dealer.result}.")
        
        if self.dealer.result > 17:
            print(f"The final dealer's result is {self.dealer.result}.")
        
        for box in self.player.boxes:
            if box.busted == False and box.blackjack == False and box.surrender == False and box.result > self.dealer.result:
                box.profit = box.wager * 2
                print(f"Congratulations to box at position {box.position}. You win as your result is over the dealer's one."
                      + " Your profit is {box.profit}.")
                
            elif box.busted == False and box.blackjack == False and box.surrender == False and box.result < self.dealer.result:
                print(f"Unfortunately the box at position {box.position} didn't win as their result is under the dealer's one."
                      + " Your profit is {box.profit}.")

    def hit(self, cards): 
        card = self.deck.pop() 
        cards.append(card.value) 
        
        return cards 
        
    def surrender(self, box): 
        box.surrender = True 
        box.profit = box.wager / 2 
        print(f"You chosed to surrender, therefore the game has ended for you and your profit is {box.profit}") 
        
    def double_down(self, box): 
        card = self.deck.pop() 
        box.cards.append(card.value) 
        box.result += card.value 
        box.wager += self.wager 
        
        if box.result > 21: 
            print("You are busted! You lose this game. You loose all the money you have wagered! Go and cry :D!") 
            box.busted = True 
        elif card.value == 1 and box.result <= 10: 
            box.result += 10
            box.addedten = True
            print(f"Excellent! Your result is {box.result}") 
        else: print(f"Excellent! Your result is {box.result}") 
            
    def split(self, box): 
        extraboxwager = Player.take_player_wager()
        extraboxcards = list(box.cards.pop(0))
        extrabox = Box.Box(len((self.player.boxes) + 1), extraboxwager, extraboxcards)
        extrabox.splitted = True
        
        box.splitted = True
        
        regboxsecondcard = self.deck.pop() 
        extraboxsecondcard = self.deck.pop() 
        
        box.cards.append(regboxsecondcard.value) 
        extrabox.cards.append(extraboxsecondcard.value)
        
        for box in list(box, extrabox): 
            result = sum(box.cards) 
            if result > 21: 
                print("You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                box.busted = True
                break
                
            elif result < 21: 
                while True: 
                    decision = input("Would you like to hit? If yes, please enter Y otherwise enter N: ") 
                    while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                        decision = input("Invalid input! Please enter either Y or N: ")
                        
                        while not decision == "N" and result < 21: 
                            box.cards = Game.hit(box.cards) 
                            result = sum(box.cards) 
                            
                            if result > 21: 
                                print("You are busted! You lose this game. You loose all the money you have wagered! Go and cry :D!")
                                box.busted = True
                                break
                            elif 1 in box.cards and result <= 10: 
                                result += 10
                                box.addedten = True
                            else:
                                print(f"Your result has been upgraded to {result}.")
                            
                            decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                        
                            while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                decision = input("Invalid input! Please enter either Y or N: ")
                                
    @classmethod 
    def play(cls,self):
        '''Create all the boxes and give one card to all of them.'''
        self.player.boxes = Game.pick_player_box(Game.freeboxes, Game.pick_num_of_boxes())
        
        '''Give first card to the dealer and check for insurance''' 
        self.dealer.cards = Game.deal_dealer_first_card() 
        
        '''Give a second card to all the boxes.''' 
        for box in self.player.boxes: 
            box.cards = Game.deal_player_second_card_per_box(box.cards)
            result = sum(box.cards) 
            
            '''BJ and no insurance'''
            if (1 in box.cards and 10 in box.cards) and (box.insurance == False): 
                box.blackjack = True 
                box.profit = box.wager * 3 
                print(f"You have a BlackJack and you win! Your profit is {box.profit}. Congratulations!")
                break
                '''BJ and insurance'''
            elif (1 in box.cards and 10 in box.cards) and (box.insurance == True): 
                box.blackjack = True 
                box.profit = box.wager 
                print(f"You have a BlackJack and you win! You keep your money, your profit is {box.profit}")
                '''busted'''
            elif result > 21: 
                box.busted = True 
                print("You are busted! You lose this game and all the money you have wagered! Go and cry :D!") 
                '''1 or 11'''
            elif 1 in box.cards and result <= 10: 
                result += 10
                box.addedten = True
                print(f"Your result is {result}.") 
                
                decision = input("You have 3 moves to choose from. The first one is to hit, the second one is to stay, the third one is " + "to surrender. Please enter the number of your preferred one: ") 
                while (not decision.isdigit()) or (not decision in range (1, 4)): 
                    decision = input("Invalid input! Please enter a number between 1 and 3 inclusive: ") 
                if int(decision) == 1: 
                    box.cards = Game.hit(box.cards) 
                    result = sum(box.cards) 
                    
                    if result < 21: 
                        while True: 
                            decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                            while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                decision = input("Invalid input! Please enter either Y or N: ") 
                                
                            while not decision == "N" and result < 21: 
                                box.cards = Game.hit(box.cards) 
                                result = sum(box.cards)
                                
                                if result <= 11:
                                    result += 10
                                
                                elif result > 21 and box.addedten == True:
                                    result -= 10
                                    box.addedten = False
                                    
                                decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                        
                                while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                    decision = input("Invalid input! Please enter either Y or N: ")
                            
                    elif result > 21 and box.addedten == True:
                        result -= 10
                        box.addedten = False
                        print(f"Your result is {result}.")
                        
                        while True: 
                            decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                            while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                decision = input("Invalid input! Please enter either Y or N: ") 
                                
                            while not decision == "N" and result < 21: 
                                box.cards = Game.hit(box.cards) 
                                result = sum(box.cards)
                                
                                if result <= 11:
                                    result += 10
                                    box.addedten = True
                                
                                elif result > 21 and box.addedten == True:
                                    result -= 10
                                    box.addedten = False
                                
                                elif result > 21 and box.addedten == False:
                                    print("You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                                    box.busted = True
                                    break

                                else:    
                                    decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                        
                                    while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                        decision = input("Invalid input! Please enter either Y or N: ")
                    '''stay'''        
                elif int(decision) == 2: 
                    print(f"You have chosed to stay with result of {result}.")
                    '''surrender'''
                else: 
                    Game.surrender(box)
                '''double down'''
            elif result == 9 or result == 10 or result == 11:
                decision = input("Card or double. Double is only one card. Insert 1 if you want a card, otherwise insert 2: ")

                while (not decision.isdigit()) or (not int(decision) in range(1, 3)):
                    decision = input("Invalid input! Please insert either 1 or 2: ")
                
                if int(decision) == 1:
                    newdecision = "Y"
                    while result < 21 and newdecision == "Y":
                        box.cards = Game.hit(box.cards)
                        result = sum(box.cards)

                        if 1 in box.cards and result > 21 and box.addedten == True:
                            result -= 10
                            box.addedten = False

                        if result > 21 and box.addedten == False:
                            print("You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                            box.busted = True
                            break

                        if 1 in box.cards and result <= 11 and box.addedten == False:
                            result += 10
                            box.addedten = True
                        
                        newdecision = input('Would you like to hit again. If yes insert "Y" otherwise insert "N": ')

                        while (not newdecision.isalpha()) or (not newdecision == "Y") or (not newdecision == "N"): 
                            newdecision = input("Invalid input! Please enter either Y or N: ")
                    
                    if newdecision == "N":
                        print(f"Your result is {result}.")

                elif int(decision) == 2:
                    Game.double_down(box)
                '''hit, stay or surrrender'''
            elif result < 21:
                decision = input("You have 3 moves to choose from. The first one is to hit, the second one is to stay, the third one is "
                                  + "to surrender. Please enter the number of your preferred one: ") 
                while (not decision.isdigit()) or (not int(decision) in range (1, 4)): 
                    decision = input("Invalid input! Please enter a number between 1 and 3 inclusive: ")
                
                if int(decision) == 1: 
                    box.cards = Game.hit(box.cards) 
                    result = sum(box.cards) 
                    
                    if result < 21: 
                        while True: 
                            decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                            while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                decision = input("Invalid input! Please enter either Y or N: ") 
                                
                            while not decision == "N" and result < 21: 
                                box.cards = Game.hit(box.cards) 
                                result = sum(box.cards)
                                
                                if result <= 11:
                                    result += 10
                                
                                elif result > 21 and box.addedten == True:
                                    result -= 10
                                    box.addedten = False
                                    
                                decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                        
                                while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                    decision = input("Invalid input! Please enter either Y or N: ")
                            
                    elif result > 21 and box.addedten == True:
                        result -= 10
                        box.addedten = False
                        print(f"Your result is {result}.")
                        
                        while True: 
                            decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                            while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                decision = input("Invalid input! Please enter either Y or N: ") 
                                
                            while not decision == "N" and result < 21: 
                                box.cards = Game.hit(box.cards) 
                                result = sum(box.cards)
                                
                                if result <= 11:
                                    result += 10
                                    box.addedten = True
                                
                                elif result > 21 and box.addedten == True:
                                    result -= 10
                                    box.addedten = False
                                
                                elif result > 21 and box.addedten == False:
                                    print("You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                                    box.busted = True
                                    break

                                else:    
                                    decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                        
                                    while (not decision.isalpha()) or (not decision == "Y") or (not decision == "N"): 
                                        decision = input("Invalid input! Please enter either Y or N: ")
                    '''stay'''        
                elif int(decision) == 2: 
                    print(f"You have chosed to stay with result of {result}.")
                    '''surrender'''
                else: 
                    Game.surrender(box)




                box.cards = Game.double_down(box)
                           
game = Game() 
game.play(game)