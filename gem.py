import pygame
import random

# ==============================================================================
# SECCIÓN 1: CONFIGURACIÓN
# ==============================================================================
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (100, 149, 237)
ANCHO = 800
ALTO = 600
FUENTE_TIPO = 'consolas'
FUENTE_GRANDE = 24
FUENTE_PEQUENA = 20

# ==============================================================================
# SECCIÓN 2: ESTRUCTURA DE DATOS (ÁRBOL BINARIO DE BÚSQUEDA)
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
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo)

    def _insertar_recursivo(self, actual, nuevo_nodo):
        if nuevo_nodo.poder < actual.poder:
            if actual.izquierda is None:
                actual.izquierda = nuevo_nodo
            else:
                self._insertar_recursivo(actual.izquierda, nuevo_nodo)
        else:
            if actual.derecha is None:
                actual.derecha = nuevo_nodo
            else:
                self._insertar_recursivo(actual.derecha, nuevo_nodo)

    def buscar(self, poder):
        return self._buscar_recursivo(self.raiz, poder)

    def _buscar_recursivo(self, actual, poder):
        if actual is None or actual.poder == poder:
            return actual
        if poder < actual.poder:
            return self._buscar_recursivo(actual.izquierda, poder)
        return self._buscar_recursivo(actual.derecha, poder)

    def eliminar(self, poder):
        self.raiz = self._eliminar_recursivo(self.raiz, poder)

    def _eliminar_recursivo(self, actual, poder):
        if actual is None: return actual
        if poder < actual.poder:
            actual.izquierda = self._eliminar_recursivo(actual.izquierda, poder)
        elif poder > actual.poder:
            actual.derecha = self._eliminar_recursivo(actual.derecha, poder)
        else:
            if actual.izquierda is None: return actual.derecha
            elif actual.derecha is None: return actual.izquierda
            temp = self.encontrar_minimo(actual.derecha)
            actual.poder, actual.nombre = temp.poder, temp.nombre
            actual.coordenadax, actual.coordenaday = temp.coordenadax, temp.coordenaday
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
        while actual.izquierda is not None:
            actual = actual.izquierda
        return actual

    def encontrar_maximo(self, nodo=None):
        actual = nodo if nodo is not None else self.raiz
        if not actual: return None
        while actual.derecha is not None:
            actual = actual.derecha
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

    def predecesor(self, poder):
        ancestro, actual = None, self.raiz
        while actual is not None:
            if poder > actual.poder:
                ancestro, actual = actual, actual.derecha
            elif poder < actual.poder:
                actual = actual.izquierda
            else:
                if actual.izquierda is not None: return self.encontrar_maximo(actual.izquierda)
                break
        return ancestro

