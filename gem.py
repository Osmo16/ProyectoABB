import pygame
import random
import math

# ==============================================================================
# SECCIÓN 1: CONFIGURACIÓN
# ==============================================================================
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (100, 149, 237)
ROJO = (255, 80, 80)
AMARILLO = (255, 255, 0)
ANCHO, ALTO = 800, 600
FUENTE_TIPO = 'consolas'
FUENTE_GRANDE = 24
FUENTE_PEQUENA = 20

# ==============================================================================
# SECCIÓN 2: ESTRUCTURA DE DATOS (ÁRBOL BINARIO DE BÚSQUEDA)
# (Esta sección no cambia, es el núcleo lógico del proyecto)
# ==============================================================================
class Nodo:
    def __init__(self, poder, nombre, coordx, coordy):
        self.poder = poder
        self.nombre = nombre
        self.coordenadax = coordx
        self.coordenaday = coordy
        self.izquierda = None
        self.derecha = None

class ArbolBST:
    def __init__(self):
        self.raiz = None

    def insertar(self, poder, nombre, coordx, coordy):
        nuevo_nodo = Nodo(poder, nombre, coordx, coordy)
        if self.raiz is None: self.raiz = nuevo_nodo
        else: self._insertar_recursivo(self.raiz, nuevo_nodo)

    def _insertar_recursivo(self, actual, nuevo_nodo):
        if nuevo_nodo.poder < actual.poder:
            if actual.izquierda is None: actual.izquierda = nuevo_nodo
            else: self._insertar_recursivo(actual.izquierda, nuevo_nodo)
        else:
            if actual.derecha is None: actual.derecha = nuevo_nodo
            else: self._insertar_recursivo(actual.derecha, nuevo_nodo)

    def buscar(self, poder):
        return self._buscar_recursivo(self.raiz, poder)

    def _buscar_recursivo(self, actual, poder):
        if actual is None or actual.poder == poder: return actual
        if poder < actual.poder: return self._buscar_recursivo(actual.izquierda, poder)
        return self._buscar_recursivo(actual.derecha, poder)

    def eliminar(self, poder):
        self.raiz = self._eliminar_recursivo(self.raiz, poder)

    def _eliminar_recursivo(self, actual, poder):
        if actual is None: return actual
        if poder < actual.poder: actual.izquierda = self._eliminar_recursivo(actual.izquierda, poder)
        elif poder > actual.poder: actual.derecha = self._eliminar_recursivo(actual.derecha, poder)
        else:
            if actual.izquierda is None: return actual.derecha
            elif actual.derecha is None: return actual.izquierda
            temp = self.encontrar_minimo(actual.derecha)
            actual.poder, actual.nombre = temp.poder, temp.nombre
            actual.derecha = self._eliminar_recursivo(actual.derecha, temp.poder)
        return actual
    
    def recorrido_inorden(self):
        elementos = []
        self._inorden_recursivo(self.raiz, elementos)
        return elementos

    def _inorden_recursivo(self, nodo, elementos):
        if nodo:
            self._inorden_recursivo(nodo.izquierda, elementos)
            elementos.append(nodo)
            self._inorden_recursivo(nodo.derecha, elementos)

    def encontrar_minimo(self, nodo=None):
        actual = nodo if nodo is not None else self.raiz
        if not actual: return None
        while actual.izquierda is not None: actual = actual.izquierda
        return actual
    
    def sucesor(self, poder):
        ancestro, actual = None, self.raiz
        while actual is not None:
            if poder < actual.poder:
                ancestro, actual = actual, actual.izquierda
            elif poder > actual.poder:
                actual = actual.derecha
            else:
                if actual.derecha is not None: return self.encontrar_minimo(actual.derecha)
                break
        return ancestro
        
# ==============================================================================
# SECCIÓN 3: CLASES DEL JUEGO 2D
# ==============================================================================
class Jugador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30) # Un simple cuadrado
        self.velocidad = 5

    def mover(self, dx, dy):
        self.rect.x += dx * self.velocidad
        self.rect.y += dy * self.velocidad
        # Mantener dentro de la pantalla
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(ALTO, self.rect.bottom)

    def dibujar(self, superficie):
        pygame.draw.rect(superficie, VERDE, self.rect)

