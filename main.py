import pygame
import random
from libreria import *
import json

ANCHO=800
ALTO=600
VERDE=[0,255,0]
ROJO=[255,0,0]
AZUL=[0,0,255]
AMARILLO=[255,255,0]
AZUL_2=[0,255,255]
NEGRO=[0,0,0]
BLANCO=[255,255,255]
GRIS = [180,180,180]
BORDE_MAPA = 200

class Jugador(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite):
        '''
        El atributo direccion hace se utiliza para saber que sprite mostrar cuando se dibuja, mientras que los
        atributos direccion_x y direccion_y hacen referencia a hacia donde está mirando el jugador
        '''
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Jugador.png', 3, 2)
        self.puntaje = 0
        self.direccion = 0
        self.contador = 0
        self.direccion_x = 0
        self.direccion_y = 0
        self.saltar = False
        self.image = self.imagen[self.direccion][self.contador]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velocidad = 5
        self.velx = 0
        self.vely = 0
        self.salud = 249
        self.limite_contador_disparo = 15
        self.imagen_corazones = recortar_imagen('imagenes/sprites/VidaJugador.png', 3, 1)
        self.contador_disparo = random.randint(0, self.limite_contador_disparo)
        self.sonido_disparo = pygame.mixer.Sound('sonidos/efectos_sonido/bola_ignea.wav')
        self.sonido_disparo.set_volume(0.5)
        self.sonido_daño = pygame.mixer.Sound('sonidos/efectos_sonido/daño_jugador.wav')
        self.sonido_daño.set_volume(0.5)
        self.sonido_muerte = pygame.mixer.Sound('sonidos/efectos_sonido/muerte_jugador.wav')

    def update(self):
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.contador_disparo += 1
        self.gravedad(1)
        self.dibujar()

    def gravedad(self, valor_gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += valor_gravedad

    def dibujar(self):
        if self.velx != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador < 30:
                self.contador += 1
            else:
                self.contador = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[self.direccion][self.contador // 11]

    def disparar(self):
        if self.contador_disparo < self.limite_contador_disparo:
            return False
        else:
            self.contador_disparo = 0
            self.sonido_disparo.play()
            return True


    def mover(self, key):
        if key == pygame.K_LEFT:
            self.velx = -self.velocidad
            self.vely = 0
            self.direccion = 0
            self.direccion_x = -1

        if key == pygame.K_RIGHT:
            self.velx = self.velocidad
            self.vely = 0
            self.direccion = 1
            self.direccion_x = 1

        if key == pygame.K_UP and self.saltar == True:
            self.saltar = False
            #self.vely = -12
            self.vely = -16


    def detener(self):
        self.velx = 0
        #self.vely = 0

    def verificar_colision(self, direccion):
        '''if self.rect.bottom > ALTO:
            self.vely = 0'''

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left -10
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right + 10
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top #- 0.1
                        self.vely = 0
                        self.saltar = True
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom #+ 0.1
                        self.vely = 0

class Ocultista(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Ocultista.png', 3, 4)
        self.direccion_sprite = 0
        self.contador_sprite = 0
        self.contador_movimiento = 60
        self.image = self.imagen[self.direccion_sprite][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velocidad = 4
        self.velx = 0
        self.vely = 0
        self.daño = 1
        self.salud = 250
        self.puntaje = 5
        self.sondio_muerte = pygame.mixer.Sound('sonidos/efectos_sonido/muerte_ocultista.wav')

    def update(self):
        self.mover()
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.gravedad(1)
        self.dibujar()
    
    def gravedad(self, valor_gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += valor_gravedad

    def mover(self):
        if self.contador_movimiento > 60:
            direccion_movimiento = random.randint(0,1)
            #Movimiento hacia izquierda
            if direccion_movimiento == 0:
                self.velx = -self.velocidad
                self.direccion_sprite = 1
            #Movimiento hacia derecha
            if direccion_movimiento == 1:
                self.velx = self.velocidad
                self.direccion_sprite = 2

            self.contador_movimiento = 0
        else:
            self.contador_movimiento += 1

    def verificar_colision(self, direccion):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top
                        self.vely = 0
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom
                        self.vely = 0

    def dibujar(self):
        if self.velx != 0 or self.vely != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador_sprite < 30:
                self.contador_sprite += 1
            else:
                self.contador_sprite = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[self.direccion_sprite][self.contador_sprite // 11]

class Arpia(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Arpia.png', 3, 4)
        self.direccion_sprite = 0
        self.contador_sprite = 0
        self.contador_movimiento = 60
        self.image = self.imagen[self.direccion_sprite][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velocidad = 4
        self.velx = 0
        self.vely = 0
        self.daño = 1
        self.salud = 250
        self.puntaje = 5
        self.sondio_muerte = pygame.mixer.Sound('sonidos/efectos_sonido/muerte_ocultista.wav')

    def update(self):
        self.mover()
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.dibujar()

    def mover(self):
        if self.contador_movimiento > 60:
            direccion_movimiento = random.randint(0,3)
            #Movimiento hacia izquierda
            if direccion_movimiento == 0:
                self.velx = -self.velocidad
                self.direccion_sprite = 1
            #Movimiento hacia derecha
            if direccion_movimiento == 1:
                self.velx = self.velocidad
                self.direccion_sprite = 2
            #Movimiento hacia abajo
            if direccion_movimiento == 2:
                self.velx = 0
                self.vely = self.velocidad
                self.direccion_sprite = 0
            #Movimiento hacia arriba
            if direccion_movimiento == 3:
                self.velx = 0
                self.vely = -self.velocidad
                self.direccion_sprite = 3

            self.contador_movimiento = 0
        else:
            self.contador_movimiento += 1

    def verificar_colision(self, direccion):

        '''if self.rect.top < 0:
            self.velx = 0
            self.vely = 0
            self.rect.y = 10'''

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top
                        self.vely = 0
                        self.saltar = True
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom
                        self.vely = 0

    def dibujar(self):
        if self.velx != 0 or self.vely != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador_sprite < 30:
                self.contador_sprite += 1
            else:
                self.contador_sprite = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[self.direccion_sprite][self.contador_sprite // 11]

class Dragon(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Dragon.png', 3, 2)
        self.direccion_sprite = 0
        self.contador_sprite = 0
        self.contador_movimiento = 60
        self.image = self.imagen[0][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velocidad = 4
        self.velx = 0
        self.vely = 0
        self.daño = 1
        self.salud = 249
        self.puntaje = 100
        self.contador_disparo = random.randint(0,10)
        self.sprite_salud = recortar_imagen('imagenes/sprites/VidaDragon.png', 3, 1)
        self.sondio_muerte = pygame.mixer.Sound('sonidos/efectos_sonido/muerte_ocultista.wav')

    def update(self):
        self.mover()
        self.contador_disparo += 1
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.dibujar()

    def disparar(self):
        if self.contador_disparo > 30:
            self.contador_disparo = 0
            return True
        else:
            return False

    def mover(self):
        if self.contador_movimiento > 10:
            direccion_movimiento = random.randint(0,1)
            #Movimiento hacia abajo
            if direccion_movimiento == 0:
                self.velx = 0
                self.vely = self.velocidad
            #Movimiento hacia arriba
            if direccion_movimiento == 1:
                self.velx = 0
                self.vely = -self.velocidad

            self.contador_movimiento = 0
        else:
            self.contador_movimiento += 1

    def verificar_colision(self, direccion):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left - 10
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right + 10
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top - 10
                        self.vely = 0
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom + 10
                        self.vely = 0

    def dibujar(self):
        if self.velx != 0 or self.vely != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador_sprite < 30:
                self.contador_sprite += 1
            else:
                self.contador_sprite = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[0][self.contador_sprite // 11]

class Cobra(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Cobra.png', 3, 4)
        self.direccion_sprite = 0
        self.contador_sprite = 0
        self.contador_movimiento = 60
        self.contador_salto = random.randint(0,80)
        self.image = self.imagen[self.direccion_sprite][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velocidad = 2
        self.velx = 0
        self.vely = 0
        self.daño = 1
        self.saltar = False
        self.puntaje = 5
        self.sondio_muerte = pygame.mixer.Sound('sonidos/efectos_sonido/muerte_ocultista.wav')

    def update(self):
        self.mover()
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.gravedad(1)
        self.dibujar()
    
    def gravedad(self, valor_gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += valor_gravedad

    def mover(self):
        if self.contador_movimiento > 60:
            direccion_movimiento = random.randint(0,1)
            #Movimiento hacia izquierda
            if direccion_movimiento == 0:
                self.velx = -self.velocidad
                self.direccion_sprite = 1
            #Movimiento hacia derecha
            if direccion_movimiento == 1:
                self.velx = self.velocidad
                self.direccion_sprite = 2

            self.contador_movimiento = 0
        else:
            self.contador_movimiento += 1
        
        #Revision de salto
        if self.contador_salto > 80:
            decision = random.randint(0,1)
            if decision == 1:
                self.vely = -12
                self.contador_salto = 0
        else:
            self.contador_salto += 1




    def verificar_colision(self, direccion):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top
                        self.vely = 0
                        self.saltar = True
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom
                        self.vely = 0

    def dibujar(self):
        if self.velx != 0 or self.vely != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador_sprite < 30:
                self.contador_sprite += 1
            else:
                self.contador_sprite = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[self.direccion_sprite][self.contador_sprite // 11]

class Golem(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Golem.png', 3, 2)
        self.direccion_sprite = 0
        self.contador_sprite = 0
        self.contador_movimiento = 60
        self.image = self.imagen[self.direccion_sprite][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velocidad = 4
        self.contador_disparo = random.randint(0,60)
        self.velx = 0
        self.vely = 0
        self.daño = 1
        self.salud = 250
        self.puntaje = 10
        self.sondio_muerte = pygame.mixer.Sound('sonidos/efectos_sonido/muerte_ocultista.wav')

    def update(self):
        self.mover()
        self.contador_disparo += 1
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.gravedad(1)
        self.dibujar()
    
    def gravedad(self, valor_gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += valor_gravedad

    def disparar(self):
        if self.contador_disparo > 120:
            self.contador_disparo = 0
            return True
        else:
            return False

    def mover(self):
        if self.contador_movimiento > 60:
            direccion_movimiento = random.randint(0,1)
            #Movimiento hacia izquierda
            if direccion_movimiento == 0:
                self.velx = -self.velocidad
                self.direccion_sprite = 0
            #Movimiento hacia derecha
            if direccion_movimiento == 1:
                self.velx = self.velocidad
                self.direccion_sprite = 1

            self.contador_movimiento = 0
        else:
            self.contador_movimiento += 1

    def verificar_colision(self, direccion):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top
                        self.vely = 0
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom
                        self.vely = 0

    def dibujar(self):
        if self.velx != 0 or self.vely != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador_sprite < 30:
                self.contador_sprite += 1
            else:
                self.contador_sprite = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[self.direccion_sprite][self.contador_sprite // 11]

class HombreLobo(pygame.sprite.Sprite):
    def __init__(self, pos, ls_bloques_limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Lobo.png', 3, 2)
        self.direccion_sprite = 0
        self.contador_sprite = 0
        self.contador_movimiento = 60
        self.image = self.imagen[self.direccion_sprite][self.contador_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.velocidad = 4
        self.contador_invocacion = random.randint(0,60)
        self.velx = 0
        self.vely = 0
        self.daño = 1
        self.salud = 249
        self.puntaje = 100
        self.sprite_salud = recortar_imagen('imagenes/sprites/VidaHombreLobo.png', 3, 1)
        self.sondio_muerte = pygame.mixer.Sound('sonidos/efectos_sonido/muerte_ocultista.wav')

    def update(self):
        self.mover()
        self.contador_invocacion += 1
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.gravedad(1)
        self.dibujar()
    
    def gravedad(self, valor_gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += valor_gravedad

    def invocar(self):
        if self.contador_invocacion > 80:
            self.contador_invocacion = 0
            return True
        else:
            return False

    def mover(self):
        if self.contador_movimiento > 60:
            direccion_movimiento = random.randint(0,1)
            #Movimiento hacia izquierda
            if direccion_movimiento == 0:
                self.velx = -self.velocidad
                self.direccion_sprite = 0
            #Movimiento hacia derecha
            if direccion_movimiento == 1:
                self.velx = self.velocidad
                self.direccion_sprite = 1

            self.contador_movimiento = 0
        else:
            self.contador_movimiento += 1

    def verificar_colision(self, direccion):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top
                        self.vely = 0
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom
                        self.vely = 0

    def dibujar(self):
        if self.velx != 0 or self.vely != 0:
            #el contador tiene que ser igual a los ticks a lo que va el juego
            if self.contador_sprite < 30:
                self.contador_sprite += 1
            else:
                self.contador_sprite = 0
            #Se divide el contador por 11 para darle una animación mas lenta a la hora de mostrar en pantalla
            self.image = self.imagen[self.direccion_sprite][self.contador_sprite // 11]

class BolaIgnea(pygame.sprite.Sprite):
    daño = 20
    nombre_imagen = 'imagenes/sprites/BolaIgnea.png'

    def __init__(self, pos, direccion_x):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen(BolaIgnea.nombre_imagen, 4, 2)
        self.direccion_x = direccion_x
        self.apuntado = 0
        self.image = self.imagen[1][self.apuntado]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velocidad = 6
        self.velx = 0
        self.daño = BolaIgnea.daño

    def update(self):
        self.mover()
        self.dibujar()

    def mover(self):
        if self.direccion_x == 1:
            self.velx = self.velocidad
            self.apuntado = 0
        if self.direccion_x == -1:
            self.velx = -self.velocidad
            self.apuntado = 1

        self.rect.x+=self.velx


    def dibujar(self):
        self.image = self.imagen[1][self.apuntado]

class BolaIgneaDragon(pygame.sprite.Sprite):
    daño = 10
    nombre_imagen = 'imagenes/sprites/AlientoDragon.png'

    def __init__(self, pos, direccion_x):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen(BolaIgneaDragon.nombre_imagen, 4, 2)
        self.direccion_x = direccion_x
        self.apuntado = -1
        self.image = self.imagen[1][self.apuntado]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velocidad = 6
        self.velx = 0
        self.daño = BolaIgnea.daño

    def update(self):
        self.mover()
        self.dibujar()

    def mover(self):
        if self.direccion_x == 1:
            self.velx = self.velocidad
            self.apuntado = 0
        if self.direccion_x == -1:
            self.velx = -self.velocidad
            self.apuntado = 1

        self.rect.x+=self.velx


    def dibujar(self):
        self.image = self.imagen[1][self.apuntado]

class BolaIgneaGolem(pygame.sprite.Sprite):
    daño = 20
    nombre_imagen = 'imagenes/sprites/BolaIgnea.png'

    def __init__(self, pos, direccion_x):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen(BolaIgneaGolem.nombre_imagen, 4, 2)
        self.direccion_x = direccion_x
        self.apuntado = -1
        self.image = self.imagen[1][self.apuntado]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.velocidad = 6
        self.velx = 0
        self.daño = BolaIgneaGolem.daño

    def update(self):
        self.mover()
        self.dibujar()

    def mover(self):
        if self.direccion_x == 1:
            self.velx = self.velocidad
            self.apuntado = 0
        if self.direccion_x == -1:
            self.velx = -self.velocidad
            self.apuntado = 1

        self.rect.x+=self.velx


    def dibujar(self):
        self.image = self.imagen[1][self.apuntado]

class BloqueLimite(pygame.sprite.Sprite):
    def __init__(self, posicion,  posicion_bloque = [0,0], ruta_imagen = "imagenes/sprites/bloques.jpg"):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen(ruta_imagen, 5, 1)
        self.image = self.imagen[posicion_bloque[0]][posicion_bloque[1]]
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]

    def update(self):
        pass

class Pua(pygame.sprite.Sprite):
    daño = 1
    def __init__(self, posicion,  posicion_bloque = [0,1], ruta_imagen = "imagenes/sprites/PuaAzul.png"):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen(ruta_imagen, 2, 1)
        self.image = self.imagen[posicion_bloque[0]][posicion_bloque[1]]
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]
        self.daño = Pua.daño

    def update(self):
        pass

class ModificadorBolaIgnea(pygame.sprite.Sprite):
    aumento_daño = 20
    nombre_cambio_imagen = 'imagenes/sprites/AlientoDragon.png'
    def __init__(self, posicion, ls_bloques_limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Modificadores.png', 10, 4)
        self.image = self.imagen[2][5]
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.vely = 0
        self.velx = 0

    def gravedad(self, valor_gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += valor_gravedad

    def verificar_colision(self, direccion):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top
                        self.vely = 0
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom
                        self.vely = 0

    def update(self):
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.gravedad(1)

class ModificadorVida(pygame.sprite.Sprite):
    aumento_vida = 50
    def __init__(self, posicion, ls_bloques_limite):
        pygame.sprite.Sprite.__init__(self)
        self.imagen = recortar_imagen('imagenes/sprites/Modificadores.png', 10, 4)
        self.image = self.imagen[0][0]
        self.rect = self.image.get_rect()
        self.rect.x = posicion[0]
        self.rect.y = posicion[1]
        self.ls_bloques_limite = ls_bloques_limite
        self.vely = 0
        self.velx = 0

    def gravedad(self, valor_gravedad):
        if self.vely == 0:
            self.vely = 1
        else:
            self.vely += valor_gravedad

    def verificar_colision(self, direccion):

        ls_colision = pygame.sprite.spritecollide(self, self.ls_bloques_limite, False)

        for bloque in ls_colision:
            # Si la direccion es 0 entonces revisa la colision en x (Horizontal)
            if direccion == 0:
                if self.velx > 0:
                    if self.rect.right > bloque.rect.left:
                        self.rect.right = bloque.rect.left
                        self.velx = 0
                if self.velx < 0:
                    if self.rect.left < bloque.rect.right:
                        self.rect.left = bloque.rect.right
                        self.velx = 0

            #Si la direccion es 1 entonces revisa la colision en y (vertical)
            if direccion == 1:
                if self.vely > 0:
                    if self.rect.bottom > bloque.rect.top:
                        self.rect.bottom = bloque.rect.top
                        self.vely = 0
                if self.vely < 0:
                    if self.rect.top < bloque.rect.bottom:
                        self.rect.top = bloque.rect.bottom
                        self.vely = 0

    def update(self):
        self.rect.x+=self.velx
        self.verificar_colision(0)
        self.rect.y+=self.vely
        self.verificar_colision(1)
        self.gravedad(1)

class Fondo(pygame.sprite.Sprite):
    def __init__(self, pos, nombre_imagen):
        pygame.sprite.Sprite.__init__(self)
        self.posx = pos[0]
        self.posy = pos[1]
        self.velx = 0
        self.vely = 0
        self.imagen = pygame.image.load(nombre_imagen)
        self.rect = self.imagen.get_rect()
        self.ancho = self.rect[2]
        self.alto = self.rect[3]
        self.limite_derecho = ANCHO - BORDE_MAPA
        self.limite_izquierdo = BORDE_MAPA
        self.limite_superior = BORDE_MAPA
        self.limite_inferior = ALTO - BORDE_MAPA

    def mover(self):
        self.posx += self.velx
        self.posy += self.vely

    def update(self):
        self.mover()

def cargar_mapa(ruta_json):
    ls_bloques_limite = pygame.sprite.Group()
    informacion_mapa = cargar_json(ruta_json)
    diccionario_mapa_colision = informacion_mapa['layers'][0]
    ls_mapa_colision = diccionario_mapa_colision['data']
    limite_fila = diccionario_mapa_colision['height']
    limite_columna = diccionario_mapa_colision['width']
    contador_bloque = 0

    for fila in range(limite_fila):
        for columna in range(limite_columna):
            if ls_mapa_colision[contador_bloque] == 1:
                bloque = BloqueLimite([columna*32, fila*32])
                ls_bloques_limite.add(bloque)
            contador_bloque += 1

    return ls_bloques_limite

def cargar_mapa_nivel_2(ruta_json):
    ls_bloques_limite = pygame.sprite.Group()
    informacion_mapa = cargar_json(ruta_json)
    diccionario_mapa_colision = informacion_mapa['layers'][0]
    ls_mapa_colision = diccionario_mapa_colision['data']
    limite_fila = diccionario_mapa_colision['height']
    limite_columna = diccionario_mapa_colision['width']
    contador_bloque = 0

    for fila in range(limite_fila):
        for columna in range(limite_columna):
            if ls_mapa_colision[contador_bloque] == 5:
                bloque = BloqueLimite([columna*32, fila*32], [0,4])
                ls_bloques_limite.add(bloque)
            contador_bloque += 1

    return ls_bloques_limite

def cargar_enemigos(ruta_json, ls_bloques_limite):
    diccionario_grupos = {}
    ocultistas = pygame.sprite.Group()
    cobras = pygame.sprite.Group()
    arpias = pygame.sprite.Group()
    dragones = pygame.sprite.Group()
    hombres_lobo = pygame.sprite.Group()
    puas = pygame.sprite.Group()

    informacion_mapa = cargar_json(ruta_json)
    diccionario_mapa_colision = informacion_mapa['layers'][0]
    ls_mapa_colision = diccionario_mapa_colision['data']
    limite_fila = diccionario_mapa_colision['height']
    limite_columna = diccionario_mapa_colision['width']
    contador_bloque = 0

    for fila in range(limite_fila):
        for columna in range(limite_columna):
            # el 19 se debe a que en la informacion con la que queda cargado el mapa es justo el que representa
            #a los ocultistas
            pos = [columna*32, fila*32]
            if ls_mapa_colision[contador_bloque] == 6:
                ocultista = Ocultista(pos, ls_bloques_limite)
                ocultistas.add(ocultista)
            if ls_mapa_colision[contador_bloque] == 12:
                arpia = Arpia(pos, ls_bloques_limite)
                arpias.add(arpia)
            if ls_mapa_colision[contador_bloque] == 19:
                dragon = Dragon(pos, ls_bloques_limite)
                dragones.add(dragon)
            if ls_mapa_colision[contador_bloque] == 26  :
                pua = Pua(pos)
                puas.add(pua)
            contador_bloque += 1

    diccionario_grupos['ocultistas'] = ocultistas
    diccionario_grupos['arpias'] = arpias
    diccionario_grupos['dragones'] = dragones
    diccionario_grupos['puas'] = puas
    return diccionario_grupos

def cargar_enemigos_nivel_2(ruta_json, ls_bloques_limite):
    diccionario_grupos = {}
    cobras = pygame.sprite.Group()
    golems = pygame.sprite.Group()
    hombres_lobo = pygame.sprite.Group()
    puas = pygame.sprite.Group()

    informacion_mapa = cargar_json(ruta_json)
    diccionario_mapa_colision = informacion_mapa['layers'][0]
    ls_mapa_colision = diccionario_mapa_colision['data']
    limite_fila = diccionario_mapa_colision['height']
    limite_columna = diccionario_mapa_colision['width']
    contador_bloque = 0

    for fila in range(limite_fila):
        for columna in range(limite_columna):
            # el 19 se debe a que en la informacion con la que queda cargado el mapa es justo el que representa
            #a los ocultistas
            pos = [columna*32, fila*32]
            if ls_mapa_colision[contador_bloque] == 12:
                cobra = Cobra(pos, ls_bloques_limite)
                cobras.add(cobra)
            if ls_mapa_colision[contador_bloque] == 6  :
                golem = Golem(pos, ls_bloques_limite)
                golems.add(golem)
            if ls_mapa_colision[contador_bloque] == 18  :
                hombre_lobo = HombreLobo(pos, ls_bloques_limite)
                hombres_lobo.add(hombre_lobo)
            if ls_mapa_colision[contador_bloque] == 25  :
                pua = Pua(pos, [0,1], 'imagenes/sprites/PuaRoja.png')
                puas.add(pua)
            contador_bloque += 1

    diccionario_grupos['cobras'] = cobras
    diccionario_grupos['golems'] = golems
    diccionario_grupos['hombres_lobo'] = hombres_lobo
    diccionario_grupos['puas'] = puas
    return diccionario_grupos

def mostrar_info(pantalla, fuente, texto, color, dimensiones, pos):
    letra = pygame.font.Font(fuente, dimensiones)
    superficie = letra.render(texto, True, color)
    rect = superficie.get_rect()
    pantalla.blit(superficie, pos)

def mostrar_info_salud(pantalla, matriz_sprites, salud_jugador, pos):
    cantidad_corazones = (salud_jugador + 50) // 50
    posx = pos[0]
    posy = pos[1]

    for i in range(cantidad_corazones):
        pantalla.blit(matriz_sprites[0][0], [posx, posy])
        posx += 32

if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO,ALTO])
    reloj = pygame.time.Clock()

    '''Banderas'''
    fin = False
    fin_nivel1 = False
    fin_nivel2 = True
    fin_pantalla_inicio = False
    fin_pantalla_gameover = True
    fin_pantalla_victoria = True
    fin_pantalla_pausa = False
    recoger_modificadres = False
    '''--------'''

    '''Musica'''
    pygame.mixer.music.load('sonidos/musica_fondo/sonido_fondo.wav')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    '''------'''


    '''Pantalla inicio'''
    fondo_inicio = pygame.image.load('imagenes/fondo/fondo_inicio.png')
    

    while (not fin) and (not fin_pantalla_inicio):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fin_pantalla_inicio = True
        pantalla.fill(NEGRO)
        pantalla.blit(fondo_inicio, [0,0])
        info_inicio = '(Presiona la tecla espacio...)'
        mostrar_info(pantalla, None, info_inicio, BLANCO, 30, [250, 550])

        pygame.display.flip()

    '''---------------'''

    '''Nivel 1'''
    '''Grupos objetos'''
    bloques_limite = cargar_mapa('tiled/nivel_1/mapa_colision.json')
    jugadores = pygame.sprite.Group()
    bolas_igneas = pygame.sprite.Group()
    bolas_igneas_dragon = pygame.sprite.Group()
    modificadores_vida = pygame.sprite.Group()
    modificadores_bola_ignea = pygame.sprite.Group()

    diccionario_grupos = cargar_enemigos('tiled/nivel_1/mapa_colision.json', bloques_limite)
    ocultistas = diccionario_grupos['ocultistas']
    arpias = diccionario_grupos['arpias']
    dragones = diccionario_grupos['dragones']
    puas = diccionario_grupos['puas']

    '''Instancias de objetos y agragado a grupos'''
    fondo = Fondo([-320, -320], 'imagenes/fondo/Cielo.jpg')
    jugador = Jugador([600,0], bloques_limite)
    jugadores.add(jugador)

    '''-----------------------------------------'''

    while (not fin) and (not fin_nivel1):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                jugador.mover(event.key)
                if event.key == pygame.K_SPACE and jugador.disparar() and jugador.salud > 0:
                    posicion = [jugador.rect.x, jugador.rect.y]
                    direccion_x = jugador.direccion_x
                    bola_ignea = BolaIgnea(posicion, direccion_x)
                    bolas_igneas.add(bola_ignea)
                    print(f'Projectiles en pantalla: {len(bolas_igneas)}')
                
                #Pantalla Pausa
                if event.key == pygame.K_p:
                    fondo_pausa = pygame.image.load('imagenes/fondo/fondo_pause.png')
                    while (not fin_pantalla_pausa):
                        #Gestion de eventos
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                fin = True
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    fin_pantalla_pausa = True
                        pantalla.fill(NEGRO)
                        pantalla.blit(fondo_pausa, [0,0])
                        info_inicio = '(Presiona la tecla espacio...)'
                        mostrar_info(pantalla, None, info_inicio, BLANCO, 30, [250, 550])
                        pygame.display.flip()
                    fin_pantalla_pausa = False
                        
            if event.type == pygame.KEYUP:
                if event.key != pygame.K_UP and event.key != pygame.K_SPACE:
                    jugador.detener()

        
        '''Jugador'''
        for jugador in jugadores:
            #Revision de muerte de jugador
            if jugador.salud < 0:
                #pygame.mixer.music.pause()
                jugador.sonido_daño.stop()
                jugador.sonido_disparo.stop()
                jugador.sonido_muerte.play()
                fin_nivel1 = True
                fin_pantalla_gameover = False
                jugadores.remove(jugador)

            #Revision de colision contra bolas de dragon
            ls_colision = pygame.sprite.spritecollide(jugador, bolas_igneas_dragon, True)
            if(len(ls_colision) > 0):
                jugador.salud -= BolaIgnea.daño
                jugador.sonido_daño.play()
                print(f'Salud del jugador: {jugador.salud}')

            #Revision de colisicion contra las puas
            ls_colision = pygame.sprite.spritecollide(jugador, puas, False)
            if(len(ls_colision) > 0):
                jugador.salud -= Pua.daño
                jugador.sonido_daño.play()
                print(f'Salud del jugador: {jugador.salud}')

            #Revision de colision contra el modificador de vida
            ls_colision = pygame.sprite.spritecollide(jugador, modificadores_vida, True)
            if(len(ls_colision) > 0):
                jugador.salud = 249
                print(f'Salud del jugador: {jugador.salud}')

            #Revision de colision contra el modificador de bola ignea
            ls_colision = pygame.sprite.spritecollide(jugador, modificadores_bola_ignea, True)
            if(len(ls_colision) > 0):
                BolaIgnea.daño += 10
                BolaIgnea.nombre_imagen = 'imagenes/sprites/AlientoDragon.png' 

            if(len(modificadores_bola_ignea) == 0 and len(modificadores_vida) == 0 and recoger_modificadres == True):
                fin_nivel1 = True
                fin_nivel2 = False

            #Revision de vacio
            if jugador.rect.y > fondo.limite_inferior:
                jugador.sonido_daño.stop()
                jugador.sonido_disparo.stop()
                jugador.sonido_muerte.play()
                fin_nivel1 = True
                fin_pantalla_gameover = False
                jugadores.remove(jugador)

        '''-------'''

        '''Bolas igneas'''
        for bola_ignea in bolas_igneas:
            #Revision borde superior
            if bola_ignea.rect.bottom < 0:
                bolas_igneas.remove(bola_ignea)
            #Revision borde inferior
            if bola_ignea.rect.top > ALTO:
                bolas_igneas.remove(bola_ignea)
            #Revision borde derecho
            if bola_ignea.rect.left > ANCHO:
                bolas_igneas.remove(bola_ignea)
            #Revision borde izquierdo
            if bola_ignea.rect.right < 0:
                bolas_igneas.remove(bola_ignea)

            #Revision de colision con un bloque
            ls_colision = pygame.sprite.spritecollide(bola_ignea, bloques_limite, False)
            if(len(ls_colision) > 0):
                bolas_igneas.remove(bola_ignea)

            #Revision de colision con las bolas igneas del dragon
            ls_colision = pygame.sprite.spritecollide(bola_ignea, bolas_igneas_dragon, True)
            if(len(ls_colision) > 0):
                bolas_igneas.remove(bola_ignea)
        '''------------'''

        '''Ocultistas'''
        for ocultista in ocultistas:

            #Revisar si el ocultista colisiona con el jugador
            ls_colision = pygame.sprite.spritecollide(ocultista, jugadores, False)
            if(len(ls_colision) > 0):
                jugador.salud -= ocultista.daño
                jugador.sonido_daño.play()
                print(f'Salud jugador: {jugador.salud}')

            #Revision de impacto de un bola_ignea
            ls_colision = pygame.sprite.spritecollide(ocultista, bolas_igneas, True)
            if(len(ls_colision) > 0):
                jugador.puntaje += ocultista.puntaje
                print(f'El puntaje del jugador es: {jugador.puntaje}')
                ocultista.sondio_muerte.play()
                ocultistas.remove(ocultista)
        '''--------'''

        '''Arpias'''
        for arpia in arpias:

            #Revisar si la cobra colisiona con el jugador
            ls_colision = pygame.sprite.spritecollide(arpia, jugadores, False)
            if(len(ls_colision) > 0):
                jugador.salud -= arpia.daño
                jugador.sonido_daño.play()
                print(f'Salud jugador: {jugador.salud}')

            #Revision de impacto de un bola_ignea
            ls_colision = pygame.sprite.spritecollide(arpia, bolas_igneas, True)
            if(len(ls_colision) > 0):
                jugador.puntaje += arpia.puntaje
                print(f'El puntaje del jugador es: {jugador.puntaje}')
                arpia.sondio_muerte.play()
                arpias.remove(arpia)
        '''--------'''

        '''Dragon'''
        for dragon in dragones:

            #Revisar si la cobra colisiona con el jugador
            ls_colision = pygame.sprite.spritecollide(dragon, jugadores, False)
            if(len(ls_colision) > 0):
                jugador.salud -= dragon.daño
                jugador.sonido_daño.play()
                print(f'Salud jugador: {jugador.salud}')

            #Revision de impacto de un bola_ignea
            ls_colision = pygame.sprite.spritecollide(dragon, bolas_igneas, True)
            if(len(ls_colision) > 0):
                dragon.salud -= BolaIgnea.daño
                print(f'La salud del dragon es: {dragon.salud}')
                dragon.sondio_muerte.play()
            
            #Revision de disparo de bola ignea
            if dragon.disparar():
                bola_ignea_dragon = BolaIgneaDragon([dragon.rect.left, dragon.rect.centery], -1)
                bolas_igneas_dragon.add(bola_ignea_dragon)

            #Revision de muerte del dragon
            if dragon.salud < 0:
                recoger_modificadres = True
                modificador_vida = ModificadorVida([dragon.rect.centerx + 10, dragon.rect.centery], bloques_limite)
                modificadores_vida.add(modificador_vida)
                modificador_bola_ignea = ModificadorBolaIgnea([dragon.rect.centerx - 10, dragon.rect.centery], bloques_limite)
                modificadores_bola_ignea.add(modificador_bola_ignea)
                jugador.puntaje += dragon.puntaje
                dragones.remove(dragon)
                
        '''--------'''

        '''Bolas igeneas dragon'''
        for bola_ignea in bolas_igneas_dragon:
            #Revision borde superior
            if bola_ignea.rect.bottom < 0:
                bolas_igneas_dragon.remove(bola_ignea)
            #Revision borde inferior
            if bola_ignea.rect.top > ALTO:
                bolas_igneas_dragon.remove(bola_ignea)
            #Revision borde derecho
            if bola_ignea.rect.left > ANCHO:
                bolas_igneas_dragon.remove(bola_ignea)
            #Revision borde izquierdo
            if bola_ignea.rect.right < 0:
                bolas_igneas_dragon.remove(bola_ignea)

            #Revision de colision con un bloque
            ls_colision = pygame.sprite.spritecollide(bola_ignea, bloques_limite, False)
            if(len(ls_colision) > 0):
                bolas_igneas_dragon.remove(bola_ignea)
                print(f'Bolas de dragon: {len(bolas_igneas_dragon)}')
        '''--------------------'''



        '''Gestion fondo'''
        #Gestion borde derecho
        if jugador.rect.right > fondo.limite_derecho:
            jugador.rect.right = fondo.limite_derecho
            fondo.posx -= jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.x -= jugador.velocidad
            #Reubicacion ocultistas
            for ocultista in ocultistas:
                ocultista.rect.x -= jugador.velocidad
            #Reubicacion arpias
            for arpia in arpias:
                arpia.rect.x -= jugador.velocidad
            #Reubicacion bolas igneas jugador
            for bola_ignea in bolas_igneas:
                bola_ignea.rect.x -= jugador.velocidad
            #Reubicacion bolas igneas dragon
            for bola_ignea in bolas_igneas_dragon:
                bola_ignea.rect.x -= jugador.velocidad
            #Reubicacion dragon
            for dragon in dragones:
                dragon.rect.x -= jugador.velocidad
            #Reubicacion modificadores de vida
            for modificador_vida in modificadores_vida:
                modificador_vida.rect.x -= jugador.velocidad
            #Reubicacion modificadores de bola ignea
            for modificador_bola_ignea in modificadores_bola_ignea:
                modificador_bola_ignea.rect.x -= jugador.velocidad
            #Reubicacion puas
            for pua in puas:
                pua.rect.x -= jugador.velocidad

            
        #Gestion borde izquierdo
        if jugador.rect.left < fondo.limite_izquierdo:
            jugador.rect.left = fondo.limite_izquierdo
            fondo.posx += jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.x += jugador.velocidad
            #Reubicacion ocultistas
            for ocultista in ocultistas:
                ocultista.rect.x += jugador.velocidad
            #Reubicacion arpias
            for arpia in arpias:
                arpia.rect.x += jugador.velocidad
            #Reubicacion bolas igneas jugador
            for bola_ignea in bolas_igneas:
                bola_ignea.rect.x += jugador.velocidad
            #Reubicacion bolas igneas dragon
            for bola_ignea in bolas_igneas_dragon:
                bola_ignea.rect.x += jugador.velocidad 
            #Reubicacion dragon
            for dragon in dragones:
                dragon.rect.x += jugador.velocidad   
            #Reubicacion modificadores de vida
            for modificador_vida in modificadores_vida:
                modificador_vida.rect.x += jugador.velocidad
            #Reubicacion modificadores de bola ignea
            for modificador_bola_ignea in modificadores_bola_ignea:
                modificador_bola_ignea.rect.x += jugador.velocidad
            #Reubicacion puas
            for pua in puas:
                pua.rect.x += jugador.velocidad
            

        #Gestion border superior
        if jugador.rect.top < fondo.limite_superior:
            jugador.rect.top = fondo.limite_superior
            fondo.posy += jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.y += jugador.velocidad
            #Reubicacion ocultistas
            for ocultista in ocultistas:
                ocultista.rect.y += jugador.velocidad
            #Reubicacion arpias
            for arpia in arpias:
                arpia.rect.y += jugador.velocidad
            #Reubicacion bolas igneas jugador
            for bola_ignea in bolas_igneas:
                bola_ignea.rect.y += jugador.velocidad
            #Reubicacion bolas igneas dragon
            for bola_ignea in bolas_igneas_dragon:
                bola_ignea.rect.y += jugador.velocidad
            #Reubicacion dragon
            for dragon in dragones:
                dragon.rect.y += jugador.velocidad
            #Reubicacion modificadores de vida
            for modificador_vida in modificadores_vida:
                modificador_vida.rect.y += jugador.velocidad
            #Reubicacion modificadores de bola ignea
            for modificador_bola_ignea in modificadores_bola_ignea:
                modificador_bola_ignea.rect.y += jugador.velocidad
            #Reubicacion puas
            for pua in puas:
                pua.rect.y += jugador.velocidad

        #Gestrion borde inferior
        if jugador.rect.bottom > fondo.limite_inferior:
            jugador.rect.bottom = fondo.limite_inferior
            fondo.posy -= jugador.vely
           #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.y -= jugador.vely
            #Reubicacion ocultistas
            for ocultista in ocultistas:
                ocultista.rect.y -= jugador.vely
            #Reubicacion arpias
            for arpia in arpias:
                arpia.rect.y -= jugador.vely
            #Reubicacion bolas igneas jugador
            for bola_ignea in bolas_igneas_dragon:
                bola_ignea.rect.y -= jugador.vely
            #Reubicacion bolas igneas dragon
            for bola_ignea in bolas_igneas:
                bola_ignea.rect.y -= jugador.vely
            #Reubicacion dragon
            for dragon in dragones:
                dragon.rect.y -= jugador.vely
            #Reubicacion modificadores de vida
            for modificador_vida in modificadores_vida:
                modificador_vida.rect.y -= jugador.vely
                #Reubicacion modificadores de bola ignea
            for modificador_bola_ignea in modificadores_bola_ignea:
                modificador_bola_ignea.rect.y -= jugador.vely
            #Reubicacion puas
            for pua in puas:
                pua.rect.y -= jugador.vely

        '''-------------'''
        

        pantalla.fill(NEGRO)
        '''Actualizacion de grupos'''
        bloques_limite.update()
        jugadores.update()
        bolas_igneas.update()
        ocultistas.update()
        arpias.update()
        dragones.update()
        bolas_igneas_dragon.update()
        modificadores_vida.update()
        modificadores_bola_ignea.update()
        puas.update()
        '''-----------------------'''

        '''Digujado de grupos'''
        pantalla.blit(fondo.imagen, [fondo.posx, fondo.posy])
        bloques_limite.draw(pantalla)
        jugadores.draw(pantalla)
        bolas_igneas.draw(pantalla)
        ocultistas.draw(pantalla)
        arpias.draw(pantalla)
        dragones.draw(pantalla)
        bolas_igneas_dragon.draw(pantalla)
        modificadores_vida.draw(pantalla)
        modificadores_bola_ignea.draw(pantalla)
        puas.draw(pantalla)
        '''------------------'''

        '''Refresco pantalla'''
        #Muestra los corazones del dragon
        for dragon in dragones:   
            posicion_salud_dragon = [dragon.rect.left - 30, dragon.rect.top - 30]
            mostrar_info_salud(pantalla, dragon.sprite_salud, dragon.salud, posicion_salud_dragon)
        info_puntaje_jugador = 'Puntaje: ' +  str(jugador.puntaje)
        mostrar_info(pantalla, None, info_puntaje_jugador, AZUL, 44, [600,20])
        mostrar_info_salud(pantalla, jugador.imagen_corazones, jugador.salud, [50,20])
        info_salud_jugador = 'Salud: ' +  str(jugador.salud + 1)
        mostrar_info(pantalla, None, info_salud_jugador, AZUL, 30, [55,70])
        pygame.display.flip()
        reloj.tick(30)
        '''-----------------'''

    ocultistas.empty()
    arpias.empty()
    bolas_igneas.empty()
    bloques_limite.empty()
    bolas_igneas_dragon.empty()
    modificadores_vida.empty()
    modificadores_bola_ignea.empty()
    dragones.empty()
    puas.empty()
    '''-------'''

    '''Nivel 2'''
    '''Grupos objetos'''
    bloques_limite = cargar_mapa_nivel_2('tiled/nivel_2/mapa_colision.json')
    #jugadores = pygame.sprite.Group()
    bolas_igneas = pygame.sprite.Group()
    bolas_igneas_golem = pygame.sprite.Group()
    cobras_hombre_lobo = pygame.sprite.Group()

    diccionario_grupos = {}
    diccionario_grupos = cargar_enemigos_nivel_2('tiled/nivel_2/mapa_colision.json', bloques_limite)
    cobras = diccionario_grupos['cobras']
    golems = diccionario_grupos['golems']
    hombres_lobo = diccionario_grupos['hombres_lobo']
    puas = diccionario_grupos['puas']

    '''Instancias de objetos y agragado a grupos'''
    fondo = Fondo([-320,-320], 'imagenes/fondo/Castillo.jpg')
    jugador.rect.x, jugador.rect.y = 0,200
    jugador.ls_bloques_limite = bloques_limite

    '''-----------------------------------------'''

    while (not fin) and (not fin_nivel2):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
            if event.type == pygame.KEYDOWN:
                jugador.mover(event.key)
                if event.key == pygame.K_SPACE and jugador.disparar() and jugador.salud > 0:
                    posicion = [jugador.rect.x, jugador.rect.y]
                    direccion_x = jugador.direccion_x
                    bola_ignea = BolaIgnea(posicion, direccion_x)
                    bolas_igneas.add(bola_ignea)
                    print(f'Projectiles en pantalla: {len(bolas_igneas)}')
                
                #Pantalla Pausa
                if event.key == pygame.K_p:
                    fondo_pausa = pygame.image.load('imagenes/fondo/fondo_pause.png')
                    while (not fin_pantalla_pausa):
                        #Gestion de eventos
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                fin = True
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE:
                                    fin_pantalla_pausa = True
                        pantalla.fill(NEGRO)
                        pantalla.blit(fondo_pausa, [0,0])
                        info_inicio = '(Presiona la tecla espacio...)'
                        mostrar_info(pantalla, None, info_inicio, BLANCO, 30, [250, 550])
                        pygame.display.flip()
                    fin_pantalla_pausa = False
                        
            if event.type == pygame.KEYUP:
                if event.key != pygame.K_UP and event.key != pygame.K_SPACE:
                    jugador.detener()

        
        '''Jugador'''
        for jugador in jugadores:
            #Revision de muerte de jugador
            if jugador.salud < 0:
                #pygame.mixer.music.pause()
                jugador.sonido_daño.stop()
                jugador.sonido_disparo.stop()
                jugador.sonido_muerte.play()
                fin_nivel2 = True
                fin_pantalla_gameover = False
                jugadores.remove(jugador)

            #Revision de colision contra bolas de golem
            ls_colision = pygame.sprite.spritecollide(jugador, bolas_igneas_golem, True)
            if(len(ls_colision) > 0):
                jugador.salud -= BolaIgneaGolem.daño
                jugador.sonido_daño.play()
                print(f'Salud del jugador: {jugador.salud}')
            
            #Revision de colision contra puas
            ls_colision = pygame.sprite.spritecollide(jugador, puas, False)
            if(len(ls_colision) > 0):
                jugador.salud -= Pua.daño
                jugador.sonido_daño.play()
                print(f'Salud del jugador: {jugador.salud}')

            #Revision de vacio
            if jugador.rect.y > fondo.limite_inferior:
                fin_nivel2 = True
                fin_pantalla_gameover = False
                jugador.sonido_daño.stop()
                jugador.sonido_disparo.stop()
                jugador.sonido_muerte.play()

                jugadores.remove(jugador)

        '''-------'''

        '''Bolas igneas'''
        for bola_ignea in bolas_igneas:
            #Revision borde superior
            if bola_ignea.rect.bottom < 0:
                bolas_igneas.remove(bola_ignea)
            #Revision borde inferior
            if bola_ignea.rect.top > ALTO:
                bolas_igneas.remove(bola_ignea)
            #Revision borde derecho
            if bola_ignea.rect.left > ANCHO:
                bolas_igneas.remove(bola_ignea)
            #Revision borde izquierdo
            if bola_ignea.rect.right < 0:
                bolas_igneas.remove(bola_ignea)

            #Revision de colision con un bloque
            ls_colision = pygame.sprite.spritecollide(bola_ignea, bloques_limite, False)
            if(len(ls_colision) > 0):
                bolas_igneas.remove(bola_ignea)

            #Revision de colision con las bolas igneas del golem
            ls_colision = pygame.sprite.spritecollide(bola_ignea, bolas_igneas_golem, True)
            if(len(ls_colision) > 0):
                bolas_igneas.remove(bola_ignea)
        '''------------'''

        '''golems'''
        for golem in golems:

            #Revisar si el golem colisiona con el jugador
            ls_colision = pygame.sprite.spritecollide(golem, jugadores, False)
            if(len(ls_colision) > 0):
                jugador.salud -= golem.daño
                jugador.sonido_daño.play()
                print(f'Salud jugador: {jugador.salud}')

            #Revision de impacto de un bola_ignea
            ls_colision = pygame.sprite.spritecollide(golem, bolas_igneas, True)
            if(len(ls_colision) > 0):
                jugador.puntaje += golem.puntaje
                print(f'El puntaje del jugador es: {jugador.puntaje}')
                golem.sondio_muerte.play()
                golems.remove(golem)

            if golem.disparar():
                pos_bola_ignea = [golem.rect.x, golem.rect.y]
                if golem.velx > 0:
                    direccion = 1
                else: 
                    direccion = -1

                bola_ignea_golem = BolaIgneaGolem(pos_bola_ignea, direccion)
                bolas_igneas_golem.add(bola_ignea_golem)
        '''--------'''

        '''Bolas igeneas golem'''
        for bola_ignea in bolas_igneas_golem:
            #Revision borde superior
            if bola_ignea.rect.bottom < 0:
                bolas_igneas_golem.remove(bola_ignea)
            #Revision borde inferior
            if bola_ignea.rect.top > ALTO:
                bolas_igneas_golem.remove(bola_ignea)
            #Revision borde derecho
            if bola_ignea.rect.left > ANCHO:
                bolas_igneas_golem.remove(bola_ignea)
            #Revision borde izquierdo
            if bola_ignea.rect.right < 0:
                bolas_igneas_golem.remove(bola_ignea)

            #Revision de colision con un bloque
            ls_colision = pygame.sprite.spritecollide(bola_ignea, bloques_limite, False)
            if(len(ls_colision) > 0):
                bolas_igneas_golem.remove(bola_ignea)
                print(f'Bolas de golem: {len(bolas_igneas_golem)}')
        '''--------------------'''

        '''Cobras'''
        for cobra in cobras:

            #Revisar si la cobra colisiona con el jugador
            ls_colision = pygame.sprite.spritecollide(cobra, jugadores, False)
            if(len(ls_colision) > 0):
                jugador.salud -= cobra.daño
                jugador.sonido_daño.play()
                print(f'Salud jugador: {jugador.salud}')

            #Revision de impacto de un bola_ignea
            ls_colision = pygame.sprite.spritecollide(cobra, bolas_igneas, True)
            if(len(ls_colision) > 0):
                jugador.puntaje += cobra.puntaje
                print(f'El puntaje del jugador es: {jugador.puntaje}')
                cobra.sondio_muerte.play()
                cobras.remove(cobra)
        '''--------'''

        '''Cobras hombre lobo'''
        for cobra in cobras_hombre_lobo:

            #Revisar si la cobra colisiona con el jugador
            ls_colision = pygame.sprite.spritecollide(cobra, jugadores, False)
            if(len(ls_colision) > 0):
                jugador.salud -= cobra.daño
                jugador.sonido_daño.play()
                print(f'Salud jugador: {jugador.salud}')

            #Revision de impacto de un bola_ignea
            ls_colision = pygame.sprite.spritecollide(cobra, bolas_igneas, True)
            if(len(ls_colision) > 0):
                jugador.puntaje += cobra.puntaje
                print(f'El puntaje del jugador es: {jugador.puntaje}')
                cobra.sondio_muerte.play()
                cobras_hombre_lobo.remove(cobra)
        '''--------'''

        '''Hombre lobo'''
        for hombre_lobo in hombres_lobo:

            #Revisar si la cobra colisiona con el jugador
            ls_colision = pygame.sprite.spritecollide(hombre_lobo, jugadores, False)
            if(len(ls_colision) > 0):
                jugador.salud -= hombre_lobo.daño
                jugador.sonido_daño.play()
                print(f'Salud jugador: {jugador.salud}')

            #Revision de impacto de un bola_ignea
            ls_colision = pygame.sprite.spritecollide(hombre_lobo, bolas_igneas, True)
            if(len(ls_colision) > 0):
                hombre_lobo.salud -= BolaIgnea.daño
                print(f'La salud del hombre lobo es: {hombre_lobo.salud}')
                hombre_lobo.sondio_muerte.play()
            
            #Revision de invocacion de cobras
            if (len(cobras_hombre_lobo) < 5):
                if hombre_lobo.invocar():
                    cobra = Cobra([hombre_lobo.rect.x, hombre_lobo.rect.y], bloques_limite)
                    cobras_hombre_lobo.add(cobra)

            #Revision de muerte del dragon
            if hombre_lobo.salud < 0:
                jugador.puntaje += hombre_lobo.puntaje
                fin_pantalla_victoria = False
                fin_nivel2 = True
                hombres_lobo.remove(hombre_lobo)
                
        '''--------'''



        '''Gestion fondo'''
        #Gestion borde derecho
        if jugador.rect.right > fondo.limite_derecho:
            jugador.rect.right = fondo.limite_derecho
            fondo.posx -= jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.x -= jugador.velocidad
            #Reubicacion golem
            for golem in golems:
                golem.rect.x -= jugador.velocidad
            #Reubicacion cobra
            for cobra in cobras:
                cobra.rect.x -= jugador.velocidad
            #Reubicacion cobra hombre lobo
            for cobra in cobras_hombre_lobo:
                cobra.rect.x -= jugador.velocidad
            #Reubicacion bolas igneas jugador
            for bola_ignea in bolas_igneas:
                bola_ignea.rect.x -= jugador.velocidad
            #Reubicacion bolas igneas dragon
            for bola_ignea in bolas_igneas_golem:
                bola_ignea.rect.x -= jugador.velocidad
            #Reubicacion hombre lobo
            for hombre_lobo in hombres_lobo:
                hombre_lobo.rect.x -= jugador.velocidad
            #Reubicacion puas
            for pua in puas:
                pua.rect.x -= jugador.velocidad

            
        #Gestion borde izquierdo
        if jugador.rect.left < fondo.limite_izquierdo:
            jugador.rect.left = fondo.limite_izquierdo
            fondo.posx += jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.x += jugador.velocidad
            #Reubicacion golem
            for golem in golems:
                golem.rect.x += jugador.velocidad
            #Reubicacion cobra
            for cobra in cobras:
                cobra.rect.x += jugador.velocidad
            #Reubicacion cobra hombre lobo
            for cobra in cobras_hombre_lobo:
                cobra.rect.x += jugador.velocidad
            #Reubicacion bolas igneas jugador
            for bola_ignea in bolas_igneas:
                bola_ignea.rect.x += jugador.velocidad
            #Reubicacion bolas igneas dragon
            for bola_ignea in bolas_igneas_golem:
                bola_ignea.rect.x += jugador.velocidad
            #Reubicacion hombre lobo
            for hombre_lobo in hombres_lobo:
                hombre_lobo.rect.x += jugador.velocidad   
            #Reubicacion puas
            for pua in puas:
                pua.rect.x += jugador.velocidad


        #Gestion border superior
        if jugador.rect.top < fondo.limite_superior:
            jugador.rect.top = fondo.limite_superior
            fondo.posy += jugador.velocidad
            #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.y += jugador.velocidad
            #Reubicacion golem
            for golem in golems:
                golem.rect.y += jugador.velocidad
            #Reubicacion cobra
            for cobra in cobras:
                cobra.rect.y += jugador.velocidad
            #Reubicacion cobra hombre lobo
            for cobra in cobras_hombre_lobo:
                cobra.rect.y += jugador.velocidad
            #Reubicacion bolas igneas jugador
            for bola_ignea in bolas_igneas:
                bola_ignea.rect.y += jugador.velocidad
            #Reubicacion bolas igneas dragon
            for bola_ignea in bolas_igneas_golem:
                bola_ignea.rect.y += jugador.velocidad
            #Reubicacion hombre lobo
            for hombre_lobo in hombres_lobo:
                hombre_lobo.rect.y += jugador.velocidad
            #Reubicacion puas
            for pua in puas:
                pua.rect.y += jugador.velocidad

        #Gestrion borde inferior
        if jugador.rect.bottom > fondo.limite_inferior:
            jugador.rect.bottom = fondo.limite_inferior
            fondo.posy -= jugador.vely
           #Reubicacion bloques
            for bloque in bloques_limite:
                bloque.rect.y -= jugador.vely
            #Reubicacion golem
            for golem in golems:
                golem.rect.y -= jugador.vely
            #Reubicacion cobra
            for cobra in cobras:
                cobra.rect.y -= jugador.vely
            #Reubicacion cobra hombre lobo
            for cobra in cobras_hombre_lobo:
                cobra.rect.y -= jugador.vely
            #Reubicacion bolas igneas jugador
            for bola_ignea in bolas_igneas_golem:
                bola_ignea.rect.y -= jugador.vely
            #Reubicacion bolas igneas dragon
            for bola_ignea in bolas_igneas:
                bola_ignea.rect.y -= jugador.vely
            #Reubicacion hombre lobo
            for hombre_lobo in hombres_lobo:
                hombre_lobo.rect.y -= jugador.vely
            #Reubicacion puas
            for pua in puas:
                pua.rect.y -= jugador.vely


        '''-------------'''
        

        pantalla.fill(NEGRO)
        '''Actualizacion de grupos'''
        bloques_limite.update()
        jugadores.update()
        bolas_igneas.update()
        golems.update()
        cobras.update()
        hombres_lobo.update()
        bolas_igneas_golem.update()
        cobras_hombre_lobo.update()
        puas.update()
        '''-----------------------'''

        '''Digujado de grupos'''
        pantalla.blit(fondo.imagen, [fondo.posx, fondo.posy])
        bloques_limite.draw(pantalla)
        jugadores.draw(pantalla)
        bolas_igneas.draw(pantalla)
        golems.draw(pantalla)
        cobras.draw(pantalla)
        hombres_lobo.draw(pantalla)
        bolas_igneas_golem.draw(pantalla)
        cobras_hombre_lobo.draw(pantalla)
        puas.draw(pantalla)

        '''------------------'''

        '''Refresco pantalla'''
        #Muestra los corazones del hombre lobo
        for hombre_lobo in hombres_lobo:   
            posicion_salud_hombre_lobo = [hombre_lobo.rect.left - 50, hombre_lobo.rect.top - 50]
            mostrar_info_salud(pantalla, hombre_lobo.sprite_salud, hombre_lobo.salud, posicion_salud_hombre_lobo)
        info_puntaje_jugador = 'Puntaje: ' +  str(jugador.puntaje)
        mostrar_info(pantalla, None, info_puntaje_jugador, AZUL, 44, [600,20])
        mostrar_info_salud(pantalla, jugador.imagen_corazones, jugador.salud, [50,20])
        info_salud_jugador = 'Salud: ' +  str(jugador.salud + 1)
        mostrar_info(pantalla, None, info_salud_jugador, AZUL, 30, [55,70])
        pygame.display.flip()
        reloj.tick(30)
        '''-----------------'''
    
    '''---'''

    '''Pantalla game over'''
    fondo_game_over = pygame.image.load('imagenes/fondo/fondo_game_over.jpg')
    
    while (not fin) and (not fin_pantalla_gameover):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
        pantalla.fill(NEGRO)
        pantalla.blit(fondo_game_over, [0,0])
        info_puntaje_jugador = 'PUNTAJE FINAL: ' + str(jugador.puntaje)
        mostrar_info(pantalla, None, info_puntaje_jugador, BLANCO, 44, [250, 50])

        pygame.display.flip()

    '''---------------'''

    '''Pantalla win'''
    fondo_win = pygame.image.load('imagenes/fondo/fondo_win.png')
    
    while (not fin) and (not fin_pantalla_victoria):
        #Gestion de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True
        pantalla.fill(NEGRO)
        pantalla.blit(fondo_win, [0,0])
        info_puntaje_jugador = 'PUNTAJE FINAL: ' + str(jugador.puntaje)
        mostrar_info(pantalla, None, info_puntaje_jugador, BLANCO, 44, [250, 400])

        pygame.display.flip()

    '''---------------'''