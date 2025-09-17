print("hola")
import pygame   
import sys
import random

class Node:
    def __init__(self, power, name, x=0, y=0):
        self.power = power
        self.name = name
        self.x = x
        self.y = y
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.raiz = None

    def insert(self, power, name):
        self.raiz = self._insert(self.raiz, power, name)

    def _insert(self, node, power, name):
        if node is None:
            return node(power, name)
        if power < node.power:
            node.left = self._insert(node.left, power, name)
        elif power > node.power:
            node.right = self._insert(node.right, power, name)
        return node

    def search(self, power):
        return self._search(self.raiz, power)

    def _search(self, node, power):
        if node is None or node.power == power:
            return node
        if power < node.power:
            return self._search(node.left, power)
        else:
            return self._search(node.right, power)

    def minimum(self, node=None):
        node = node or self.raiz
        while node and node.left:
            node = node.left
        return node

    def maximum(self, node=None):
        node = node or self.raiz
        while node and node.right:
            node = node.right
        return node

    # ====================
    # Dibujar árbol
    # ====================
    def dibujar(self, surface, fuente, x, y, nivel=1, node=None):
        if node is None:
            node = self.raiz
        if node is None:
            return

        # Dibujar node actual
        pygame.draw.circle(surface, (100, 200, 250), (x, y), 20)
        texto = fuente.render(str(node.power), True, (0, 0, 0))
        surface.blit(texto, (x - 10, y - 10))

        # Posiciones hijos
        dx = 300 // nivel
        dy = 70

        if node.left:
            pygame.draw.line(surface, (0, 0, 0), (x, y), (x - dx, y + dy))
            self.dibujar(surface, fuente, x - dx, y + dy, nivel + 1, node.left)

        if node.right:
            pygame.draw.line(surface, (0, 0, 0), (x, y), (x + dx, y + dy))
            self.dibujar(surface, fuente, x + dx, y + dy, nivel + 1, node.right)



class Juego:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Guardianes del Bosque Ancestral")
        self.fuente = pygame.font.SysFont("Arial", 20)
        self.arbol = Tree()

        # Lista de eventos predefinidos
        self.eventos = [
            ("insert", 50, "Gema del Río"),
            ("insert", 30, "Gema del Viento"),
            ("insert", 70, "Gema del Fuego"),
            ("buscar", 40, ""),
            ("minimo", None, ""),
            ("maximo", None, ""),
            ("insert", 60, "Gema de la Tierra"),
            ("insert", 80, "Gema del Trueno"),
            ("buscar", 30, ""),
            ("buscar", 90, ""),
            ("minimo", None, ""),
            ("maximo", None, ""),
            ("insert", 20, "Gema del Hielo"),
            ("insert", 10, "Gema de la Luna"),
            ("insert", 25, "Gema del Sol"),
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
        if tipo == "insert":
            self.arbol.insert(poder, nombre)
            self.mensaje = f"Insertada gema {poder} - {nombre}"
        elif tipo == "buscar":
            node = self.arbol.buscar(poder)
            if node:
                self.mensaje = f"Gema {poder} encontrada: {node.nombre}"
            else:
                self.mensaje = f"Gema {poder} no existe"
        elif tipo == "minimo":
            node = self.arbol.minimo()
            if node:
                self.mensaje = f"Gema mínima: {node.poder} - {node.nombre}"
        elif tipo == "maximo":
            node = self.arbol.maximo()
            if node:
                self.mensaje = f"Gema máxima: {node.poder} - {node.nombre}"

# ====================
# Main
# ====================
if __name__ == "__main__":
    juego = Juego()
    juego.ejecutar()