class GemaVisual:
    def __init__(self, poder, nombre, x, y):
        self.poder = poder
        self.nombre = nombre
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def dibujar(self, superficie):
        pygame.draw.ellipse(superficie, self.color, self.rect)
        pygame.draw.ellipse(superficie, BLANCO, self.rect, 2)

# ==============================================================================
# SECCIÓN 4: SIMULACIÓN PRINCIPAL CON PYGAME
# ==============================================================================
def dibujar_texto(superficie, texto, tam, x, y, color):
    fuente = pygame.font.SysFont(FUENTE_TIPO, tam)
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(topleft=(x, y))
    superficie.blit(superficie_texto, rect_texto)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Guardianes del Bosque - Juego 2D Interactivo")
    reloj = pygame.time.Clock()
    
    # --- Inicialización del Juego ---
    inventario_bst = ArbolBST()
    jugador = Jugador(ANCHO // 2, ALTO // 2)
    
    gemas_en_mapa = [
        GemaVisual(50, "Gema del Río", 100, 150),
        GemaVisual(30, "Gema del Viento", 200, 400),
        GemaVisual(70, "Gema de Fuego", 600, 100),
        GemaVisual(20, "Gema de Tierra", 700, 500),
        GemaVisual(45, "Gema de Sombra", 350, 80),
        GemaVisual(80, "Gema de Luz", 50, 500)
    ]
    
    log_evento = "¡Usa las flechas para moverte y recoge las gemas!"
    
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        
        # --- MANEJO DE ENTRADAS (CONTROLES) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j: # Evento de Jefe
                    poder_req = random.randint(35, 75)
                    gema = inventario_bst.buscar(poder_req)
                    if gema:
                        log_evento = f"Jefe pide {poder_req}. ¡La tienes! Entregas '{gema.nombre}'."
                        inventario_bst.eliminar(poder_req)
                    else:
                        suc = inventario_bst.sucesor(poder_req)
                        if suc:
                            log_evento = f"Jefe pide {poder_req}. Das la más cercana: '{suc.nombre}' ({suc.poder})."
                            inventario_bst.eliminar(suc.poder)
                        else:
                            log_evento = f"Jefe pide {poder_req}. No tienes gemas para darle."

        keys = pygame.key.get_pressed()
        mov_x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        mov_y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        jugador.mover(mov_x, mov_y)

        # --- LÓGICA DEL JUEGO (COLISIONES) ---
        gemas_a_recolectar = []
        for gema_visual in gemas_en_mapa:
            if jugador.rect.colliderect(gema_visual.rect):
                gemas_a_recolectar.append(gema_visual)
        
        for gema_recolectada in gemas_a_recolectar:
            # La interacción del jugador (colisión) llama a la operación del árbol
            inventario_bst.insertar(gema_recolectada.poder, gema_recolectada.nombre, gema_recolectada.rect.x, gema_recolectada.rect.y)
            log_evento = f"¡Recolectaste '{gema_recolectada.nombre}' (Poder: {gema_recolectada.poder})!"
            gemas_en_mapa.remove(gema_recolectada)

        # --- DIBUJAR EN PANTALLA ---
        pantalla.fill(NEGRO)
        
        # Dibujar objetos del juego
        jugador.dibujar(pantalla)
        for gema in gemas_en_mapa:
            gema.dibujar(pantalla)
        
        # Dibujar HUD (Interfaz de usuario)
        pygame.draw.rect(pantalla, (20, 20, 20), (0, ALTO - 100, ANCHO, 100))
        dibujar_texto(pantalla, "Log del Evento:", FUENTE_PEQUENA, 10, ALTO - 95, AMARILLO)
        dibujar_texto(pantalla, log_evento, FUENTE_PEQUENA, 20, ALTO - 70, BLANCO)
        
        inventario_ordenado = inventario_bst.recorrido_inorden()
        texto_inv = "Inventario: " + ", ".join([str(g.poder) for g in inventario_ordenado])
        dibujar_texto(pantalla, texto_inv, FUENTE_PEQUENA, 10, ALTO - 40, BLANCO)
        
        dibujar_texto(pantalla, "Mover: [Flechas] | Evento Jefe: [J]", FUENTE_PEQUENA, 10, 10, BLANCO)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()