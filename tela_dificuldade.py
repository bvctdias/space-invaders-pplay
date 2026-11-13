def tela_dificuldade(janela, teclado, mouse, b_facil, b_medio, b_dificil):
    janela.set_background_color((18,50,103))

    b_facil.desenhar()
    b_medio.desenhar()
    b_dificil.desenhar()

    janela.draw_text("MENU PRINCIPAL: ESC", 15, janela.height - 25, size=15, color=(252,252,252), font_name="Monaco")

    if teclado.key_down("ESC"):
        return "menu"

    # niveis = [1, 2, 3]

    if mouse.button_down(1):
        if b_facil.cursor(mouse):
            return 1
        elif b_medio.cursor(mouse):
            return 2
        elif b_dificil.cursor(mouse):
            return 3
    
    return None # nenhuma mudança na tela


