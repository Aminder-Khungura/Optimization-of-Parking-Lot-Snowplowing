import pygame
import HARD_CODED_VALUES as HCV


class Stats:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.total_removed = 0
        self.amount_removed = 0
        self.distance_travelled = 0
        self.collisions = 0
        self.snowpiles = 0
        self.score_font = pygame.font.SysFont('Corbel', HCV.FONT_SIZE)
        self.log_title_font = pygame.font.SysFont('arial', HCV.LOG_TITLE_SIZE)
        self.log_font = pygame.font.SysFont('arial', HCV.LOG_FONT_SIZE)
        self.legend = pygame.image.load('legend.jpg')
        self.legend = pygame.transform.scale(self.legend, (HCV.LEGEND_X_TRANSFORM, HCV.LEGEND_Y_TRANSFORM))

    def display_info(self):
        carry = self.score_font.render("Amount of Snow Moved: " + str(self.amount_removed), True, HCV.WHITE, HCV.BLACK)
        score = self.score_font.render("Score: " + str(self.total_removed), True, HCV.WHITE, HCV.BLACK)
        distance = self.score_font.render("Distance Travelled: " + str(self.distance_travelled), True, HCV.WHITE, HCV.BLACK)
        collision = self.score_font.render("Collisions: " + str(self.collisions), True, HCV.WHITE, HCV.BLACK)
        snowpile = self.score_font.render("Snowpiles: " + str(self.snowpiles), True, HCV.WHITE, HCV.BLACK)
        self.parent_screen.blit(carry, (HCV.CARRY_X, HCV.CARRY_Y))
        self.parent_screen.blit(score, (HCV.SCORE_X, HCV.SCORE_Y))
        self.parent_screen.blit(distance, (HCV.DISTANCE_X, HCV.DISTANCE_Y))
        self.parent_screen.blit(collision, (HCV.COLLISION_X, HCV.COLLISION_Y))
        self.parent_screen.blit(snowpile, (HCV.SNOWPILE_X, HCV.SNOWPILE_Y))
        self.parent_screen.blit(self.legend, [HCV.LEGEND_X, HCV.LEGEND_Y])

    def write_log(self, string_1, string_2, string_3, string_4):
        title = self.log_title_font.render('MOVEMENT LOG', True, HCV.WHITE, HCV.BLACK)
        coor = self.log_font.render(string_1, True, HCV.WHITE, HCV.BLACK)
        available_directions = self.log_font.render(string_2, True, HCV.WHITE, HCV.BLACK)
        move = self.log_font.render(string_3, True, HCV.WHITE, HCV.BLACK)
        finish = self.log_font.render(string_4, True, HCV.WHITE, HCV.BLACK)
        self.parent_screen.blit(title, (HCV.LOG_TITLE_X, HCV.LOG_TITLE_Y))
        self.parent_screen.blit(coor, (HCV.LOG_COOR_X, HCV.LOG_COOR_Y))
        self.parent_screen.blit(available_directions, (HCV.LOG_AVAILABLE_DIRECTIONS_X, HCV.LOG_AVAILABLE_DIRECTIONS_Y))
        self.parent_screen.blit(move, (HCV.LOG_MOVE_X, HCV.LOG_MOVE_Y))
        self.parent_screen.blit(finish, (HCV.LOG_FINISH_X, HCV.LOG_FINISH_Y))