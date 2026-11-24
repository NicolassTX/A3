import math
import os
import random
import sys

import pygame

# Configuracoes gerais
LARGURA = 800
ALTURA = 600
FPS = 60
FUNDO = (8, 13, 32)
BRANCO = (240, 244, 255)
CIANO = (80, 225, 245)
CINZA = (125, 137, 158)
VERDE = (100, 245, 170)

pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Shooter")
relogio = pygame.time.Clock()
fonte_titulo = pygame.font.Font(None, 68)
fonte_grande = pygame.font.Font(None, 44)
fonte_normal = pygame.font.Font(None, 28)
fonte_pequena = pygame.font.Font(None, 21)

# A imagem fica dentro da pasta do projeto, independente de onde o jogo for aberto.
pasta_projeto = os.path.dirname(os.path.abspath(__file__))
caminho_nave = os.path.join(pasta_projeto, "assets", "nave.png")
try:
    imagem_original = pygame.image.load(caminho_nave).convert_alpha()
    imagem_nave = pygame.transform.smoothscale(imagem_original, (66, 66))
except (pygame.error, FileNotFoundError):
    imagem_nave = None

# Cada estrela guarda posicao, tamanho e velocidade.
estrelas = [
    [random.randrange(LARGURA), random.randrange(ALTURA),
     random.choice((1, 1, 2)), random.randint(18, 55)]
    for _ in range(90)
]

estado = "MENU"
rodando = True
pontuacao = 0
vidas = 3
jogador_x = LARGURA // 2
jogador_y = ALTURA - 65
projeteis = []
asteroides = []
itens = []
tempo_spawn = 0.0
tempo_disparo = 0.0
tempo_invulneravel = 0.0
tempo_tiro_rapido = 0.0


def desenhar_texto(texto, fonte, cor, x, y):
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect(center=(x, y))
    tela.blit(imagem, retangulo)


def desenhar_fundo(dt):
    tela.fill(FUNDO)
    for estrela in estrelas:
        estrela[1] += estrela[3] * dt
        if estrela[1] > ALTURA:
            estrela[0] = random.randrange(LARGURA)
            estrela[1] = 0
        pygame.draw.circle(tela, (170, 190, 220),
                           (int(estrela[0]), int(estrela[1])), estrela[2])


def desenhar_nave(x, y):
    if imagem_nave:
        retangulo = imagem_nave.get_rect(center=(int(x), int(y)))
        tela.blit(imagem_nave, retangulo)
    else:
        # Desenho reserva caso a imagem seja removida acidentalmente.
        pontos = [(int(x), int(y - 24)), (int(x - 20), int(y + 18)),
                  (int(x), int(y + 9)), (int(x + 20), int(y + 18))]
        pygame.draw.polygon(tela, CIANO, pontos)
        pygame.draw.polygon(tela, BRANCO, pontos, 2)


