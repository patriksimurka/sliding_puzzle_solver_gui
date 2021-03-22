with open('log3.txt', 'r') as f:
	lines = [i.strip() for i in f]

x = 0
d = {}
c = {}

for i in lines:
	if i == 'x':
		x += 1

	if len(i.split()) > 1:
		d[i.split()[0]] = d.get(i.split()[0], 0) + 1
		c[i.split()[0]] = c.get(i.split()[0], []) + [i.split()[1]]

casy = {}

for i, val in c.items():
	res = 0.0
	for j in val:
		res += float(j)
	casy[i] = res/len(c[i])

print(casy)
d = sorted(d.items(), key=lambda x: x[1])
print(x)
#print(d)
print(c)

