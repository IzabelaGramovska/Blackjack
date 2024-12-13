import pygame
import random
import sys

values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10, "A":1} 
ranks = list(values.keys())
class Card: 
    def __init__(self, rank): 
        self.rank = rank 
        self.value = values[rank]
        
    def __str__(self): 
        return f"{self.value} of {self.rank}" 

class Deck: 
    def __init__(self):
        self.cards = 6 * [Card(rank) for rank in ranks]
        random.shuffle(self.cards)
    
    def draw_card(self):
        return self.cards.pop()
    
class Box: 
    def __init__(self, position, wager, coordinates): 
        self.position = position 
        self.wager = wager 
        self.cards = [] 
        self.result = 0 
        self.blackjack = False 
        self.profit = 0 
        self.insurance = False 
        self.busted = False 
        self.surrender = False
        self.splitted = False
        self.addedten = False
        self.coordinates = coordinates
        
class Player: 
    def __init__(self): 
        self.name = "" 
        self.balance = 0 
        self.boxes = []

    # this method handles all the situations when the player is asked to enter their balance(between 10 an 1000), or m=ti make a decision 
    # whether they would like to hit again or no
    # with @staticmethod the method can be accessed outside
    @staticmethod
    def validate_input(value, valid_range=None, is_digit =True):
        while True:
            if is_digit and value.isdigit():
                value = int(value)
                if valid_range and value in valid_range:
                    return value
                elif not valid_range:
                    return value
            elif not is_digit and value.isalpha():
                return value
            # If the input is invalid
            return None 
        
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

