import pygame as pg
import camera
import projection
import object_3d
import numpy as np

class SoftwareRenderer:
    def __init__(self, file_path):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 144
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 36)
        self.create_objects(file_path)
        
    def create_objects(self, file_path):
        self.file = file_path
        self.camera = camera.Camera(self, [-5, 5, -50])
        self.projection = projection.Projection(self)
        self.object = self.get_object_from_file(self.file)
        
    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return object_3d.Object3D(self, vertex, faces)
        
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.object.draw()
        self.render_camera_position_text()
        
    def render_camera_position_text(self):
        text_x = self.font.render(f"X: {self.camera.position[0]}", True, (255, 255, 255))
        text_y = self.font.render(f"Y: {self.camera.position[1]}", True, (255, 255, 255))
        text_z = self.font.render(f"Z: {self.camera.position[2]}", True, (255, 255, 255))
        text_rotation = self.font.render(f"Rotation: {self.camera.rotation_angle}", True, (255, 255, 255))
        text_fps = self.font.render(f"FPS: {str(self.clock.get_fps())}", True, (255, 255, 255))
        
        self.screen.blit(text_x, (10, 10))
        self.screen.blit(text_y, (10, 50))
        self.screen.blit(text_z, (10, 90))
        self.screen.blit(text_rotation, (10, 130))
        self.screen.blit(text_fps, (10, 170))
        
    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            icon_file = 'pandaaiicon.ico'
            icon = pg.image.load(icon_file)
            pg.display.set_icon(icon)
            pg.display.set_caption("PandaAI 3D Renderer")
            pg.display.flip()
            self.clock.tick(self.FPS)