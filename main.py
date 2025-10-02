import pygame
import random

# --- INICIALIZAÇÃO E CONFIGURAÇÕES GERAIS ---
pygame.init()

clock = pygame.time.Clock()
FPS = 60

LARGURA = 1280
ALTURA = 720 + 200

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('LOTR Battle')

fonte = pygame.font.SysFont('Times New Roman', 32)
fonte_grande = pygame.font.SysFont('Times New Roman', 72)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
branco = (255, 255, 255)

# --- CARREGAMENTO DE IMAGENS ---
background_img = pygame.image.load('imagens/Fundo/Battleground1_redimensionado.png').convert_alpha()
painel_img = pygame.image.load('imagens/painel/painel_redimensionado.png').convert_alpha()
arrow_img = pygame.image.load('imagens/Seleção/arrow.png').convert_alpha()
vitoria_img = pygame.image.load('imagens/Fundo/tela_vitória.png').convert_alpha()
derrota_img = pygame.image.load('imagens/Fundo/tela_derrota.png').convert_alpha()
menu_bg_img = pygame.image.load('imagens/Fundo/menu.png').convert_alpha()


# --- CLASSES E FUNÇÕES ---

def desenha_textos(texto, fonte, texto_cor, x, y):
    img = fonte.render(texto, True, texto_cor)
    tela.blit(img, (x, y))

def desenha_bg():
    tela.blit(background_img, (0, 0))
    
def desenha_painel():
    tela.blit(painel_img, (0, ALTURA - 200))
    for i, heroi in enumerate(equipe_do_jogador):
        desenha_textos(f'{heroi.nome.upper()} | VIDA: {int(heroi.vida)}/{heroi.vida_max}', fonte, verde, 100, ALTURA - 200 + 30 + (i * 50))
    
    lutador_da_vez = lista_lutadores[lutador_atual]
    desenha_textos(f"TURNO DE {lutador_da_vez.nome.upper()}", fonte, branco, 450, ALTURA - 200 + 30)
    if lutador_da_vez in equipe_do_jogador and estado_batalha == 'selecionando_acao':
        x_acao, y_acao_base = 470, ALTURA - 200 + 80
        desenha_textos('ATACAR', fonte, vermelho, x_acao, y_acao_base)
        desenha_textos('DEFENDER', fonte, vermelho, x_acao, y_acao_base + 40)
        if acao_selecionada == 0: tela.blit(arrow_img, (x_acao - 40, y_acao_base))
        elif acao_selecionada == 1: tela.blit(arrow_img, (x_acao - 40, y_acao_base + 40))

    for i, inimigo in enumerate(lista_inimigos):
        desenha_textos(f'{inimigo.nome.upper()} | VIDA: {int(inimigo.vida)}/{inimigo.vida_max}', fonte, vermelho, 800, ALTURA - 200 + 30 + (i * 50))

