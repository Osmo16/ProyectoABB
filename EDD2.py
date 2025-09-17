import pygame
import sys
import random

# ====================
# Clase Nodo
# ====================
class Nodo:
    def __init__(self, poder, nombre, x=0, y=0):
        self.poder = poder
        self.nombre = nombre
        self.x = x
        self.y = y
        self.izq = None
        self.der = None

# ====================
# Clase Arbol BST
# ====================
class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, poder, nombre):
        self.raiz = self._insertar(self.raiz, poder, nombre)

    def _insertar(self, nodo, poder, nombre):
        if nodo is None:
            return Nodo(poder, nombre)
        if poder < nodo.poder:
            nodo.izq = self._insertar(nodo.izq, poder, nombre)
        elif poder > nodo.poder:
            nodo.der = self._insertar(nodo.der, poder, nombre)
        return nodo

    def buscar(self, poder):
        return self._buscar(self.raiz, poder)

    def _buscar(self, nodo, poder):
        if nodo is None or nodo.poder == poder:
            return nodo
        if poder < nodo.poder:
            return self._buscar(nodo.izq, poder)
        else:
            return self._buscar(nodo.der, poder)

    def minimo(self, nodo=None):
        nodo = nodo or self.raiz
        while nodo and nodo.izq:
            nodo = nodo.izq
        return nodo

    def maximo(self, nodo=None):
        nodo = nodo or self.raiz
        while nodo and nodo.der:
            nodo = nodo.der
        return nodo

    # ====================
    # Dibujar árbol
    # ====================
    def dibujar(self, surface, fuente, x, y, nivel=1, nodo=None):
        if nodo is None:
            nodo = self.raiz
        if nodo is None:
            return

        # Dibujar nodo actual
        pygame.draw.circle(surface, (100, 200, 250), (x, y), 20)
        texto = fuente.render(str(nodo.poder), True, (0, 0, 0))
        surface.blit(texto, (x - 10, y - 10))

        # Posiciones hijos
        dx = 300 // nivel
        dy = 70

        if nodo.izq:
            pygame.draw.line(surface, (0, 0, 0), (x, y), (x - dx, y + dy))
            self.dibujar(surface, fuente, x - dx, y + dy, nivel + 1, nodo.izq)

        if nodo.der:
            pygame.draw.line(surface, (0, 0, 0), (x, y), (x + dx, y + dy))
            self.dibujar(surface, fuente, x + dx, y + dy, nivel + 1, nodo.der)

# ====================
# Clase Juego
# ====================
class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Guardianes del Bosque Ancestral")
        self.fuente = pygame.font.SysFont("Arial", 20)
        self.arbol = ArbolBST()

        # Lista de eventos predefinidos
        self.eventos = [
            ("insertar", 50, "Gema del Río"),
            ("insertar", 30, "Gema del Viento"),
            ("insertar", 70, "Gema del Fuego"),
            ("buscar", 40, ""),
            ("minimo", None, ""),
            ("maximo", None, ""),
            ("insertar", 60, "Gema de la Tierra"),
            ("insertar", 80, "Gema del Trueno"),
            ("buscar", 30, ""),
            ("buscar", 90, ""),
            ("minimo", None, ""),
            ("maximo", None, ""),
            ("insertar", 20, "Gema del Hielo"),
            ("insertar", 10, "Gema de la Luna"),
            ("insertar", 25, "Gema del Sol"),
            ("buscar", 25, ""),
            ("buscar", 15, ""),
            ("minimo", None, ""),
            ("maximo", None, ""),
            ("buscar", 70, ""),
        ]
        self.evento_actual = 0
        self.mensaje = ""

    def ejecutar(self):
        reloj = pygame.time.Clock()
        tiempo_evento = 0

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Cada 2 segundos ejecutar un evento
            tiempo_evento += reloj.get_time()
            if tiempo_evento > 2000 and self.evento_actual < len(self.eventos):
                self.procesar_evento(self.eventos[self.evento_actual])
                self.evento_actual += 1
                tiempo_evento = 0

            # Dibujar
            self.pantalla.fill((255, 255, 255))
            self.arbol.dibujar(self.pantalla, self.fuente, 400, 50)
            texto = self.fuente.render(self.mensaje, True, (0, 0, 0))
            self.pantalla.blit(texto, (20, 550))
            pygame.display.flip()
            reloj.tick(30)

    def procesar_evento(self, evento):
        tipo, poder, nombre = evento
        if tipo == "insertar":
            self.arbol.insertar(poder, nombre)
            self.mensaje = f"Insertada gema {poder} - {nombre}"
        elif tipo == "buscar":
            nodo = self.arbol.buscar(poder)
            if nodo:
                self.mensaje = f"Gema {poder} encontrada: {nodo.nombre}"
            else:
                self.mensaje = f"Gema {poder} no existe"
        elif tipo == "minimo":
            nodo = self.arbol.minimo()
            if nodo:
                self.mensaje = f"Gema mínima: {nodo.poder} - {nodo.nombre}"
        elif tipo == "maximo":
            nodo = self.arbol.maximo()
            if nodo:
                self.mensaje = f"Gema máxima: {nodo.poder} - {nodo.nombre}"

# ====================
# Main
# ====================
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()
