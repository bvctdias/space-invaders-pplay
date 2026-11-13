class Score:                                                    # Objeto para pontuação
    def __init__(self):
        self.pontos = 0
        self.multiplicador = 1
        self.sequencia = 0
        self.texto_aviso = ""
        self.tempo_aviso = 0
        self.duracao_aviso = 2.5
        self.cor_score = (125, 190, 255)
        self.cor_aviso = self.cor_score
    
    def adicionar(self, pontos=10, aviso=None):
        pontos_recebidos = pontos * self.multiplicador
        self.pontos += pontos_recebidos
        self.sequencia += 1

        if aviso is not None:
            self.avisar(aviso, self.cor_score)

    def avisar(self, texto, cor, separador=True):
        if separador:
            self.texto_aviso = f" | {texto}"
        else:
            self.texto_aviso = f" {texto}"
        self.cor_aviso = cor
        self.tempo_aviso = self.duracao_aviso

    def atualizar(self, delta):
        if self.tempo_aviso > 0:
            self.tempo_aviso -= delta

            if self.tempo_aviso <= 0:
                self.tempo_aviso = 0
                self.texto_aviso = ""

    def adicionar_bonus(self, pontos):
        self.pontos += pontos
    
    def ativar_dobro(self):
        self.multiplicador = 2
    
    def desativar_dobro(self):
        self.multiplicador = 1
    
    def zerar_sequencia(self):
        self.sequencia = 0
    
    def desenhar(self, janela, efeito_ativo=None, tempo_restante=0):
        fonte = "Monaco"
        texto = f"SCORE  {self.pontos:06d}"
        janela.draw_text(texto, 15, 10, size=20, color=self.cor_score, font_name=fonte, bold=True)   # Texto principal
        texto_bonus = {"escudo": "ESCUDO", "tiro_duplo": "TIRO DUPLO", "dobra_ponto": "2X PTS", "desafio_monstro": "DESAFIO 5X"}
        
        if efeito_ativo is not None:   # Indicador temporário
            aviso = (f"{texto_bonus[efeito_ativo]} | {tempo_restante:.1f}")
            janela.draw_text(aviso, 15, 35, size=20, color=(87, 145, 68), font_name=fonte, bold=True)

        if self.tempo_aviso > 0:
            janela.draw_text(self.texto_aviso, 175, 10, size=20, color=self.cor_aviso, font_name=fonte, bold=True)
