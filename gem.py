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
ANCHO, ALTO = 1000, 700
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
        # Verifica si la clave ya existe antes de insertar
        if self.buscar(poder) is not None:
            return  # No hace nada si la gema con ese poder ya está en el inventario

        nuevo_nodo = Nodo(poder, nombre, coordx, coordy)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo)

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
    
    def encontrar_maximo(self, nodo=None):
        actual = nodo if nodo is not None else self.raiz
        if not actual:
            return None
        while actual.derecha is not None:
            actual = actual.derecha
        return actual
    
    def eliminar_aleatorio(self):
        elementos = self.recorrido_inorden()
        if not elementos:
            return None
        
        gema_a_eliminar = random.choice(elementos)
        self.eliminar(gema_a_eliminar.poder)
        return gema_a_eliminar.poder
    
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
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocidad = 5
        self.tam_original = 30
        self.factor_pulsacion = 1.0

    def mover(self, dx, dy):
        self.rect.x += dx * self.velocidad
        self.rect.y += dy * self.velocidad
        # Mantener dentro de la pantalla
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(ALTO, self.rect.bottom)

    def dibujar(self, superficie):
        # Actualiza el factor de pulsación (ejemplo con seno para un efecto suave)
        self.factor_pulsacion = 1 + 0.1 * math.sin(pygame.time.get_ticks() / 150)
        
        tam_actual = int(self.tam_original * self.factor_pulsacion)
        rect_actual = pygame.Rect(0, 0, tam_actual, tam_actual)
        rect_actual.center = self.rect.center # Mantiene el centro en su lugar
        
        pygame.draw.rect(superficie, VERDE, rect_actual)
        pygame.draw.rect(superficie, BLANCO, rect_actual, 2)
        
class GemaVisual:
    def __init__(self, poder, nombre, x, y):
        self.poder = poder
        self.nombre = nombre
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def dibujar(self, superficie):
        pygame.draw.ellipse(superficie, self.color, self.rect)
        pygame.draw.ellipse(superficie, BLANCO, self.rect, 2)

class CofreVisual:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.abierto = False
        self.color = AMARILLO

    def dibujar(self, superficie):
        if not self.abierto:
            pygame.draw.rect(superficie, self.color, self.rect)
            pygame.draw.rect(superficie, NEGRO, self.rect, 2)

class PortalVisual:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = AZUL

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, self.rect.center, 30)
        pygame.draw.circle(superficie, BLANCO, self.rect.center, 30, 2)

class TrampaVisual:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = ROJO
        self.activa = True

    def dibujar(self, superficie):
        if self.activa:
            pygame.draw.ellipse(superficie, self.color, self.rect)
            pygame.draw.ellipse(superficie, AZUL, self.rect, 2)

