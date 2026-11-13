from PPlay.sprite import Sprite
from PPlay.collision import Collision

from funcoes import piscar

import random


class JogoIA:
    def __init__(self, janela):
        self.janela = janela

        # Limites da simulacao: somente a metade direita da janela.
        self.limite_esquerdo = janela.width/2 + 25
        self.limite_direito = janela.width - 25

        self.nave = Sprite("imagens/naves/ship.png")
        self.nave.y = janela.height - self.nave.height - 45
        self.centralizar_nave()

        self.velocidade_nave = 60
        self.alvo = None

        self.nave_visivel = True
        self.nave_invulneravel = False
        self.tempo_invulneravel = 0
        self.tempo_pisca_nave = 0
        self.intervalo_pisca_nave = 0.12
        self.duracao_invulnerabilidade = 1.2

        self.tiros = []
        self.velocidade_tiro = 400
        self.tempo_tiro = 0
        self.intervalo_tiro = random.uniform(0.5, 1.2)

        self.monstros = []
        self.direcao_monstros = 1
        self.velocidade_monstros = 35

        self.ataques_monstros = []
        self.velocidade_ataque = 200
        self.tempo_ataque = 0
        self.intervalo_ataque = random.uniform(0.8, 1.8)

        self.tempo_reinicio = 0
        self.criar_monstros()


    def centralizar_nave(self):
        self.nave.x = (
            self.limite_esquerdo
            + self.limite_direito
            - self.nave.width
        ) / 2


    def criar_monstros(self):
        self.monstros = []

        linhas = 3
        colunas = 5
        espacamento_x = 10
        espacamento_y = 12

        referencia = Sprite("imagens/monstros/monster_1.png")

        largura_formacao = (
            colunas * referencia.width
            + (colunas - 1) * espacamento_x
        )

        largura_area = self.limite_direito - self.limite_esquerdo
        x_inicial = (
            self.limite_esquerdo
            + largura_area/2
            - largura_formacao/2
        )

        y_inicial = 190

        for linha in range(linhas):
            for coluna in range(colunas):
                monstro = Sprite("imagens/monstros/monster_1.png")

                monstro.x = x_inicial + coluna * (
                    monstro.width + espacamento_x
                )

                monstro.y = y_inicial + linha * (
                    monstro.height + espacamento_y
                )

                monstro.estado = "normal"
                monstro.visivel = True
                monstro.tempo_estado = 0
                monstro.alternancias = 0

                self.monstros.append(monstro)

        self.direcao_monstros = 1
        self.tempo_reinicio = 0


    def atualizar(self, delta):
        self.mover_nave(delta)
        self.atirar(delta)
        self.mover_tiros(delta)
        self.mover_monstros(delta)
        self.atualizar_monstros(delta)
        self.atirar_monstros(delta)
        self.atualizar_ataques_monstros(delta)
        self.atualizar_nave_atingida(delta)

        if not self.monstros:
            self.tempo_reinicio += delta

            if self.tempo_reinicio >= 1:
                self.tiros = []
                self.ataques_monstros = []
                self.criar_monstros()


    def mover_nave(self, delta):
        ataque_perigoso = None

        for ataque in self.ataques_monstros:
            perto_na_vertical = (
                ataque.y >= self.nave.y - 180
                and ataque.y <= self.nave.y + self.nave.height
            )
            alinhado_com_nave = (
                ataque.x + ataque.width >= self.nave.x - 20
                and ataque.x <= self.nave.x + self.nave.width + 20
            )

            if perto_na_vertical and alinhado_com_nave:
                ataque_perigoso = ataque
                break

        if ataque_perigoso is not None:
            centro_ataque = ataque_perigoso.x + ataque_perigoso.width/2
            centro_nave = self.nave.x + self.nave.width/2

            if centro_ataque <= centro_nave:
                destino_x = self.limite_direito - self.nave.width
            else:
                destino_x = self.limite_esquerdo

        else:
            if (
                self.alvo not in self.monstros
                or self.alvo.estado != "normal"
            ):
                candidatos = []

                for monstro in self.monstros:
                    if monstro.estado == "normal":
                        candidatos.append(monstro)

                if candidatos:
                    centro_nave = self.nave.x + self.nave.width/2
                    self.alvo = min(
                        candidatos,
                        key=lambda monstro: abs(
                            monstro.x + monstro.width/2 - centro_nave
                        )
                    )
                else:
                    self.alvo = None

            if self.alvo is not None:
                destino_x = (
                    self.alvo.x
                    + self.alvo.width/2
                    - self.nave.width/2
                )
            else:
                destino_x = (
                    self.limite_esquerdo
                    + self.limite_direito
                    - self.nave.width
                ) / 2

        destino_x = max(
            self.limite_esquerdo,
            min(destino_x, self.limite_direito - self.nave.width)
        )

        distancia = destino_x - self.nave.x
        passo = self.velocidade_nave * delta

        if abs(distancia) <= passo:
            self.nave.x = destino_x
        elif distancia < 0:
            self.nave.x -= passo
        else:
            self.nave.x += passo


    def atirar(self, delta):
        self.tempo_tiro += delta

        if self.tempo_tiro >= self.intervalo_tiro:
            tiro = Sprite("imagens/ataques/shoot.png")

            tiro.x = (
                self.nave.x
                + self.nave.width/2
                - tiro.width/2
            )
            tiro.y = self.nave.y - tiro.height

            self.tiros.append(tiro)

            self.tempo_tiro = 0
            self.intervalo_tiro = random.uniform(0.5, 1.2)


    def mover_tiros(self, delta):
        for tiro in self.tiros[:]:
            tiro.y -= self.velocidade_tiro * delta

            acertou = False

            for monstro in self.monstros[:]:
                if (
                    monstro.estado == "normal"
                    and Collision.collided(tiro, monstro)
                ):
                    monstro.estado = "piscando"
                    monstro.tempo_estado = 0
                    monstro.alternancias = 0
                    acertou = True
                    break

            if acertou or tiro.y + tiro.height < 0:
                self.tiros.remove(tiro)


    def mover_monstros(self, delta):
        monstros_em_movimento = []

        for monstro in self.monstros:
            if monstro.estado != "explosao":
                monstros_em_movimento.append(monstro)

        if not monstros_em_movimento:
            return

        mais_esquerdo = monstros_em_movimento[0].x
        mais_direito = (
            monstros_em_movimento[0].x
            + monstros_em_movimento[0].width
        )

        for monstro in monstros_em_movimento:
            mais_esquerdo = min(mais_esquerdo, monstro.x)
            mais_direito = max(
                mais_direito,
                monstro.x + monstro.width
            )

        deslocamento = (
            self.velocidade_monstros
            * self.direcao_monstros
            * delta
        )

        bateu_esquerda = (
            mais_esquerdo + deslocamento <= self.limite_esquerdo
        )
        bateu_direita = (
            mais_direito + deslocamento >= self.limite_direito
        )

        if bateu_esquerda or bateu_direita:
            self.direcao_monstros *= -1
            deslocamento *= -1

        for monstro in monstros_em_movimento:
            monstro.x += deslocamento


    def atualizar_monstros(self, delta):
        intervalo_pisca = 0.08
        duracao_explosao = 0.15

        for monstro in self.monstros[:]:
            if monstro.estado == "piscando":
                visibilidade_anterior = monstro.visivel

                monstro.tempo_estado, monstro.visivel = piscar(
                    monstro.visivel,
                    monstro.tempo_estado,
                    intervalo_pisca,
                    delta
                )

                if monstro.visivel != visibilidade_anterior:
                    monstro.alternancias += 1

                if monstro.alternancias >= 4:
                    explosao = Sprite("imagens/monstros/explosao.png")
                    explosao.x = (
                        monstro.x
                        + monstro.width/2
                        - explosao.width/2
                    )
                    explosao.y = (
                        monstro.y
                        + monstro.height/2
                        - explosao.height/2
                    )
                    explosao.estado = "explosao"
                    explosao.visivel = True
                    explosao.tempo_estado = 0

                    indice = self.monstros.index(monstro)
                    self.monstros[indice] = explosao

            elif monstro.estado == "explosao":
                monstro.tempo_estado += delta

                if monstro.tempo_estado >= duracao_explosao:
                    self.monstros.remove(monstro)


    def atirar_monstros(self, delta):
        self.tempo_ataque += delta

        if self.tempo_ataque < self.intervalo_ataque:
            return

        candidatos = []

        for monstro in self.monstros:
            if monstro.estado == "normal":
                candidatos.append(monstro)

        if candidatos:
            monstro = random.choice(candidatos)
            ataque = Sprite("imagens/ataques/attack1.png")
            ataque.x = (
                monstro.x
                + monstro.width/2
                - ataque.width/2
            )
            ataque.y = monstro.y + monstro.height

            self.ataques_monstros.append(ataque)

        self.tempo_ataque = 0
        self.intervalo_ataque = random.uniform(0.8, 1.8)


    def atualizar_ataques_monstros(self, delta):
        for ataque in self.ataques_monstros[:]:
            ataque.y += self.velocidade_ataque * delta

            if (
                not self.nave_invulneravel
                and Collision.collided(ataque, self.nave)
            ):
                self.ataques_monstros.remove(ataque)
                self.atingir_nave()

            elif ataque.y > self.janela.height:
                self.ataques_monstros.remove(ataque)


    def atingir_nave(self):
        self.centralizar_nave()
        self.nave_invulneravel = True
        self.nave_visivel = False
        self.tempo_invulneravel = 0
        self.tempo_pisca_nave = 0


    def atualizar_nave_atingida(self, delta):
        if not self.nave_invulneravel:
            return

        self.tempo_invulneravel += delta

        self.tempo_pisca_nave, self.nave_visivel = piscar(
            self.nave_visivel,
            self.tempo_pisca_nave,
            self.intervalo_pisca_nave,
            delta
        )

        if self.tempo_invulneravel >= self.duracao_invulnerabilidade:
            self.nave_invulneravel = False
            self.nave_visivel = True
            self.tempo_invulneravel = 0


    def desenhar(self):
        if self.nave_visivel:
            self.nave.draw()

        for tiro in self.tiros:
            tiro.draw()

        for ataque in self.ataques_monstros:
            ataque.draw()

        for monstro in self.monstros:
            if monstro.visivel:
                monstro.draw()
