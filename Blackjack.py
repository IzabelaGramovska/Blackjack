import pygame
import random
import sys
import math

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
                self.screen.fill('skyblue')
                self.draw_text("Invalid input. Please try again.", self.RED, (500, 250))

            
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
                    self.draw_text(f"Enter the desired wager, which can be somewhere between 10 and {self.logic.player.balance}, in your extra box: ", self.BLACK, (300, 250))
                else:
                    self.draw_text(f"Enter the desired wager, which can be somewhere between 10 and {self.logic.player.balance}, in the box at position {box_position}: ", self.BLACK, (300, 250))
            else:
                self.draw_text("Invalid input. Please try again.", self.RED, (380,250))


            
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

    def choose_yes_or_no(self, prompt, values):
        choice = ''
        self.show_invalid_message = False

        while True:
            self.screen.fill('skyblue')

            if not self.show_invalid_message:
                self.draw_text(prompt, self.BLACK, (300, 250))
            else:
                self.draw_text(f'Invalid input. Please try again. Enter either {values[0]} or {values[1]}.', self.RED, (400, 250))

            txt_surface = self.input_font.render(choice, True, self.BLACK)
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
                        if choice.strip().upper() in values:
                            return choice.strip().upper()
                        else:
                            self.show_invalid_message = True
                            choice = ''
                    elif event.key == pygame.K_BACKSPACE:
                        choice = choice[:-1]
                    else:
                        choice += event.unicode
    def draw_box_with_cards(self, box):
        x, y, width, height = box.coordinates
        pygame.draw.rect(self.screen, 'darkblue', [x, y, width, height], 0, 5)

        if box.splitted:
            half_width = width // 2
            card_spacing_x = 15
            card_spacing_y = 25

            for i, card_value in enumerate(box.cards[0]):
                card_x = x + 10 + i * card_spacing_x
                card_y = y + 20 + i * card_spacing_y
                pygame.draw.rect(self.screen, 'white', [card_x, card_y, 40, 60], 0, 5)
                pygame.draw.rect(self.screen, 'red', [card_x, card_y, 40, 60], 3, 5)
                card_rank = next(rank for rank, value in values.items() if value == card_value)
                self.screen.blit(self.font.render(card_rank, True, "black"), (card_x + 10, card_y + 10))

            for i, card_value in enumerate(box.cards[1]):
                card_x = x + half_width + 10 + i * card_spacing_x
                card_y = y + 20 + i * card_spacing_y
                pygame.draw.rect(self.screen, 'white', [card_x, card_y, 40, 60], 0, 5)
                pygame.draw.rect(self.screen, 'red', [card_x, card_y, 40, 60], 3, 5)
                card_rank = next(rank for rank, value in values.items() if value == card_value)
                self.screen.blit(self.font.render(card_rank, True, "black"), (card_x + 10 , card_y + 10))
        else:
            card_spacing_x = 15
            card_spacing_y = 25
            for i, card_value in enumerate(box.cards):
                card_x = x + 10 + i * card_spacing_x
                card_y = y + 20 + i * card_spacing_y
                pygame.draw.rect(self.screen, 'white', [card_x, card_y, 80, 110], 0, 5)
                pygame.draw.rect(self.screen, 'red', [card_x, card_y, 80, 110], 3, 5)
                card_rank = next(rank for rank, value in values.items() if value == card_value)
                self.screen.blit(self.font.render(card_rank, True, "black"), (card_x + 10, card_y + 10))

        self.draw_score(box)
    
    def deal_a_new_card_to_stack(self, box, stack_index):
        new_card = self.logic.deck.draw_card()
        box.cards[stack_index].append(new_card.value)

        stack_sum = sum(box.cards[stack_index])
        if 1 in box.cards[stack_index] and stack_sum <= 11:
            stack_sum += 10  

        box.result = stack_sum

        self.draw_box_with_cards(box)
        pygame.display.flip()

    def deal_initial_cards(self):
        self.screen.fill('skyblue')
        for i in range(7):
            left_float = 215 * i
            pygame.draw.rect(self.screen, 'darkblue', [12 + left_float, 12, 190, 320], 0, 5)

        for box in self.logic.player.boxes:
            self.deal_a_new_card(box)             

        dealer_x, dealer_y = 640, 630
        new_card = self.logic.deck.draw_card()
        self.logic.dealer.cards.append(new_card.value)
        self.logic.dealer.result = sum(card for card in self.logic.dealer.cards)
        pygame.draw.rect(self.screen, 'white', [dealer_x, dealer_y, 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'blue', [dealer_x, dealer_y, 80, 110], 3, 5) 
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (dealer_x + 10, dealer_y + 10))

        pygame.display.flip()
        pygame.time.wait(2000)
        
        if new_card.rank == 'A': 
            self.logic.dealer.insurance = True
            for box in self.logic.player.boxes:
                if self.logic.player.balance >= box.wager / 2:
                    player_choice = self.choose_yes_or_no(f"It is insurance time. Would you like to insure your bets in box at position {box.position}? If yes, please enter Y otherwise enter N: ", ['Y', 'N'])

                    if player_choice == "Y":
                        self.logic.player.balance -= box.wager / 2
                        box.wager += box.wager / 2
                        box.insurance = True
                else:
                    self.screen.fill('skyblue')
                    self.draw_text(f"Not enough balance for insurance on box {box.position}!", self.RED, (400, 300))
                    pygame.display.flip()
                    pygame.time.wait(2000)

            self.screen.fill('skyblue')
            for i in range(7):
                left_float = 215 * i
                pygame.draw.rect(self.screen, 'darkblue', [12 + left_float, 12, 190, 320], 0, 5)

            for box in self.logic.player.boxes:
                self.draw_box_with_cards(box)

            pygame.draw.rect(self.screen, 'white', [dealer_x, dealer_y, 80, 110], 0, 5)
            pygame.draw.rect(self.screen, 'blue', [dealer_x, dealer_y, 80, 110], 3, 5) 
            self.screen.blit(self.font.render(new_card.rank, True, "black"), (dealer_x + 10, dealer_y + 10))

            pygame.display.flip()
                
    def render_decision_buttons(self, actions):
        button_area_rect = pygame.Rect(20, 400, 350, 350)  
        pygame.draw.rect(self.screen, 'skyblue', button_area_rect)

        buttons = {}

        button_mapping = {
            "HIT": [50, 440, 200, 50],
            "STAY": [50, 500, 200, 50],
            "SPLIT": [50, 560, 200, 50],
            "DOUBLE": [50, 620, 200, 50],
            "SURRENDER": [50, 680, 200, 50], 
        }

        button_text_positions = {
            "HIT": (110, 445),
            "STAY": (110, 505),
            "SPLIT": (110, 565),
            "DOUBLE": (110, 625),
            "SURRENDER": (110, 685),
        }

        for action in actions:
            if action in button_mapping:
                rect = button_mapping[action]
                text_pos = button_text_positions[action]
                button = self.draw_button(action, rect, text_pos)
                buttons[action] = button

        pygame.display.update(button_area_rect)
        return buttons
    
    def deal_a_new_card_to_stack(self, box, stack_index):
        new_card = self.logic.deck.draw_card()
        box.cards[stack_index].append(new_card.value)

        stack_sum = sum(box.cards[stack_index])
        if 1 in box.cards[stack_index] and stack_sum <= 11:
            stack_sum += 10  

        box.result = stack_sum  
        self.draw_box_with_cards(box)  
        pygame.display.flip()

    def handle_decision_input(self, box, stack_index=None):
        actions = ["HIT", "STAY", "SURRENDER"]
        if len(box.cards) == 2 and box.cards[0] == box.cards[1] and self.logic.player.balance >= box.wager:
            actions.append("SPLIT")
        if not box.splitted and self.logic.player.balance >= box.wager * 2 and len(box.cards) == 2 and 9 <= box.result <= 11:
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
                            return action


    def deal_a_new_card(self, box, split_box_cards = []):
        new_card = self.logic.deck.draw_card()
        box.cards.append(new_card.value)

        box_sum = sum(box.cards)
        if 1 in box.cards and box_sum <= 11:
            box_sum += 10  

        box.result = box_sum

        self.draw_box_with_cards(box)
        pygame.display.flip()

    def deal_dealer_cards(self, index):
        new_card = self.logic.deck.draw_card()
        self.logic.dealer.cards.append(new_card.value)
        self.logic.dealer.result = sum(self.logic.dealer.cards)

        dealer_x, dealer_y = 640, 630
        pygame.draw.rect(self.screen, 'white', [dealer_x + (dealer_x * index), dealer_y  + (5 * index), 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'blue', [dealer_x + (dealer_x * index), dealer_y  + (5 * index), 80, 110], 3, 5)   
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (dealer_x + 10, dealer_y + 10))  

        pygame.display.flip()


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

        return button

    def draw_score(self, box, is_active=False, tie=False, win=False, lose=False):
        x, y, width, height = box.coordinates

        border_color = 'green' if is_active else 'darkblue'
        pygame.draw.rect(self.screen, border_color, [x, y, width, height], 5)

        pygame.draw.rect(self.screen, 'skyblue', [x, y + height + 10, width, 30])

        if box.splitted:
            stack1_score = sum(box.cards[0])
            stack2_score = sum(box.cards[1])

            stack1_score += 10 if 1 in box.cards[0] and stack1_score <= 11 else 0
            stack2_score += 10 if 1 in box.cards[1] and stack2_score <= 11 else 0

            score_text_1 = "BUSTED" if stack1_score > 21 else f"Score[{stack1_score}]"
            score_text_2 = "BUSTED" if stack2_score > 21 else f"Score[{stack2_score}]"

            self.screen.blit(self.font.render(score_text_1, True, self.RED if stack1_score > 21 else self.BLACK), (x + 7, y + height + 15))
            self.screen.blit(self.font.render(score_text_2, True, self.RED if stack2_score > 21 else self.BLACK), (x + 7 + width // 2, y + height + 15))
        else:
            score_text = "BUSTED" if box.busted else f"Score[{box.result}]"
            self.screen.blit(self.font.render(score_text, True, self.RED if box.busted else self.BLACK), (x + 10, y + height + 15))

        pygame.display.flip()
        
    def draw_dealer_score(self):
        pygame.draw.rect(self.screen, 'skyblue', [1000, 700, 200, 200])

        if self.logic.dealer.result > 21:
            self.screen.blit(self.font.render('BUSTED', True, self.BLACK), (900, 700))
        else:
            self.screen.blit(self.font.render(f'Score[{self.logic.dealer.result}]', True, self.BLACK), (900, 700))
        pygame.display.flip()

    def draw_profit(self):
        for box in self.logic.player.boxes:
            x, y, width, height = box.coordinates

            pygame.draw.rect(self.screen, 'skyblue', [x, y + height + 40, width, 30])

            self.screen.blit(
                self.font.render(f'PROFIT: {box.profit}', True, self.BLACK),
                (x + 10, y + height + 45)
            )

        pygame.display.flip()
    
    def draw_dealer_profit(self):
        pygame.draw.rect(self.screen, 'skyblue', [800, ])

    def split(self, box, card_rank):
        """Handles splitting of a box into two stacks."""
        if self.logic.player.balance < box.wager:
            self.screen.fill('skyblue')
            self.draw_text("Not enough balance to split!", self.RED, (400, 300))
            pygame.display.flip()
            pygame.time.wait(2000)
            return

        self.logic.player.balance -= box.wager
        box.splitted = True

        first_card = box.cards.pop(0)
        second_card = box.cards.pop(0)
        box.cards = [[first_card], [second_card]]

        for stack in box.cards:
            new_card = self.logic.deck.draw_card()
            stack.append(new_card.value)

        self.draw_box_with_cards(box)

        for i in range(len(box.cards)):
            stack_busted = False
            while not stack_busted:
                self.draw_box_with_cards(box)  
                self.draw_score(box, is_active=True)  

                decision = self.handle_decision_input(box, stack_index=i)
                if decision == "STAY":
                    break
                elif decision == "HIT":
                    self.deal_a_new_card_to_stack(box, stack_index=i)
                    stack_sum = sum(box.cards[i])
                    if 1 in box.cards[i] and stack_sum <= 11:
                        stack_sum += 10  
                    if stack_sum > 21:
                        stack_busted = True
                        self.draw_score(box) 
                        break
                elif decision == "DOUBLE":
                    self.deal_a_new_card_to_stack(box, stack_index=i)
                    box.wager *= 2
                    break
                elif decision == "SURRENDER":
                    self.surrender(box)
                    break

            self.draw_box_with_cards(box)
            self.draw_score(box)

        self.draw_score(box, is_active=False)

    def surrender(self, box): 
        box.surrender = True 
        box.profit = box.wager / 2 
        self.draw_score(box)

    def double_down(self, box):
        new_card = self.logic.deck.draw_card()
        box.cards.append(new_card.value)
        box.wager *= 2
        
        if len(box.cards) > 1 and 1 in box.cards and sum(box.cards) <= 11 and not box.addedten:
            box.result = sum(box.cards) + 10
            box.addedten = True
        elif len(box.cards)> 1 and 1 in box.cards and sum(box.cards) > 21 and box.addedten:
            box.result = sum(box.cards) -10
            box.addedten = False
        else:
            box.result = sum(box.cards)

        x, y, width, height = box.coordinates
        card_spacing_x = 15
        card_spacing_y = 25
        card_x = x + 10 + (len(box.cards) - 1) * card_spacing_x
        card_y = y + 20 + (len(box.cards) - 1) * card_spacing_y

        pygame.draw.rect(self.screen, 'white', [card_x, card_y, 80, 110], 0, 5)
        pygame.draw.rect(self.screen, 'red', [card_x, card_y, 80, 110], 3, 5) 
        self.screen.blit(self.font.render(new_card.rank, True, "black"), (card_x + 10, card_y + 10))

        self.draw_score(box)
        pygame.display.flip()

        if box.result > 21 and box.addedten:
            box.result -= 10
            box.addedten = False
        elif box.result > 21:
            box.busted = True

    def handle_blackjack(self, box):
        if 1 in box.cards and 10 in box.cards:
            box.blackjack = True 
            box.profit = box.wager * 3
            return True
        return False

    def handle_split(self, box, card_rank):
        self.split(box, card_rank)  

        for i in range(len(box.cards)): 
            while True:
                self.draw_score(box, is_active=True) 
                decision = self.handle_decision_input(box)
                if decision == "STAY":
                    break  
                elif decision == "HIT":
                    self.deal_a_new_card_to_stack(box, stack_index=i)
                    stack_sum = sum(box.cards[i])
                    if 1 in box.cards[i] and stack_sum <= 11:
                        stack_sum += 10  
                    if stack_sum > 21:
                        self.draw_score(box, is_active=True) 
                        break  
                elif decision == "DOUBLE":
                    self.deal_a_new_card_to_stack(box, stack_index=i)
                    box.wager *= 2  
                    break
                elif decision == "SURRENDER":
                    self.surrender(box)
                    break
        self.draw_score(box, is_active=False) 

    def handle_busted(self, box):
        if box.result > 21 and not box.addedten: 
            box.busted = True
            self.draw_score(box)
            return True
        return False
    
    def handle_double_down(self, box):
        if box.result in [9,10,11]:
            while True:
                decision = self.handle_decision_input(box)
                if decision == "STAY":
                    self.draw_score(box)
                    break
                elif decision == "HIT":
                    while box.result < 21:
                        decision = self.handle_decision_input(box)
                        if decision == "STAY":
                            self.draw_score(box)
                            break
                        elif decision == "HIT":
                            if box.cards[-1] == 1 and box.result <= 11 and not box.addedten:
                                box.result = sum(box.cards) + 10
                                box.addedten = True
                                self.draw_score(box)
                            else:
                                box.result = sum(box.cards)
                                self.draw_score(box)
                        elif decision == "SURRENDER":
                            box.surrender = True
                            self.draw_score(box)
                            break

                    if box.result > 21 and box.addedten:
                        box.result -= 10
                        box.addedten = False
                        self.draw_score(box)

                        while box.result < 21:
                            decision = self.handle_decision_input(box)

                            if decision == "STAY":
                                self.draw_score(box)
                                break
                            elif decision == "HIT":
                                if box.cards[-1] == 1 and box.result <= 11 and not box.addedten:
                                    box.result = sum(box.cards) + 10
                                    box.addedten = True
                                    self.draw_score(box)
                                else:
                                    box.result = sum(box.cards)
                                    self.draw_score(box)
                            elif decision == "SURRENDER":
                                box.surrender = True
                                self.draw_score(box)
                                break

                    if box.result > 21 and not box.addedten:
                        box.busted = True
                        self.draw_score(box)
                        break
                elif decision == "SURRENDER":
                    box.surrender = True
                    self.draw_score(box)
                    break
                elif decision == "DOUBLE":
                    return True
                return True
        return False

    def handle_hit_stay_surrender(self,box):
        if box.result < 21:
            while True:
                decision = self.handle_decision_input(box)
                if decision == "STAY":
                    self.draw_score(box)
                    break
                elif decision == "HIT":
                    while box.result < 21:
                        decision = self.handle_decision_input(box)

                        if decision == "STAY":
                            self.draw_score(box)
                            break
                        elif decision == "HIT":
                            if 1 in box.cards and box.result <= 11 and not box.addedten:
                                box.result = sum(box.cards) + 10
                                box.addedten = True
                                self.draw_score(box)
                            else:
                                box.result = sum(box.cards)
                                self.draw_score(box)
                        elif decision == "SURRENDER":
                            box.surrender = True
                            self.draw_score(box)
                            break

                    if box.result > 21 and box.addedten:
                        box.result -= 10
                        box.addedten = False
                        self.draw_score(box)

                        while box.result < 21:
                            decision = self.handle_decision_input(box)

                            if decision == "STAY":
                                self.draw_score(box)
                                break
                            elif decision == "HIT":
                                if box.cards[-1] == 1 and box.result <= 11 and not box.addedten:
                                    box.result = sum(box.cards) + 10
                                    box.addedten = True
                                    self.draw_score(box)
                                else:
                                    box.result = sum(box.cards)
                                    self.draw_score(box)
                            elif decision == "SURRENDER":
                                box.surrender = True
                                self.draw_score(box)
                                break

                    if box.result > 21 and not box.addedten:
                        box.busted = True
                        self.draw_score(box)
                        break
                elif decision == "SURRENDER":
                    box.surrender = True
                    self.draw_score(box)
                    break
                return True
        return False

    def deal_other_dealer_cards(self):
        dealmorecards = False
        card_offset = 30  
        dealer_x, dealer_y = 640, 630  

        for box in self.logic.player.boxes:
            if not box.blackjack and not box.surrender and not box.busted:
                dealmorecards = True

        if dealmorecards:
            new_card = self.logic.deck.draw_card()
            self.logic.dealer.cards.append(new_card.value)
            self.logic.dealer.result = sum(self.logic.dealer.cards)

            card_x = dealer_x + len(self.logic.dealer.cards) * card_offset
            pygame.draw.rect(self.screen, 'white', [card_x, dealer_y, 80, 110], 0, 5)
            pygame.draw.rect(self.screen, 'blue', [card_x, dealer_y, 80, 110], 3, 5)  
            self.screen.blit(self.font.render(new_card.rank, True, "black"), (card_x + 10, dealer_y + 10))
            pygame.display.flip()

            if self.logic.dealer.cards[0] == 1 and self.logic.dealer.cards[1] == 10:
                for box in self.logic.player.boxes:
                        if not box.busted and not box.surrender and not box.blackjack and box.insurance:
                            box.profit = box.wager * 3
                            self.draw_score(box, win=True)
                        elif box.blackjack and box.insurance:
                            box.profit = box.wager
                            self.draw_score(box, tie=True)

            else:
                while self.logic.dealer.result < 17:
                    new_card = self.logic.deck.draw_card()
                    self.logic.dealer.cards.append(new_card.value)
                    self.logic.dealer.result = sum(self.logic.dealer.cards)
                    
                    card_x = dealer_x + len(self.logic.dealer.cards) * card_offset
                    pygame.draw.rect(self.screen, 'white', [card_x, dealer_y, 80, 110], 0, 5)
                    pygame.draw.rect(self.screen, 'blue', [card_x, dealer_y, 80, 110], 3, 5) 
                    self.screen.blit(self.font.render(new_card.rank, True, "black"), (card_x + 10, dealer_y + 10))
                    pygame.display.flip()

                if 17 <= self.logic.dealer.result < 22:
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
        self.logic.player.name = self.take_input("Enter your name please:", position=(580, 250))

        self.screen.fill('skyblue')
        self.draw_text(f"Hello {self.logic.player.name}! I am Layo and I will be your dealer in the next game. Let's start playing!", self.BLACK, (400,350))
        pygame.display.flip()
        pygame.time.wait(3000)

        self.logic.player.balance = self.take_input("Enter your balance ranging from 10 to 100000", is_digit=True, valid_range=range(10, 100001), position=(540,250))
        max_num_of_boxes = int(self.logic.player.balance / 10)
        if max_num_of_boxes >= 7:
            max_num_of_boxes = 7

        if max_num_of_boxes >= 2:
            num_of_boxes = self.take_input(f"Enter the number of boxes you would like to pay with, ranging from 1 to {max_num_of_boxes} inclusive:", is_digit=True, valid_range=range(1,8))
        

        if num_of_boxes < 2:
            boxes_positions = self.pick_free_box(1)
        elif num_of_boxes < 7:
            boxes_positions = self.pick_free_box(num_of_boxes)
        else:
            boxes_positions = [1, 2, 3, 4, 5, 6, 7]

        for i in range(len(boxes_positions)):
            wager = self.take_player_wager(boxes_positions[i])
            self.logic.player.balance -= wager
            left_float = 215 * (boxes_positions[i]-1)
            self.logic.player.boxes.append(Box(boxes_positions[i], wager, (12 + left_float, 12, 190, 320)))

        self.deal_initial_cards()

        for box in self.logic.player.boxes:
            new_card_rank = self.deal_a_new_card(box)

            if 1 in box.cards and 10 in box.cards:
                box.blackjack = True 
                box.profit = box.wager * 3

            self.draw_score(box)
            
        for box in self.logic.player.boxes:
            if box.blackjack or box.busted:
                continue

            self.draw_score(box, is_active=True)

            while True:
                decision = self.handle_decision_input(box)
                if decision == "STAY":
                    break
                elif decision == "HIT":
                    self.deal_a_new_card(box)
                    if box.result >= 21:
                        box.busted = True
                        break
                elif decision == "SPLIT":
                    self.split(box, box.cards[0])
                    break
                elif decision == "DOUBLE":
                    self.double_down(box)
                    break
                elif decision == "SURRENDER":
                    self.surrender(box)
                    break

            self.draw_score(box, is_active=False)
                  
        self.deal_other_dealer_cards()
        self.draw_dealer_score()
        self.draw_profit()

        while True:
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

game = RenderGame()
game.run()