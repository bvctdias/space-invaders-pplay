from PPlay.sprite import Sprite

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