def pause(janela, teclado, jogo):
    # janela.set_background_color((33, 40, 48))
    jogo.desenhar()

    janela.draw_text("SPACE INVADERS", janela.width/2, janela.height/2 - 45, size=60, color=(255,80,80), font_name="Impact", italic=True)
    janela.draw_text(f"SCORE: {jogo.placar.pontos:06d}", janela.width/2, janela.height/2 + 35, size=30, color=(255,255,255), font_name="Monaco")
    janela.draw_text("ENTER: CONTINUAR | ESC: MENU", janela.width/2, janela.height/2 + 75, size=20, color=(255,255,255), font_name="Monaco")

    if teclado.key_down("ENTER"):
        return "jogo"
    elif teclado.key_down("ESC"):
        return "menu"

    return "pause"