class Logic:
    freeboxes = [1, 2, 3, 4, 5, 6, 7]
        
    def __init__(self): 
        self.deck = Deck()  
        self.player = Player() 
        self.dealer = Dealer()
        
    def pick_player_box(self, freeboxes, numofboxes):
        for box in range(1, numofboxes + 1):
            boxposition = Player.validate_input(self.player, f"The free boxes you can choose from are at positions {freeboxes}. Choose your preferred one: ", range(1, 8), is_digit=True)

            while not boxposition in freeboxes:
                boxposition = input("Invalid input! This box had been chosen already. Choose a new one:  ")
                if boxposition in freeboxes:
                    break

            freeboxes.remove(boxposition)

            wager = Player.take_player_wager(self.player)
            self.player.balance -= wager
            cards = self.deal_card([], f"The first card for box number {boxposition}")
            box = Box(boxposition,wager,cards)
            self.player.boxes.append(box) 
            
        return self.player.boxes
          
    def deal_other_dealer_cards(self):
        dealmorecards = False

        for box in self.player.boxes:
            if not box.blackjack and not box.surrender and not box.busted:
                dealmorecards = True

        if dealmorecards:
            self.dealer.cards = self.deal_card(self.dealer.cards, 'The new card the dealer has just drawn')
            self.dealer.result = sum(self.dealer.cards)
            print(f"The dealer's result till now is {self.dealer.result}.")
            
            if 1 in self.dealer.cards and 10 in self.dealer.cards:
                self.dealer.insurance = True

                for box in self.player.boxes:
                    if box.insurance:
                        box.profit = box.wager / 2
                        print(f"Insurance win! Your addtional insuarnce bet is paid 2:1 and your profit is {box.profit}")
                    elif not box.insurance:
                        box.profit = 0
                        print(f"Insurance win! Unfortunately you loose all your wager. Your profit is 0.")

            while self.dealer.result < 17:
                self.dealer.cards = self.deal_card(self.dealer.cards, 'The card the dealer has just drawn')
                self.dealer.result += sum(self.dealer.cards)
                print(f"The dealer's result till now is {self.dealer.result}.")
                        
            if self.dealer.result > 17 and self.dealer.result < 22:
                for box in self.player.boxes:
                    if box.result == self.dealer.result and not box.surrender:
                        print(f"It's a tie! You neither win nor loose, you just keep the money you have wagered.")

                    elif not box.busted and not box.blackjack and not box.surrender and box.result > self.dealer.result:
                        box.profit = box.wager * 2
                        print(f"Congratulations to box at position {box.position}. You win as your result is over the dealer's one. Your profit is {box.profit}.")
                
                    elif not box.busted and not box.blackjack and not box.surrender and box.result < self.dealer.result:
                        print(f"Unfortunately the box at position {box.position} doesn't win as their result is under the dealer's one. Your profit is {box.profit}.")
            elif self.dealer.result > 21:
                for box in self.player.boxes:
                    if not box.busted and not box.surrender:
                        box.profit = box.wager * 2
                        print(f"Congratulations to box at position {box.position}. You win as the dealer's got busted. Your profit is {box.profit}.")
        
        print("The game has just ended!")

    def hit(self, cards):
        return self.deal_card(cards, 'The new card you just drawn') 
        
    def surrender(self, box): 
        box.surrender = True 
        box.profit = box.wager / 2 
        print(f"Your result is {box.result}. You chosed to surrender, therefore the game has ended for you and your profit is {box.profit}")        
    
    def double_down(self, box):  
        box.cards = self.deal_card(box.cards, "The card you have just drawn")
        box.result = sum(box.cards)
        box.wager += box.wager 
        
        if box.result > 21: 
            print(f"Your result is {box.result}. You are busted and lose this game. You loose all the money you have wagered! Go and cry :D!") 
            box.busted = True 
        elif box.cards[2] == 1 and box.result <= 10: 
            box.result += 10
            box.addedten = True
            print(f"Excellent! Your result is {box.result}") 
        else: print(f"Excellent! Your result is {box.result}") 
            
    def split(self, box):
        extraboxwager = input("Choose how much you want to wager in your box, ranging from 10 to 10 000 inclusive: ") 
        
        while (not extraboxwager.isdigit()) or (not int(extraboxwager) in range(10, 10001) or (int(extraboxwager) > self.balance)): 
            extraboxwager = input("Incorrect input! Please try again: ") 
            
        self.balance -= int(extraboxwager) 
        
        extraboxwager = int(extraboxwager)
        extraboxcards = [box.cards.pop(0)]
        extrabox = Box(len((self.player.boxes) + 1), extraboxwager, extraboxcards)
        extrabox.splitted = True
        
        box.splitted = True

        box.cards = self.deal_card(box.cards, "The second card for the first box of the split")
        extrabox.cards = self.deal_card(extrabox.cards, "The second card for the second box of the split") 
        
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
                            box.cards = self.hit(self, box.cards) 
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
                                
    def handle_blackjack(self, box):
        if 1 in box.cards and 10 in box.cards:
            box.blackjack = True 
            box.profit = box.wager * 3

            if box.insurance:
                print(f"You have a BlackJack and you win! Your profit is {box.profit}. Congratulations!")
            else:
                print(f"You have a BlackJack and you win! Your profit is {box.profit}. Congratulations!")

            return True
        return False
    
    def handle_busted(self, box):
        if box.result > 21: 
            box.busted = True 
            print("You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
            return True
        return False
    
    def handle_double_down(self, box):
        if box.result in [9,10,11]:
            decision = Player.choose_yes_or_no(self.player, "Card or double. Double is only one card. Insert 1 if you want a card, otherwise insert 2: ", [1,2], is_digit=True)
                
            if decision == 1:
                newdecision = "Y"
                while box.result < 21 and newdecision == "Y":
                    box.cards = self.hit(self, box.cards)
                    box.result = sum(box.cards)

                    if 1 in box.cards and box.result > 21 and box.addedten:
                        box.result -= 10
                        box.addedten = False
                        print(f"Your result is {box.result}.")

                    if box.result > 21 and not box.addedten:
                        print(f"Your result is {box.result}. You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                        box.busted = True
                        break

                    if 1 in box.cards and box.result <= 11 and not box.addedten:
                        box.result += 10
                        box.addedten = True
                        print(f"Your result is {box.result}.")

                    newdecision = Player.choose_yes_or_no(self.player, 'Would you like to hit again. If yes insert "Y" otherwise insert "N": ', ['Y', 'N'], is_digit=False)
                        
                    if newdecision == "N":
                        print(f"Your result is {box.result}.")

            elif decision == 2:
                self.double_down(self, box)
            return True
        return False

    def handle_1_or_11(self, box):
        if 1 in box.cards and box.result <= 11: 
            box.result += 10
            box.addedten = True
            print(f"Your result is {box.result}.") 

            decision = Player.validate_input(self.player, "You have 3 moves to choose from. The first one is to hit, the second one is to stay, the third one is to surrender. Please enter the number of your preferred one: ", range(1, 4), is_digit=True)

            if decision == 1: 
                box.cards = self.hit(self, box.cards) 
                box.result = sum(box.cards) + 10
                    
                if box.result < 21: 
                    while True:
                        decision = Player.choose_yes_or_no(self.player, f"Your result is {box.result}. Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                        while not decision == "N" and box.result < 21: 
                            box.cards = self.hit(self, box.cards)
                            box.result = sum(box.cards) + 10
                                
                            if box.result > 21 and box.addedten:
                                box.result -= 10
                                box.addedten = False
                                print(f"Your result is {box.result}.")

                            elif box.result > 21 and not box.addedten:
                                print(f"Your result is {box.result}. You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                                box.busted = True
                                break
                                    
                            decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)
                        break
                            
                elif box.result > 21 and box.addedten:
                    box.result -= 10
                    box.addedten = False
                    print(f"Your result is {box.result}.")
                        
                    while True: 
                        decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                        while not decision == "N" and box.result < 21: 
                            box.cards = self.hit(self, box.cards) 
                            box.result = sum(box.cards)
                                
                            if box.result <= 11 and not box.addedten:
                                box.result += 10
                                box.addedten = True
                                print(f"Your result is {box.result}.")
                                
                            elif box.result > 21 and box.addedten:
                                box.result -= 10
                                box.addedten = False
                                print(f"Your result is {box.result}.")
                                
                            elif box.result > 21 and not box.addedten:
                                print(f"Your result is {box.result}. You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                                box.busted = True
                                break

                            else:    
                                decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)
                        break
                    '''stay'''        
            elif decision == 2: 
                print(f"You have chosen to stay with result of {box.result}.")
                '''surrender'''
            else:  
                print(f"Your result is {box.result}.") 
                self.surrender(self, box)
            return True
        return False

    def handle_split(self, box):
        if box.cards[0] == box.cards[1]:
            print(f"Your result is {box.result}.")

            decision = Player.validate_input(self.player, "You have four moves to chose from - 1 - hit, 2 - stay, 3 - surrender, 4 - split. Enter a number ranging from 1 to 4: ", range(1,5), is_digit=True )

            if decision == 1:
                box.cards = self.hit(self, box.cards)
                box.result = sum(box.cards)
                print(f"Your result is {box.result}.")

                if box.result < 21: 
                    while True: 
                        decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                        while not decision == "N" and box.result < 21: 
                            box.cards = self.hit(self, box.cards) 
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
                self.surrender(self, box)
            elif decision == 4:
                self.split(self,box)
            return True
        return False

    def handle_hit_stay_surrender(self,box):
        if box.result < 21:
            decision = Player.validate_input(self.player, f"Your result is {box.result}. You have 3 moves to choose from. The first one is to hit, the second one is to stay, the third one is to surrender. Please enter the number of your preferred one: ", range(1,4), is_digit=True )
                
            if decision == 1: 
                box.cards = self.hit(self, box.cards)
                box.result = sum(box.cards)
                print(f"Your result is {box.result}") 
                    
                if box.result < 21: 
                    while True: 
                        decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                        while not decision == "N" and box.result < 21: 
                            box.cards = self.hit(self, box.cards) 
                            box.result = sum(box.cards)
                                
                            if box.result <= 11 and not box.addedten:
                                box.result += 10
                                box.addedten = True
                                print(f"Your result is {box.result}")
                                
                            elif box.result > 21 and box.addedten:
                                box.result -= 10
                                box.addedten = False
                                print(f"Your result is {box.result}")
                                
                            elif box.result < 21 and box.addedten:
                                box.cards = self.hit(self, box.cards) 
                                box.result = sum(box.cards)
                                print(f"Your result is {box.result}")

                            elif box.result > 21 and not box.addedten:
                                box.busted = True
                                print(f"You are busted and lose this game and all the money you have wagered! Go and cry :D!")
                                break
 
                            decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)
                        break
                            
                elif box.result > 21 and box.addedten:
                    box.result -= 10
                    box.addedten = False
                    print(f"Your result is {box.result}.")
                        
                    while True: 
                        decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False) 
                                
                        while not decision == "N" and box.result < 21: 
                            box.cards = self.hit(self, box.cards) 
                            box.result = sum(box.cards)
                                
                            if box.result <= 11:
                                box.result += 10
                                box.addedten = True
                                print(f"Your result is {box.result}")
                                
                            elif box.result > 21 and box.addedten:
                                box.result -= 10
                                box.addedten = False
                                print(f"Your result is {box.result}")
                                
                            elif box.result > 21 and not box.addedten:
                                print(f"Your result is {box.result}. You are busted! You lose this game and all the money you have wagered! Go and cry :D!")
                                box.busted = True
                                break

                            else:    
                                decision = Player.choose_yes_or_no(self.player, "Would you like to hit again? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)
                        break
                elif box.result > 21 and not box.addedten:
                    box.busted = True
                    print(f"You are busted and lose this game and all the money you have wagered! Go and cry :D!")
                    '''stay'''        
            elif decision == 2: 
                print(f"You have chosen to stay with result of {box.result}.")
                '''surrender'''
            else: 
                self.surrender(self, box)
    
class RenderGame:
    def __init__(self):
        pygame.init()
        self.WIDTH = 1510
        self.HEIGHT = 780
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("Blackjack!")
        self.font = pygame.font.Font(None, 30)
        self.input_font = pygame.font.Font(None, 21)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.input_box = pygame.Rect(600, 320, 200, 40)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.clock = pygame.time.Clock()
        self.active = False
        self.color = self.color_inactive
        self.show_invalid_message = False
        self.fps = 60
        self.logic = Logic()
        self.show_invalid_message = False

    def draw_text(self, text, color, position):
        prompt_surface = self.font.render(text, True, color)
        self.screen.blit(prompt_surface, position)

    def take_player_name(self):
        self.logic.player.name = ''
        self.show_invalid_message = False

        while True:
            self.screen.fill('skyblue')

            if not self.show_invalid_message:
                self.draw_text("Please enter your name:",self.BLACK, (600,250))
            else:
                self.draw_text("Invalid input. Please try again.", self.RED, (600,250))

            txt_surface = self.input_font.render(self.logic.player.name, True, self.BLACK)
            width = max(300, txt_surface.get_width() + 10)
            self.input_box.w = width
            self.screen.blit(txt_surface, ((self.input_box.x + 5, self.input_box.y + 5)))
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        if self.logic.player.name.strip() and not self.logic.player.name.isdigit():
                            self.show_invalid_message = False
                            return self.logic.player.name.strip()
                        else:
                            self.show_invalid_message = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.logic.player.name = self.logic.player.name[:-1]
                    else:
                        self.logic.player.name += event.unicode
    
    def take_player_balance(self):
        balance_input = ''
        self.show_invalid_message = False

        while True:
            self.screen.fill('skyblue')
            
            if not self.show_invalid_message:
                self.draw_text("Enter your balance (10-100000):",self.BLACK, (600,250))
            else:
                self.draw_text("Invalid input. Please try again.", self.RED, (600,250))

            txt_surface = self.input_font.render(balance_input, True, self.BLACK)
            width = max(200, txt_surface.get_width() + 10)
            self.input_box.w = width
            self.screen.blit(txt_surface, ((self.input_box.x + 5, self.input_box.y + 5)))
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)

            pygame.display.flip() 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        if balance_input.isdigit():
                            balance = int(balance_input)
                        if 10 <= balance <= 100000:
                            self.show_invalid_message = False
                            return balance
                        self.show_invalid_message = True
                        balance_input = ''
                    elif event.key == pygame.K_BACKSPACE:
                        balance_input = balance_input[:-1]
                    else:
                        balance_input += event.unicode

    def display_greetings(self):
        while True:
            self.screen.fill('skyblue')
            self.draw_text(f"Hello {self.logic.player.name}! Let's start playing!", self.BLACK, (410,350))
            self.draw_text(f"{self.logic.dealer}", self.BLACK, (410, 410) )
            
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return
    
    def take_num_of_boxes(self):
        user_input = ''
        self.show_invalid_message = False

        while True:
            self.screen.fill('skyblue')

            if not self.show_invalid_message:
                self.draw_text("Enter the number of boxes you want to play with, which can range from one to seven", self.BLACK, (250, 250))
            else:
                self.draw_text("Invalid input. Please try again.", self.RED, (400,250))
            
            txt_surface = self.input_font.render(user_input, True, self.BLACK)
            width = max(200, txt_surface.get_width() + 10)
            self.input_box.w = width
            self.screen.blit(txt_surface, ((self.input_box.x + 5, self.input_box.y + 5)))
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        if user_input.isdigit():
                            user_input = int(user_input)
                        if 1 <= user_input <= 7:
                            self.show_invalid_message = False
                            return user_input
                        self.show_invalid_message = True
                        user_input = ''
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

    def draw_boxes(self):
        while True:
            self.screen.fill('skyblue')

            for i in range(7):
                left_float = 215 * i
                pygame.draw.rect(self.screen, 'darkblue', [12 + left_float, 12, 190, 320], 0, 5)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    return
    
    def pick_free_box(self, number_of_boxes):
        free_boxes = [1, 2, 3, 4, 5, 6, 7]
        busy_box = False
        user_input = ''
        boxes_list = []

        for i in range(number_of_boxes):
            run = True
            while run:
                self.screen.fill('skyblue')

                if not busy_box:
                    self.draw_text(f"The free boxes you can choose from are at positions {free_boxes}. Choose your preferred one: ", self.BLACK, (250,250))
                else:
                    self.draw_text(f"Invalid input! This box had been chosen already. Choose a new one from the positions {free_boxes}:  ", self.RED, (250,250))
                
                txt_surface = self.input_font.render(user_input, True, self.BLACK)
                width = max(200, txt_surface.get_width() + 10)
                self.input_box.w = width
                self.screen.blit(txt_surface, ((self.input_box.x + 5, self.input_box.y + 5)))
                pygame.draw.rect(self.screen, self.color, self.input_box, 2)

                pygame.display.flip() 

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.input_box.collidepoint(event.pos):
                            self.active = not self.active
                        else:
                            self.active = False
                        self.color = self.color_active if self.active else self.color_inactive
                    elif event.type == pygame.KEYDOWN and self.active:
                        if event.key == pygame.K_RETURN:
                            if user_input.isdigit():
                                user_input_int = int(user_input)
                                if user_input_int in free_boxes:
                                    free_boxes.remove(user_input_int)
                                    boxes_list.append(user_input_int)
                                    busy_box = False
                                    user_input = ''
                                    run = False
                                elif not user_input.isdigit() or not user_input in free_boxes:
                                    busy_box = True
                                    user_input = ''
                        elif event.key == pygame.K_BACKSPACE:
                            user_input = user_input[:-1]
                        else:
                            user_input += event.unicode
            run = True
        return boxes_list

    def take_player_wager(self, box_position):
        wager = ''
        self.show_invalid_message = False

        'range(10, self.balance + 1)'

        while True:
            self.screen.fill('skyblue')

            if not self.show_invalid_message:
                self.draw_text(f"Enter the desired wager, which can be somewhere between 10 and {self.logic.player.balance}, in the box at position {box_position}: ", self.BLACK, (200, 250))
            else:
                self.draw_text("Invalid input. Please try again.", self.RED, (400,250))
            
            txt_surface = self.input_font.render(wager, True, self.BLACK)
            width = max(200, txt_surface.get_width() + 10)
            self.input_box.w = width
            self.screen.blit(txt_surface, ((self.input_box.x + 5, self.input_box.y + 5)))
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        if wager.isdigit():
                            wager = int(wager)
                        if 10 <= wager <= self.logic.player.balance:
                            self.show_invalid_message = False
                            return wager
                        self.show_invalid_message = True
                        wager = ''
                    elif event.key == pygame.K_BACKSPACE:
                        wager = wager[:-1]
                    else:
                        wager += event.unicode

    def choose_yes_or_no(self, prompt, values, is_digit=True):
        choice = ''
        self.show_invalid_message = False

        while True:
            self.screen.fill('skyblue')

            if not self.show_invalid_message:
                self.draw_text(prompt, self.BLACK, (350, 250))
            else:
                self.draw_text(f'Invalid input. Please try again. Enter either {values[0]} or {values[1]}.', self.RED, (400, 250))

            txt_surface = self.input_font.render(choice, True, self.BLACK)
            width = max(200, txt_surface.get_width() + 10)
            self.input_box.w = width
            self.screen.blit(txt_surface, ((self.input_box.x + 5, self.input_box.y + 5)))
            pygame.draw.rect(self.screen, self.color, self.input_box, 2)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                    else:
                        self.active = False
                    self.color = self.color_active if self.active else self.color_inactive
                elif event.type == pygame.KEYDOWN and self.active:
                    if event.key == pygame.K_RETURN:
                        if is_digit and choice.isdigit():
                            choice = int(choice)
                            if choice in values:
                                self.show_invalid_message = False
                                return choice
                        elif not is_digit and choice.isalpha():
                            self.show_invalid_message = False
                            return choice
                        else:
                            self.show_invalid_message = True
                            choice = ''
                    elif event.key == pygame.K_BACKSPACE:
                        wager = wager[:-1]
                    else:
                        wager += event.unicode

    def deal_initial_cards(self):
        self.screen.fill('skyblue')
        for i in range(7):
            left_float = 215 * i
            pygame.draw.rect(self.screen, 'darkblue', [12 + left_float, 12, 190, 320], 0, 5)

        for box in self.logic.player.boxes:
            x, y, width, height = box.coordinates

            # Adjust card position inside the box
            card_x = x + (width // 2) - 30  # Center the card horizontally
            card_y = y + (height // 3)      # Place the card vertically inside the box

            # Draw one card for the box
            new_card = self.logic.deck.draw_card()
            box.cards.append(new_card.value)

            # Draw the new card
            pygame.draw.rect(self.screen, 'white', [card_x, card_y, 60, 90], 0, 5)  # Card background
            self.screen.blit(self.font.render(new_card.rank, True, "black"), (card_x + 10, card_y + 10))  # Card rank

        # Deal one card to the dealer
        dealer_x, dealer_y = 1000, 50  # Fixed dealer position
        new_card = self.logic.deck.draw_card()
        self.logic.dealer.cards.append(new_card.value)
        self.logic.dealer.result = sum(self.logic.dealer.cards)

        # Draw the dealer's card
        pygame.draw.rect(self.screen, 'white', [dealer_x, dealer_y, 60, 90], 0, 5)  # Card background
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (dealer_x + 10, dealer_y + 10))  # Card rank

        pygame.display.flip()
        
        # in case of insurance
        if self.logic.dealer.cards[0] == 1: 
            self.logic.dealer.insurance = True
            for box in self.logic.player.boxes:
                player_choice = self.choose_yes_or_no("It is insurance time. Would you like to insure your bets? If yes, please enter Y otherwise enter N: ")

                if player_choice == "Y": 
                    box.wager += box.wager / 2 
                    box.insurance = True

                    self.screen.fill('skyblue')
                    self.draw_text("You just made an insurance. If the dealer has a blackjack, you will lose your original wager but the insurance bet will be paid 2 to 1.", self.BLACK, (200,250))
                else:
                    self.screen.fill('skyblue')
                    self.draw_text("You have just chosen not to insure your bets.", self.BLACK, (200,250))

    def run(self):
        self.logic.player.name = self.take_player_name()
        self.logic.player.balance = self.take_player_balance()
        self.display_greetings()
        num_of_boxes = self.take_num_of_boxes()
        boxes_positions = self.pick_free_box(num_of_boxes)
        print(boxes_positions)

        for i in range(len(boxes_positions)):
            wager = self.take_player_wager(boxes_positions[i])
            self.logic.player.balance -= wager
            left_float = 215 * boxes_positions[i] 
            self.logic.player.boxes.append(Box(boxes_positions[i], wager, (12 + left_float, 12, 190, 320)))

        self.draw_boxes()
        self.deal_initial_cards()
        

game = RenderGame()
game.run()