from PPlay.window import Window
from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.collision import Collision
import random

class Button:                                                   # Objeto botão - a partir de imagem
    def __init__(self, imagem):                                 # cria o botão e carrega a imagem
        self.sprite = Sprite(imagem)
    def desenhar(self):                                         # desenha o botao na janela
        self.sprite.draw()
    def centralizar(self, janela, y):                           # centraliza o botao na horizontal e permite definir a vertical
        self.sprite.x = janela.width/2 - self.sprite.width/2    # centro horizontal da janela
        self.sprite.y = y - self.sprite.height/2                # centro da coordenada vertical
    def cursor(self, mouse):                                    # verifica se o cursor esta no botao
        return mouse.is_over_object(self.sprite)

class Ship:                                                     # Objeto nave - controlada pelo jogador
    def __init__(self, imagem, janela, margem=5):               # cria a imagem e calcula seus limites horizontais
        self.sprite = Sprite(imagem)
        self.limite_esquerda = margem
        self.limite_direita = janela.width - self.sprite.width - margem
        self.sprite.x = janela.width/2 - self.sprite.width/2
        self.sprite.y = janela.height - self.sprite.height - 7*margem
    def limitar(self):                                          # impede que a nave saia da janela
        self.sprite.x = max(
            self.limite_esquerda, 
            min(self.sprite.x, self.limite_direita))
    def desenhar(self):                                         # desenha a nave
        self.sprite.draw()
    def trocar_imagem(self, imagem):
        x_atual = self.sprite.x
        y_atual = self.sprite.y
        self.sprite = Sprite(imagem)
        self.sprite.x = x_atual
        self.sprite.y = y_atual

class Monsters:
    def __init__(self, linhas, colunas, janela):
        self.linhas = linhas
        self.colunas = colunas
        self.matriz = []

        self.direcao = 1    # inicialmente vai pra direita, quando -1 vai pra esquerda

        # cada linha vai receber um monster (facil = 3 linahs, medio = 4 linhas, dificil = 5 linhas)
        self.imagens = [
            "imagens/monstros/monster_1.png",
            "imagens/monstros/monster_2.png",
            "imagens/monstros/monster_3.png",
            "imagens/monstros/monster_4.png",
            "imagens/monstros/monster_5.png"
        ]

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

            indice_imagem = linhas - linha - 1      # a linha da base da matriz recebe o monster_1
            imagem = self.imagens[indice_imagem]

            for coluna in range(colunas):
                monstro = Sprite(imagem)

                monstro.x = x_inicial + coluna * (largura + espacamento_x)
                monstro.y = y_inicial + linha * (altura + espacamento_y)

                linha_monstros.append(monstro)

            self.matriz.append(linha_monstros)

    def desenhar(self):
        for linha in self.matriz:
            for monstro in linha:
                monstro.draw()

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

        deslocamento = velocidade * self.direcao * delta

        # verificacao booleana da colisao
        colisao_esquerda = (faixa_esquerda + deslocamento <= 0)
        colisao_direita = (faixa_direita + deslocamento >= janela.width)

        if colisao_esquerda or colisao_direita:     # se a verificacao acima for True - choque com a parede
            self.direcao *= -1  # inverter
            down = monstros[0].height/2     # desce a metade da altura de um monstro

            for monstro in monstros:        # tds os monstros descem juntos
                monstro.y += down

            deslocamento = velocidade * self.direcao * delta    # desloca na nova direcao

        for monstro in monstros:        # movimento horizontal dos monstros
            monstro.x += deslocamento

    def colisaoPlayer(self, nave):
        for linha in self.matriz:
            for monstro in linha:
                faixa_inferior = monstro.y + monstro.height

                if faixa_inferior >= nave.sprite.y:
                    return True     # encerra o metodo e indica que o monstro chegou no player

        return False    # nenhum monstro chegou a nave

