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
    def __init__(self):
        self.cards = 6 * [Card(rank, suite) for rank in ranks for suite in suites]
        random.shuffle(self.cards)
    
    def draw_card(self):
        return self.cards.pop()
    
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
    def __init__(self): 
        self.name = "" 
        self.balance = 0 
        self.boxes = []

# this method handles all the situations when the player is asked to enter their balance(between 10 an 1000), or m=ti make a decision 
# whether they would like to hit again or no
    def take_input(self, prompt, valid_range=None, is_digit =True):
        while True:
            value = input(prompt)
            if is_digit and value.isdigit():
                value = int(value)
                if valid_range and value in valid_range:
                    return value
            elif not is_digit and value.isalpha():
                return value
            print("Invalid input. Please try again.")
    
    def choose_yes_or_no(self, prompt, values, is_digit = True):
        value = input(prompt)

        while True:
            if is_digit and value.isdigit():
                value = int(value)
                if value in values:
                    return value
            elif not is_digit and value.isalpha():
                if value in values:
                    return value
            value = input(f'Invalid input. Please try again. Enter either {values[0]} or {values[1]}: ')
    
    def take_player_name(self):
        return self.take_input("Enter your name: ", is_digit=False)
        
    def take_player_balance(self): 
        return self.take_input("Enter your balance (1-100000): ", range(5, 100001)) 
        
    def take_player_wager(self):
       return self.take_input(f"Enter your wager (10-{self.balance}): ", range(10, self.balance + 1))
        
    def __str__(self): 
        return f"My name is {self.name} and I have {self.balance} balance." 

class Dealer: 
    def __init__(self): 
        self.name = "Layo" 
        self.cards = [] 
        self.result = 0 
        self.insurance = False 
        
    def __str__(self): 
        return f"My name is {self.name} and I will be your dealer for the next game!" 

