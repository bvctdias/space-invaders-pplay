'''
SPACE INVADERS

ORGANIZAÇÃO DO PROJETO


main.py:
- Cria a janela, o teclado e o mouse.
- Cria e posiciona os botões dos menus.
- Mantém o loop principal do programa.
- Calcula o delta time utilizado nas movimentações.
- Controla a troca entre as telas:
    menu, jogo, dificuldade, ranking, pausa e game over.
- Cria uma nova partida ou reinicia a partida atual.


button.py:
- Contém a classe Button.
- Carrega a imagem utilizada pelo botão.
- Desenha e centraliza os botões.
- Verifica se o cursor do mouse está sobre o botão.


funcoes.py:
- dificuldade():
    calcula velocidades, intervalos, linhas e colunas de acordo
    com o nível selecionado.
- piscar():
  alterna a visibilidade de um objeto usando delta time.
- atirar():
  cria e posiciona um novo tiro acima da nave.


player.py:
- Contém as classes Ship e Player.
- Ship controla a sprite e os limites horizontais da nave.
- Player controla o movimento da nave por A, D e setas.
- Controla o intervalo de recarga entre os disparos.
- Mantém os tiros ativos na lista self.tiros.
- Movimenta e remove os tiros que saem da tela.
- Chama a verificação de colisão dos tiros com os monstros.
- Remove o tiro depois de atingir um monstro.
- Adiciona ao placar os pontos retornados pela colisão.
- Implementa tiro duplo e mudança da imagem do tiro.
- Controla o escudo e a invulnerabilidade após receber dano.
- Reposiciona a nave e faz ela piscar durante a invulnerabilidade.


monsters.py:
- Contém a classe Monsters.
- Cria uma matriz configurável de monstros.
- Distribui tipos diferentes de monstros entre as linhas.
- Define a vida de cada tipo de monstro.
- Movimenta toda a formação horizontalmente.
- Inverte a direção da formação ao alcançar uma parede.
- Faz todos os monstros descerem no mesmo frame.
- Aumenta a velocidade quando restam menos monstros.
- Verifica se os monstros alcançaram a altura do player.
- Verifica colisões entre tiros e monstros.
- Faz o monstro atingido piscar.
- Substitui o monstro destruído pela sprite de explosão.
- Remove a explosão da matriz depois da animação.
- Calcula os pontos de acordo com o tipo do monstro.
- Cria e movimenta os ataques dos monstros.
- Verifica colisões dos ataques com o player.
- Controla o monstro especial do desafio 5X.
- Verifica quando todos os monstros foram destruídos.


COLISÃO ENTRE TIROS E MONSTROS:

1. O player dispara e adiciona o tiro em self.tiros.
2. O tiro é movimentado a cada frame.
3. Player chama monstros.colisaoTiro(tiro).
4. colisaoTiro() percorre a matriz procurando uma colisão.
5. Quando ocorre a colisão, o monstro perde uma vida.
6. O tiro é removido da lista e desaparece.
7. O monstro atingido pisca duas vezes.
8. Se ainda possuir vida, volta ao estado normal.
9. Se a vida chegar a zero, aparece uma explosão.
10. Depois da explosão, o monstro é removido da matriz.
11. Os pontos retornados são adicionados ao placar.


bonus.py:
- Contém as classes Bonus e ExtraLife.
- Bonus cria um objeto que cai em posição aleatória.
- O bônus pisca enquanto se movimenta.
- Ao ser coletado, adiciona um ponto ao placar.
- Sorteia um dos seguintes efeitos:
    tiro duplo, escudo, pontos em dobro ou monstro-desafio.
- Controla a duração e o encerramento dos efeitos.
- Faz o bônus reaparecer após um intervalo aleatório.
- ExtraLife cria um coração que aparece com menor frequência.
- Ao ser coletado, recupera uma vida.
- Se o player já estiver com as vidas completas,
  adiciona cinco pontos ao placar.
- Se destruir todos os monstros em menos de 1min ganha +500pts


score.py:
- Contém a classe Score.
- Armazena a pontuação atual.
- Adiciona os pontos obtidos ao destruir monstros.
- Aplica o multiplicador de pontos quando estiver ativo.
- Adiciona separadamente os pontos recebidos por bônus.
- Controla a sequência de monstros destruídos.
- Desenha o score e o efeito ativo na tela.


lifes.py:
- Contém a classe Lifes.
- Armazena a quantidade atual de vidas.
- Atualiza a imagem dos corações.
- Remove uma vida quando o player é atingido.
- Adiciona uma vida ao coletar um coração.
- Impede que a quantidade ultrapasse três vidas.
- Informa quando todas as vidas terminaram.


tela_jogo.py:
- Contém as classes TelaJogo e InfosTela.
- Reúne player, monstros, bônus, vidas e placar.
- Atualiza todos os objetos a cada frame.
- Controla ataques, colisões e condições de game over.
- Cria uma nova formação quando todos os monstros são eliminados.
- Alterna o aumento de linhas e colunas entre as fases.
- Limita a formação a sete linhas e dez colunas.
- Aumenta gradualmente a velocidade e a frequência dos ataques.
- Desenha todos os elementos da partida.
- Exibe fase, dificuldade, controles e FPS.
- Permite reiniciar completamente o estado da partida.


tela_dificuldade.py:
- Desenha os botões das três dificuldades.
- Retorna 1 para fácil, 2 para médio e 3 para difícil.
- Permite voltar ao menu pressionando ESC.


tela_pause.py:
- Redesenha o estado atual da partida sem atualizá-lo.
- Mantém o jogo congelado ao fundo.
- Exibe o score durante a pausa.
- ENTER continua a partida.
- ESC retorna ao menu.


tela_game_over.py:
- Exibe a mensagem de fim de jogo.
- Exibe a pontuação final.
- ENTER reinicia a partida.
- ESC retorna ao menu principal.


tela_rank.py:
- Desenha a tela de ranking.
- Será responsável por ler e exibir as pontuações salvas.
    - Lista os 5 melhores jogadores de forma ordenada.
- ESC retorna ao menu principal.

ranking.py:
- Gera um arquivo com nome, pontuacao e data


source .venv/bin/activate
'''

