iimport pandas as panda

my_data = panda.read_csv('CallesMedellin.csv', sep = ";")

vertice = []
Aristas = []
calles = my_data.iloc[: ,1]

for i in calles:
	if i in vertice:
		pass
	else:
		vertice.append(i)

import math

class Vertice:
	
	def __init__(self, i):
		
		self.id = i
		self.vecinos = []
		self.visitado = False
		self.padre = None
		self.costo = float('inf')

	def agregarVecino(self, v, p):
		if v not in self.vecinos:
			self.vecinos.append([v, p])

class Grafica:

	def __init__(self):
	
		self.vertices = {}

	def agregarVertice(self, id):
		
		if id not in self.vertices:
			self.vertices[id] = Vertice(id)

	def agregarArista(self, a, b, p):
		
		if a in self.vertices and b in self.vertices:
			self.vertices[a].agregarVecino(b, p)
			self.vertices[b].agregarVecino(a, p)

	def imprimirGrafica(self):
		for v in self.vertices:
			print("El costo del vértice "+str(self.vertices[v].id)+" es "+ str(self.vertices[v].costo)+" llegando desde "+str(self.vertices[v].padre))
			
	
	def camino(self, a, b):
		camino = []
		actual = b
		while actual != None:
			camino.insert(0, actual)
			actual = self.vertices[actual].padre
		return [camino, self.vertices[b].costo]

	def minimo(self, l):
		
		if len(l) > 0:
			m = self.vertices[l[0]].costo
			v = l[0]
			for e in l:
				if m > self.vertices[e].costo:
					m = self.vertices[e].costo
					v = e
			return v
		return None

	def dijkstra(self, a):
		
		if a in self.vertices:
			# 1 y 2
			self.vertices[a].costo = 0
			actual = a
			noVisitados = []
			
			for v in self.vertices:
				if v != a:
					self.vertices[v].costo = float('inf')
				self.vertices[v].padre = None
				noVisitados.append(v)

			while len(noVisitados) > 0:
				#3
				for vec in self.vertices[actual].vecinos:
					if self.vertices[vec[0]].visitado == False:
						# 3.a
						if self.vertices[actual].costo + vec[1] < self.vertices[vec[0]].costo:
							self.vertices[vec[0]].costo = self.vertices[actual].costo + vec[1]
							self.vertices[vec[0]].padre = actual

				# 4
				self.vertices[actual].visitado = True
				noVisitados.remove(actual)

				# 5 y 6
				actual = self.minimo(noVisitados)
		else:
			return False

g = Grafica()

for i in range(len(vertice)):
    vertice_dato = vertice[i]
    g.agregarVertice(vertice_dato)

for i in range(0,68749):
	g.agregarArista(my_data.loc[i,'origin'],my_data.loc[i,'destination'], my_data.loc[i,'harassmentRisk']+my_data.loc[i,'length'])

g.dijkstra(vertice[0])
print("El mejor camino es: ...")
print(g.camino(vertice[0], vertice[20]))
print(vertice[50])
