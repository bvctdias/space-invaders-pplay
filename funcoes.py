from PPlay.sprite import Sprite

def dificuldade(nivel=1, vel_monstros_base=25, vel_ataque_base=120, intervalo_ataque_base=5, recarga_tiro=0.3):
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