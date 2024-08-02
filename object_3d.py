import pygame as pg
import matrix_functions
import numpy as np
from numba import njit

@njit(fastmath=True)
def any_func(arr, a, b):
	return np.any((arr == a) | (arr == b))

class Object3D:
	def __init__(self, render, vertices='', faces=''):
		self.render = render
		self.vertices = np.array(vertices)
		self.faces = faces
		self.translate([0.0001, 0.0001, 0.0001])

		self.font = pg.font.SysFont('Arial', 30, bold=True)
		self.color_faces = [(pg.Color(255,255,0), face) for face in self.faces]
		self.movement_flag, self.draw_vertices = True, False
		self.label = ''
		
	def draw(self):
		self.screen_projection()
		self.movement()
		
	def movement(self):
		if self.movement_flag:
			self.rotate_y(pg.time.get_ticks() % 0.005)
		
	def screen_projection(self):
		vertices = self.vertices @ self.render.camera.camera_matrix()
		vertices = vertices @ self.render.projection.projection_matrix
		vertices /= vertices[:, -1].reshape(-1, 1)
		vertices[(vertices > 2) | (vertices < -2)] = 0
		vertices = vertices @ self.render.projection.to_screen_matrix
		vertices = vertices[:, :2]
		
		for index, color_face in enumerate(self.color_faces):
			color, face = color_face
			polygon = vertices[face]
			if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
				pg.draw.polygon(self.render.screen, color, polygon, 1)
				if self.label:
					text = self.font.render(self.label[index], True, pg.Color((255,255,255)))
					self.render.screen.blit(text, polygon[-1])
				
		if self.draw_vertices:
			for vertex in vertices:
				polygon = vertices[face]
				if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
					pg.draw.circle(self.render.screen, pg.Color(255, 255, 255), vertex, 2)
		
	def translate(self, pos):
		self.vertices = self.vertices @ matrix_functions.translate(pos)
		
	def scale(self, scale_to):
		self.vertices = self.vertices @ matrix_functions.scale(scale_to)
		
	def rotate_x(self, angle):
		self.vertices = self.vertices @ matrix_functions.rotate_x(angle)
		
	def rotate_y(self, angle):
		self.vertices = self.vertices @ matrix_functions.rotate_y(angle)
		
	def rotate_z(self, angle):
		self.vertices = self.vertices @ matrix_functions.rotate_z(angle)

class Axes(Object3D):
	def __init__(self, render, vertexes=None, faces=None):
		super().__init__(render, vertexes, faces)
		if vertexes is None:
			vertexes = np.array([
				(0,0,0,1),
				(1,0,0,1),
				(0,1,0,1),
				(0,0,1,1)
			])
		if faces is None:
			faces = np.array([
				(0,1),
				(0,2),
				(0,3)
			])
		self.colors = [pg.Color(255,0,0), pg.Color(0,255,0), pg.Color(0,0,255)]
		self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
		self.draw_vertexes = False