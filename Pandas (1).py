import pandas as panda
import math
from shapely.wkt import loads
import matplotlib.pyplot as plt
import geopandas as gpd
import time


my_data = panda.read_csv('calles_de_medellin_con_acoso.csv', sep = ";")
polygon_data = panda.read_csv("poligono_de_medellin.csv",sep=";")

fig, ax  = plt.subplots()



poly = loads(polygon_data.iloc[0]["geometry"])



p = gpd.GeoSeries(poly)

p.plot(ax=ax)

vertice = []  #informacion de calles de origin (todos los nodos)
Aristas = []
calles = my_data.iloc[: ,1]

for i in calles:
	if i  not in vertice:
		vertice.append(i)


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

class Grafo:

	def __init__(self):
	
		self.vertices = {}

	def agregarVertice(self, id):
		
		if id not in self.vertices:
			self.vertices[id] = Vertice(id)

	def agregarArista(self, a, b, p):
		
		if a in self.vertices and b in self.vertices:
			self.vertices[a].agregarVecino(b, p)

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

	def eliminarCamino(self,camino):

		if len(camino)  < 3: 

			raise NotImplemented()
		
		

		nodosAEliminar = camino[1:-1]

		for nodo in nodosAEliminar:

			for vertice in self.vertices.values():

				vertice.vecinos = list(filter(lambda par: par[0] != nodo,vertice.vecinos))
			
			self.vertices.pop(nodo)
			

			

	#Dado los noVisitados, conseguir el de menor costo
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

def graficarCamino(camino,color):

	for i in range(len(camino)-1):

		filtered = my_data[(my_data.origin==camino[i]) &  (my_data.destination == camino[i+1])].geometry.iloc[0]


		ax.plot(*(loads(filtered)).xy,color=color)

def calcularDistanciaCamino(grafo:Grafo,camino):

	distancia = 0

	for i in range(len(camino)-1):

		distancia +=  my_data[(my_data.origin==camino[i]) &  (my_data.destination == camino[i+1])].length.iloc[0]

	return distancia

def calcularRiesgoCamino(grafo:Grafo,camino):

	risk = 0

	for i in range(len(camino)-1):

		risk +=  my_data[(my_data.origin==camino[i]) &  (my_data.destination == camino[i+1])].harassmentRisk.iloc[0]

	return risk



puntoInicial = "(-75.5673082, 6.2483328)"
puntoFinal = "(-75.5836885, 6.245388)"

#ax.scatter(x=[eval(puntoInicial)[0],eval[puntoFinal][0]],y=[eval(puntoInicial)[0],eval[puntoFinal][0]])
inicio = time.time()
g = Grafo()

for i in range(len(vertice)):
    vertice_dato = vertice[i]
    g.agregarVertice(vertice_dato)

for i in range(0,68749):


	g.agregarArista(my_data.loc[i,'origin'],my_data.loc[i,'destination'], my_data.loc[i,'harassmentRisk']+(my_data.loc[i,'length']))

	if not my_data.loc[i,"oneway"]:

		g.agregarArista(my_data.loc[i,'destination'],my_data.loc[i,'origin'],my_data.loc[i,'harassmentRisk']+(my_data.loc[i,'length']))



g.dijkstra(puntoInicial)

camino1 = g.camino(puntoInicial,puntoFinal)[0]


print("duracion camino 1:",time.time()-inicio,f"distancia total:{calcularDistanciaCamino(g,camino1)} riesgo total: {calcularRiesgoCamino(g,camino1)}")

graficarCamino(camino1,"red")

g2 = Grafo()

for i in range(len(vertice)):
    vertice_dato = vertice[i]
    g2.agregarVertice(vertice_dato)

for i in range(0,68749):


	g2.agregarArista(my_data.loc[i,'origin'],my_data.loc[i,'destination'], (my_data.loc[i,'harassmentRisk']**(my_data.loc[i,'length'])))

	if not my_data.loc[i,"oneway"]:

		g2.agregarArista(my_data.loc[i,'destination'],my_data.loc[i,'origin'], (my_data.loc[i,'harassmentRisk']**(my_data.loc[i,'length'])))

inicio=time.time()
g2.dijkstra(puntoInicial)

camino2 = g2.camino(puntoInicial,puntoFinal)[0]
print("duracion camino 2:",time.time()-inicio,f"distancia total:{calcularDistanciaCamino(g2,camino2)} riesgo total: {calcularRiesgoCamino(g2,camino2)}")
graficarCamino(camino2,"green")




g3 = Grafo()

for i in range(len(vertice)):
    vertice_dato = vertice[i]
    g3.agregarVertice(vertice_dato)

for i in range(0,68749):


	g3.agregarArista(my_data.loc[i,'origin'],my_data.loc[i,'destination'], (my_data.loc[i,'harassmentRisk'])*3267+my_data.loc[i,'length']*1234)

	if not my_data.loc[i,"oneway"]:

		g3.agregarArista(my_data.loc[i,'destination'],my_data.loc[i,'origin'], (my_data.loc[i,'harassmentRisk'])*3267+(my_data.loc[i,'length']*1234))

inicio = time.time()

g3.dijkstra(puntoInicial)


camino3 = g3.camino(puntoInicial,puntoFinal)[0]

print("duracion camino 3:",time.time()-inicio,f"distancia total:{calcularDistanciaCamino(g3,camino3)} riesgo total: {calcularRiesgoCamino(g3,camino3)}")

graficarCamino(camino3,"yellow")


plt.show()