# --- NOVA FUNÇÃO PARA DESENHAR O MENU (VERSÃO CENTRALIZADA) ---
def desenha_menu():
    tela.blit(menu_bg_img, (0, 0))
    desenha_textos('ESCOLHA SUA EQUIPE', fonte_grande, branco, LARGURA // 2 - 350, 50)
    
    y_pos_herois = 450 # Posição Y dos heróis ajustada
    
    # Mostra os heróis disponíveis
    for i, heroi in enumerate(personagens_disponiveis):
        x_pos = 200 + i * 250
        tela.blit(heroi.image, (x_pos, y_pos_herois))

        # Lógica para centralizar o texto do nome
        texto_nome = fonte.render(heroi.nome, True, branco)
        texto_x = x_pos + (heroi.image.get_width() / 2) - (texto_nome.get_width() / 2)
        texto_y = y_pos_herois + heroi.image.get_height() + 15
        tela.blit(texto_nome, (texto_x, texto_y))

        # Desenha o cursor de seleção
        if i == cursor_menu:
            pygame.draw.rect(tela, branco, (x_pos - 10, y_pos_herois - 10, heroi.image.get_width() + 20, heroi.image.get_height() + 20), 3)

    # Mostra a equipe sendo montada
    desenha_textos('Equipe selecionada:', fonte, branco, 100, 750)
    for i, heroi in enumerate(equipe_do_jogador):
        desenha_textos(heroi.nome, fonte, verde, 350 + i * 150, 750)


class Personagem():
    def __init__(self, x, y, nome, vida_max, força, defesa, velocidade, escala_img=6):
        self.nome = nome
        self.vida_max = vida_max
        self.vida = vida_max
        self.força = força
        self.defesa = defesa
        self.velocidade = velocidade
        self.defendendo = False
        self.vivo = True
        img = pygame.image.load(f'imagens/Personagens/{self.nome}/0.png').convert_alpha()
        # Ajustei a classe para que a escala seja um parâmetro, tornando-a mais limpa
        self.image = pygame.transform.scale(img, (int(img.get_width() / escala_img), int(img.get_height() / escala_img)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def atacar(self, alvo):
        defesa_alvo = alvo.defesa
        if alvo.defendendo: defesa_alvo *= 2
        dano = self.força * (50 / (50 + defesa_alvo))
        alvo.vida -= dano
        if alvo.vida < 1:
            alvo.vida = 0
            alvo.vivo = False

    def defender(self):
        self.defendendo = True

    def draw(self):
        tela.blit(self.image, self.rect)
        if not self.vivo:
            cinza_transparente = (50, 50, 50, 150)
            superficie_cinza = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            superficie_cinza.fill(cinza_transparente)
            tela.blit(superficie_cinza, self.rect.topleft)

# --- CRIAÇÃO DE TODAS AS INSTÂNCIAS DE PERSONAGENS ---
Aragorn = Personagem(350, 430, 'Aragorn', 250, 30, 25, 12)
Frodo = Personagem(280, 500, 'Frodo', 120, 10, 15, 20, escala_img=9)
Legolas = Personagem(200, 430, 'Legolas', 160, 42, 15, 18)
Gandalf = Personagem(250, 380, 'Gandalf', 200, 40, 20, 8)
Sauron = Personagem(900, 360, 'Sauron', 450, 50, 30, 10, escala_img=3)
Nazgul1 = Personagem(1100, 300, 'Nazgûl', 180, 28, 20, 16)
Nazgul2 = Personagem(1100, 550, 'Nazgûl', 180, 28, 20, 16)

# --- VARIÁVEIS DE ESTADO DO JOGO ---
estado_do_jogo = 'menu'
personagens_disponiveis = [Aragorn, Legolas, Gandalf, Frodo]
equipe_do_jogador = []
cursor_menu = 0
lista_inimigos = [Sauron, Nazgul1, Nazgul2]

lista_lutadores, lutador_atual, estado_batalha, acao_selecionada, alvo_selecionado, jogo_acabou, vitoria = [], 0, 'selecionando_acao', 0, 0, False, 0

# --- LOOP PRINCIPAL DO JOGO ---
rodando = True
while rodando:
    clock.tick(FPS)
    
    if estado_do_jogo == 'menu':
        desenha_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: rodando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: cursor_menu = (cursor_menu + 1) % len(personagens_disponiveis)
                if event.key == pygame.K_LEFT: cursor_menu = (cursor_menu - 1) % len(personagens_disponiveis)
                if event.key == pygame.K_z:
                    heroi_selecionado = personagens_disponiveis[cursor_menu]
                    if heroi_selecionado not in equipe_do_jogador and len(equipe_do_jogador) < 3:
                        equipe_do_jogador.append(heroi_selecionado)
                    if len(equipe_do_jogador) == 3:
                        estado_do_jogo = 'batalha'
                        lista_lutadores = equipe_do_jogador + lista_inimigos
                        lista_lutadores.sort(key=lambda x: x.velocidade, reverse=True)

    elif estado_do_jogo == 'batalha':
        desenha_bg()
        desenha_painel()
        for personagem in equipe_do_jogador + lista_inimigos: personagem.draw()

        if estado_batalha == 'selecionando_alvo':
            alvos_vivos = [i for i in lista_inimigos if i.vivo]
            if alvos_vivos:
                alvo = alvos_vivos[alvo_selecionado % len(alvos_vivos)]
                tela.blit(arrow_img, (alvo.rect.centerx - 45, alvo.rect.y))

        if not jogo_acabou:
            lutador_da_vez = lista_lutadores[lutador_atual]
            if lutador_da_vez.vivo:
                lutador_da_vez.defendendo = False
                if lutador_da_vez in equipe_do_jogador:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: rodando = False
                        if event.type == pygame.KEYDOWN:
                            if estado_batalha == 'selecionando_acao':
                                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: acao_selecionada = (acao_selecionada + 1) % 2
                                if event.key == pygame.K_z:
                                    if acao_selecionada == 0:
                                        estado_batalha = 'selecionando_alvo'
                                        alvos_vivos_check = [i for i in lista_inimigos if i.vivo]
                                        if alvo_selecionado >= len(alvos_vivos_check): alvo_selecionado = 0
                                    if acao_selecionada == 1:
                                        lutador_da_vez.defender()
                                        lutador_atual = (lutador_atual + 1) % len(lista_lutadores)
                            elif estado_batalha == 'selecionando_alvo':
                                alvos_vivos = [i for i in lista_inimigos if i.vivo]
                                if alvos_vivos:
                                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN: alvo_selecionado = (alvo_selecionado + 1) % len(alvos_vivos)
                                    if event.key == pygame.K_x: estado_batalha = 'selecionando_acao'
                                    if event.key == pygame.K_z:
                                        alvo = alvos_vivos[alvo_selecionado]
                                        lutador_da_vez.atacar(alvo)
                                        lutador_atual = (lutador_atual + 1) % len(lista_lutadores)
                                        estado_batalha = 'selecionando_acao'
                else:
                    pygame.time.delay(1000)
                    alvos_vivos = [h for h in equipe_do_jogador if h.vivo]
                    if alvos_vivos:
                        alvo = random.choice(alvos_vivos)
                        lutador_da_vez.atacar(alvo)
                    lutador_atual = (lutador_atual + 1) % len(lista_lutadores)
            else:
                lutador_atual = (lutador_atual + 1) % len(lista_lutadores)
            
            vivos_herois = sum(1 for h in equipe_do_jogador if h.vivo)
            vivos_inimigos = sum(1 for i in lista_inimigos if i.vivo)
            if vivos_herois == 0:
                vitoria = -1; jogo_acabou = True
            elif vivos_inimigos == 0:
                vitoria = 1; jogo_acabou = True
        else:
            if vitoria == 1: tela.blit(vitoria_img, (LARGURA // 2 - vitoria_img.get_width() // 2, ALTURA // 2 - vitoria_img.get_height() // 2))
            elif vitoria == -1: tela.blit(derrota_img, (LARGURA // 2 - derrota_img.get_width() // 2, ALTURA // 2 - derrota_img.get_height() // 2))
            for event in pygame.event.get():
                if event.type == pygame.QUIT: rodando = False

    pygame.display.update()
            
pygame.quit()