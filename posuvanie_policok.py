import tkinter

width = height = 500
a = 100
pad = 50
canvas = tkinter.Canvas(width=width, height=height)
canvas.pack()
cisla = ['7', '1', '', '4', '13', '9', '3', '2', '14', '11', '12', '6', '10', '15', '8', '5']

for i in range(len(cisla)):
	if cisla[i] == '':
		canvas.create_rectangle(pad+a*(i%4), pad+(i//4)*a+a, pad+a*(i%4)+a, pad+(i//4)*a, fill='orange')
	else:
		canvas.create_rectangle(pad+a*(i%4), pad+(i//4)*a+a, pad+a*(i%4)+a, pad+(i//4)*a, fill='grey')
canvas.mainloop()
