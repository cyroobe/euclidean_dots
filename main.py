import pygame
from random import randint, choice


WIDTH, HEIGHT = 1000, 600
BG_COLOR = (0, 150, 150)
FPS = 150
CLOCK = pygame.time.Clock()
COLORS = [(255, 255, 255), (155, 155, 155), (200, 200, 200)]
PRIMARY_COLOR = (104, 51, 228)
SECONDARY_COLOR = (58, 38, 106)
BG_COLOR = (25, 25, 25)
CONN_COlOR_1 = (205, 205, 205)
CONN_COlOR_2 = (50, 50, 50)


pygame.init()
pygame.display.set_caption("Euclidean dots")
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Fragment_point:
    """
        Class that represent a point on the screen.
        Also controls the connections between other points and the mouse.
    """

    def __init__(self, initial_position) -> None:
        # The point radius
        self.radium = randint(1, 2)
        # List of all possible speed's
        self.possible_speed = [-3, -2, -1, 1, 2, 3]
        self.speed = [choice(self.possible_speed), choice(
            self.possible_speed)]          # Random initial speed
        self.in_use_color = choice(COLORS)  # Random
        # Point position on screen
        self.position = [initial_position[0], initial_position[1]]
        # Other point and mouse distance to connect
        self.point_distance, self.mouse_distance = randint(10, 100), 200
        # To store the mouse position
        self.mouse_pos = pygame.mouse.get_pos()

    def get_position(self) -> list:
        """
            The point position is returned to be used on the other point
            to determinate the proximity from other points.
        """
        return self.position

    def euclidean_distance(self, p1, p2) -> int:
        """
            Euclidean distance
        """
        return (((int(p1[0])-int(p2[0]))**2) + ((int(p1[1]) - int(p2[1]))**2))**0.5

    def mouse_connection(self) -> None:
        """
            Check if the distance from the mouse is proper to make a connection.
        """
        distance = self.euclidean_distance(
            (self.mouse_pos[0], self.mouse_pos[1]), (self.position[0], self.position[1]))
        if self.mouse_pos[0] in range(10, WIDTH-10) and self.mouse_pos[1] in range(10, HEIGHT-10):
            if (distance <= self.mouse_distance and distance > 150):
                pygame.draw.line(screen, SECONDARY_COLOR, tuple(
                    self.position), self.mouse_pos, 2)
            if distance <= 150:
                pygame.draw.line(screen, PRIMARY_COLOR, tuple(
                    self.position), self.mouse_pos, 3)

    def other_point_connections(self, other_point_position: list) -> None:
        """
            Check if the distance from other points is proper to make connections.
        """
        for pos in other_point_position:
            if (self.euclidean_distance(pos, (self.position[0], self.position[1])) <= self.point_distance):
                pygame.draw.line(screen, CONN_COlOR_2, tuple(self.position), pos, 1) if (self.euclidean_distance(pos, (self.position[0], self.position[1])) > self.point_distance - 20) else\
                    pygame.draw.line(screen, CONN_COlOR_1,
                                     tuple(self.position), pos, 1)

    def change_direction(self):
        """
            When the fade out of the screen this function will invert their 
            direction.
        """
        if (self.position[0] not in range(-5, WIDTH+5)):
            self.speed[0] *= -1
            self.radium = randint(1, 2)
        if (self.position[1] not in range(-5, HEIGHT+5)):
            self.speed[1] *= -1
            self.radium = randint(1, 2)

    def draw(self, other_point_pos) -> None:
        """
            To draw a point and their configuration.
        """
        self.mouse_pos = pygame.mouse.get_pos()
        self.other_point_connections(other_point_pos)
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        pygame.draw.circle(screen, self.in_use_color,
                           tuple(self.position), self.radium)
        self.change_direction()


class Animation:
    def __init__(self) -> None:
        self.point_number = 200
        self.point_list = [Fragment_point(
            (randint(20, WIDTH-20), randint(20, HEIGHT-20))) for _ in range(self.point_number)]

    def generate_new_points_by_click(self) -> None:
        """
            To generate new points by clicking
        """
        self.point_list.append(Fragment_point(pygame.mouse.get_pos()))

    def draw_all_points(self) -> None:
        """
            This function draw all the points on the screen and also the mouse connections to.
        """
        [point.draw([tuple(point.get_position())
                    for point in self.point_list]) for point in self.point_list]
        if pygame.mouse.get_pressed(3)[0]:
            self.generate_new_points_by_click()
        [point.mouse_connection() for point in self.point_list]


animation = Animation()


def main():
    while True:
        # CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_KP_ENTER]:
                    exit()

        screen.fill(BG_COLOR)
        animation.draw_all_points()
        pygame.display.update()


if __name__ == "__main__":
    main()
