import random
import pygame

class FlappyBird:
    def __init__(self):
        pygame.init()
        pygame.event.set_grab(False)
        self.pantalla = pygame.display.set_mode((700, 600))
        self.clock = pygame.time.Clock()
        self.fuente = pygame.font.SysFont('Impact', 50)
        
        self.bird_img = pygame.image.load('Imagenes/bird.png').convert_alpha()
        self.bird_img = pygame.transform.scale(self.bird_img, (50, 50))
        self.tubo_img_base = pygame.image.load('Imagenes/tuberia.png').convert_alpha()
        self.tubo_img_base.set_colorkey((255, 255, 255))
        self.tubo_img_base = pygame.transform.scale(self.tubo_img_base, (50, 500))
        self.tubo_img_arriba = pygame.transform.flip(self.tubo_img_base, False, True)
        
        self.reset()

    def reset(self):
        if not hasattr(self, 'mejor_puntaje'):
            self.mejor_puntaje = 0
        if not hasattr(self, 'puntos'): 
            self.puntos = 0
        self.mejor_puntaje = max(self.mejor_puntaje, self.puntos)
    
        self.x, self.y = 50, 300
        self.bird_vel = 0
        self.gravedad = 0.4
        self.salto = -8
        self.puntos = 0
        self.tubos = [
            {"x": 700,  "y": random.randint(150, 380), "pasado": False},
            {"x": 950,  "y": random.randint(150, 380), "pasado": False},
            {"x": 1200, "y": random.randint(150, 380), "pasado": False},
        ]
        return self.get_state()

    def get_state(self):
        """Devuelve valores RAW (sin normalizar) - la normalizacion la hace flappy_env.py"""
        tubos_delante = [t for t in self.tubos if t["x"] > self.x - 50]
        if len(tubos_delante) == 0:
            proximo_tubo = self.tubos[0]
        else:
            proximo_tubo = min(tubos_delante, key=lambda t: t["x"])

        return {
            "pajaro_y":   self.y,               # 0 a 600
            "pajaro_vel": self.bird_vel,         # -8 a +10 aprox
            "tubo_x":     proximo_tubo["x"] - self.x,  # 0 a 700
            "tubo_y":     proximo_tubo["y"],     # 150 a 380
        }

    def step(self, accion):
        recompensa = 0.1
        terminado = False

        if accion == 1:
            self.bird_vel = self.salto

        self.bird_vel += self.gravedad
        self.y += self.bird_vel

        hitbox_bird = pygame.Rect(self.x + 5, self.y + 5, 40, 40)
        
        for tubo in self.tubos:
            tubo["x"] -= 5
            
            if tubo["x"] + 50 < self.x and not tubo["pasado"]:
                tubo["pasado"] = True
                self.puntos += 1
                recompensa = 15.0

            if tubo["x"] < -50:
                tubo["x"] = 700
                tubo["y"] = random.randint(150, 380)
                tubo["pasado"] = False

            rect_arriba = pygame.Rect(tubo["x"], 0, 50, tubo["y"])
            rect_abajo  = pygame.Rect(tubo["x"], tubo["y"] + 160, 50, 600)

            if hitbox_bird.colliderect(rect_arriba) or hitbox_bird.colliderect(rect_abajo):
                recompensa = -20.0
                terminado = True

        if self.y > 550 or self.y < 0:
            recompensa = -20.0
            terminado = True
            
        return self.get_state(), recompensa, terminado

    def render(self):
        self.pantalla.fill((135, 206, 235))
        self.pantalla.blit(self.bird_img, (self.x, self.y))
        for tubo in self.tubos:
            self.pantalla.blit(self.tubo_img_arriba, (tubo["x"], tubo["y"] - 500))
            self.pantalla.blit(self.tubo_img_base,   (tubo["x"], tubo["y"] + 160))

       # Puntaje actual - arriba al centro
        fuente_grande = pygame.font.SysFont('Impact', 50)
        texto = f"{self.puntos}"
        sombra = fuente_grande.render(texto, True, (0, 0, 0, 128))
        self.pantalla.blit(sombra, (353, 53))
        marcador = fuente_grande.render(texto, True, (255, 255, 255))
        self.pantalla.blit(marcador, (350, 50))

        # Mejor puntaje - abajo a la derecha, mas chiquito
        fuente_chica = pygame.font.SysFont('Impact', 35)
        mejor_texto = f"MEJOR: {self.mejor_puntaje}"
        sombra_mejor = fuente_chica.render(mejor_texto, True, (0, 0, 0))
        self.pantalla.blit(sombra_mejor, (507, 562))
        marcador_mejor = fuente_chica.render(mejor_texto, True, (255, 213, 80))
        self.pantalla.blit(marcador_mejor, (510, 560))

        pygame.display.flip()
        #self.clock.tick(200)

if __name__ == "__main__":
    juego = FlappyBird()
    corriendo = True
    while corriendo:
        accion = 0
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: corriendo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE: accion = 1
        _, _, muerto = juego.step(accion)
        juego.render()
        if muerto:
            juego.reset()
        juego.clock.tick(60)
    pygame.quit()