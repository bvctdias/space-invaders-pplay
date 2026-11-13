from PPlay.sprite import Sprite

class Lifes:                                                    # Objeto para os caracoes de vida
    def __init__(self, janela, vidas=3, margem=15):
        self.janela = janela
        self.vidas = vidas
        self.margem = margem
        self.sprite = None

        self.atualizar_imagem()


    def atualizar_imagem(self):
        if self.vidas <= 0:
            self.sprite = None
            return

        self.sprite = Sprite(f"imagens/lifes/{self.vidas}_vidas.png")
        # self.sprite.x = janela.width/2 - self.sprite.width/2
        self.sprite.x = self.janela.width - self.sprite.width - self.margem
        self.sprite.y = self.margem


    def perder_vida(self):
        if self.vidas > 0:
            self.vidas -= 1
            self.atualizar_imagem()
        return self.vidas <= 0


    def ganhar_vida(self):
        if self.vidas >= 3:
            return False

        self.vidas += 1
        self.atualizar_imagem()

        return True

    
    def desenhar(self):
        if self.sprite is not None:
            self.sprite.draw()

