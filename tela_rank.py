from ranking import Ranking
from jogo_ia import JogoIA

dados_ranking = Ranking()
jogo_ia = None


def ranking(janela, teclado):
    global jogo_ia

    if jogo_ia is None:
        jogo_ia = JogoIA(janela)

    janela.set_background_color((112, 13, 13))

    jogo_ia.atualizar(janela.delta_time())

    janela.draw_text("SPACE INVADERS", 15, 15, size=62, color=(0, 0, 0), font_name="Impact", italic=True)
    janela.draw_text("SPACE INVADERS", 17, 17, size=60, color=(94, 188, 2), font_name="Impact", italic=True)

    dados_ranking.desenhar(janela)
    jogo_ia.desenhar()

    janela.draw_text("MENU PRINCIPAL: ESC", 15, janela.height - 25, size=15, color=(252, 252, 252), font_name="Monaco")

    if teclado.key_down("ESC"):
        return "menu"

    return "rank"
