import tkinter

width = height = 500
a = 100
pad = 50
canvas = tkinter.Canvas(width=width, height=height)
canvas.pack()
prd = [[7, 1, '', 4],
		 [13, 9, 3, 2],
		 [14, 11, 12, 6],
		 [10, 15, 8, 5]]
zlte = ['1', '3', '6', '8', '9', '11', '14', '']

cisla = [[1,2,3,''],
	     [5,6,7,4],
	     [8,9,10,11],
	     [12,13,14,15]]
current = [0, 3]
tahy = 0
solutions = []

def kresli():
	canvas.delete('vsetko')
	canvas.create_text(a+13, pad//2, text="Počet ťahov: " + str(tahy), font='Arial 15', tags='vsetko')
	for i in range(len(cisla)):
		for j in range(len(cisla[0])):
			if cisla[i][j] in zlte:
				canvas.create_rectangle(pad+a*j, pad+i*a+a, pad+a*j+a, pad+i*a, fill='orange', tags='vsetko')
			else:
				canvas.create_rectangle(pad+a*j, pad+i*a+a, pad+a*j+a, pad+i*a, fill='grey', tags='vsetko')
			canvas.create_text((pad+a*j+pad+a*j+a)//2, (pad+i*a+a+pad+i*a)//2, text=cisla[i][j], font='Arial 15', tags='vsetko')

def is_solved(board):
	flat = [i for sub in board for i in sub if isinstance(i, int)]
	for i in range(len(flat)-1):
		if int(flat[i]) > int(flat[i+1]):
			return False
	return True

def get_solutions(current, board, path):
	print(path)
	if len(path) > 8:
		return False

	if is_solved(board):
		solutions.append(path)
		return True

	if current[0] < len(cisla) - 1:
		board[current[0]][current[1]], board[current[0]+1][current[1]] = board[current[0]+1][current[1]], board[current[0]][current[1]]
		solved = get_solutions([current[0]+1, current[1]], board, path + ['d'])
		if solved:
			print(path)
		board[current[0]][current[1]], board[current[0]+1][current[1]] = board[current[0]+1][current[1]], board[current[0]][current[1]]

	if current[1] > 0:
		board[current[0]][current[1]], board[current[0]][current[1]-1] = board[current[0]][current[1]-1], board[current[0]][current[1]]
		solved = get_solutions([current[0], current[1]-1], board, path + ['l'])
		if solved:
			print(path)
		board[current[0]][current[1]], board[current[0]][current[1]-1] = board[current[0]][current[1]-1], board[current[0]][current[1]]

	if current[0] > 0:
		board[current[0]][current[1]], board[current[0]-1][current[1]] = board[current[0]-1][current[1]], board[current[0]][current[1]]
		solved = get_solutions([current[0]-1, current[1]], board, path + ['h'])
		if solved:
			print(path)
		board[current[0]][current[1]], board[current[0]-1][current[1]] = board[current[0]-1][current[1]], board[current[0]][current[1]]

	if current[1] < len(cisla[0]) - 1:
		board[current[0]][current[1]], board[current[0]][current[1]+1] = board[current[0]][current[1]+1], board[current[0]][current[1]]
		solved = get_solutions([current[0], current[1]+1], board, path + ['r'])
		if solved:
			print(path)
		board[current[0]][current[1]], board[current[0]][current[1]+1] = board[current[0]][current[1]+1], board[current[0]][current[1]]

	
		
print(get_solutions([0, 3], cisla, []))
print(solutions)


def dole(e):
	global current, tahy
	if current[0] < len(cisla) - 1:
		cisla[current[0]][current[1]], cisla[current[0]+1][current[1]] = cisla[current[0]+1][current[1]], cisla[current[0]][current[1]]
		current = [current[0]+1, current[1]]
		tahy += 1
		kresli()

def hore(e):
	global current, tahy
	if current[0] > 0:
		cisla[current[0]][current[1]], cisla[current[0]-1][current[1]] = cisla[current[0]-1][current[1]], cisla[current[0]][current[1]]
		current = [current[0]-1, current[1]]
		tahy += 1
		kresli()

def doprava(e):
	global current, tahy
	if current[1] < len(cisla[0]) - 1:
		cisla[current[0]][current[1]], cisla[current[0]][current[1]+1] = cisla[current[0]][current[1]+1], cisla[current[0]][current[1]]
		current = [current[0], current[1]+1]
		tahy += 1
		kresli()

def dolava(e):
	global current, tahy
	if current[1] > 0:
		cisla[current[0]][current[1]], cisla[current[0]][current[1]-1] = cisla[current[0]][current[1]-1], cisla[current[0]][current[1]]
		current = [current[0], current[1]-1]
		tahy += 1
		kresli()

kresli()
canvas.bind_all('<KeyRelease-Down>', dole)
canvas.bind_all('<KeyRelease-Up>', hore)
canvas.bind_all('<KeyRelease-Right>', doprava)
canvas.bind_all('<KeyRelease-Left>', dolava)
canvas.mainloop()
