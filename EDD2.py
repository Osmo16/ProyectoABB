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

    def minimo(self, node=None):
        node = node or self.raiz
        while node and node.left:
            node = node.left
        return node

    def maximo(self, node=None):
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