# ==============================================================================
# SECCIÓN 3: LÓGICA DEL JUEGO
# ==============================================================================
class Juego:
    def __init__(self):
        self.inventario = ArbolBST()
        self.eventos = []
        self._crear_eventos_iniciales()
        self.log_evento = "Bienvenido a 'Guardianes del Bosque'. Presiona ESPACIO."

    def _crear_eventos_iniciales(self):
        gemas = [(50, "Gema del Río", 10, 15), (30, "Gema Viento", 5, 8), (70, "Gema Fuego", 20, 22), (20, "Gema Tierra", 2, 3), (45, "Gema Sombra", 12, 18), (80, "Gema Luz", 25, 30), (65, "Gema Tormenta", 18, 14)]
        for g in gemas: self.eventos.append({'tipo': 'RECOGER', 'datos': g})
        
        eventos = [{'tipo': 'JEFE', 'poder_req': 40}, {'tipo': 'COFRE'}, {'tipo': 'PORTAL'}, {'tipo': 'RECOGER', 'datos': (90, "Gema Estelar", 50, 50)}, {'tipo': 'TRAMPA', 'poder': 30}, {'tipo': 'JEFE', 'poder_req': 68}, {'tipo': 'REINICIAR'}, {'tipo': 'RECOGER', 'datos': (100, "Gema Ancestral", 1, 1)}, {'tipo': 'JEFE', 'poder_req': 95}, {'tipo': 'TRAMPA', 'poder': 70}] * 2
        self.eventos.extend(eventos)
        random.shuffle(self.eventos)

    def simular_siguiente_evento(self):
        if not self.eventos:
            self.log_evento = "FIN DE LA SIMULACIÓN."
            return
        evento = self.eventos.pop(0)
        tipo = evento['tipo']
        if tipo == 'RECOGER':
            p, n, x, y = evento['datos']
            self.inventario.insertar(p, n, x, y)
            self.log_evento = f"Recoges '{n}' (Poder: {p}). INSERTAR({p})"
        elif tipo == 'JEFE':
            p_req = evento['poder_req']
            gema = self.inventario.buscar(p_req)
            if gema:
                self.log_evento = f"Jefe pide {p_req}. ¡Encontrada! Entregas '{gema.nombre}'."
                self.inventario.eliminar(p_req)
            else:
                cercana = self.inventario.sucesor(p_req) or self.inventario.predecesor(p_req)
                if cercana:
                    self.log_evento = f"Jefe pide {p_req}. No la tienes. Das la más cercana: '{cercana.nombre}' ({cercana.poder})."
                    self.inventario.eliminar(cercana.poder)
                else: self.log_evento = f"Jefe pide {p_req}. No tienes gemas. ¡Has perdido!"
        elif tipo == 'COFRE':
            gema_min = self.inventario.encontrar_minimo()
            self.log_evento = f"Cofre abierto con la gema de menor poder: '{gema_min.nombre}' ({gema_min.poder})." if gema_min else "No tienes gemas para abrir el cofre."
        elif tipo == 'PORTAL':
            gema_max = self.inventario.encontrar_maximo()
            self.log_evento = f"Portal activado con la gema de mayor poder: '{gema_max.nombre}' ({gema_max.poder})." if gema_max else "No tienes gemas para el portal."
        elif tipo == 'TRAMPA':
            p_perdido = evento['poder']
            if self.inventario.buscar(p_perdido):
                self.inventario.eliminar(p_perdido)
                self.log_evento = f"¡Trampa! Pierdes la gema con poder {p_perdido}."
            else: self.log_evento = f"Caes en trampa, pero no tenías la gema de poder {p_perdido}."
        elif tipo == 'REINICIAR':
            self.log_evento = "Reiniciando el juego. Todas las gemas se han perdido."
            self.inventario.raiz = None

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
    pygame.display.set_caption("Guardianes del Bosque - Simulación BST")
    reloj = pygame.time.Clock()
    mi_juego = Juego()
    
    ejecutando = True
    while ejecutando:
        reloj.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: ejecutando = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mi_juego.simular_siguiente_evento()

        pantalla.fill(NEGRO)
        dibujar_texto(pantalla, "Simulación de Eventos del Juego", FUENTE_GRANDE, 20, 20, BLANCO)
        dibujar_texto(pantalla, "Evento:", FUENTE_PEQUENA, 20, 60, VERDE)
        
        # --- LÍNEA CORREGIDA ---
        dibujar_texto(pantalla, mi_juego.log_evento, FUENTE_PEQUENA, 40, 90, BLANCO)
        
        dibujar_texto(pantalla, "Inventario de Gemas (Ordenado por Poder):", FUENTE_GRANDE, 20, 200, AZUL)
        y_pos = 240
        for gema in mi_juego.inventario.recorrido_inorden():
            texto_gema = f"- Poder: {gema.poder}, Nombre: {gema.nombre}"
            dibujar_texto(pantalla, texto_gema, FUENTE_PEQUENA, 40, y_pos, BLANCO)
            y_pos += 30

        dibujar_texto(pantalla, "Presiona [ESPACIO] para el siguiente evento.", FUENTE_GRANDE, 20, ALTO - 50, VERDE)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()