class Score:                                                    # Objeto para pontuação
    def __init__(self):
        self.pontos = 0
        self.multiplicador = 1
        self.sequencia = 0
    def adicionar(self, pontos):
        self.pontos += pontos * self.multiplicador
        self.sequencia += 1
    def ativar_dobro(self):
        self.multiplicador = 2
    def desativar_dobro(self):
        self.multiplicador = 1
    def zerar_sequencia(self):
        self.sequencia = 0
    def desenhar(self, janela, efeito_ativo=None, tempo_restante=0):
        fonte = "Monaco"
        texto = f"SCORE  {self.pontos:06d}"
        janela.draw_text(texto, 15, 10, size=20, color=(125, 190, 255), font_name=fonte, bold=True)   # Texto principal
        texto_bonus = {"escudo": "ESCUDO", "tiro_duplo": "TIRO DUPLO", "dobra_ponto": "2X PTS"}
        if efeito_ativo is not None:   # Indicador temporário
            aviso = (f"{texto_bonus[efeito_ativo]} | {tempo_restante:.1f}")
            janela.draw_text(aviso, 15, 35, size=20, color=(87, 145, 68), font_name=fonte, bold=True)

class InfosTela:
    def desenhar(self, janela, nivel):
        niveis = {1:"FÁCIL", 2:"MÉDIO", 3:"DIFÍCIL"}
        texto = f"DIFICULDADE: {niveis[nivel]} --  MOVER: A/D ou SETAS | ATIRAR: W ou ESPAÇO | MENU: ESC"
        janela.draw_text(texto, 15, janela.height - 25, size=15, color=(252,252,252), font_name="Monaco")

class Lifes:                                                    # Objeto para os caracoes de vida
    def __init__(self, imagem, janela, margem=15):
        self.sprite = Sprite(imagem)
        # self.sprite.x = janela.width/2 - self.sprite.width/2
        self.sprite.x = janela.width - self.sprite.width - margem
        self.sprite.y = margem
    def desenhar(self):
        self.sprite.draw()

def dificuldade(nivel=1, vel_monstros_base=40, vel_ataque_base=10, intervalo_ataque_base=3, recarga_tiro=0.4):
    vel_monstros = vel_monstros_base * nivel                           # aumenta a velocidade dos monstros de acordo com o nivel
    vel_ataque = vel_ataque_base * nivel                            # aumenta a velocidade de ataque de acordo com o nivel
    intervalo_ataque = intervalo_ataque_base / nivel                        # reduz o intervalo entre ataques de acordo com o nível
    intervalo_recarga = recarga_tiro * nivel
    linhas_monstros = nivel + 2
    if nivel == 3: colunas_monstros = 2 * nivel
    else: colunas_monstros = nivel + 4
    return (
        vel_monstros,
        vel_ataque,
        intervalo_ataque,
        intervalo_recarga,
        linhas_monstros,
        colunas_monstros
        )

def piscar(visivel, tempo, intervalo, delta):                   # Controle do efeito de piscar do objeto (bonus e nave)
    tempo += delta
    if tempo >= intervalo:                                      # condicao para alterar a visibilidade do objeto
        visivel = not visivel
        tempo = 0
    return tempo, visivel

def atirar(nave, imagem, desloc_x=0):
    tiro = Sprite(imagem)
    tiro.x = (nave.sprite.x + nave.sprite.width/2 - tiro.width/2 + desloc_x)
    tiro.y = nave.sprite.y - tiro.height
    return tiro


# Janela
janela = Window(1024, 768)
janela.set_title("Space Invaders")
placar = Score()

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

# Nave
nave = Ship("imagens/naves/ship.png", janela)
v_player = 400                                                  # Dinamica da nave

# Defaults
tela_atual = "menu"
nivel = 1   # dificuldade
(
    vel_monstros,
    vel_ataque,
    intervalo_ataque,
    intervalo_recarga,
    linhas_monstros,
    colunas_monstros
) = dificuldade(nivel)
infos_tela = InfosTela()

# Controles
teclado = Keyboard()
mouse = Mouse()

# Vidas
n_vidas = 3 # qtd inicial de vidas
vidas = Lifes(f"imagens/lifes/{n_vidas}_vidas.png", janela)

