import tkinter
import time
import random
import collections
import concurrent.futures
from functools import cached_property
from functools import cache

width = height = 500
a = 100
pad = 50
canvas = tkinter.Canvas(width=width, height=height)
canvas.pack()
zlte = [1, 3, 6, 8, 9, 11, 14, 0]
result = []


class Puzzle:
    def __init__(self, board, canvas):
        self.board = board
        self.width = len(board)
        self.tahy = 0
        self.canvas = canvas
        self.current = self.get_current()
        self.search = False

    def kresli(self):
        self.canvas.delete('vsetko')
        self.canvas.create_text(a + 13, pad // 2, text="Počet ťahov: " + str(self.tahy), font='Arial 15', tags='vsetko')
        if not self.search:
            self.canvas.create_text(width // 2, height - pad // 2, text='Stlačením medzerníka program nájde riešenie.',
                                    font='Arial 15', tags='info')
        for i in range(self.width):
            for j in range(self.width):
                if self.board[i][j] in zlte:
                    self.canvas.create_rectangle(pad + a * j, pad + i * a + a, pad + a * j + a, pad + i * a,
                                                 fill='orange', tags='vsetko')
                else:
                    self.canvas.create_rectangle(pad + a * j, pad + i * a + a, pad + a * j + a, pad + i * a,
                                                 fill='grey', tags='vsetko')

                if self.board[i][j] == 0:
                    self.canvas.create_text((pad + a * j + pad + a * j + a) // 2, (pad + i * a + a + pad + i * a) // 2,
                                            text='', font='Arial 15', tags='vsetko')
                else:
                    self.canvas.create_text((pad + a * j + pad + a * j + a) // 2, (pad + i * a + a + pad + i * a) // 2,
                                            text=self.board[i][j], font='Arial 15', tags='vsetko')

        self.current = self.get_current()

    @cache
    def get_solution(self, e='<KeyRelease-space>'):
        global result
        result = []
        self.search = True
        self.canvas.delete('info')
        self.canvas.delete('vysledok')
        self.canvas.create_text(width // 2, height - pad // 2, text='Hľadá sa optimálne riešenie, trvá to do 10 sekúnd.',
                                font='Arial 15', tags='opt')
        self.canvas.create_text(width // 2, height - pad // 8, text='(Ale väčšinou je to oveľa rýchlejšie.)',
                                font='Arial 9', tags='hladam')
        self.canvas.update()

        puzzle = Puzzle(self.board, self.canvas)
        o = Solver(puzzle, 10)  # casovy limit 10 sekund
        opt = o.solve(1)  # optimalne hladanie s presnostou (ratio) 1

        if opt is not None:  # ak je optimalne riesenie najdene
            presnost = 1
            self.solve_graphically(result, presnost)
        else:
            self.canvas.delete('opt')
            self.canvas.create_text(width // 2, height - pad // 2, text='Hľadá sa neoptimálne riešenie, môže to trvať až minútu.',
                                font='Arial 15', tags='hladam')
            self.canvas.update()
            start = time.time()
            ratios = [2, 3, 4, 5, 6,
                      7]  # tieto presnosti sa experimentovanim ukazali ako najslubnejsie, ale desatinne presnosti som neskusal
            s = Solver(puzzle, 290)  # 5 minut celkovo
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(s.solve, ratio) for ratio in ratios]
            if not result:
                self.canvas.delete('hladam')
                self.canvas.create_text(width // 2, height - pad // 2, text='Riešenie nenájdené.', font='Arial 15',
                                        tags='vysledok')
            else:
                self.solve_graphically(result)

    def solve_graphically(self, moves,
                          presnost=float('inf')):  # nahodna presnost, aby som dal najavo, ze riesenie nie je optimalne
        self.tahy = 0
        self.canvas.delete('hladam')
        self.canvas.delete('opt')
        if presnost == 1:
            self.canvas.create_text(width // 2, height - pad // 2, text='Nájdené optimálne riešenie.', font='Arial 15',
                                    tags='vysledok')
        else:
            if len(moves) <= self.width ** 3:
                self.canvas.create_text(width // 2, height - pad // 2, text='Nájdené riešenie nemusí byť optimálne.',
                                        font='Arial 15', tags='vysledok')
            else:
                self.canvas.create_text(width // 2, height - pad // 2, text='Nájdené neoptimálne riešenie.',
                                        font='Arial 15', tags='vysledok')

        for move in moves:
            if move == 'D':
                self.down()
            elif move == 'U':
                self.up()
            elif move == 'L':
                self.left()
            elif move == 'R':
                self.right()
            self.canvas.update()
            time.sleep(0.2)

    def down(self, e='<KeyRelease-Down>'):
        if self.current[0] < self.width - 1:
            self.board[self.current[0]][self.current[1]], self.board[self.current[0] + 1][self.current[1]] = \
            self.board[self.current[0] + 1][self.current[1]], self.board[self.current[0]][self.current[1]]
            self.tahy += 1
            self.kresli()

    def up(self, e='<KeyRelease-Up>'):
        if self.current[0] > 0:
            self.board[self.current[0]][self.current[1]], self.board[self.current[0] - 1][self.current[1]] = \
            self.board[self.current[0] - 1][self.current[1]], self.board[self.current[0]][self.current[1]]
            self.tahy += 1
            self.kresli()

    def right(self, e='<KeyRelease-Right>'):
        if self.current[1] < self.width - 1:
            self.board[self.current[0]][self.current[1]], self.board[self.current[0]][self.current[1] + 1] = \
            self.board[self.current[0]][self.current[1] + 1], self.board[self.current[0]][self.current[1]]
            self.tahy += 1
            self.kresli()

    def left(self, e='<KeyRelease-Left>'):
        if self.current[1] > 0:
            self.board[self.current[0]][self.current[1]], self.board[self.current[0]][self.current[1] - 1] = \
            self.board[self.current[0]][self.current[1] - 1], self.board[self.current[0]][self.current[1]]
            self.tahy += 1
            self.kresli()

    @cached_property
    def solved(self):
        flat = [i for sub in self.board for i in sub]
        for i in range(0, len(flat) - 1):
            if str(flat[i]) != str(i + 1):
                return False
        return True

    def get_current(self):
        for i in range(self.width):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    current = [i, j]
                    return current

    @cached_property
    def actions(self):
        def create_move(at, to):
            return lambda: self.move(at, to)

        moves = []
        for i in range(self.width):
            for j in range(self.width):
                dirs = {'R': (i, j - 1),
                        'L': (i, j + 1),
                        'D': (i - 1, j),
                        'U': (i + 1, j)}

                for action, (r, c) in dirs.items():
                    if r >= 0 and c >= 0 and r < self.width and c < self.width and self.board[r][c] == 0:
                        move = create_move((i, j), (r, c)), action
                        moves.append(move)
        return moves

    @cached_property
    def manhattan(self):
        distance = 0
        for i in range(self.width):
            for j in range(self.width):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j] - 1, self.width)
                    distance += abs(x - i) + abs(y - j)
        return distance

    def shuffle(self, num):
        puzzle = self
        for _ in range(num):
            puzzle = random.choice(puzzle.actions)[0]()
        return puzzle

    def copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board, self.canvas)

    def move(self, at, to):
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row


