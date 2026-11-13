from PPlay.sprite import Sprite
from PPlay.collision import Collision

from funcoes import piscar

import random


class Monsters:
    def __init__(self, linhas, colunas, janela, intervalo_boss_especial=3, bosses_destruidos=0):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = []
        self.total_inicial = linhas * colunas
        self.ataques = []
        self.tempo_ataque = 0
        self.ultimo_abate_boss = False
        self.ultimo_abate_desafio = False
        self.desafio_destruido = False
        self.intervalo_boss_especial = intervalo_boss_especial
        self.bosses_destruidos = bosses_destruidos

        self.direcao = 1    # inicialmente vai pra direita, quando -1 vai pra esquerda

        # cada linha vai receber um monster (facil = 3 linahs, medio = 4 linhas, dificil = 5 linhas)
        self.imagens = [
            "imagens/monstros/monster_1.png",
            "imagens/monstros/monster_2.png",
            "imagens/monstros/monster_3.png",
            "imagens/monstros/monster_4.png",
            "imagens/monstros/monster_5.png"
        ]

        self.resistencia = {1:1, 2:1, 3:2, 4:2, 5:3}

        referencia = Sprite(self.imagens[0])
        largura = referencia.width
        altura = referencia.height
        espacamento_x = largura/2
        espacamento_y = altura/2

        largura_total = (colunas * largura) + ((colunas -1) * espacamento_x)
        # altura_total = (linhas * altura) + ((linhas -1) * espacamento_y)

        # inicio da formacao centralizada
        x_inicial = janela.width/2 - largura_total/2
        y_inicial = 100   # afatado para o placar

        for linha in range(linhas):
            linha_monstros = []

            # a linha da base da matriz recebe o monster_1
            linhas_base = linhas - linha - 1
            # incremento da linha quando todos forem destruídos de forma ciclica
            indice_imagem = linhas_base % len(self.imagens)

            imagem = self.imagens[indice_imagem]

            for coluna in range(colunas):
                monstro = Sprite(imagem)

                monstro.x = x_inicial + coluna * (largura + espacamento_x)
                monstro.y = y_inicial + linha * (altura + espacamento_y)

                monstro.estado = "normal"
                monstro.visivel = True
                monstro.tempo_estado = 0
                monstro.alternancias = 0

                monstro.tipo = indice_imagem + 1
                monstro.vida = self.resistencia[monstro.tipo]
                monstro.desafio = False
                monstro.boss = False
                
                monstro.linha_grade = linha
                monstro.coluna_grade = coluna

                linha_monstros.append(monstro)

            self.matriz.append(linha_monstros)

        # dados de formacao para desafio monstro aletorio 5x
        self.x_inicial = x_inicial
        self.y_inicial = y_inicial
        self.desloc_x = 0
        self.desloc_y = 0
        self.largura = largura
        self.altura = altura
        self.espacamento_x = espacamento_x
        self.espacamento_y = espacamento_y

        # inicia cada horda com um boss em uma posicao aleatoria da matriz
        self.criarBoss()


    def desenhar(self):
        for linha in self.matriz:
            for monstro in linha:
                if monstro.visivel:
                    monstro.draw()


    def qtd_monstros(self):
        qtd = 0
        for linha in self.matriz:
            for monstro in linha:
                if monstro.estado != "explosao":
                    qtd += 1
        return qtd


    def mover(self, janela, velocidade, delta):
        monstros = []

        for linha in self.matriz:
            for monstro in linha:
                monstros.append(monstro)

        # lista vazia encerr a funcao
        if not monstros:
            return

        faixa_esquerda = monstros[0].x
        for monstro in monstros:
            if monstro.x < faixa_esquerda:
                faixa_esquerda = monstro.x

        faixa_direita = monstros[0].x + monstros[0].width
        for monstro in monstros:
            borda_direita = monstro.x + monstro.width
            if borda_direita > faixa_direita:
                faixa_direita = borda_direita

        # conforme elmino monstros a velocidade da orga aumenta
        qtd_atual = self.qtd_monstros()
        eliminados = self.total_inicial - qtd_atual
        proporcao_eliminada = eliminados/self.total_inicial
        fator_vel = 1 + proporcao_eliminada
        vel_atual = velocidade * fator_vel

        deslocamento = vel_atual * self.direcao * delta

        # verificacao booleana da colisao
        colisao_esquerda = (faixa_esquerda + deslocamento <= 0)
        colisao_direita = (faixa_direita + deslocamento >= janela.width)

        if colisao_esquerda or colisao_direita:     # se a verificacao acima for True - choque com a parede
            self.direcao *= -1  # inverter
            down = monstros[0].height/2     # desce a metade da altura de um monstro

            for monstro in monstros:        # tds os monstros descem juntos
                monstro.y += down
            self.desloc_y += down

            deslocamento = vel_atual * self.direcao * delta    # desloca na nova direcao

        for monstro in monstros:        # movimento horizontal dos monstros
            monstro.x += deslocamento
        self.desloc_x += deslocamento


    def colisaoPlayer(self, nave):
        for linha in self.matriz:
            for monstro in linha:
                faixa_inferior = monstro.y + monstro.height

                if faixa_inferior >= nave.sprite.y:
                    return True     # encerra o metodo e indica que o monstro chegou no player

        return False    # nenhum monstro chegou a nave


    # OTIMIZACAO SOLICITADA - AULA 11
    '''
    1 - calcula o retangulo que envolve a formacao
    2 - verifica se o tiro esta fora dele
    3 - collided contra cada monstro quando o tiro entra nessa area
    '''
    def colisaoTiro(self, tiro):
        self.ultimo_abate_boss = False
        self.ultimo_abate_desafio = False
        monstros_ativos = []

        # se o monstro estiver no estado normal ele eh colocado na lista
        for linha in self.matriz:
            for monstro in linha:
                if (monstro.estado == "normal"):
                    monstros_ativos.append(monstro)

        if not monstros_ativos:
                return None

        # limites do retangulo
        limite_esquerdo = monstros_ativos[0].x
        limite_direito = monstros_ativos[0].x + monstros_ativos[0].width
        limite_superior = monstros_ativos[0].y
        limite_inferior = monstros_ativos[0].y + monstros_ativos[0].height

        # percorrer os monstros encontrados para determinar as extremidades de formacao
        for monstros in monstros_ativos:
            limite_esquerdo = min(limite_esquerdo, monstros.x)
            limite_direito = max(limite_direito, monstros.x + monstros.width)
            limite_superior = min(limite_superior, monstros.y)
            limite_inferior = max(limite_inferior, monstros.y + monstros.height)

        # tiro completamente fora da area ocupada pelos monstros
        tiro_fora = (tiro.x + tiro.width < limite_esquerdo
                     or tiro.x > limite_direito
                     or tiro.y + tiro.height < limite_superior
                     or tiro.y > limite_inferior)
        if tiro_fora:
            return None

        # colisoes individuais somente se dentro da area
        for monstro in monstros_ativos:
            if Collision.collided(tiro, monstro):
                monstro.vida -= 1
                
                monstro.estado = "piscando"
                monstro.tempo_estado = 0
                monstro.alternancias = 0
                
                if monstro.vida > 0:
                    if monstro.boss:
                        if monstro.fase_boss == 1 and monstro.vida == 5:
                            self.trocarCorBoss(monstro, 2)
                        elif monstro.fase_boss == 2 and monstro.vida == 3:
                            self.trocarCorBoss(monstro, 3)
                    return 0

                pontos = monstro.tipo * 10    # tipo eh pelo numero da linha.. linha 1, monstro 1, 1x10 = 10 pontos
                
                if monstro.boss:
                    pontos = 100
                    self.ultimo_abate_boss = True
                    self.bosses_destruidos += 1

                    if self.bosses_destruidos >= self.intervalo_boss_especial:
                        pontos += self.destruirLinhaColunaBoss(monstro)
                        self.bosses_destruidos = 0

                if monstro.desafio:
                    pontos *= 5
                    self.ultimo_abate_desafio = True
                    self.desafio_destruido = True

                return pontos
                
        return None


    def destruirLinhaColunaBoss(self, boss):
        pontos = 0

        for linha in self.matriz:
            for monstro in linha[:]:
                mesma_linha = (monstro.linha_grade == boss.linha_grade)
                mesma_coluna = (monstro.coluna_grade == boss.coluna_grade)

                if monstro is boss or not (mesma_linha or mesma_coluna):
                    continue

                # inimigos que ja estao mortos ou explodindo ja deram pontos
                if monstro.estado == "explosao" or monstro.vida <= 0:
                    continue

                pontos_monstro = monstro.tipo * 10

                if monstro.desafio:
                    pontos_monstro *= 5
                    self.ultimo_abate_desafio = True
                    self.desafio_destruido = True

                pontos += pontos_monstro
                monstro.vida = 0
                monstro.estado = "piscando"
                monstro.visivel = True
                monstro.tempo_estado = 0
                monstro.alternancias = 0

        return pontos


    def atualizar(self,delta):
        intervalo_pisca = 0.08
        duracao_explosao = 0.15
        posicao_boss_destruido = None

        for linha in self.matriz:
            for monstro in linha[:]:

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

                    # piscar 2x = invisivel/visivel 2x
                    if monstro.alternancias >= 4:
                        if monstro.vida > 0:
                            monstro.estado = "normal"
                            monstro.visivel = True
                            monstro.tempo_estado = 0
                            monstro.alternancias = 0

                        else:
                            explosao = Sprite("imagens/monstros/explosao.png")
                            explosao.x = monstro.x + monstro.width/2 - explosao.width/2
                            explosao.y = monstro.y + monstro.height/2 - explosao.height/2

                            explosao.estado = "explosao"
                            explosao.visivel = True
                            explosao.tempo_estado = 0

                            explosao.linha_grade = monstro.linha_grade
                            explosao.coluna_grade = monstro.coluna_grade

                            explosao.desafio = monstro.desafio
                            explosao.boss = monstro.boss

                            linha[linha.index(monstro)] = explosao

                elif monstro.estado == "explosao":
                    monstro.tempo_estado += delta

                    if monstro.tempo_estado >= duracao_explosao:
                        if monstro.boss:
                            posicao_boss_destruido = (
                                monstro.linha_grade,
                                monstro.coluna_grade
                            )
                        linha.remove(monstro)

        # o boss renasce enquanto ainda houver outros monstros na horda
        if posicao_boss_destruido is not None:
            existem_outros_monstros = False

            for linha in self.matriz:
                for monstro in linha:
                    if not monstro.boss and monstro.estado != "explosao":
                        existem_outros_monstros = True
                        break

                if existem_outros_monstros:
                    break

            if existem_outros_monstros:
                self.criarBoss()

        self.limpar_buffer()


    def atualizarAtaques(self, janela, delta, player, vel_ataque, intervalo_ataque):
        self.tempo_ataque += delta

        # por enquanto cria ataque quando termina o intervalo
        if self.tempo_ataque >= intervalo_ataque:
            candidatos = []

            for linha in self.matriz:
                for monstro in linha:
                    if monstro.estado == "normal":
                        candidatos.append(monstro)

            if candidatos:
                atacante = random.choice(candidatos)
                ataque = Sprite(f"imagens/ataques/attack{atacante.tipo}.png")

                ataque.x = atacante.x + atacante.width/2 - ataque.width/2
                ataque.y = atacante.y + atacante.height

                self.ataques.append(ataque)

            self.tempo_ataque = 0

        # movimenta e verifica os ataques
        atingido = False

        for ataque in self.ataques[:]:
            ataque.y += vel_ataque * delta

            if Collision.collided(ataque, player.sprite):
                self.ataques.remove(ataque)

                if player.receber_dano():
                    atingido = True
                continue

            if ataque.y > janela.height:
                self.ataques.remove(ataque)

        return atingido

    def desenharAtaques(self):
        for ataque in self.ataques:
            ataque.draw()


    def todos_destruidos(self):
        for linha in self.matriz:
            if len(linha) > 0:
                return False
        return True


    def limpar_buffer(self):
        while(self.matriz and len(self.matriz[-1]) == 0):
            self.matriz.pop()
            self.linhas -= 1


    def criarMonstroDesafio(self):
        ocupadas = []

        for linha in self.matriz:
            for monstro in linha:
                ocupadas.append((monstro.linha_grade, monstro.coluna_grade))

        vazias = []

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                posicao = (linha, coluna)

                if posicao not in ocupadas:
                    vazias.append(posicao)

        # se a matriz estiver cheia nao coloca em lugar nenhum
        if not vazias:
            return False

        linha, coluna = random.choice(vazias)
        tipo = random.randint(1, 5)

        monstro = Sprite(f"imagens/monstros/monsterd_{tipo}.png")
        monstro.x = self.x_inicial + self.desloc_x + coluna * (self.largura + self.espacamento_x)
        monstro.y = self.y_inicial + self.desloc_y + linha * (self.altura + self.espacamento_y)

        monstro.estado = "normal"
        monstro.visivel = True
        monstro.tempo_estado = 0
        monstro.alternancias = 0

        monstro.tipo = tipo
        monstro.vida = tipo
        monstro.desafio = True
        monstro.boss = False

        monstro.linha_grade = linha
        monstro.coluna_grade = coluna

        self.matriz[linha].append(monstro)

        return True


    def removerMonstroDesafio(self):
        for linha in self.matriz:
            for monstro in linha[:]:
                if monstro.desafio:
                    linha.remove(monstro)


    def criarBoss(self):
        # impede a criacao de dois bosses ao mesmo tempo
        for linha in self.matriz:
            for monstro in linha:
                if monstro.boss:
                    return False

        if not self.matriz or self.linhas == 0:
            return False

        # o boss pode substituir monstros comuns, mas nao o monstro do desafio 5x
        posicoes_disponiveis = []

        for linha_grade in range(self.linhas):
            for coluna_grade in range(self.colunas):
                posicao_desafio = False

                for monstro in self.matriz[linha_grade]:
                    if monstro.coluna_grade == coluna_grade and monstro.desafio:
                        posicao_desafio = True
                        break

                if not posicao_desafio:
                    posicoes_disponiveis.append((linha_grade, coluna_grade))

        if not posicoes_disponiveis:
            return False

        linha_grade, coluna_grade = random.choice(posicoes_disponiveis)

        # se houver outro monstro na posicao, o boss assume o lugar dele
        for monstro in self.matriz[linha_grade][:]:
            if monstro.coluna_grade == coluna_grade:
                self.matriz[linha_grade].remove(monstro)

        boss = Sprite("imagens/monstros/boss_1.png")
        boss.x = self.x_inicial + self.desloc_x + coluna_grade * (self.largura + self.espacamento_x)
        boss.y = self.y_inicial + self.desloc_y + linha_grade * (self.altura + self.espacamento_y)

        boss.estado = "normal"
        boss.visivel = True
        boss.tempo_estado = 0
        boss.alternancias = 0

        boss.tipo = 5
        # resistencia total: 1 tiro na fase 1, 2 na fase 2 e 3 na fase 3
        boss.vida = 6
        boss.desafio = False
        boss.boss = True
        boss.fase_boss = 1

        boss.linha_grade = linha_grade
        boss.coluna_grade = coluna_grade

        self.matriz[linha_grade].append(boss)

        return True


    def trocarCorBoss(self, boss_atual, nova_fase):
        novo_boss = Sprite(f"imagens/monstros/boss_{nova_fase}.png")

        novo_boss.x = boss_atual.x
        novo_boss.y = boss_atual.y

        novo_boss.estado = "piscando"
        novo_boss.visivel = True
        novo_boss.tempo_estado = 0
        novo_boss.alternancias = 0

        novo_boss.tipo = boss_atual.tipo
        novo_boss.vida = boss_atual.vida
        novo_boss.desafio = False
        novo_boss.boss = True
        novo_boss.fase_boss = nova_fase

        novo_boss.linha_grade = boss_atual.linha_grade
        novo_boss.coluna_grade = boss_atual.coluna_grade

        for linha in self.matriz:
            if boss_atual in linha:
                indice = linha.index(boss_atual)
                linha[indice] = novo_boss
                break







# monstros da primeira fileira derrotados com 1 tiro, da 2 com 2 e assim por diante.. eles piscam quando sofre o dano
# quando acertar qualquer monstro ele pisca duas vezes bem rápido e quando é destruído troca pra uma sprite de explosão (um png).. se eu tiver que dar 2 ou mais tiros ele só pisca ate ser destruído e trocar a sprite

