from PPlay.sprite import Sprite

from funcoes import atirar, piscar

'''
A classe Player pode controlar
- a nave (Ship)
- movimento
- tiros
- tempo de recarga
- colisao dos tiros com os mosntros
- pontuaçao
- controla o dano, reaparecimento e invulnerabilidade
'''

class Ship:                                                     # Objeto nave - controlada pelo jogador
    def __init__(self, imagem, janela, margem=5):               # cria a imagem e calcula seus limites horizontais
        self.sprite = Sprite(imagem)
        
        self.limite_esquerda = margem
        self.limite_direita = janela.width - self.sprite.width - margem
        
        self.sprite.x = janela.width/2 - self.sprite.width/2
        self.sprite.y = janela.height - self.sprite.height - 7 * margem

    
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



class Player:
    def __init__(self, janela, intervalo_recarga):
        self.nave = Ship("imagens/naves/ship.png", janela)

        self.v_player = 400
        self.vel_tiro_player = 500

        self.tiros = []

        self.tempo_recarga = 0
        self.intervalo_recarga = intervalo_recarga

        self.janela = janela

        self.invulneravel = False
        self.tempo_invulneravel = 0
        self.duracao_invulneravel = 2

        self.visivel = True
        self.tempo_pisca = 0
        self.intervalo_pisca = 0.15

        self.escudo_ativo = False


    @property
    def sprite(self):
        return self.nave.sprite


    def atualizar(self, delta, teclado, efeito_ativo, monstros, placar):
        self.atualizar_invulnerabilidade(delta)
        
        # movimento pelas setas
        self.nave.sprite.move_key_x(self.v_player)
        
        # movimento por A e D
        if teclado.key_pressed("A"):
            self.nave.sprite.x -= self.v_player * delta
        elif teclado.key_pressed("D"):
            self.nave.sprite.x += self.v_player * delta

        # impede que a nave saia da tela
        self.nave.limitar()

        # recarga do tiro
        self.tempo_recarga += delta

        shoot = (teclado.key_pressed("SPACE") or teclado.key_pressed("W"))

        if shoot and (self.tempo_recarga >= self.intervalo_recarga):
            self.tempo_recarga = 0

            if efeito_ativo == "dobra_ponto":
                imagem_tiro = ("imagens/ataques/shoot2x.png")
            else:
                imagem_tiro = ("imagens/ataques/shoot.png")

            if efeito_ativo == "tiro_duplo":
                tiro_esquerdo = atirar(self.nave, imagem_tiro, -15)
                tiro_direito = atirar(self.nave, imagem_tiro, 15)
                self.tiros.append(tiro_esquerdo)
                self.tiros.append(tiro_direito)
            else:
                tiro = atirar(self.nave, imagem_tiro)
                self.tiros.append(tiro)

        # atualizacao dos tiros
        for tiro in self.tiros[:]:
            tiro.y -= (self.vel_tiro_player * delta)

            pontos = monstros.colisaoTiro(tiro)
            if pontos is not None:
                self.tiros.remove(tiro)
                if pontos > 0:
                    pontos_recebidos = pontos * placar.multiplicador
                    placar.adicionar(pontos)

                    if monstros.ultimo_abate_boss:
                        placar.avisar(f"+{pontos_recebidos} PTS", (255, 80, 80), separador=False)
                    elif monstros.ultimo_abate_desafio:
                        placar.avisar(f"+{pontos_recebidos} PTS", (255, 80, 80), separador=False)
                continue

            if tiro.y + tiro.height < 0:
                self.tiros.remove(tiro)
                continue


    def receber_dano(self):
        # escudo e invulnerabilidade impedem o dano
        if self.escudo_ativo or self.invulneravel:
            return False

        # reposicionar nave no centro se sofrer dano
        self.nave.sprite.x = self.janela.width/2 - self.nave.sprite.width/2

        self.invulneravel = True
        self.tempo_invulneravel = 0
        self.tempo_pisca = 0
        self.visivel = True

        return True # para descontar uma vida


    def atualizar_invulnerabilidade(self, delta):
        if not self.invulneravel:
            return

        self.tempo_invulneravel += delta

        self.tempo_pisca, self.visivel = piscar(self.visivel, self.tempo_pisca, self.intervalo_pisca, delta)

        if self.tempo_invulneravel >= self.duracao_invulneravel:
            self.invulneravel = False
            self.tempo_invulneravel = 0
            self.visivel = True


    def desenhar(self):
        for tiro in self.tiros:
            tiro.draw()

        if self.visivel:
            self.nave.desenhar()


    def trocar_imagem(self, imagem):
        self.nave.trocar_imagem(imagem)