def desenhar_menu(dt):
    desenhar_fundo(dt)
    desenhar_texto("SPACE SHOOTER", fonte_titulo, CIANO, LARGURA // 2, 145)
    desenhar_nave(LARGURA // 2, 275)
    desenhar_texto("Destrua asteroides, colete energia e sobreviva!",
                   fonte_normal, BRANCO, LARGURA // 2, 355)
    desenhar_texto("ENTER - iniciar", fonte_normal, VERDE, LARGURA // 2, 420)
    desenhar_texto("Mover: A/D ou setas   |   Disparar: ESPACO",
                   fonte_pequena, BRANCO, LARGURA // 2, 465)
    desenhar_texto("P - pausar   |   ESC - sair", fonte_pequena, CINZA,
                   LARGURA // 2, 495)


def desenhar_asteroide(asteroide):
    x = int(asteroide["x"])
    y = int(asteroide["y"])
    raio = asteroide["raio"]
    pontos = [(int(x + dx), int(y + dy)) for dx, dy in asteroide["pontos"]]
    cor = (145, 153, 172) if raio >= 24 else (115, 130, 155)
    pygame.draw.polygon(tela, cor, pontos)
    pygame.draw.polygon(tela, (65, 76, 98), pontos, 2)
    pygame.draw.circle(tela, (75, 86, 108), (x - raio // 3, y - raio // 4),
                       max(2, raio // 5))
    pygame.draw.circle(tela, (75, 86, 108), (x + raio // 3, y + raio // 3),
                       max(2, raio // 7))


def desenhar_jogo(dt=0):
    desenhar_fundo(dt)

    for projetil in projeteis:
        retangulo = pygame.Rect(int(projetil["x"] - 3), int(projetil["y"]), 6, 16)
        pygame.draw.rect(tela, CIANO, retangulo, border_radius=3)
        pygame.draw.rect(tela, BRANCO, retangulo.inflate(-3, -5), border_radius=2)

    for asteroide in asteroides:
        desenhar_asteroide(asteroide)

    # O item de energia e mostrado como um cristal brilhante.
    for item in itens:
        x, y = int(item["x"]), int(item["y"])
        pontos = [(x, y - 11), (x + 9, y), (x, y + 11), (x - 9, y)]
        pygame.draw.polygon(tela, VERDE, pontos)
        pygame.draw.polygon(tela, BRANCO, pontos, 2)

    mostrar_nave = tempo_invulneravel <= 0 or int(tempo_invulneravel * 10) % 2 == 0
    if mostrar_nave:
        desenhar_nave(jogador_x, jogador_y)
    if tempo_invulneravel > 0:
        pygame.draw.circle(tela, CIANO, (int(jogador_x), int(jogador_y)), 35, 2)

    nivel = min(10, 1 + pontuacao // 100)
    pygame.draw.line(tela, (40, 54, 82), (0, 50), (LARGURA, 50), 1)
    tela.blit(fonte_normal.render(f"Pontos: {pontuacao}", True, BRANCO), (18, 14))
    desenhar_texto(f"NIVEL {nivel}", fonte_normal, CIANO, LARGURA // 2, 27)
    texto_vidas = fonte_normal.render(f"Vidas: {vidas}", True, BRANCO)
    tela.blit(texto_vidas, (LARGURA - texto_vidas.get_width() - 18, 14))

    if tempo_tiro_rapido > 0:
        restante = math.ceil(tempo_tiro_rapido)
        desenhar_texto(f"TIRO RAPIDO: {restante}s", fonte_pequena, VERDE,
                       LARGURA // 2, ALTURA - 24)


def desenhar_game_over(dt):
    desenhar_fundo(dt)
    desenhar_texto("GAME OVER", fonte_titulo, CIANO, LARGURA // 2, 205)
    desenhar_texto(f"Pontuacao final: {pontuacao}", fonte_grande, BRANCO,
                   LARGURA // 2, 280)
    desenhar_texto("ENTER - jogar novamente", fonte_normal, VERDE,
                   LARGURA // 2, 365)
    desenhar_texto("M - voltar ao menu    ESC - sair", fonte_pequena, CINZA,
                   LARGURA // 2, 410)


def desenhar_pausa():
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    camada.fill((3, 7, 18, 185))
    tela.blit(camada, (0, 0))
    desenhar_texto("JOGO PAUSADO", fonte_titulo, CIANO, LARGURA // 2, 260)
    desenhar_texto("Pressione P ou ENTER para continuar", fonte_normal,
                   BRANCO, LARGURA // 2, 325)


def reiniciar_jogo():
    global pontuacao, vidas, jogador_x, projeteis, asteroides, itens
    global tempo_spawn, tempo_disparo, tempo_invulneravel, tempo_tiro_rapido
    pontuacao = 0
    vidas = 3
    jogador_x = LARGURA // 2
    projeteis = []
    asteroides = []
    itens = []
    tempo_spawn = 0.0
    tempo_disparo = 0.0
    tempo_invulneravel = 0.0
    tempo_tiro_rapido = 0.0


def criar_asteroide(nivel):
    raio = random.choice((14, 20, 27))
    pontos = []
    for indice in range(10):
        angulo = indice * (2 * math.pi / 10)
        distancia = raio * random.uniform(0.78, 1.12)
        pontos.append((math.cos(angulo) * distancia,
                       math.sin(angulo) * distancia))
    # Os asteroides surgem em uma faixa central para concentrar a acao.
    return {
        "x": random.randint(180 + raio, 620 - raio),
        "y": -raio,
        "raio": raio,
        "velocidade": random.randint(100, 155) + (nivel - 1) * 12,
        "pontos": pontos,
    }


def atualizar_jogo(dt, teclas):
    global jogador_x, pontuacao, vidas, tempo_spawn
    global tempo_disparo, tempo_invulneravel, tempo_tiro_rapido, estado

    nivel = min(10, 1 + pontuacao // 100)
    velocidade_nave = 370
    direcao = 0
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        direcao -= 1
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        direcao += 1
    jogador_x += direcao * velocidade_nave * dt
    jogador_x = max(35, min(LARGURA - 35, jogador_x))

    # O bonus reduz o intervalo entre disparos por alguns segundos.
    tempo_disparo = max(0.0, tempo_disparo - dt)
    tempo_tiro_rapido = max(0.0, tempo_tiro_rapido - dt)
    intervalo_disparo = 0.12 if tempo_tiro_rapido > 0 else 0.28
    if teclas[pygame.K_SPACE] and tempo_disparo <= 0:
        projeteis.append({"x": jogador_x, "y": jogador_y - 28})
        tempo_disparo = intervalo_disparo

    # Atualiza os disparos e verifica se atingiram algum asteroide.
    for projetil in projeteis[:]:
        projetil["y"] -= 540 * dt
        retangulo_projetil = pygame.Rect(int(projetil["x"] - 3),
                                         int(projetil["y"]), 6, 16)
        if projetil["y"] < -20:
            projeteis.remove(projetil)
            continue
        for asteroide in asteroides[:]:
            raio = asteroide["raio"]
            retangulo_asteroide = pygame.Rect(
                int(asteroide["x"] - raio), int(asteroide["y"] - raio),
                raio * 2, raio * 2
            )
            if retangulo_projetil.colliderect(retangulo_asteroide):
                projeteis.remove(projetil)
                asteroides.remove(asteroide)
                pontuacao += 10
                if random.random() < 0.18:
                    itens.append({"x": asteroide["x"], "y": asteroide["y"]})
                break

    # A cada 100 pontos o nivel sobe e os asteroides ficam mais frequentes e rapidos.
    intervalo_spawn = max(0.42, 0.95 - (nivel - 1) * 0.06)
    tempo_spawn += dt
    if tempo_spawn >= intervalo_spawn:
        asteroides.append(criar_asteroide(nivel))
        tempo_spawn = 0.0

    # Itens coletaveis caem lentamente; pegar um ativa tiro rapido por 6 segundos.
    retangulo_nave = pygame.Rect(jogador_x - 21, jogador_y - 23, 42, 46)
    for item in itens[:]:
        item["y"] += 115 * dt
        retangulo_item = pygame.Rect(int(item["x"] - 10), int(item["y"] - 10), 20, 20)
        if retangulo_item.colliderect(retangulo_nave):
            itens.remove(item)
            tempo_tiro_rapido = 6.0
        elif item["y"] > ALTURA + 15:
            itens.remove(item)

    tempo_invulneravel = max(0.0, tempo_invulneravel - dt)
    for asteroide in asteroides[:]:
        asteroide["y"] += asteroide["velocidade"] * dt
        raio = asteroide["raio"]
        retangulo_asteroide = pygame.Rect(
            int(asteroide["x"] - raio), int(asteroide["y"] - raio),
            raio * 2, raio * 2
        )
        if asteroide["y"] - raio > ALTURA:
            # Deixar um asteroide escapar tambem custa uma vida.
            asteroides.remove(asteroide)
            if tempo_invulneravel <= 0:
                vidas -= 1
                tempo_invulneravel = 1.0
                if vidas <= 0:
                    estado = "GAME_OVER"
                    break
        elif tempo_invulneravel <= 0 and retangulo_nave.colliderect(retangulo_asteroide):
            asteroides.remove(asteroide)
            vidas -= 1
            tempo_invulneravel = 1.0
            if vidas <= 0:
                estado = "GAME_OVER"
                break


while rodando:
    dt = min(relogio.tick(FPS) / 1000.0, 0.05)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
            elif estado == "MENU" and evento.key == pygame.K_RETURN:
                reiniciar_jogo()
                estado = "JOGANDO"
            elif estado == "JOGANDO" and evento.key == pygame.K_p:
                estado = "PAUSADO"
            elif estado == "PAUSADO" and evento.key in (pygame.K_p, pygame.K_RETURN):
                estado = "JOGANDO"
            elif estado == "GAME_OVER":
                if evento.key == pygame.K_RETURN:
                    reiniciar_jogo()
                    estado = "JOGANDO"
                elif evento.key == pygame.K_m:
                    estado = "MENU"

    if estado == "MENU":
        desenhar_menu(dt)
    elif estado == "JOGANDO":
        atualizar_jogo(dt, pygame.key.get_pressed())
        desenhar_jogo(dt)
    elif estado == "PAUSADO":
        desenhar_jogo()
        desenhar_pausa()
    else:
        desenhar_game_over(dt)

    pygame.display.flip()

pygame.quit()
sys.exit()