def crear_gema_aleatoria():
    """
    Crea y devuelve una nueva gema con poder, nombre y posición aleatorios.
    """
    poder = random.randint(1, 150)
    
    nombre = "Orbe Especial"
    
    # Posición aleatoria, con un margen para que no aparezca en los bordes
    x = random.randint(50, ANCHO - 50)
    y = random.randint(50, ALTO - 150) # Un poco más de margen abajo por el HUD
    
    return GemaVisual(poder, nombre, x, y)

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
    pygame.display.set_caption("Guardianes del Bosque")
    reloj = pygame.time.Clock()
    
    # --- Inicialización del Juego ---
    score = 0
    game_over = False
    TIEMPO_APARICION_COFRE = 45000 
    tiempo_ultimo_cofre = pygame.time.get_ticks()
    TIEMPO_APARICION_PORTAL = 60000  
    tiempo_ultimo_portal = pygame.time.get_ticks()
    portal_en_mapa = None
    TIEMPO_APARICION_TRAMPA = 30000  
    tiempo_ultima_trampa = pygame.time.get_ticks()
    trampas_en_mapa = [
        TrampaVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150)),
        TrampaVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150)),
        TrampaVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150)),
        TrampaVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150)),
    ]

    inventario_bst = ArbolBST()
    jugador = Jugador(ANCHO // 2, ALTO // 2)

    # Crea una lista de gemas en posiciones aleatorias
    gemas_en_mapa = [
        GemaVisual(50, "Gema del Río", random.randint(5, ANCHO - 50), random.randint(5, ALTO - 150)),
        GemaVisual(30, "Gema del Viento", random.randint(25, ANCHO - 50), random.randint(25, ALTO - 150)),
        GemaVisual(70, "Gema de Fuego", random.randint(150, ANCHO - 50), random.randint(50, ALTO - 150)),
        GemaVisual(20, "Gema de Tierra", random.randint(200, ANCHO - 50), random.randint(75, ALTO - 150)),
        GemaVisual(45, "Gema de Sombra", random.randint(245, ANCHO - 50), random.randint(100, ALTO - 150)),
        GemaVisual(80, "Gema de Luz", random.randint(375, ANCHO - 50), random.randint(150, ALTO - 150)),
    ]
    # Crea una lista de cofres en posiciones aleatorias
    cofres_en_mapa = [
        CofreVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150)),
        CofreVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150)),
    ]
    # Crea un portal en una posicion aleatoria
    portal = PortalVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150))
    
    log_evento = "¡Muévete para recoger las gemas!"
    
    

    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        
        # --- 1. MANEJO DE EVENTOS ---
        # Este bloque solo se preocupa por las entradas del usuario (teclado, cerrar ventana)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j: # Evento de Jefe
                        
                        poder_req = random.randint(1, 150)
                        gema = inventario_bst.buscar(poder_req)
                        if gema:
                            score += 2
                            inventario_bst.eliminar(poder_req)
                        elif inventario_bst.sucesor(poder_req):
                            suc = inventario_bst.sucesor(poder_req)
                            score += 1
                            inventario_bst.eliminar(suc.poder)
                        else:
                            score = max(0, score - 1)
                        
                        
                        log_evento = f"Evento de Jefe: Dame la gema de poder {poder_req} o la mas cercana. Puntaje: {score}"
        
        if score >= 50:
            game_over = True
            log_evento = f"¡Alcanzaste {score} puntos y ganaste el juego!"
     
        if not game_over: 
            keys = pygame.key.get_pressed()
            mov_x = keys[pygame.K_d] - keys[pygame.K_a]
            mov_y = keys[pygame.K_s] - keys[pygame.K_w]
            jugador.mover(mov_x, mov_y)

            # Lógica de colisiones
            gemas_a_recolectar = []
            for gema_visual in gemas_en_mapa:
                if jugador.rect.colliderect(gema_visual.rect):
                    gemas_a_recolectar.append(gema_visual)
            
            for gema_recolectada in gemas_a_recolectar:
                inventario_bst.insertar(gema_recolectada.poder, gema_recolectada.nombre, gema_recolectada.rect.x, gema_recolectada.rect.y)
                log_evento = f"¡Recolectaste '{gema_recolectada.nombre}' (Poder: {gema_recolectada.poder})!"
                gemas_en_mapa.remove(gema_recolectada)
                gemas_en_mapa.append(crear_gema_aleatoria())
            
            # Lógica de aparición de cofres
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_ultimo_cofre >= TIEMPO_APARICION_COFRE:
                # Generar un nuevo cofre en una posición aleatoria
                nuevo_cofre = CofreVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150))
                cofres_en_mapa.append(nuevo_cofre)
                tiempo_ultimo_cofre = tiempo_actual # Actualiza el temporizador
                log_evento = "¡Un cofre ha aparecido en el bosque!"
            
            # --- Lógica de colisión con cofres ---
            cofres_a_abrir = []
            for cofre in cofres_en_mapa:
                if not cofre.abierto and jugador.rect.colliderect(cofre.rect):
                    cofres_a_abrir.append(cofre)

            for cofre_abrir in cofres_a_abrir:
                gema_minima = inventario_bst.encontrar_minimo()
                if gema_minima:
                    score += 5
                    inventario_bst.eliminar(gema_minima.poder)
                    cofre_abrir.abierto = True
                    cofre_abrir.color = BLANCO # Cambia el color para indicar que está abierto
                    log_evento = f"¡Abres un cofre usando la gema de poder {gema_minima.poder}! +5 puntos."
                else:
                    log_evento = "No tienes gemas para abrir el cofre. ¡Recolecta una gema!"
            
            # --- Lógica de aparición del portal ---
            tiempo_actual = pygame.time.get_ticks()
            if portal_en_mapa is None and tiempo_actual - tiempo_ultimo_portal >= TIEMPO_APARICION_PORTAL:
                portal_en_mapa = PortalVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150))
                tiempo_ultimo_portal = tiempo_actual
                log_evento = "¡Un portal mágico ha aparecido!"
            
            # --- Lógica de colisión con el portal ---
            if portal_en_mapa and jugador.rect.colliderect(portal_en_mapa.rect):
                gema_maxima = inventario_bst.encontrar_maximo()
                if gema_maxima:
                    score += 7
                    inventario_bst.eliminar(gema_maxima.poder)
            
                    # Teletransportar al jugador a una nueva posición
                    jugador.rect.x = random.randint(50, ANCHO - 50)
                    jugador.rect.y = random.randint(50, ALTO - 150)
                    
                    log_evento = f"¡Usaste la gema de poder {gema_maxima.poder} para activar el portal! +7 puntos."
                    portal_en_mapa = None  # Elimina el portal después de usarlo
                else:
                    log_evento = "No tienes gemas para activar el portal."
            
            # --- Lógica de aparición de las trampas ---
            tiempo_actual = pygame.time.get_ticks()
            if len(trampas_en_mapa) < 10 and tiempo_actual - tiempo_ultima_trampa >= TIEMPO_APARICION_TRAMPA:
                nueva_trampa = TrampaVisual(random.randint(50, ANCHO - 50), random.randint(50, ALTO - 150))
                trampas_en_mapa.append(nueva_trampa)
                tiempo_ultima_trampa = tiempo_actual
                log_evento = "¡Una nueva trampa ha aparecido!"
            
            # --- Lógica de colisión con las trampas ---
            trampas_a_eliminar = []
            for trampa in trampas_en_mapa:
                if jugador.rect.colliderect(trampa.rect):
                    gema_perdida_poder = inventario_bst.eliminar_aleatorio()
                    score = max(0, score - 2)
                    
                    if gema_perdida_poder is not None:
                        log_evento = f"¡Caíste en una trampa! Pierdes 2 puntos y la gema de poder {gema_perdida_poder}."
                    else:
                        log_evento = "¡Caíste en una trampa! Pierdes 2 puntos, pero no tienes gemas para perder."
                    
                    trampas_a_eliminar.append(trampa)
            
            for trampa_eliminar in trampas_a_eliminar:
                trampas_en_mapa.remove(trampa_eliminar)

            # Dibujado de la pantalla de juego
            pantalla.fill(NEGRO)
            jugador.dibujar(pantalla)
            for gema in gemas_en_mapa:
                gema.dibujar(pantalla)
            for cofre in cofres_en_mapa:
                cofre.dibujar(pantalla)
            if portal_en_mapa:
                portal_en_mapa.dibujar(pantalla)
            for trampa in trampas_en_mapa:
                trampa.dibujar(pantalla)
            
            # Dibujar HUD
            pygame.draw.rect(pantalla, (20, 20, 20), (0, ALTO - 100, ANCHO, 100))
            dibujar_texto(pantalla, "Log del Evento:", FUENTE_PEQUENA, 10, ALTO - 95, AMARILLO)
            dibujar_texto(pantalla, log_evento, FUENTE_PEQUENA, 20, ALTO - 70, BLANCO)
            inventario_ordenado = inventario_bst.recorrido_inorden()
            texto_inv = "Inventario: " + ", ".join([str(g.poder) for g in inventario_ordenado])
            dibujar_texto(pantalla, texto_inv, FUENTE_PEQUENA, 10, ALTO - 40, BLANCO)
            dibujar_texto(pantalla, "Mover: [WASD] | Evento Jefe: [J]", FUENTE_PEQUENA, 10, 10, BLANCO)
            dibujar_texto(pantalla, f"Puntaje: {score} / 50", FUENTE_GRANDE, ANCHO - 220, 10, BLANCO)

        else: 
            pantalla.fill(AZUL)
            dibujar_texto(pantalla, "¡GANASTE!", FUENTE_GRANDE, ANCHO // 2.2, ALTO // 2 - 50, BLANCO)
            dibujar_texto(pantalla, log_evento, FUENTE_PEQUENA, ANCHO // 2.6, ALTO // 2 + 10, BLANCO)
            dibujar_texto(pantalla, "Cierra la ventana para salir", FUENTE_PEQUENA, ANCHO // 2, ALTO - 50, BLANCO)
        
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