from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse

from button import Button
from ranking import Ranking, EntradaNomeRanking
from tela_jogo import TelaJogo
from tela_dificuldade import tela_dificuldade
from tela_rank import ranking
from tela_pause import pause
from tela_game_over import game_over

import random


# Janela
janela = Window(1024, 768)
janela.set_title("Space Invaders")

# Controles
teclado = Keyboard()
mouse = Mouse()

# Botoes do menu principal
b_jogar = Button("imagens/buttons/play.png")
b_jogar.centralizar(janela, janela.height/5)
b_dificuldade = Button("imagens/buttons/difficult.png")
b_dificuldade.centralizar(janela, 2*janela.height/5)
b_ranking = Button("imagens/buttons/ranking.png")
b_ranking.centralizar(janela, 3*janela.height/5)
b_sair = Button("imagens/buttons/exit.png")
b_sair.centralizar(janela, 4*janela.height/5)

# Botoes do menu de dificuldade
b_facil = Button("imagens/buttons/easy.png")
b_facil.centralizar(janela, janela.height/4)
b_facil.sprite.x = janela.width/3 - b_facil.sprite.width/2
b_medio = Button("imagens/buttons/medium.png")
b_medio.centralizar(janela, 2*janela.height/4)
b_dificil = Button("imagens/buttons/hard.png")
b_dificil.centralizar(janela, 3*janela.height/4)
b_dificil.sprite.x = 2*janela.width/3 - b_dificil.sprite.width/2

# Estado inicial
tela_atual = "menu"
nivel = 1   # dificuldade

# Primeira partida
jogo = TelaJogo(janela, nivel)

dados_ranking = Ranking()
entrada_nome = None


while True:

    delta = janela.delta_time()


    if tela_atual == "menu":                                    # Executa o menu principal
        janela.set_background_color((62,40,81))

        b_jogar.desenhar()
        b_dificuldade.desenhar()
        b_ranking.desenhar()
        b_sair.desenhar()

        if mouse.button_down(1):                                # Detecta o instante de clique esquerdo em algum botao
            if b_jogar.cursor(mouse):
                # criar nova partida
                jogo = TelaJogo(janela, nivel)

                tela_atual = "jogo"

            elif b_dificuldade.cursor(mouse):
                tela_atual = "dificuldade"

            elif b_ranking.cursor(mouse):
                tela_atual = "rank"

            elif b_sair.cursor(mouse):
                janela.close()


    elif tela_atual == "jogo":
        proxima_tela = jogo.executar(delta, teclado)
        if proxima_tela == "game_over":
            entrada_nome = EntradaNomeRanking(dados_ranking, jogo.placar.pontos)
        tela_atual = proxima_tela


    elif tela_atual == "dificuldade":
        resultado = tela_dificuldade(janela, teclado, mouse, b_facil, b_medio, b_dificil)

        if resultado == "menu":
            tela_atual = "menu"

        elif resultado in [1, 2, 3]:
            nivel = resultado
            # cria nova partida na dificuldade escolhida
            #jogo = TelaJogo(janela, nivel)
            jogo.reiniciar(nivel)
            tela_atual = "jogo"


    elif tela_atual == "rank":
        tela_atual = ranking(janela, teclado)


    elif tela_atual == "pause":
        tela_atual = pause(janela, teclado, jogo)


    elif tela_atual == "game_over":
        resultado = game_over(janela, teclado, jogo.placar, entrada_nome)
        
        if resultado == "reiniciar":
            # jogo = TelaJogo(janela, nivel)
            jogo.reiniciar()
            entrada_nome = None
            tela_atual = "jogo"

        elif resultado == "menu":
            entrada_nome = None
            tela_atual = "menu"


    janela.update()