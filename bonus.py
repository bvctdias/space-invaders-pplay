from PPlay.sprite import Sprite
from PPlay.collision import Collision

from funcoes import piscar

import random

class Bonus:
    def __init__(self,janela):
        self.janela = janela

        self.sprite = Sprite("imagens/ataques/bonus.png")

        self.sprite.x = random.randint(0, int(self.janela.width - self.sprite.width))
        self.sprite.y = - self.sprite.height

        self.ativo = True
        self.visivel = True

        self.vel_bonus = 250

        self.tempo_pisca = 0
        self.intervalo_pisca = 0.15

        self.tempo_bonus = 0
        self.intervalo_bonus = random.randint(4, 15)

        self.efeitos = [
            "tiro_duplo",
            "escudo",
            "dobra_ponto",
            "desafio_monstro"
        ]

        self.efeito_ativo = None
        self.tempo_efeito = 0
        self.duracao_efeito = 5


    def atualizar(self, delta, player, placar, monstros):
        # encerra o desafio assim que o monstro 5x for destruido
        if self.efeito_ativo == "desafio_monstro" and monstros.desafio_destruido:
            self.efeito_ativo = None
            self.tempo_efeito = 0
            monstros.desafio_destruido = False

        if self.ativo:
            self.sprite.y += (self.vel_bonus * delta)
            (
                self.tempo_pisca,
                self.visivel
            ) = piscar(self.visivel, self.tempo_pisca, self.intervalo_pisca, delta)

            if self.sprite.y > self.janela.height:
                self.ativo = False
                self.tempo_bonus = 0
                self.intervalo_bonus = random.randint(4, 15)
            
            elif Collision.collided(self.sprite, player.sprite):
                placar.adicionar_bonus(1)
                self.ativar_efeito(player, placar, monstros)
                self.ativo = False
                self.visivel = False
                self.tempo_bonus = 0
        
        else:
            self.tempo_bonus += delta

            if self.tempo_bonus >= self.intervalo_bonus:
                self.reaparecer()

        # controle da duracao do efeito
        if self.efeito_ativo is not None:
            self.tempo_efeito += delta
            if self.tempo_efeito >= self.duracao_efeito:
                self.encerrar_efeito(player, placar, monstros)


    def ativar_efeito(self, player, placar, monstros):
        # encerra efeito se tiver algum ativo
        if self.efeito_ativo is not None:
            self.encerrar_efeito(player, placar, monstros)

        self.duracao_efeito = 5     # tempo padrao dos efeitos

        self.efeito_ativo = random.choice(self.efeitos)
        self.tempo_efeito = 0

        if self.efeito_ativo == "escudo":
            player.escudo_ativo = True
            player.trocar_imagem("imagens/naves/nave_escudo.png")
        elif self.efeito_ativo == "dobra_ponto":
            placar.ativar_dobro()
        elif self.efeito_ativo == "desafio_monstro":
            show_up = monstros.criarMonstroDesafio()
            if show_up:
                self.duracao_efeito = 10    # se for o bonus 5x o monstro fica um tempo maior na tela que os ourtos efeitos
            else:
                self.efeito_ativo = None
        # tiro duplo no player


    def encerrar_efeito(self, player, placar, monstros):
        if self.efeito_ativo == "escudo":
            player.escudo_ativo = False
            player.trocar_imagem("imagens/naves/ship.png")
        elif self.efeito_ativo == "dobra_ponto":
            placar.desativar_dobro()
        elif self.efeito_ativo == "desafio_monstro":
            monstros.removerMonstroDesafio()

        self.efeito_ativo = None
        self.tempo_efeito = 0


    def reaparecer(self):
        self.sprite.x = random.randint(0, int(self.janela.width - self.sprite.width))
        self.sprite.y = - self.sprite.height

        self.ativo = True
        self.visivel = True
        self.tempo_bonus = 0
        self.tempo_pisca = 0


    def tempo_restante(self):
        if self.efeito_ativo is None:
            return 0
        return max(0, self.duracao_efeito - self.tempo_efeito)


    def desenhar(self):
        if self.ativo and self.visivel:
            self.sprite.draw()
            

