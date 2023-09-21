from z3 import *

with open('gameboard.txt', 'r') as f:
	board = f.read()

board = list(map(list, board.replace(' ', '0').split('\n')))


def gen_neighbors(x, y):
	return [
		[x+dx, y+dy]
		for dx in range(-1,2)
		for dy in range(-1,2)
		if dx != 0 or dy != 0
	]


s = Solver()

for y in range(len(board)):
	print(y)
	for x in range(len(board[0])):
		curr = int(board[y][x], 16)
		if curr > 0 and curr < 9:
			count = 0
			for dx, dy in gen_neighbors(x, y):
				neighbour = int(board[dy][dx], 16)
				if neighbour == 0x9:
					spot = Int(f'{dx}_{dy}')
					s.add(And([spot >= 0, spot <= 1]))
					count += spot
				elif neighbour == 0xB:
					count += 1
			s.add(curr == count)


print('Checking')
if s.check() != sat:
	print('Not SAT')
	exit()

print('SAT')
m = s.model()

print('Writing')
with open('board.txt', 'w') as f:
	for y in range(len(board)):
		row = ''
		for x in range(len(board[0])):
			if board[y][x] == '9':
				if m[Int(f'{x}_{y}')] == 1:
					board[y][x] = 'A'
			elif board[y][x] == '0':
				board[y][x] = ' '
			row += board[y][x]
		f.write(row + '\n')


#  CTF{d8675fca837faa20bc0f3a7ad10e9d2682fa0c35c40872938f1d45e5ed97ab27}

