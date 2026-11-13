from ranking import Ranking

dados_ranking = Ranking()

def game_over(janela, teclado, placar, entrada_nome):
    janela.set_background_color((33, 40, 48))

    janela.draw_text("GAME OVER", janela.width/2 - 50, janela.height/2 - 45, size=60, color=(255,80,80), font_name="Impact")
    #janela.draw_text(f"SCORE: {placar.pontos:06d}", janela.width/2 - 50, janela.height/2 + 35, size=30, color=(255,255,255), font_name="Monaco")
    
    texto_score = f"SCORE: {placar.pontos:06d}"
    if entrada_nome.novo_record:
        texto_score += " - NOVO RECORDE!"
    janela.draw_text(texto_score, janela.width/2 - 50, janela.height/2 + 35, size=30, color=(255,255,255), font_name="Monaco")

    # Mostra as três primeiras colocações
    melhores = dados_ranking.melhores(3)
    y_ranking = janela.height/2 + 200
    for posicao, resultado in enumerate(melhores, start=1):
        nome = resultado["nome"][:12]
        pontuacao = resultado["pontuacao"]
        texto = f"{posicao}º  {nome:<12}  {pontuacao:06d} PTS"
        janela.draw_text(texto, janela.width/2 - 50, y_ranking, size=18, color=(150, 150, 150), font_name="Monaco")
        y_ranking += 35

    if not entrada_nome.resultado_salvo:
        nome_visivel = entrada_nome.nome + "_"
        janela.draw_text(f"DIGITE O NOME E PRESSIONE ENTER", janela.width/2 - 50, janela.height/2 + 80, size=18, color=(200,200,200), font_name="Monaco")
        janela.draw_text(f"NOME: {nome_visivel}", janela.width/2 - 50, janela.height/2 + 120, size=25, color=(255,210,70), font_name="Monaco", bold=True)

        entrada_nome.atualizar(teclado)
        return "game_over"
    
    janela.draw_text("ENTER: REINICIAR | ESC: MENU", janela.width/2 - 50, janela.height/2 + 80, size=20, color=(255,255,255), font_name="Monaco")
    janela.draw_text("RESULTADO SALVO!", janela.width/2 - 50, janela.height/2 + 120, size=22, color=(94,188,2), font_name="Monaco", bold=True)
    
    if teclado.key_down("ENTER"):
        return "reiniciar"
    elif teclado.key_down("ESC"):
        return "menu"

    return "game_over"