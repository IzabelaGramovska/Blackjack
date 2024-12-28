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
        return f"{self.rank}" 

class Deck: 
    def __init__(self):
        self.replenish_deck()

    def replenish_deck(self):
        self.cards = 6 * [Card(rank) for rank in ranks]
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            self.replenish_deck()
        return self.cards.pop() if self.cards else None
    
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
        self.buttons = []
        self.hit_button = self.draw_button('HIT', [80, 670, 150, 60], (87, 675))
        self.stay = self.draw_button('STAY', [80, 570, 150, 60], (87, 575))
        self.split_butt = self.draw_button('SPLIT', [80, 470, 150, 60], (87, 475))
        self.double = self.draw_button('DOUBLE', [280, 650, 150, 60], (287, 655))
        self.surrender_button = self.draw_button('SURRENDER', [280, 550, 150, 60], (287, 555))

    def draw_text(self, text, color, position):
        prompt_surface = self.font.render(text, True, color)
        self.screen.blit(prompt_surface, position)

    def take_input(self, prompt, is_digit=False, valid_range=None, position=(400, 250)):
        user_input = ''
        self.show_invalid_message = False
        
        while True:
            self.screen.fill('skyblue')
            self.draw_text(prompt, self.BLACK, position)

            if self.show_invalid_message:
                self.draw_text("Invalid input. Please try again.", self.RED, (400, 310))

            
            txt_surface = self.input_font.render(user_input, True, self.BLACK)
            self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
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
                        if is_digit and user_input.isdigit():
                            user_input = int(user_input)
                            if valid_range and user_input in valid_range:
                                return user_input
                        elif not is_digit and user_input.strip():
                            return user_input.strip()
                        self.show_invalid_message = True
                        user_input = ''
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode

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

    def take_player_wager(self, box_position, split_choice=False):
        wager = ''
        self.show_invalid_message = False

        while True:
            self.screen.fill('skyblue')

            if not self.show_invalid_message:
                if split_choice:
                    self.draw_text(f"Enter the desired wager, which can be somewhere between 10 and {self.logic.player.balance}, in your extra box: ", self.BLACK, (200, 250))
                else:
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
                            wager_int = int(wager)
                        if 10 <= wager_int <= self.logic.player.balance:
                            self.show_invalid_message = False
                            return wager_int
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
                self.draw_text(prompt, self.BLACK, (300, 250))
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
                            choice_int = int(choice)
                            if choice_int in values:
                                self.show_invalid_message = False
                                return choice_int
                        elif not is_digit and choice.isalpha():
                            self.show_invalid_message = False
                            return choice
                        else:
                            self.show_invalid_message = True
                            choice = ''
                    elif event.key == pygame.K_BACKSPACE:
                        choice = choice[:-1]
                    else:
                        choice += event.unicode

    def deal_initial_cards(self):
        self.screen.fill('skyblue')
        for i in range(7):
            left_float = 215 * i
            pygame.draw.rect(self.screen, 'darkblue', [12 + left_float, 12, 190, 320], 0, 5)

        for box in self.logic.player.boxes:
            self.deal_a_new_card(box)  # This also calls draw_score

        # Deal dealer's card (unchanged)
        dealer_x, dealer_y = 640, 630
        new_card = self.logic.deck.draw_card()
        self.logic.dealer.cards.append(new_card.value)
        self.logic.dealer.result = sum(self.logic.dealer.cards)
        pygame.draw.rect(self.screen, 'white', [dealer_x, dealer_y, 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'blue', [dealer_x, dealer_y, 80, 110], 3, 5)  # Card border
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (dealer_x + 10, dealer_y + 10))

        pygame.display.flip()
        
        # in case of insurance
        if self.logic.dealer.cards[0] == 1: 
            self.logic.dealer.insurance = True
            for box in self.logic.player.boxes:
                player_choice = self.choose_yes_or_no("It is insurance time. Would you like to insure your bets? If yes, please enter Y otherwise enter N: ", ['Y', 'N'], is_digit=False)

                if player_choice == "Y": 
                    box.wager += box.wager / 2 
                    box.insurance = True

                    self.screen.fill('skyblue')
                    self.draw_text("You just made an insurance. If the dealer has a blackjack, you will lose your original wager but the insurance bet will be paid 2 to 1.", self.BLACK, (200,250))
                else:
                    self.screen.fill('skyblue')
                    self.draw_text("You have just chosen not to insure your bets.", self.BLACK, (200,250))

    def render_decision_buttons(self, actions):
        button_area_rect = pygame.Rect(50, 650, 1000, 100)
        pygame.draw.rect(self.screen, 'skyblue', button_area_rect)

        buttons = {}

        button_position = {
            "HIT": [80, 670, 150, 60],
            "STAY": [280, 670, 150, 60],
            "SPLIT": [480, 670, 150, 60],
            "DOUBLE": [680, 670, 150, 60],
            "SURRENDER": [880, 670, 150, 60], 
        }

        button_text_positions = {
            "HIT": (100, 680),
            "STAY": (300, 680),
            "SPLIT": (500, 680),
            "DOUBLE": (700, 680),
            "SURRENDER": (900, 680),
        }

        for action in actions:
            if action in button_position:
                rect = button_position[action]
                text_pos = button_text_positions[action]
                button = self.draw_button(action, rect, text_pos)
                buttons[action] = button
        
        pygame.display.update(button_area_rect)
        return buttons

    def handle_decision_input(self, box):
        """Handle decision input from the player based on valid actions."""
        # Determine valid actions based on the box's state.
        actions = ["HIT", "STAY", "SURRENDER"]  # Base actions always available.
        if len(box.cards) == 2 and box.cards[0] == box.cards[1]:  # Allow split if cards are identical.
            actions.append("SPLIT")
        if len(box.cards) == 2 and 9 <= box.result <= 11:  # Allow double down for specific results.
            actions.append("DOUBLE")

        buttons = self.render_decision_buttons(actions)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    for action, button in buttons.items():
                        if button.collidepoint(event.pos):
                            if action == "HIT":
                                self.deal_a_new_card(box)
                                return "HIT"
                            elif action == "STAY":
                                return "STAY"
                            elif action == "SPLIT":
                                self.split(box)
                                return "SPLIT"
                            elif action == "DOUBLE":
                                self.double_down(box)
                                return "DOUBLE"
                            elif action == "SURRENDER":
                                self.surrender(box)
                                return "SURRENDER"            

    def deal_a_new_card(self, box):
        new_card = self.logic.deck.draw_card()
        box.cards.append(new_card.value)

        x, y, width, height = box.coordinates

        # Calculate card position: each new card is placed slightly diagonally
        card_spacing_x = 15  # Horizontal spacing between cards
        card_spacing_y = 25  # Vertical spacing between cards
        card_x = x + 10 + (len(box.cards) - 1) * card_spacing_x
        card_y = y + 20 + (len(box.cards) - 1) * card_spacing_y

        # Draw the card
        pygame.draw.rect(self.screen, 'white', [card_x, card_y, 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'red', [card_x, card_y, 80, 110], 3, 5)  # Card border
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (card_x + 10, card_y + 10))

        # Update the score display below the box
        box.result = sum(box.cards)
        self.draw_score(box)

        pygame.display.flip()

    def deal_dealer_cards(self, index):
        new_card = self.logic.deck.draw_card()
        self.logic.dealer.cards.append(new_card.value)
        self.logic.dealer.result = sum(self.logic.dealer.cards)

        dealer_x, dealer_y = 640, 630
        pygame.draw.rect(self.screen, 'white', [dealer_x + (dealer_x * index), dealer_y  + (5 * index), 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'blue', [dealer_x + (dealer_x * index), dealer_y  + (5 * index), 80, 110], 3, 5)   # Card background
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (dealer_x + 10, dealer_y + 10))  # Card rank

        pygame.display.flip()

        self.draw_dealer_score()

    def draw_button(self, text, coordinates, position):
        button = pygame.draw.rect(self.screen, 'green', coordinates, 0, 5)
        pygame.draw.rect(self.screen, "white", coordinates, 3, 5)

        text_surface = self.font.render(text, True, self.BLACK)
        text_width, text_height = text_surface.get_size()

        button_x, button_y, button_width, button_height = coordinates
        text_x = button_x + (button_width - text_width) // 2
        text_y = button_y + (button_height - text_height) // 2

        self.screen.blit(text_surface, (text_x, text_y))
        self.buttons.append(button)

        pygame.display.flip()

    def draw_score(self, box, extra_box=False, tie=False, win=False, lose=False):
        x, y, width, height = box.coordinates

        # Clear the score area below the box
        pygame.draw.rect(self.screen, 'skyblue', [x, y + height + 10, width, 30])

        if box.blackjack:
            self.screen.blit(self.font.render('BJ', True, self.BLACK), (x + 10, y + height + 15))
        elif box.surrender:
            self.screen.blit(self.font.render('SURRENDERED', True, self.BLACK), (x + 10, y + height + 15))
        elif tie:
            self.screen.blit(self.font.render('TIE', True, self.BLACK), (x + 10, y + height + 15))
        elif win:
            self.screen.blit(self.font.render('WIN', True, self.BLACK), (x + 10, y + height + 15))
        elif win:
            self.screen.blit(self.font.render('LOSE', True, self.BLACK), (x + 10, y + height + 15))
        elif box.splitted and not extra_box:
            self.screen.blit(self.font.render(f'Score[{box.result}]', True, self.BLACK), (x + 10, y + height + 15))
        elif box.splitted and extra_box:
            self.screen.blit(self.font.render(f'Score[{box.result}]', True, self.BLACK), (x + 10, y + height + 15))
        elif box.busted:
            self.screen.blit(self.font.render('BUSTED', True, self.RED), (x + 10, y + height + 15))
        else:
            self.screen.blit(self.font.render(f'Score[{box.result}]', True, self.BLACK), (x + 10, y + height + 15))
        
        pygame.display.flip()
        
    def draw_dealer_score(self):
        self.screen.blit(self.font.render(f'Score[{self.logic.dealer.result}]', True, self.BLACK), (687, 475)) 

    def draw_profit(self):
        for box in self.logic.player.boxes:
            x, y, width, height = box.coordinates
            self.screen.blit(self.font.render(f'PROFIT: {box.profit}', True, self.BLACK), ((y + height) + 80, (x + width) + 60))

    def split(self, box):
        extra_box_wager = self.take_player_wager(8, split_choice = True)
        self.balance -= int(extra_box_wager) 
        
        extra_box_wager_int = int(extra_box_wager)
        extra_box_cards = box.cards[1]
        box.cards.pop(1)
        extra_box = Box(len((self.logic.player.boxes) + 1), extra_box_wager_int, extra_box_cards)
        extra_box.splitted = True
        box.splitted = True

        # Draw the box again
        x, y, width, height = box.coordinates
        pygame.draw.rect(self.screen, 'darkblue', box.coordinates, 0, 5)

        card_spacing = 30
        # original card_x = x + 10 + (len(box.cards) - 1) * card_spacing 
        card_x = x + 5 + (len(box.cards) - 1) * card_spacing
        # original card_y = y + 20
        card_y = y + 10  

        # Draw the first card of the split
        pygame.draw.rect(self.screen, 'white', [card_x, card_y, 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'red', [card_x, card_y, 80, 110], 3, 5)  # Card border
        self.screen.blit(self.font.render(box.cards[0].rank, True, "black"), (card_x + 10, card_y + 10))

        pygame.display.flip()

        card_x = x + 35 + (len(box.cards) - 1) * card_spacing
        card_y = y + 40  

        # Draw the second - first card of the split
        pygame.draw.rect(self.screen, 'white', [card_x, card_y, 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'red', [card_x, card_y, 80, 110], 3, 5)  # Card border
        self.screen.blit(self.font.render(extra_box.cards[0].rank, True, "black"), (card_x + 10, card_y + 10))

        pygame.display.flip()

        # Draw the second cards to the boxes
        #To the first one
        new_card = self.logic.deck.draw_card()
        box.cards.append(new_card.value)

        card_spacing = 30  
        card_x = x + 5 + (len(box.cards) - 1) * card_spacing  
        card_y = y + 10  

        # Ensure cards don't overflow the box width
        max_cards_in_row = (width - 20) // card_spacing  # Max cards in a single row
        if len(box.cards) > max_cards_in_row:
            card_x = x + 5 + ((len(box.cards) - 1) % max_cards_in_row) * card_spacing
            card_y = y + 10 + ((len(box.cards) - 1) // max_cards_in_row) * 50  # Move down a row

        # Draw the card
        pygame.draw.rect(self.screen, 'white', [card_x, card_y, 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'red', [card_x, card_y, 80, 110], 3, 5)  # Card border
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (card_x + 10, card_y + 10))

        pygame.display.flip()

        #To the second one
        new_card = self.logic.deck.draw_card()
        extra_box.cards.append(new_card.value)

        card_spacing = 30  
        card_x = x + 35 + (len(box.cards) - 1) * card_spacing  
        card_y = y + 40  

        # Ensure cards don't overflow the box width
        max_cards_in_row = (width - 20) // card_spacing  # Max cards in a single row
        if len(box.cards) > max_cards_in_row:
            card_x = x + 35 + ((len(box.cards) - 1) % max_cards_in_row) * card_spacing
            card_y = y + 40 + ((len(box.cards) - 1) // max_cards_in_row) * 50  # Move down a row

        # Draw the card
        pygame.draw.rect(self.screen, 'white', [card_x, card_y, 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'red', [card_x, card_y, 80, 110], 3, 5)  # Card border
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (card_x + 10, card_y + 10))

        pygame.display.flip()
        
        for single_box in list(box, extra_box): 
            single_box.result = sum(single_box.cards)
 
            if 1 in single_box and single_box.result <= 11 and not single_box.addedten:
                single_box.result += 10
                box.addedten = True
                
                if extra_box:
                    self.draw_score(single_box, extra_box=True)
                else:
                    self.draw_score(single_box)

                
                if single_box.result < 21:
                    run = True
                    while run:
                        self.hit_button
                        self.stay
                        self.surrender_button

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                run = False
                            if event.type == pygame.MOUSEBUTTONUP:
                                if self.hit_button.collidepoint(event.pos):
                                    single_box.cards = self.hit(single_box.cards)
                                    single_box.result = sum(single_box.cards)
                                    
                                    if single_box.result > 21 and not single_box.addedten:
                                        self.screen.fill('skyblue')
                                        self.draw_text("You are busted! You lose this game. You loose all the money you have wagered! Go and cry :D!", self.BLACK, (400, 250))
                                        single_box.busted = True
                                        if extra_box:
                                            self.draw_score(single_box, extra_box=True)
                                        else:
                                            self.draw_score(single_box)
                                        run = False
                                    elif single_box.result > 21 and single_box.addedten:
                                        single_box.result -= 10
                                        single_box.addedten = False

                                    if extra_box:
                                        self.draw_score(single_box, extra_box=True)
                                    else:
                                        self.draw_score(single_box)
                                elif self.stay.collidepoint(event.pos):
                                    if extra_box:
                                        self.draw_score(single_box, extra_box=True)
                                    else:
                                        self.draw_score(single_box)
                                    run = False
                                elif self.surrender_button.collidepoint(event.pos):
                                    if extra_box:
                                        self.draw_score(single_box, extra_box=True)
                                    else:
                                        self.draw_score(single_box)
                                    single_box.surrender = True
                                    run = False
            elif 1 in single_box.cards and 10 in single_box.cards:
                if extra_box:
                    self.draw_score(single_box, extra_box=True)
                else:
                    self.draw_score(single_box)
                break
            elif single_box.result < 21: 
                run = True
                while run:
                    self.hit_button
                    self.stay
                    self.surrender_button

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.MOUSEBUTTONUP:
                            if self.hit_button.collidepoint(event.pos):
                                single_box.cards = self.hit(single_box.cards)
                                single_box.result = sum(single_box.cards)
                                if extra_box:
                                    self.draw_score(single_box, extra_box=True)
                                else:
                                    self.draw_score(single_box)
                                if single_box.result > 21:
                                    self.screen.fill('skyblue')
                                    self.draw_text("You are busted! You lose this game. You loose all the money you have wagered! Go and cry :D!", self.BLACK, (400, 250))
                                    single_box.busted = True
                                    run = False
                            elif self.stay.collidepoint(event.pos):
                                if extra_box:
                                    self.draw_score(single_box, extra_box=True)
                                else:
                                    self.draw_score(single_box)
                                run = False
                            elif self.surrender_button.collidepoint(event.pos):
                                if extra_box:
                                    self.draw_score(single_box, extra_box=True)
                                else:
                                    self.draw_score(single_box)
                                single_box.surrender = True
                                run = False

    def hit(self, box):
        self.deal_a_new_card(box)
        
        return box.cards

    def surrender(self, box): 
        box.surrender = True 
        box.profit = box.wager / 2 
        self.draw_score(box)

    def double_down(self, box):  
        self.deal_a_new_card(box)
        box.wager += box.wager 
        
        if box.result > 21:
            box.busted = True 
            self.draw_score(box)
            self.screen.fill('skyblue')
            self.draw_text(f"Your result is {box.result}. You are busted and lose this game. You loose all the money you have wagered! Go and cry :D!", self.RED, (400,250))
            
        elif box.cards[2] == 1 and box.result <= 10: 
            box.result += 10
            box.addedten = True
        self.draw_score(box)

    def handle_blackjack(self, box):
        if 1 in box.cards and 10 in box.cards:
            box.blackjack = True 
            box.profit = box.wager * 3

            self.screen.fill('skyblue')

            if box.insurance:
                self.draw_text(f"You have a BlackJack and you win! Your profit is {box.profit}. Congratulations!", self.BLACK, (400,250))
            else:
                self.draw_text(f"You have a BlackJack and you win! Your profit is {box.profit}. Congratulations!", self.BLACK, (400,250))

            return True
        return False

    def handle_split(self, box):
        if box.cards[0] == box.cards[1]:
            self.hit_button
            self.split_butt
            self.surrender_button
            self.stay

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.hit_button.collidepoint(event.pos):
                            box.cards = self.hit(box.cards)
                            box.result = sum(box.cards)
                            self.draw_score(box)
                            run = True
                            while run:
                                while box.result < 21:
                                    self.hit_button
                                    self.stay
                                    self.surrender_button

                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False
                                        if event.type == pygame.MOUSEBUTTONUP:
                                            if self.hit_button.collidepoint(event.pos):
                                                box.cards = self.hit(box.cards)
                                                box.result = sum(box.cards)
                                                self.draw_score(box)
                                            elif self.stay.collidepoint(event.pos):
                                                self.draw_score(box)
                                                run = False
                                            elif self.surrender_button.collidepoint(event.pos):
                                                self.draw_score(box)
                                                box.surrender = True
                                                run = False
                        elif self.stay.collidepoint(event.pos):
                            self.draw_score(box)
                            run = False
                        elif self.surrender_button.collidepoint(event.pos):
                            box.surrender = True
                            self.draw_score(box)
                            run = False
                        elif self.split_butt.collidepoint(event.pos):
                            self.split(box)
                        return True
        return False

    def handle_busted(self, box):
        if box.result > 21: 
            box.busted = True
            self.screen.fill('skyblue')
            self.draw_text("You are busted! You lose this game and all the money you have wagered! Go and cry :D!", self.RED, (400,250))

            self.draw_score(box)
            return True
        return False
    
    def handle_double_down(self, box):
        if box.result in [9,10,11]:
            self.hit_button
            self.double

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.hit_button.collidepoint(event.pos):
                            box.cards = self.hit(box.cards)
                            box.result = sum(box.cards)
                            self.draw_score(box)
                            run = True
                            while run:
                                while box.result < 21:
                                    self.hit_button
                                    self.stay
                                    self.surrender_button
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False
                                        if event.type == pygame.MOUSEBUTTONUP:
                                            if self.hit_button.collidepoint(event.pos):
                                                box.cards = self.hit(box.cards)
                                                box.result = sum(box.cards)
                                                self.draw_score(box)
                                            elif self.stay.collidepoint(event.pos):
                                                self.draw_score(box)
                                                run = False
                                                break
                                            elif self.surrender_button.collidepoint(event.pos):
                                                self.draw_score(box)
                                                box.surrender = True
                                                run = False
                                                break
                                if box.result > 21:
                                    self.screen.fill('skyblue')
                                    self.draw_score(box)
                                    self.draw_text("You are busted! You lose this game and all the money you have wagered! Go and cry :D!", self.RED, (400,250))
                                    box.busted = True
                                    run = False
                        elif self.stay.collidepoint(event.pos):
                            self.draw_score(box)
                            run = False
                        elif self.surrender_button.collidepoint(event.pos):
                            box.surrender = True
                            self.draw_score(box)
                            run = False
                        elif self.split_butt.collidepoint(event.pos):
                            self.split(box)
                        return True
        return False
    
    def handle_1_or_11(self, box):
        if 1 in box.cards and box.result <= 11: 
            box.result += 10
            box.addedten = True
            self.draw_score(box)

            self.hit_button
            self.stay
            self.surrender_button

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.hit_button.collidepoint(event.pos):
                            box.cards = self.hit(box.cards)
                            box.result = sum(box.cards)
                            self.draw_score(box)
                            run = True
                            while run:
                                while box.result < 21:
                                    self.hit_button
                                    self.stay
                                    self.surrender_button

                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False
                                        if event.type == pygame.MOUSEBUTTONUP:
                                            if self.hit_button.collidepoint(event.pos):
                                                box.cards = self.hit(box.cards)
                                                box.result = sum(box.cards)
                                                self.draw_score(box)
                                                if box.result > 21 and box.addedten:
                                                    box.result -= 10
                                                    box.addedten = False
                                                    self.draw_score(box)
                                            elif self.stay.collidepoint(event.pos):
                                                self.draw_score(box)
                                                run = False
                                            elif self.surrender_button.collidepoint(event.pos):
                                                self.draw_score(box)
                                                box.surrender = True
                                                run = False
                                if box.result > 21 and not box.addedten:
                                    self.screen.fill('skyblue')
                                    self.draw_score(box)
                                    self.draw_text("You are busted! You lose this game and all the money you have wagered! Go and cry :D!", self.RED, (400,250))
                                    box.busted = True
                                    run = False
                        elif self.stay.collidepoint(event.pos):
                            self.draw_score(box)
                            run = False
                        elif self.surrender_button.collidepoint(event.pos):
                            box.surrender = True
                            self.draw_score(box)
                            run = False
                        return True
        return False

    def handle_hit_stay_surrender(self,box):
        if box.result < 21:
            self.hit_button
            self.stay
            self.surrender_button

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.hit_button.collidepoint(event.pos):
                            box.cards = self.hit(box.cards)
                            box.result = sum(box.cards)
                            self.draw_score(box)
                            run = True
                            while run:
                                while box.result < 21:
                                    self.hit_button
                                    self.stay
                                    self.surrender_button

                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False
                                        if event.type == pygame.MOUSEBUTTONUP:
                                            if self.hit_button.collidepoint(event.pos):
                                                box.cards = self.hit(box.cards)
                                                box.result = sum(box.cards)
                                                self.draw_score(box)
                                                if box.result > 21 and box.addedten:
                                                    box.result -= 10
                                                    box.addedten = False
                                                    self.draw_score(box)
                                            elif self.stay.collidepoint(event.pos):
                                                self.draw_score(box)
                                                run = False
                                            elif self.surrender_button.collidepoint(event.pos):
                                                self.draw_score(box)
                                                box.surrender = True
                                                run = False
                                if box.result > 21 and not box.addedten:
                                    self.screen.fill('skyblue')
                                    self.draw_score(box)
                                    self.draw_text("You are busted! You lose this game and all the money you have wagered! Go and cry :D!", self.RED, (400,250))
                                    box.busted = True
                                    run = False
                                if box.result > 21 and box.addedten:
                                    box.result -= 10
                                    box.addedten = False
                                    self.draw_score(box)
                        elif self.stay.collidepoint(event.pos):
                            self.draw_score(box)
                            run = False
                        elif self.surrender_button.collidepoint(event.pos):
                            box.surrender = True
                            self.draw_score(box)
                            run = False
                        return True
        return False

    def deal_other_dealer_cards(self):
        offset = -1
        dealmorecards = False

        for box in self.logic.player.boxes:
            if not box.blackjack and not box.surrender and not box.busted:
                dealmorecards = True

        if dealmorecards:
            offset += 1
            self.deal_dealer_cards(offset)
        
            if self.logic.dealer.cards[0] == 1 and self.logic.dealer.cards[1] == 10:
                for box in self.logic.player.boxes:
                    if box.insurance:
                        box.profit = box.wager / 2
                        self.draw_text("Insurance win! Your addtional insuarnce bet is paid 2:1.", self.BLACK, (400, 250))
                        self.draw_score(box, win=True)
                    elif not box.insurance:
                        box.profit = 0
                        self.draw_text("Insurance win! Unfortunately you loose all your wager", self.BLACK, (400, 250))
                        self.draw_score(box, lose=True)
                    break

            while self.logic.dealer.result < 17:
                offset += 1
                self.deal_dealer_cards(offset)
                        
                if 17 < self.logic.dealer.result < 22:
                    for box in self.logic.player.boxes:
                        if box.result == self.logic.dealer.result and not box.surrender:
                            self.draw_score(box, tie=True)

                        elif not box.busted and not box.blackjack and not box.surrender and box.result > self.logic.dealer.result:
                            box.profit = box.wager * 2
                            self.draw_score(box, win=True)
                    
                        elif not box.busted and not box.blackjack and not box.surrender and box.result < self.logic.dealer.result:
                            self.draw_score(box, lose=True)
                elif self.logic.dealer.result > 21:
                    for box in self.logic.player.boxes:
                        if not box.busted and not box.surrender:
                            box.profit = box.wager * 2
                            self.draw_score(box, win=True)        
    def run(self):
        self.logic.player.name = self.take_input("Enter your name please:", position=(600, 250))
        self.draw_text(f"Hello {self.logic.player.name}! Let's start playing!", self.BLACK, (410,350))
        self.logic.player.balance = self.take_input("Enter your balance ranging from 10 to 100000", is_digit=True, valid_range=range(10, 100001), position=(600,250))

        num_of_boxes = self.take_input("Enter the number of boxes you would like to pay with, ranging from 1 to 7 inclusive:", is_digit=True, valid_range=range(1,8))
        boxes_positions = self.pick_free_box(num_of_boxes)

        for i in range(len(boxes_positions)):
            wager = self.take_player_wager(boxes_positions[i])
            self.logic.player.balance -= wager
            left_float = 215 * boxes_positions[i] 
            self.logic.player.boxes.append(Box(boxes_positions[i], wager, (12 + left_float, 12, 190, 320)))

        self.deal_initial_cards()

        for box in self.logic.player.boxes:
            self.deal_a_new_card(box)
            self.draw_score(box)
            
        for box in self.logic.player.boxes:
            box.result = sum(box.cards)
            
            if self.handle_blackjack(box):
                break
            elif self.handle_busted(box):
                break
            elif self.handle_double_down(box):
                break
            elif self.handle_1_or_11(box):
                break
            elif self.handle_split(box):
                break
            else:
                self.handle_hit_stay_surrender(box)

        self.deal_other_dealer_cards()
        self.draw_profit()

        # Add an exit loop to keep the screen visible
        while True:
            self.screen.fill('skyblue')
            self.draw_text("Game in progress...", self.BLACK, (400, 300))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

game = RenderGame()
game.run()