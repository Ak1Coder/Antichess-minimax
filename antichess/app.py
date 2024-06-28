""" Import pygame for the graphics interface of the app """
import pygame

# Import Game which represents the chess game
from antichess.game import Game

# Import colour which represents the white and black colours
from antichess.colour import Colour

class App:
    """ Class representing the AntiChess app taking care of all other methods and objects"""
    app_window = None
    starting_position = "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR"
    app_is_running = False
    MAX_DEPTH = 5

    def __init__(self, width = 1200, height = 800):
        pygame.init()
        self.app_window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AntiChess")

    def run(self):
        """ Runs the app, begins the app loop """
        self.app_is_running = True

        is_in_game = False
        game = None
        state_set = False
        rects = (None, None, None, None)

        while self.app_is_running is True:
            if is_in_game:
                player_won = game.start_game()
                if player_won == "QUIT":
                    break
                width, height = self.app_window.get_size()
                self.__display_text((width / 2, height / 2), "BLACK", player_won, 12)
                pygame.display.flip()
                is_in_game = False
                state_set = True
                while state_set is True:
                    for event in pygame.event.get():
                        state_set = not bool(event.type == pygame.KEYDOWN)
                        break
                pygame.time.Clock().tick(24)

            diff_input = "1"
            state = 2
            while is_in_game is False and self.app_is_running:
                width, height = self.app_window.get_size()
                font = pygame.font.Font(None, int(min(width, height) / 15))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_app()
                    elif event.type == pygame.KEYDOWN:
                        diff_input=diff_input[:-1] if event.key==pygame.K_BACKSPACE else diff_input
                        diff_input += event.unicode if (
                            event.unicode.isdigit() is True
                            and int(event.unicode) in range(0, self.MAX_DEPTH + 1)
                            and len(diff_input) < len(str(self.MAX_DEPTH))
                            ) else ""
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        mouse_rect = pygame.Rect(*mouse_pos, 1, 1)
                        state_set = bool(state in [0, 1] and len(diff_input) != 0
                                         and 0 <= int(diff_input) <= self.MAX_DEPTH)
                        if mouse_rect.colliderect(rects[0]) and state_set:
                            is_in_game = True
                            game = Game(self.app_window,
                                        Colour.WHITE if state == 0 else Colour.BLACK,
                                        int(diff_input))
                            continue
                        self.__check_mouse_quit(mouse_rect, rects[1])
                        state = 0 if mouse_rect.colliderect(rects[2]) else state
                        state = 1 if mouse_rect.colliderect(rects[3]) else state
                        state_set = False

                if self.app_is_running is True:
                    rects = self.display_menu(state)
                    diff_surface = font.render(diff_input, True, "black")
                    self.app_window.blit(diff_surface,
                        diff_surface.get_rect(center=(
                            self.__get_diff_coords()[0],
                            self.__get_diff_coords()[1]+int(height * 0.05))))
                    pygame.display.flip()
                pygame.time.Clock().tick(24)

    def __check_mouse_quit(self, mouse_rect, rect):
        if mouse_rect.colliderect(rect):
            self.quit_app()

    def display_menu(self, colour_picked = 2):
        """ Displays the app menu """
        width, height = self.app_window.get_size()
        self.app_window.fill((255,255,255))
        tile_size = min(width, height) / 12
        x_coord, y_coord = 0, 0
        counter = 0

        while x_coord <= width:
            if counter % 2 == 1:
                col = (238,238,228)
                pygame.draw.rect(self.app_window, col, (x_coord, y_coord, tile_size, height))
            counter += 1
            x_coord += tile_size

        white_is_picked = bool(colour_picked == 0)
        black_is_picked = bool(colour_picked == 1)

        self.__display_text(self.__get_antichess_coords(), "navy", "AntiChess", 6)
        play_rect = self.__display_text(self.__get_play_coords(), "black", "PLAY", 10)
        self.__display_text(self.__get_diff_coords(), "black", "SET DIFFICULTY:", 15)
        quit_rect = self.__display_text(self.__get_quit_coords(), "black", "QUIT", 10)
        self.__display_text(self.__get_colour_coords(), "black", "CHOOSE COLOR TO PLAY:", 15)
        col = "red" if white_is_picked else "black"
        white_rect = self.__display_text(self.__get_white_coords(), col, "W", 12)
        col = "red" if black_is_picked else "black"
        black_rect = self.__display_text(self.__get_black_coords(), col, "B", 12)
        return play_rect, quit_rect, white_rect, black_rect

    def __display_text(self, coords, colour, text_to_display, font_size_div):
        """ Displays text_to_display at x_coord and y_coord and returns the rect obj to it """
        x_coord, y_coord = coords
        width, height = self.app_window.get_size()
        font = pygame.font.Font(None, int(min(width, height) / font_size_div))
        text = font.render(text_to_display, True, colour)
        text_rect = text.get_rect(center=(x_coord, y_coord))
        self.app_window.blit(text, text_rect)
        return text_rect

    def __get_antichess_coords(self):
        """ Gets coords where the name of an app should be """
        width, height = self.app_window.get_size()
        return (width / 2, height * 0.22)

    def __get_play_coords(self):
        """ Gets coords where the Play option should be """
        width, height = self.app_window.get_size()
        return (width / 2, height * 0.40)

    def __get_diff_coords(self):
        """ Gets coords where the Difference option should be """
        width, height = self.app_window.get_size()
        return (width / 2, height * 0.48)

    def __get_quit_coords(self):
        """ Gets coords where the Quit option should be """
        width, height = self.app_window.get_size()
        return (width / 2, height * 0.76)

    def __get_colour_coords(self):
        """ Gets coords where the Colours option should be """
        width, height = self.app_window.get_size()
        return (width / 2, height * 0.60)

    def __get_white_coords(self):
        """ Gets coords where the White option should be """
        width, height = self.app_window.get_size()
        return (width / 2 - width * 0.022, height * 0.67)

    def __get_black_coords(self):
        """ Gets coords where the Black option should be """
        width, height = self.app_window.get_size()
        return (width / 2 + width * 0.022, height * 0.67)

    def quit_app(self):
        """ Sets the app_is_running memeber var to False"""
        self.app_is_running = False