class ExtraLife:
    def __init__(self,janela):
        self.janela = janela
        self.sprite = Sprite("imagens/lifes/extra_life.png")

        self.velocidade = 200

        self.ativo = False
        self.visivel = True
        self.tempo = 0

        self.intervalo = random.randint(20, 35)

        self.tempo_pisca = 0
        self.intervalo_pisca = 0.15

        self.reposicionar()

    def reposicionar(self):
        self.sprite.x = random.randint(0, int(self.janela.width - self.sprite.width))
        self.sprite.y = - self.sprite.height


    def atualizar(self, delta, player, vidas, placar):
        if self.ativo:
            self.sprite.y += self.velocidade * delta
            (
                self.tempo_pisca,
                self.visivel
            ) = piscar(self.visivel, self.tempo_pisca, self.intervalo_pisca, delta)
            

            if Collision.collided(self.sprite, player.sprite):
                ganhou_vida = vidas.ganhar_vida()
                if ganhou_vida:
                    placar.avisar("+1 VIDA", (255, 80, 80), separador=False)
                else:
                    placar.adicionar_bonus(5)
                    placar.avisar("+5 PTS", (255, 80, 80), separador=False)
                self.desativar()
            elif self.sprite.y > self.janela.height:
                self.desativar()
        
        else:
            self.tempo += delta
            
            if self.tempo >= self.intervalo:
                self.reposicionar()
                
                self.ativo = True
                self.visivel = True
                
                self.tempo = 0
                self.tempo_pisca = 0


    def desativar(self):
        self.ativo = False
        self.tempo = 0

        self.intervalo = random.randint(20, 35)


    def desenhar(self):
        if self.ativo and self.visivel:
            self.sprite.draw()


class BonusHorda:
    def __init__(self, limite_tempo=60, pontos=500, duracao_aviso=3):
        self.limite_tempo = limite_tempo
        self.pontos_base = pontos
        self.duracao_aviso = duracao_aviso

        self.tempo_horda = 0
        self.tempo_aviso = 0
        self.tempo_conclusao = 0

        self.texto_aviso = ""
        self.pontos_recebidos = 0


    def atualizar(self, delta):
        self.tempo_horda += delta

        if self.tempo_aviso > 0:
            self.tempo_aviso -= delta

            if self.tempo_aviso < 0:
                self.tempo_aviso = 0


    def concluir_horda(self, placar):
        self.tempo_conclusao = self.tempo_horda
        self.pontos_recebidos = 0
        self.texto_aviso = ""

        if self.tempo_horda <= self.limite_tempo/2:
            self.texto_aviso = "HORDA PERFEITA!"
            self.pontos_recebidos = self.pontos_base * 2

        elif self.tempo_horda <= self.limite_tempo * 0.75:
            self.texto_aviso = "HORDA RELÂMPAGO!"
            self.pontos_recebidos = int(self.pontos_base * 1.5)

        elif self.tempo_horda <= self.limite_tempo:
            self.texto_aviso = "HORDA RÁPIDA!"
            self.pontos_recebidos = self.pontos_base

        if self.pontos_recebidos > 0:
            placar.adicionar_bonus(self.pontos_recebidos)
        else:
            self.texto_aviso = "HORDA CONCLUÍDA!"

        # Mostra o aviso com ou sem bônus
        self.tempo_aviso = self.duracao_aviso

        self.tempo_horda = 0


    def aviso_ativo(self):
        return self.tempo_aviso > 0


    # def desenhar(self, janela):
    #     if self.aviso_ativo():
    #         texto = (f"{self.texto_aviso} | {self.tempo_conclusao:.1f}s | +{self.pontos_recebidos} PTS")

    #         janela.draw_text(texto, 15, 35, size=20, color=(255, 210, 70), font_name="Monaco", bold=True)

    def desenhar(self, janela):
        if self.aviso_ativo():

            if self.pontos_recebidos > 0:
                texto = (f"{self.texto_aviso} | {self.tempo_conclusao:.1f}s | +{self.pontos_recebidos} PTS")
                cor = (255, 210, 70)
            else:
                texto = (f"{self.texto_aviso} | {self.tempo_conclusao:.1f}s")
                cor = (200, 200, 200)

            janela.draw_text(texto, 15, 35, size=20, color=cor, font_name="Monaco", bold=True)
