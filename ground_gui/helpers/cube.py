from pygame import display, draw
from math import sin, cos, radians
from numpy import dot


class pygame_cansat:
    def __init__(self, parent):
        self.window = display.set_mode((parent.WIDTH, parent.HEIGHT))

        self.projection_matrix = [[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]]
        
        self.center_figure_x = parent.WIDTH/2
        self.center_figure_y = parent.HEIGHT/2

        self.cube_points = []
        self.cube_points.append([[-2], [-1], [1]])
        self.cube_points.append([[1],[-1],[1]])
        self.cube_points.append([[1],[1],[1]])
        self.cube_points.append([[-2],[1],[1]])
        self.cube_points.append([[-2],[-1],[-1]])
        self.cube_points.append([[1],[-1],[-1]])
        self.cube_points.append([[1],[1],[-1]])
        self.cube_points.append([[-2],[1],[-1]])

        # Main Loop
        self.scale = 40
        self.angle_x = self.angle_y = self.angle_z = 0

    def connect_points(self, i, j, points, color):
        draw.line(self.window, color, points[i] , points[j], 2)

    def move(self):
        self.window.fill((245, 245, 245))

        rotation_x = [[1, 0, 0],
                        [0, cos(self.angle_x), -sin(self.angle_x)],
                        [0, sin(self.angle_x), cos(self.angle_x)]]

        rotation_y = [[cos(self.angle_y), 0, sin(self.angle_y)],
                        [0, 1, 0],
                        [-sin(self.angle_y), 0, cos(self.angle_y)]]

        rotation_z = [[cos(self.angle_z), -sin(self.angle_z), 0],
                        [sin(self.angle_z), cos(self.angle_z), 0],
                        [0, 0, 1]]

        points = []

        for point in self.cube_points:
                
            rotated2d = dot(rotation_z, point)
            rotated2d = dot(rotation_y, rotated2d)
            rotated2d = dot(rotation_x, rotated2d)

            projected2d = dot(self.projection_matrix, rotated2d)
            
            x = (projected2d[0][0] * self.scale) + self.center_figure_x
            y = (projected2d[1][0] * self.scale) + self.center_figure_y

            points.append((x, y))

        # --------------- Line drawings --------------- #
        # Red
        self.connect_points(0, 1, points, (255, 0, 0))
        self.connect_points(1, 2, points, (255, 0, 0))
        self.connect_points(2, 3, points, (255, 0, 0))
        self.connect_points(3, 0, points, (255, 0, 0))
        # Blue
        self.connect_points(4, 5, points, (0, 0, 255))
        self.connect_points(5, 6, points, (0, 0, 255))
        self.connect_points(6, 7, points, (0, 0, 255))
        self.connect_points(7, 4, points, (0, 0, 255))
        # Green
        self.connect_points(0, 4, points, (0, 255, 0))
        self.connect_points(1, 5, points, (0, 255, 0))
        self.connect_points(2, 6, points, (0, 255, 0))
        self.connect_points(3, 7, points, (0, 255, 0))
        # --------------------------------------------- #

        """ This is the same, but in a for loop
        for p in range(4):
            self.connect_points(p, (p+1) % 4, points, (255, 0, 0))
            self.connect_points(p+4, (p+1) % 4 + 4, points, (0, 0, 255))
            self.connect_points(p, p+4, points, (0, 255, 0))
        """
                
        display.update()
    
    def degrees_to_radians(self, pitch, roll, yaw):
        self.angle_x = radians(pitch)
        self.angle_y = radians(roll)
        self.angle_z = radians(yaw)

        self.move()
    