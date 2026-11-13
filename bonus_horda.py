class BonusHorda:
    def __init__(self, limite_tempo=60, pontos=500, duracao_aviso=3):
        self.limite_tempo = limite_tempo
        self.pontos = pontos
        self.duracao_aviso = duracao_aviso

        self.tempo_horda = 0
        self.tempo_aviso = 0
        self.recebeu_bonus = False


    def atualizar(self, delta):
        self.tempo_horda += delta

        if self.tempo_aviso > 0:
            self.tempo_aviso -= delta

            if self.tempo_aviso <= 0:
                self.tempo_aviso = 0
                self.recebeu_bonus = False


    def concluir_horda(self, placar):
        if self.tempo_horda <= self.limite_tempo:
            placar.adicionar_bonus(self.pontos)
            self.recebeu_bonus = True
            self.tempo_aviso = self.duracao_aviso

        self.tempo_horda = 0


    def aviso_ativo(self):
        return self.recebeu_bonus and self.tempo_aviso > 0


    def desenhar(self, janela):
        if self.aviso_ativo():
            texto = f"MISSÃO COMPLETA EM MENOS DE 1 MIN\n+{self.pontos} PTS"

            janela.draw_text(
                texto,
                15,
                35,
                size=20,
                color=(255, 210, 70),
                font_name="Monaco",
                bold=True
            )
