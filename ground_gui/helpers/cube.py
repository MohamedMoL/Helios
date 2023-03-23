from pygame import display, draw
from math import sin, cos, radians
from numpy import dot


class pygame_cansat:
    def __init__(self, parent):
        self.parent = parent
        self.window = display.set_mode((self.parent.WIDTH, self.parent.HEIGHT))

        self.projection_matrix = [[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]]

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

    def move(self):
        self.window.fill((255, 255, 255))

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
            
            x = (projected2d[0][0] * self.scale) + self.parent.WIDTH/2
            y = (projected2d[1][0] * self.scale) + self.parent.HEIGHT/2

            points.append((x, y))

        for p in range(4):
            self.connect_points(p, (p+1) % 4, points)
            self.connect_points(p+4, (p+1) % 4 + 4, points)
            self.connect_points(p, p+4, points)
                
        display.update()
        self.parent.update()
    
    def connect_points(self, i, j, points):
        draw.line(self.window, (0, 0, 0), points[i] , points[j])

    def rotate_cube(self, pitch, roll, yaw):
        self.angle_x = radians(pitch)
        self.angle_y = radians(roll)
        self.angle_z = radians(yaw)

        self.move()
    