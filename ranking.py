from datetime import datetime
from pathlib import Path


class Ranking:
    def __init__(self, nome_arquivo="ranking.txt"):
        pasta_projeto = Path(__file__).resolve().parent
        self.caminho_arquivo = pasta_projeto / nome_arquivo


    def salvar(self, nome, pontuacao):
        nome = nome.strip().upper().replace(";", "")

        if not nome:
            return False

        data = datetime.now().strftime("%d/%m/%Y")

        with open(self.caminho_arquivo, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{nome};{int(pontuacao)};{data}\n")

        return True


    def carregar(self):
        resultados = []

        if not self.caminho_arquivo.exists():
            return resultados

        with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")

                # Ignora linhas vazias ou incompletas.
                if len(dados) != 3:
                    continue

                nome, pontuacao, data = dados

                try:
                    pontuacao = int(pontuacao)
                except ValueError:
                    continue

                resultados.append({"nome": nome, "pontuacao": pontuacao, "data": data})

        resultados.sort(key=lambda resultado: resultado["pontuacao"], reverse=True)

        return resultados


    def melhores(self, quantidade=5):
        return self.carregar()[:quantidade]


    def desenhar(self, janela):
        fonte = "Monaco"
        melhores = self.melhores(5)

        janela.draw_text("RANKING", 15, 90, size=45, color=(94, 188, 2), font_name="Impact")

        janela.draw_text("#    NOME          PONTOS      DATA", 15, 180, size=20, color=(125, 190, 255), font_name=fonte, bold=True)

        if not melhores:
            janela.draw_text("NENHUM RESULTADO SALVO", 15, 245, size=20, color=(200, 200, 200), font_name=fonte)
            return

        y = 225

        for posicao, resultado in enumerate(melhores, start=1):
            nome = resultado["nome"][:12]
            pontuacao = resultado["pontuacao"]
            data = resultado["data"]

            texto = (
                f"{posicao:02d}   "
                f"{nome:<12}  "
                f"{pontuacao:06d}      "
                f"{data}"
            )

            janela.draw_text(texto, 15, y, size=20, color=(255, 255, 255), font_name=fonte)

            y += 45


class EntradaNomeRanking:
    def __init__(self, ranking, pontuacao, limite_nome=12):
        self.ranking = ranking
        self.pontuacao = pontuacao
        self.limite_nome = limite_nome

        self.nome = ""
        self.resultado_salvo = False

        melhor_resultado = self.ranking.melhores(1)
        # para empate nao ser considerado novo recorde
        if not melhor_resultado:
            self.novo_record = True
        else:
            maior_pontuacao = melhor_resultado[0]["pontuacao"]
            self.novo_record = self.pontuacao > maior_pontuacao


    def atualizar(self, teclado):
        if self.resultado_salvo:
            return "rank"

        teclas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

        for tecla in teclas:
            if teclado.key_down(tecla):
                if len(self.nome) < self.limite_nome:
                    self.nome += tecla

        if teclado.key_down("SPACE"):
            if self.nome and len(self.nome) < self.limite_nome:
                self.nome += " "

        # if teclado.key_down("BACKSPACE"):
        #     self.nome = self.nome[:-1]
        # PPlay nao tem backspace

        if teclado.key_down("ENTER") and self.nome.strip():
            self.resultado_salvo = self.ranking.salvar(self.nome, self.pontuacao)

            if self.resultado_salvo:
                return "rank"

        return "digitar_nome"


    # def desenhar(self, janela):
    #     janela.set_background_color((33, 40, 48))

    #     janela.draw_text("FIM DE JOGO", janela.width/2 - 170, 170, size=50, color=(255, 80, 80), font_name="Impact")
    #     janela.draw_text(f"SCORE: {self.pontuacao:06d}", janela.width/2 - 120, 260, size=25, color=(255, 255, 255), font_name="Monaco", bold=True)

    #     nome_visivel = self.nome + "_"

    #     janela.draw_text(f"NOME: {nome_visivel}", janela.width/2 - 180, 330, size=25, color=(255, 210, 70), font_name="Monaco", bold=True)
    #     janela.draw_text("DIGITE SEU NOME E PRESSIONE ENTER", janela.width/2 - 260, 390, size=18, color=(200, 200, 200), font_name="Monaco")


def tela_entrada_nome(janela, teclado, entrada_nome):
    entrada_nome.desenhar(janela)
    return entrada_nome.atualizar(teclado)


# def tela_ranking(janela, teclado, ranking):
#     janela.set_background_color((112, 13, 13))
#     ranking.desenhar(janela)

#     janela.draw_text("MENU PRINCIPAL: ESC", 15, janela.height - 25, size=15, color=(252, 252, 252), font_name="Monaco")

#     if teclado.key_down("ESC"):
#         return "menu"

#     return "rank"
