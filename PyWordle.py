from english_dictionary.scripts.read_pickle import get_dict
from random import choice, seed
from datetime import datetime
from os import system

import pygame as py

class Board:
	def __init__(self, wordSize, boardSize, font, dictionary):
		self.default = [255, 255, 255]
		self.noColor = [125, 125, 125]
		self.existsColor = [150, 150, 50]
		self.correctColor = [0, 225, 0]
		
		self.x = 0
		
		self.font = font
		self.dim = self.font.get_height()
		
		self.width = wordSize
		self.height = boardSize
		self.words = [[]]
		
		self.dictionary = dictionary
		
		self.reset()
	
	def __highlight__(self, word):
		new = ["", []]
		for char in word:
			new[0] = new[0] + char.upper()
			
			if (char in self.target):
				if (word.index(char) == self.target.index(char)):
					new[1].append(self.correctColor)
				else:
					new[1].append(self.existsColor)
			
			else:
				new[1].append(self.noColor)
		
		return new
	
	def backspace(self):
		word = "".join(self.words[self.x][0].replace(" ",""))[:-1]
		self.words[self.x][0] = word + " "*(self.width-len(word))
	
	def reset(self):
		self.x = 0
		self.words = [[" "*self.width, [self.default]*self.width]]*self.height
		
		seed(datetime.now())
		self.target = choice(list(self.dictionary.keys())).upper()
		while (len(self.target) != self.width):
			self.target = choice(list(self.dictionary.keys())).upper()
	
	def miniUpdate(self, letter):
		self.words[self.x] = [letter.upper() + " "*(self.width-len(letter)), [self.default]*self.width]
		
	def update(self, word):
		hasWon = False
		if (word == self.target):
			hasWon = True
		
		self.words[self.x] = self.__highlight__(word.upper())
		self.x += 1
		
		return hasWon
	
	def getTarget(self):
		return self.target
		
	def draw(self, surface, position):
		x = position[0]
		y = position[1]
		
		for i in range(self.height):
			for j in range(self.width):
				xP = j * (self.dim + 20) + x
				yP = i * (self.dim + 20) + y
				
				py.draw.rect(surface, self.words[i][1][j], [xP, yP, self.dim, self.dim])
				surface.blit(self.font.render(self.words[i][0][j], True, [0,0,0]), [xP+10, yP+10])


keys = {
	"a" : py.K_a,
	"b" : py.K_b,
	"c" : py.K_c,
	"d" : py.K_d,
	"e" : py.K_e,
	"f" : py.K_f,
	"g" : py.K_g,
	"h" : py.K_h,
	"i" : py.K_i,
	"j" : py.K_j,
	"k" : py.K_k,
	"l" : py.K_l,
	"m" : py.K_m,
	"n" : py.K_n,
	"o" : py.K_o,
	"p" : py.K_p,
	"q" : py.K_q,
	"r" : py.K_r,
	"s" : py.K_s,
	"t" : py.K_t,
	"u" : py.K_u,
	"v" : py.K_v,
	"w" : py.K_w,
	"x" : py.K_x,
	"y" : py.K_y,
	"z" : py.K_z
}

dictionary = get_dict()

py.init()
py.display.set_caption("PyWordle")
screen = py.display.set_mode((600, 720))
font = py.font.SysFont("times new roman", 75)
debugFont = py.font.SysFont("times new roman", 25)

textBox = py.surface.Surface([600, 200])

size = 5
rows = 6
board = Board(size, rows, font, dictionary)
word = ""
words = 0;

hasWon = False
running = True
cheat = False
while running:
	for event in py.event.get():
		if (event.type == py.QUIT):
			py.quit()
			running = False
		
		elif (event.type == py.KEYDOWN):
			if (event.key == py.K_BACKSPACE):
				board.backspace()
				word = word[:-1]
							
			elif (event.key == py.K_RETURN):
				print(hasWon)
				if (words == rows or hasWon == True):
					hasWon = False
					words = 0
					board.reset()
					
				if (len(word) == size):
					hasWon = board.update(word.upper())
					if (hasWon):
						words = 0
					else:
						words += 1
					word = ""
			
			elif (event.key == py.K_MINUS):
				if (cheat == False):
					cheat = True
				else:
					cheat = False
			
			elif (len(word) < 5):
				for char, val in keys.items():
					if (event.key == val):
						word = word + char
						board.miniUpdate(word.upper())
						break
	
	if (running):	
		system("cls")
		screen.fill([0,0,0])
		textBox.fill([0,0,0])
		
		if (cheat == True):
			screen.blit(debugFont.render(board.getTarget(), True, [0,200,50]), [0, 0])		
		
		board.draw(screen, [50, 100])
		if (words == rows and hasWon == False):
			textBox.blit(font.render("You Lost!", True, [255,20,50]), [0, 0])
			textBox.blit(font.render(f"Answer: {board.getTarget()}", True, [255,20,50]), [0, 60])
			textBox.blit(font.render("Press Enter...", True, [255,20,50]), [0, 120])
			screen.blit(textBox, [0,0])
			
		elif (hasWon == True):
			textBox.blit(font.render("You Won!", True, [0,200,50]), [0, 0])
			textBox.blit(font.render("Press Enter...", True, [0,200,50]), [0, 100])
			screen.blit(textBox, [0,0])
		
		else:
			screen.blit(font.render("PyWordle", True, [0,200,50]), [150, 0])
		
		py.display.update()