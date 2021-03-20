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

	def down(self, e='<KeyRelease-Down>'):
		if self.current[0] < len(cisla) - 1:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]+1][self.current[1]] = self.board[self.current[0]+1][self.current[1]], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def up(self, e='<KeyRelease-Up>'):
		if self.current[0] > 0:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]-1][self.current[1]] = self.board[self.current[0]-1][self.current[1]], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def right(self, e='<KeyRelease-Right>'):
		if self.current[1] < len(cisla[0]) - 1:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]][self.current[1]+1] = self.board[self.current[0]][self.current[1]+1], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def left(self, e='<KeyRelease-Left>'):
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

	def actions(self):
		def create_move(at, to):
			return lambda: self.move(at, to)

		moves = []
		for i in range(self.width):
			for j in range(self.width):
				dirs = {'R':(i, j-1),
					  'L':(i, j+1),
					  'D':(i-1, j),
					  'U':(i+1, j)}

				for action, (r, c) in dirs.items():
					if r >= 0 and c >= 0 and r < self.width and c < self.width and self.board[r][c] == 0:
						move = create_move((i,j), (r,c)), action
						moves.append(move)
		return moves

				   

doska = Puzzle([[7, 1, 0, 4],
		 [13, 9, 3, 2],
		 [14, 11, 12, 6],
		 [10, 15, 8, 5]], canvas)

print(doska.actions())

canvas.bind_all('<KeyRelease-Down>', doska.down)
canvas.bind_all('<KeyRelease-Up>', doska.up)
canvas.bind_all('<KeyRelease-Right>', doska.right)
canvas.bind_all('<KeyRelease-Left>', doska.left)
doska.canvas.mainloop()
