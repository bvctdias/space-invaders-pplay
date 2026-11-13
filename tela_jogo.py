from player import Player
from monsters import Monsters
from score import Score
from bonus import Bonus, ExtraLife, BonusHorda
from lifes import Lifes

from funcoes import dificuldade

class InfosTela:
    def desenhar(self, janela, nivel, orga):
        niveis = {1:"FÁCIL", 2:"MÉDIO", 3:"DIFÍCIL"}
        texto = f"FASE: {orga} | DIFICULDADE: {niveis[nivel]} --  MOVER: A/D ou SETAS | ATIRAR: W ou ESPAÇO | MENU: ESC | PAUSAR: P"
        janela.draw_text(texto, 15, janela.height - 25, size=15, color=(252,252,252), font_name="Monaco")

# class TelaJogo:
#     def __init__(self, janela, nivel):
#         self.janela = janela
#         self.nivel = nivel
#         (
#             self.vel_monstros,
#             self.vel_ataque,
#             self.intervalo_ataque,
#             self.intervalo_recarga,
#             linhas_monstros,
#             colunas_monstros
#         ) = dificuldade(self.nivel)

#         self.player = Player(self.janela, self.intervalo_recarga)
#         self.bonus = Bonus(self.janela)
#         self.monstros = Monsters(linhas_monstros, colunas_monstros, self.janela)
#         self.placar = Score()
#         self.vidas = Lifes(self.janela, vidas=3)
        
#         self.infos_tela = InfosTela()

#     def executar(self, delta, teclado):
#         self.janela.set_background_color((33, 40, 48))

#         if teclado.key_down("ESC"):
#             return "menu"

#         self.player.atualizar(delta, teclado, self.bonus.efeito_ativo, self.monstros, self.placar)

#         self.monstros.mover(self.janela, self.vel_monstros, delta)
#         self.monstros.atualizar(delta)

#         atacado = self.monstros.atualizarAtaques(self.janela, delta, self.player, self.vel_ataque, self.intervalo_ataque)
#         if atacado:
#             perdeu = self.vidas.perder_vida()
#             if perdeu:
#                 return "game_over"

#         self.bonus.atualizar(delta, self.player, self.placar)

#         self.player.desenhar()
#         self.monstros.desenhar()
#         self.monstros.desenharAtaques()
#         self.bonus.desenhar()
#         self.placar.desenhar(self.janela, self.bonus.efeito_ativo, self.bonus.tempo_restante())
#         self.vidas.desenhar()

#         self.infos_tela.desenhar(self.janela, self.nivel)

#         self.janela.draw_text(f"FPS: {self.janela.get_fps():.0f}", self.janela.width - 100, self.janela.height - 25, size=15, color=(255,255,255), font_name="Monaco")

#         if self.monstros.colisaoPlayer(self.player):
#             return "game_over"

#         return "jogo"



class TelaJogo:
    def __init__(self, janela, nivel):
        self.janela = janela
        self.infos_tela = InfosTela()

        self.reiniciar(nivel)


    def reiniciar(self, nivel=None):
        if nivel is not None:
            self.nivel = nivel

        (
            self.vel_monstros,
            self.vel_ataque,
            self.intervalo_ataque,
            self.intervalo_recarga,
            self.linhas_monstros,
            self.colunas_monstros
        ) = dificuldade(self.nivel)

        intervalos_boss_especial = {1: 3, 2: 4, 3: 5}
        self.intervalo_boss_especial = intervalos_boss_especial[self.nivel]

        self.player = Player(self.janela, self.intervalo_recarga)
        self.bonus = Bonus(self.janela)
        self.monstros = Monsters(
            self.linhas_monstros,
            self.colunas_monstros,
            self.janela,
            self.intervalo_boss_especial
        )
        self.placar = Score()
        self.vidas = Lifes(self.janela, vidas=3) 

        self.orga = 1
        self.prox_expansao = "linha"

        self.bonus = Bonus(self.janela)
        self.extra_life = ExtraLife(self.janela)
        self.bonus_horda = BonusHorda(limite_tempo=60, pontos=500, duracao_aviso=3)

    def executar(self, delta, teclado):
        # self.janela.set_background_color((33, 40, 48))

        if teclado.key_down("ESC"):
            return "menu"

        self.placar.atualizar(delta)

        self.player.atualizar(delta, teclado, self.bonus.efeito_ativo, self.monstros, self.placar)

        self.monstros.mover(self.janela, self.vel_monstros, delta)
        self.monstros.atualizar(delta)

        self.bonus_horda.atualizar(delta)

        if self.monstros.todos_destruidos():

            self.bonus_horda.concluir_horda(self.placar)

            self.orga += 1

            # aumento da orga apos uma destruicao completa
            if self.prox_expansao == "linha":
                if self.linhas_monstros < 7:
                    self.linhas_monstros += 1
                elif self.colunas_monstros < 10:
                    self.colunas_monstros += 1
                self.prox_expansao = "coluna"
            else:
                if self.colunas_monstros < 10:
                    self.colunas_monstros += 1
                elif self.linhas_monstros < 7:
                    self.linhas_monstros += 1
                self.prox_expansao = "linha"

            # aumento da dificuldade na nova orga
            self.vel_monstros *= 1.08   # 8% mais rapido
            self.vel_ataque *= 1.05     # 5% mais rapido
            self.intervalo_ataque = max(1, self.intervalo_ataque * 0.95)   # intervalo entre ataques menor em 10%
            
            bosses_destruidos = self.monstros.bosses_destruidos
            self.monstros = Monsters(
                self.linhas_monstros,
                self.colunas_monstros,
                self.janela,
                self.intervalo_boss_especial,
                bosses_destruidos
            )

        atacado = self.monstros.atualizarAtaques(self.janela, delta, self.player, self.vel_ataque, self.intervalo_ataque)
        if atacado:
            perdeu = self.vidas.perder_vida()
            self.placar.avisar("-1 VIDA", (255, 80, 80), separador=False)
            if perdeu:
                return "game_over"

        self.bonus.atualizar(delta, self.player, self.placar, self.monstros)
        self.extra_life.atualizar(delta, self.player, self.vidas, self.placar)

        self.desenhar()

        if teclado.key_down("P"):
            return "pause"

        if self.monstros.colisaoPlayer(self.player):
            return "game_over"

        return "jogo"

    def desenhar(self):
        self.janela.set_background_color((33, 40, 48))

        self.player.desenhar()
        self.monstros.desenhar()
        self.monstros.desenharAtaques()
        self.bonus.desenhar()
        self.extra_life.desenhar()

        if self.bonus_horda.aviso_ativo():
            self.placar.desenhar(self.janela)
        else:
            self.placar.desenhar(self.janela, self.bonus.efeito_ativo, self.bonus.tempo_restante())
        self.bonus_horda.desenhar(self.janela)

        self.vidas.desenhar()
        self.infos_tela.desenhar(self.janela, self.nivel, self.orga)

        self.janela.draw_text(f"FPS: {self.janela.get_fps():.0f}", self.janela.width - 100, self.janela.height - 25, size=15, color=(255, 255, 255), font_name="Monaco")