class Game: 
    freeboxes = [1, 2, 3, 4, 5, 6, 7]
    
    def pick_num_of_boxes(self):
        return Player.take_input(self.player,'Choose how many boxes you want to play with, ranging from 1 to 7, inclusive: ', range(1,8), is_digit=True)
        
    def __init__(self): 
        self.deck = Deck()  
        self.player = Player() 
        self.dealer = Dealer()
        
    def deal_player_first_card_per_box(self, boxposition): 
        cards = [] 
        card = self.deck.draw_card() 
        print(f"The first card for box number {boxposition} is {Card.__str__(card)}") 
        cards.append(card.value) 
        
        return cards 
        
    def pick_player_box(self, freeboxes, numofboxes):
        for box in range(1, numofboxes + 1):
            boxposition = Player.take_input(self.player, f"The free boxes you can choose from are at positions {freeboxes}. Choose your preferred one: ", range(1, 8), is_digit=True)

            while not boxposition in freeboxes:
                boxposition = input("Invalid input! This box had been chosen already. Choose a new one:  ")

            freeboxes.remove(boxposition)

            wager = Player.take_player_wager(self.player)
            self.player.balance -= wager 
            cards = self.deal_player_first_card_per_box(boxposition)
            self.player.boxes.append(Box(boxposition,wager,cards)) 
            
        return self.player.boxes
            
    def deal_dealer_first_card(self): 
        card = self.deck.draw_card()
        self.dealer.cards.append(card.value)
        self.dealer.result += card.value

        print(f"The first card for the dealer is {Card.__str__(card)}")
        
        if card.value == 1: 
            self.dealer.insurance = True
            for box in self.player.boxes:
                playerchoice = Player.choose_yes_or_no(self.player, "It is insurance time. Would you like to insure your bets? If yes, please enter Y otherwise enter N: ")

                if playerchoice == "Y": 
                    box.wager += box.wager / 2 
                    box.insurance = True 
                    print("You just made an insurance. If the dealer has a blackjack, you will lose your original wager but the insurance bet will be paid 2 to 1.") 
                else:
                    print("You have just chosen not to insure your bets.")
        return self.dealer.cards 
            
    def deal_player_second_card_per_box(self, cards, boxposition): 
        card = self.deck.draw_card()
        cards.append(card.value) 
        print(f"The second card for box number {boxposition} is {Card.__str__(card)}.") 
        return cards 
    
    def deal_other_dealer_cards(self):
        dealmorecards = False

        for box in self.player.boxes:
            if not box.blackjack and not box.surrender and not box.busted:
                dealmorecards = True

        if dealmorecards == True:
            self.dealer.result = sum(self.dealer.cards)
            card = self.deck.draw_card() 
            self.dealer.cards.append(card.value)
            self.dealer.result += card.value
            print(f"The new card the dealer has just drawn is {Card.__str__(card)} and the dealer's result till now is {self.dealer.result}.")

            if 1 in self.dealer.cards and 10 in self.dealer.cards:
                self.dealer.insurance = True

                for box in self.player.boxes:
                    if box.insurance == True:
                        box.profit = box.wager / 2
                        print(f"Insurance win! Your addtional insuarnce bet is paid 2:1 and your profit is {box.profit}")
                    elif box.insurance == False:
                        box.profit = 0
                        print(f"Insurance win! Unfortunately you loose all your wager. Your profit is 0.")

            while self.dealer.result < 17:
                card = self.deck.draw_card() 
                self.dealer.result += card.value
                self.dealer.cards.append(card.value)

                print(f"The card the dealer has just drawn is {Card.__str__(card)} and the dealer's result till now is {self.dealer.result}.")
        
            if self.dealer.result > 17 and self.dealer.result < 22:
                for box in self.player.boxes:
                    if box.result == self.dealer.result and box.surrender == False:
                        print(f"It's a tie! You neither win nor loose, you just keep the money you have wagered.")

                    elif box.busted == False and box.blackjack == False and box.surrender == False and box.result > self.dealer.result:
                        box.profit = box.wager * 2
                        print(f"Congratulations to box at position {box.position}. You win as your result is over the dealer's one. Your profit is {box.profit}.")
                
                    elif box.busted == False and box.blackjack == False and box.surrender == False and box.result < self.dealer.result:
                        print(f"Unfortunately the box at position {box.position} doesn't win as their result is under the dealer's one. Your profit is {box.profit}.")
            elif self.dealer.result > 21:
                for box in self.player.boxes:
                    if box.busted == False and box.surrender == False:
                        box.profit = box.wager * 2
                        print(f"Congratulations to box at position {box.position}. You win as the dealer's got busted. Your profit is {box.profit}.")
        
        print("The game has just ended!")

    def hit(self, cards): 
        card = self.deck.draw_card() 
        cards.append(card.value)
        print(f"The new card you just drawn is {Card.__str__(card)}.") 
        
        return cards 
        
    def surrender(self, box): 
        box.surrender = True 
        box.profit = box.wager / 2 
        print(f"Your result is {box.result}. You chosed to surrender, therefore the game has ended for you and your profit is {box.profit}")        
    
    def double_down(self, box): 
        card = self.deck.draw_card() 
        box.cards.append(card.value)
        print(f"The card you have just drawn is {Card.__str__(card)}.") 
        box.result += card.value 
        box.wager += box.wager 
        
        if box.result > 21: 
            print(f"Your result is {box.result}. You are busted and lose this game. You loose all the money you have wagered! Go and cry :D!") 
            box.busted = True 
        elif card.value == 1 and box.result <= 10: 
            box.result += 10
            box.addedten = True
            print(f"Excellent! Your result is {box.result}") 
        else: print(f"Excellent! Your result is {box.result}") 
            
    def split(self, box):
        extraboxwager = input(f"Choose how much you want to wager in your box, ranging from 10 to 10 000 inclusive: ") 
        
        while (not extraboxwager.isdigit()) or (not int(extraboxwager) in range(10, 10001) or (int(extraboxwager) > self.balance)): 
            extraboxwager = input("Incorrect input! Please try again: ") 
            
        self.balance -= int(extraboxwager) 
        
        extraboxwager = int(extraboxwager)
        extraboxcards = list(box.cards.pop(0))
        extrabox = Box.Box(len((self.player.boxes) + 1), extraboxwager, extraboxcards)
        extrabox.splitted = True
        
        box.splitted = True
        
        regboxsecondcard = self.deck.draw_card() 
        extraboxsecondcard = self.deck.draw_card() 
        
        box.cards.append(regboxsecondcard.value) 
        extrabox.cards.append(extraboxsecondcard.value)
        
        for box in list(box, extrabox): 
            box.result = sum(box.cards) 
            if box.result > 21: 
                print("You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                box.busted = True
                break
                
            elif box.result < 21: 
                while True: 
                    decision = input("Would you like to hit? If yes, please enter Y otherwise enter N: ") 
                    while (not decision.isalpha()) or (not decision == "Y") and (not decision == "N"): 
                        decision = input("Invalid input! Please enter either Y or N: ")
                        
                        while not decision == "N" and box.result < 21: 
                            box.cards = Game.hit(self, box.cards) 
                            box.result = sum(box.cards) 
                            
                            if box.result > 21: 
                                print("You are busted! You lose this game. You loose all the money you have wagered! Go and cry :D!")
                                box.busted = True
                                break
                            elif 1 in box.cards and box.result <= 11: 
                                box.result += 10
                                box.addedten = True
                            else:
                                print(f"Your result has been upgraded to {box.result}.")
                            
                            decision = input("Would you like to hit again? If yes, please enter Y otherwise enter N: ") 
                        
                            while (not decision.isalpha()) or (not decision == "Y") and (not decision == "N"): 
                                decision = input("Invalid input! Please enter either Y or N: ")
                        break
                    break
                                
    def play(self):
        '''Create all the boxes and give one card to all of them.'''
        self.player.name = Player.take_player_name(self.player)
        print(f"Hello {self.player.name}! Let's start playing!")
        print(self.dealer)
        self.player.balance = Player.take_player_balance(self.player)
        numofboxes = self.pick_num_of_boxes()
        self.player.boxes = Game.pick_player_box(self, Game.freeboxes, numofboxes)
        
        '''Give first card to the dealer and check for insurance''' 
        self.dealer.cards = Game.deal_dealer_first_card(self) 
        
        '''Give a second card to all the boxes.''' 
        for box in self.player.boxes: 
            box.cards = Game.deal_player_second_card_per_box(self, box.cards, box.position)
            print(f"All the player's cards for box at position {box.position} are {box.cards}")
            box.result = sum(box.cards)
            
            
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
            elif box.result > 21: 
                box.busted = True 
                print("You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                return
                '''double down'''
            elif box.result == 9 or box.result == 10 or box.result == 11:
                decision = Player.choose_yes_or_no(self.player, "Card or double. Double is only one card. Insert 1 if you want a card, otherwise insert 2: ", [1,2], is_digit=True)
                
                if decision == 1:
                    newdecision = "Y"
                    while box.result < 21 and newdecision == "Y":
                        box.cards = Game.hit(self, box.cards)
                        box.result = sum(box.cards)

                        if 1 in box.cards and box.result > 21 and box.addedten == True:
                            box.result -= 10
                            box.addedten = False
                            print(f"Your result is {box.result}.")

                        if box.result > 21 and box.addedten == False:
                            print(f"Your result is {box.result}. You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                            box.busted = True
                            break

                        if 1 in box.cards and box.result <= 11 and box.addedten == False:
                            box.result += 10
                            box.addedten = True
                            print(f"Your result is {box.result}.")

                        newdecision = Player.choose_yes_or_no(self.player, 'Would you like to hit again. If yes insert "Y" otherwise insert "N": ', ['Y', 'N'], is_digit=False)
                        
                        if newdecision == "N":
                            print(f"Your result is {box.result}.")

                elif decision == 2:
                    Game.double_down(self, box)
                '''1 or 11'''
            elif 1 in box.cards and box.result <= 11: 
                box.result += 10
                box.addedten = True
                print(f"Your result is {box.result}.") 

                decision = Player.take_input(self.player, "You have 3 moves to choose from. The first one is to hit, the second one is to stay, the third one is " 
                                 + "to surrender. Please enter the number of your preferred one: ", range(1, 4), is_digit=True)

                if int(decision) == 1: 
                    box.cards = Game.hit(self, box.cards) 
                    box.result = sum(box.cards) + 10
                    print(f"Your result is {box.result}.") 
                    
                    if box.result < 21: 
                        while True:
                            decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                            while not decision == "N" and box.result < 21: 
                                box.cards = Game.hit(self, box.cards)
                                box.result = sum(box.cards) + 10
                                
                                if box.result > 21 and box.addedten == True:
                                    box.result -= 10
                                    box.addedten = False
                                    print(f"Your result is {box.result}.")

                                elif box.result > 21 and box.addedten == False:
                                    print(f"Your result is {box.result}. You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                                    box.busted = True
                                    break
                                    
                                decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)
                            break
                            
                    elif box.result > 21 and box.addedten == True:
                        box.result -= 10
                        box.addedten = False
                        print(f"Your result is {box.result}.")
                        
                        while True: 
                            decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                            while not decision == "N" and box.result < 21: 
                                box.cards = Game.hit(self, box.cards) 
                                box.result = sum(box.cards)
                                
                                if box.result <= 11 and box.addedten == False:
                                    box.result += 10
                                    box.addedten = True
                                    print(f"Your result is {box.result}.")
                                
                                elif box.result > 21 and box.addedten == True:
                                    box.result -= 10
                                    box.addedten = False
                                    print(f"Your result is {box.result}.")
                                
                                elif box.result > 21 and box.addedten == False:
                                    print(f"Your result is {box.result}. You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                                    box.busted = True
                                    break

                                else:    
                                    decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)
                            break
                    '''stay'''        
                elif int(decision) == 2: 
                    print(f"You have chosen to stay with result of {box.result}.")
                    '''surrender'''
                else:  
                    print(f"Your result is {box.result}.") 
                    Game.surrender(self, box)
                '''split'''
            elif box.cards[0] == box.cards[1]:
                print(f"Your result is {box.result}.")

                decision = Player.take_input(self.player, "You have four moves to chose from - 1 - hit, 2 - stay, 3 - surrender, 4 - split. Enter a number ranging from 1 to 4: ", range(1,5), is_digit=True )

                if decision == 1:
                    box.cards = Game.hit(self, box.cards)
                    box.result = sum(box.cards)
                    print(f"Your result is {box.result}.")

                    if box.result < 21: 
                        while True: 
                            decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                            while not decision == "N" and box.result < 21: 
                                box.cards = Game.hit(self, box.cards) 
                                box.result = sum(box.cards)
                                print(f"Your result is {box.result}")

                                if box.result > 21:
                                    box.busted = True
                                    print(f"You are busted and lose this game and all the money you have wagered! Go and cry :D!")
                                    break

                                decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)

                            if box.result <= 21:
                                print(f"You have just chosed to stay with result of {box.result}.") 

                            break
                elif decision == 2:
                    print(f"You have just chosed to stay with result of {box.result}.")
                elif decision == 3:
                    Game.surrender(self, box)
                elif decision == 4:
                    Game.split(self,box)
                '''hit, stay or surrrender'''
            elif box.result < 21:
                decision = Player.take_input(self.player, f"Your result is {box.result}. You have 3 moves to choose from. The first one is to hit, the second one is to stay, the third one is to surrender. Please enter the number of your preferred one: ", range(1,4), is_digit=True )
                
                if decision == 1: 
                    box.cards = Game.hit(self, box.cards)
                    box.result = sum(box.cards)
                    print(f"Your result is {box.result}") 
                    
                    if box.result < 21: 
                        while True: 
                            decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                            while not decision == "N" and box.result < 21: 
                                box.cards = Game.hit(self, box.cards) 
                                box.result = sum(box.cards)
                                
                                if box.result <= 11 and box.addedten == False:
                                    box.result += 10
                                    box.addedten = True
                                    print(f"Your result is {box.result}")
                                
                                elif box.result > 21 and box.addedten == True:
                                    box.result -= 10
                                    box.addedten = False
                                    print(f"Your result is {box.result}")
                                
                                elif box.result < 21 and box.addedten == True:
                                    box.cards = Game.hit(self, box.cards) 
                                    box.result = sum(box.cards)
                                    print(f"Your result is {box.result}")

                                elif box.result > 21 and box.addedten == False:
                                    box.busted = True
                                    print(f"You are busted and lose this game and all the money you have wagered! Go and cry :D!")
                                    break
 
                                decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)
                            break
                            
                    elif box.result > 21 and box.addedten == True:
                        box.result -= 10
                        box.addedten = False
                        print(f"Your result is {box.result}.")
                        
                        while True: 
                            decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                            while not decision == "N" and box.result < 21: 
                                box.cards = Game.hit(self, box.cards) 
                                box.result = sum(box.cards)
                                
                                if box.result <= 11:
                                    box.result += 10
                                    box.addedten = True
                                    print(f"Your result is {box.result}")
                                
                                elif box.result > 21 and box.addedten == True:
                                    box.result -= 10
                                    box.addedten = False
                                    print(f"Your result is {box.result}")
                                
                                elif box.result > 21 and box.addedten == False:
                                    print(f"Your result is {box.result}. You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                                    box.busted = True
                                    break

                                else:    
                                    decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)
                            break
                    elif box.result > 21 and box.addedten == False:
                        box.busted = True
                        print(f"You are busted and lose this game and all the money you have wagered! Go and cry :D!")
                    '''stay'''        
                elif int(decision) == 2: 
                    print(f"You have chosen to stay with result of {box.result}.")
                    '''surrender'''
                else: 
                    Game.surrender(self, box)

        Game.deal_other_dealer_cards(self)                   
game = Game() 
game.play()