# Tiros e ataques
tiros = []
vel_tiro_player = 500
tempo_recarga = 0

# Monstros
monstros = Monsters(linhas_monstros, colunas_monstros, janela)

# Bonus
bonus = Sprite("imagens/ataques/bonus.png")
bonus.x = random.randint(0, int(janela.width - bonus.width))    # aparece em posicao aleatoria na tela
bonus.y = - bonus.height                                        # comecando acima da janela
bonus_ativo = True                                              # indica que o objeto esta em movimento
bonus_visivel = True                                            # indica a visibilidade (para funcao piscar)
vel_bonus = 250                                                 # velocidade de queda
tempo_pisca_bonus = 0                                           # tempo entre as piscadas
intervalo_pisca_bonus = 0.15                                    # intervalo entre as piscadas
tempo_bonus = 0                                                 # tempo para o proximo bonus aparecer
intervalo_bonus = random.randint(4,15)                          # sorteia o intervalo para o proximo bonus
efeitos = ["tiro_duplo", "escudo", "dobra_ponto"]               # possiveis efeitos do bonus
efeito_ativo = None                                             # nenhum efeito ativo inciialmente
tempo_efeito = 0
duracao_efeito = 5
efeito = random.choice(efeitos)                                 # sorteia um dos efeitos iniciais aleatoriamente
# tiro_duplo: cria dosi tiros por disparo 
# escudo: protege e a nave fica transparente
nave_visivel = True
tempo_pisca_nave = 0
intervalo_pisca_nave = 0.25
# dobra_ponto: usa tiro verde e define o multiplicador como 2
multiplicador_pts = 1

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
                tela_atual = "jogo"
            elif b_dificuldade.cursor(mouse):
                tela_atual = "dificuldade"
            elif b_sair.cursor(mouse):
                janela.close()


    elif tela_atual == "jogo":                                  # Executa a tela de jogo
        janela.set_background_color((33, 40, 48))

        if teclado.key_down("ESC"):                             # Volta para o menu principal de pressionar 'ESC'
            tela_atual = "menu"

        # Player
        nave.sprite.move_key_x(v_player)
        if teclado.key_pressed("A"):
            nave.sprite.x -= v_player * delta
        elif teclado.key_pressed("D"):
            nave.sprite.x += v_player * delta
        nave.limitar()                                          # Impede que a nave saia da tela
        tempo_recarga += delta
        if (teclado.key_pressed("SPACE") or teclado.key_pressed("W")) and tempo_recarga >= intervalo_recarga:                           # Detecta a intante que o 'SPACE' eh precionado
            tempo_recarga = 0
            if efeito_ativo == "dobra_ponto":
                imagem_tiro = "imagens/ataques/shoot2x.png"
            else:
                imagem_tiro = "imagens/ataques/shoot.png"
            if efeito_ativo == "tiro_duplo":
                tiro_esquerdo = atirar(nave, imagem_tiro, -15)
                tiro_direito = atirar(nave, imagem_tiro, 15)
                tiros.append(tiro_esquerdo)
                tiros.append(tiro_direito)
            else:
                tiro = atirar(nave, imagem_tiro)
                tiros.append(tiro)                              # Coloca um novo tiro na lista
        for tiro in tiros[:]:                                   # Percorre a lista de tiros copiada
            tiro.y -= vel_tiro_player * delta                   # Tiro para cima
            tiro.draw()
            if tiro.y +tiro.height <0:                          # Se o tiro sair da tela, ele eh removido da lista
                tiros.remove(tiro)

        # Monstros
        monstros.mover(janela, vel_monstros, delta)
        monstros.desenhar()
        if monstros.colisaoPlayer(nave):
            tela_atual = "game_over"

        # Bonus
        if bonus_ativo:                                         # Verifica se o bonus esta ativo
            bonus.y += vel_bonus * delta
            tempo_pisca_bonus, bonus_visivel = piscar(bonus_visivel, tempo_pisca_bonus, intervalo_pisca_bonus, delta)
            if bonus_visivel: bonus.draw()                      # se o bonus estiver visivel, desenha ele
            if bonus.y > janela.height:                         # Veririfica de o bonus saiu da janela inferior, desativa e reinicia o tempo de espera
                bonus_ativo = False
                tempo_bonus = 0
                intervalo_bonus = random.randint(4,15)          #sorteia o intervalo da prox vez que o bonus aparece
            elif Collision.collided(bonus,nave.sprite):           # Colisao do bonus com a nave
                efeito_ativo = random.choice(efeitos)
                tempo_efeito = 0
                bonus_ativo = False
                bonus_visivel = False
                tempo_bonus = 0
                if efeito_ativo == "escudo":
                    nave.trocar_imagem("imagens/naves/nave_escudo.png")
                elif efeito_ativo == "dobra_ponto":
                    placar.ativar_dobro()
        else:                                                   # bonus inativo
            tempo_bonus += delta
            if tempo_bonus >= intervalo_bonus:                  #vefirica se pode criar outro bonus
                bonus.x = random.randint(0, int(janela.width - bonus.width))
                bonus.y = -bonus.height
                bonus_ativo = True
                bonus_visivel = True
                tempo_pisca_bonus = 0

        if efeito_ativo is not None:
            tempo_efeito += delta
            if tempo_efeito >= duracao_efeito:
                if efeito_ativo == "escudo":
                    nave.trocar_imagem("imagens/naves/ship.png")
                elif efeito_ativo == "dobra_ponto":
                    placar.desativar_dobro()
                efeito_ativo = None
                tempo_efeito = 0

        tempo_restante = max(0, duracao_efeito - tempo_efeito)
        placar.desenhar(janela, efeito_ativo, tempo_restante)

        infos_tela.desenhar(janela,nivel)

        janela.draw_text(f"FPS: {janela.get_fps():.0f}", janela.width/2 - 35, 10, size=15, color=(255,255,255), font_name="Monaco")

        nave.desenhar()
        vidas.desenhar()

    elif tela_atual == "dificuldade":                           # Executa a tela de dificuldade
        janela.set_background_color((18,50,103))

        b_facil.desenhar()
        b_medio.desenhar()
        b_dificil.desenhar()

        if teclado.key_down("ESC"):                             # Volta para o menu principal de pressionar 'ESC'
            tela_atual = "menu"

        if mouse.button_down(1):                                # Detecta o instante de clique esquerdo em algum botao
            nivel_sel = None
            if b_facil.cursor(mouse):
                nivel_sel = 1
            elif b_medio.cursor(mouse):
                nivel_sel = 2
            elif b_dificil.cursor(mouse):
                nivel_sel = 3

            if nivel_sel is not None:
                nivel = nivel_sel                               # Atualiza o nível
                (
                    vel_monstros,
                    vel_ataque,
                    intervalo_ataque,
                    intervalo_recarga,
                    linhas_monstros,
                    colunas_monstros
                ) = dificuldade(nivel)
                tela_atual = "jogo"                             # Vai pra tela do jogo
                monstros = Monsters(linhas_monstros, colunas_monstros, janela)

    elif tela_atual == "game_over":
        janela.set_background_color((33, 40, 48))

        janela.draw_text("GAME OVER", janela.width/2, janela.height/2 - 45, size=60, color=(255,80,80), font_name="Impact")
        janela.draw_text("ENTER: REINICIAR | ESC: MENU", janela.width/2, janela.height/2 + 35, size=20, color=(255,255,255), font_name="Monaco")

        if teclado.key_down("ENTER"):
            monstros = Monsters(linhas_monstros, colunas_monstros, janela)
            janela_atual = "jogo"
        elif teclado.key_down("ESC"):
            tela_atual = "menu"

    janela.update()






# if Collision.collided(tiro_inimigo, nave.sprite):
#     if efeito_ativo != "escudo":
#         numero_vidas -= 1


# criar tela de game over