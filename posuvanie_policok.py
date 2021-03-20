import tkinter
import time
import random
start = time.time()
width = height = 500
a = 100
pad = 50
canvas = tkinter.Canvas(width=width, height=height)
canvas.pack()

cisla = [[7, 1, 0, 4],
		 [13, 9, 3, 2],
		 [14, 11, 12, 6],
		 [10, 15, 8, 5]]
zlte = [1, 3, 6, 8, 9, 11, 14, 0]

prd = [[1,2,3,4],
	     [5,6,7,8],
	     [9,10,11,12],
	     [13,14,15,0]]

jeff = [[1,2,3],
		[4,5,6],
		[7,8,0]]

solutions = []

class Puzzle:
	def __init__(self, board, canvas):
		self.board = board
		self.width = len(board)
		self.tahy = 0
		self.canvas = canvas
		self.kresli()

	def kresli(self):
		self.canvas.delete('vsetko')
		self.canvas.create_text(a+13, pad//2, text="Počet ťahov: " + str(self.tahy), font='Arial 15', tags='vsetko')
		for i in range(self.width):
			for j in range(self.width):
				if self.board[i][j] in zlte:
					self.canvas.create_rectangle(pad+a*j, pad+i*a+a, pad+a*j+a, pad+i*a, fill='orange', tags='vsetko')
				else:
					self.canvas.create_rectangle(pad+a*j, pad+i*a+a, pad+a*j+a, pad+i*a, fill='grey', tags='vsetko')

				if self.board[i][j] == 0:
					self.canvas.create_text((pad+a*j+pad+a*j+a)//2, (pad+i*a+a+pad+i*a)//2, text='', font='Arial 15', tags='vsetko')
				else:
					self.canvas.create_text((pad+a*j+pad+a*j+a)//2, (pad+i*a+a+pad+i*a)//2, text=self.board[i][j], font='Arial 15', tags='vsetko')

		self.current = self.get_current()

	def dole(self, e='<KeyRelease-Down>'):
		if self.current[0] < len(cisla) - 1:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]+1][self.current[1]] = self.board[self.current[0]+1][self.current[1]], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def hore(self, e='<KeyRelease-Up>'):
		if self.current[0] > 0:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]-1][self.current[1]] = self.board[self.current[0]-1][self.current[1]], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def doprava(self, e='<KeyRelease-Right>'):
		if self.current[1] < len(cisla[0]) - 1:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]][self.current[1]+1] = self.board[self.current[0]][self.current[1]+1], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def dolava(self, e='<KeyRelease-Left>'):
		if self.current[1] > 0:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]][self.current[1]-1] = self.board[self.current[0]][self.current[1]-1], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def is_solved(self):
		flat = [i for sub in self.board for i in sub]
		for i in range(0, len(flat)-1):
			if str(flat[i]) != str(i+1):
				return False
		return True

	def get_current(self):
		for i in range(self.width):
			for j in range(self.width):
				if self.board[i][j] == 0:
					current = [i, j]
					return current


def get_solutions(current, board, path, depth):
	if len(path) > depth:
		return False

	if len(path) > 1:
		if path[-1] == 'r' and path[-2] == 'l':
			return False
		if path[-1] == 'l' and path[-2] == 'r':
			return False
		if path[-1] == 'h' and path[-2] == 'd':
			return False
		if path[-1] == 'd' and path[-2] == 'h':
			return False

	if is_solved(board):
		solutions.append(path)
		return True

	if current[0] < len(cisla) - 1:
		board[current[0]][current[1]], board[current[0]+1][current[1]] = board[current[0]+1][current[1]], board[current[0]][current[1]]
		solved = get_solutions([current[0]+1, current[1]], board, path + ['d'], depth)
		if solved:
			print(path + ['d'])
		board[current[0]][current[1]], board[current[0]+1][current[1]] = board[current[0]+1][current[1]], board[current[0]][current[1]]

	if current[1] > 0:
		board[current[0]][current[1]], board[current[0]][current[1]-1] = board[current[0]][current[1]-1], board[current[0]][current[1]]
		solved = get_solutions([current[0], current[1]-1], board, path + ['l'], depth)
		if solved:
			print(path + ['l'])
		board[current[0]][current[1]], board[current[0]][current[1]-1] = board[current[0]][current[1]-1], board[current[0]][current[1]]

	if current[0] > 0:
		board[current[0]][current[1]], board[current[0]-1][current[1]] = board[current[0]-1][current[1]], board[current[0]][current[1]]
		solved = get_solutions([current[0]-1, current[1]], board, path + ['h'], depth)
		if solved:
			print(path + ['h'])
		board[current[0]][current[1]], board[current[0]-1][current[1]] = board[current[0]-1][current[1]], board[current[0]][current[1]]

	if current[1] < len(cisla[0]) - 1:
		board[current[0]][current[1]], board[current[0]][current[1]+1] = board[current[0]][current[1]+1], board[current[0]][current[1]]
		solved = get_solutions([current[0], current[1]+1], board, path + ['r'], depth)
		if solved:
			print(path + ['r'])
		board[current[0]][current[1]], board[current[0]][current[1]+1] = board[current[0]][current[1]+1], board[current[0]][current[1]]




doska = Puzzle([[7, 1, 0, 4],
		 [13, 9, 3, 2],
		 [14, 11, 12, 6],
		 [10, 15, 8, 5]], canvas)

canvas.bind_all('<KeyRelease-Down>', doska.dole)
canvas.bind_all('<KeyRelease-Up>', doska.hore)
canvas.bind_all('<KeyRelease-Right>', doska.doprava)
canvas.bind_all('<KeyRelease-Left>', doska.dolava)
doska.canvas.mainloop()