class Node:
    def __init__(self, puzzle, parent=None, action=None, ratio=1):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.ratio = ratio
        if self.parent is not None:
            self.g = parent.g + 1
        else:
            self.g = 0

    @cached_property
    def score(self):
        return self.g + self.h

    @cached_property
    def state(self):
        return str(self)

    @cached_property
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @cached_property
    def solved(self):
        return self.puzzle.solved

    @cached_property
    def actions(self):
        return self.puzzle.actions

    @cached_property
    def h(self):
        return self.puzzle.manhattan * self.ratio

    @cached_property
    def f(self):
        return self.h + self.g

    def __str__(self):
        return str(self.puzzle)


class Solver:
    def __init__(self, start, timeout=float('inf')):
        self.start = start
        self.timeout = timeout
        self.solved = False

    @cache
    def solve(self, ratio=1):
        global result
        self.ratio = ratio
        start = time.time()
        queue = collections.deque([Node(self.start)])
        seen = set()
        seen.add(queue[0].state)

        while queue and not self.solved:
            if time.time() - start > self.timeout:  # casovy limit
                break
            queue = collections.deque(sorted(list(queue), key=lambda
                node: node.f))  # dopredu idu konfiguracie s najmensou hodnotou f (pocet tahov + manhattanske vzdialenosti)
            node = queue.popleft()  # najlepsi kandidat sa zoberie
            if node.solved:
                result = [i.action for i in node.path if i.action is not None]
                if self.ratio == 1:
                    print(f'{result} - {time.time() - start}s')
                else:
                    print(f'{result} - {time.time() - start}s + 10s (timeout na nájdenie optimálneho riešenia)')
                self.solved = True
                return node.path

            for move, action in node.actions:  # vytvorenie konfiguracie pre vsetky mozne tahy
                child = Node(move(), node, action, self.ratio)

                if child.state not in seen:  # ak este konfiguracia nebola, pokracovat vo vetve
                    queue.appendleft(child)
                    seen.add(child.state)


#board = [[7, 1, 0, 4], [13, 9, 3, 2], [14, 11, 12, 6], [10, 15, 8, 5]] #Vas priklad

board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]  #spravna

puzzle = Puzzle(board, canvas)
puzzle = puzzle.shuffle(150)
puzzle.kresli()

puzzle.canvas.bind_all('<KeyRelease-Down>', puzzle.down)
puzzle.canvas.bind_all('<KeyRelease-Up>', puzzle.up)
puzzle.canvas.bind_all('<KeyRelease-Right>', puzzle.right)
puzzle.canvas.bind_all('<KeyRelease-Left>', puzzle.left)
puzzle.canvas.bind_all('<KeyRelease-space>', puzzle.get_solution)
puzzle.canvas.mainloop()
