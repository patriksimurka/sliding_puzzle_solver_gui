with open('log10.txt', 'r') as f:
	lines = [i.strip() for i in f]

cnt = 0
for i in lines:
	if i == '': break
	try:
		if float(i) > 50:
			cnt += 1
	except: cnt += 1

print(cnt)