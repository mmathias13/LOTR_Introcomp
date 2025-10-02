import pygame

# --- INICIALIZAÇÃO E CONFIGURAÇÕES GERAIS ---
pygame.init()

# Definindo o clock para controlar o FPS
clock = pygame.time.Clock()
fps = 60

# Especificações da janela do jogo
PAINEL = 200
LARGURA = 1280
ALTURA = 720 + PAINEL

# Setando a tela 
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('LOTR Battle')

# Definindo as fontes e cores
fonte = pygame.font.SysFont('Times New Roman', 26)
vermelho = (255, 0, 0)
verde = (0, 255, 0)


# --- CARREGAMENTO DE IMAGENS ---

# Imagem de fundo
background_img = pygame.image.load('imagens/Fundo/Battleground1_redimensionado.png').convert_alpha()

# Imagem do painel
painel_img = pygame.image.load('imagens/painel/painel_redimensionado.png').convert_alpha()


# --- CLASSES E FUNÇÕES ---

# Função para desenhar textos na tela
def desenha_textos(texto, fonte, texto_cor, x, y):
    img = fonte.render(texto, True, texto_cor)
    tela.blit(img, (x, y))

# Função para desenhar o background
def desenha_bg():
    tela.blit(background_img, (0, 0))
    
# Função para desenhar o painel de status
def desenha_painel(lista_herois, lista_inimigos):
    # Desenha a imagem base do painel
    tela.blit(painel_img, (0, ALTURA - PAINEL))
    
    # Mostra os status dos heróis
    y_pos = ALTURA - PAINEL + 20 # Posição Y inicial
    for i, heroi in enumerate(lista_herois):
        # Exibe "NOME VIDA: VALOR" para cada herói
        desenha_textos(f'{heroi.nome.upper()} | VIDA: {heroi.vida_max}', fonte, vermelho, 100, y_pos + (i * 40))
        
    # Mostra os status dos inimigos
    for i, inimigo in enumerate(lista_inimigos):
        desenha_textos(f'{inimigo.nome.upper()} | VIDA: {inimigo.vida_max}', fonte, vermelho, 800, y_pos + (i * 40))


# Classe Personagem (o "molde" para todos os lutadores)
class Personagem():
    def __init__(self, x, y, nome, vida_max, força, defesa, velocidade):
        self.nome = nome
        self.vida_max = vida_max
        self.vida = vida_max # Vida atual
        self.força = força
        self.defesa = defesa
        self.velocidade = velocidade
        self.vivo = True
        
        # Carrega a imagem e otimiza com .convert_alpha()
        img = pygame.image.load(f'imagens/Personagens/{self.nome}/0.png').convert_alpha()

        # Ajusta a escala da imagem de cada personagem
        if self.nome == 'Sauron':
            escala = 3
        elif self.nome == 'Frodo':
            escala = 9
        else:
            escala = 6
        
        nova_largura = int(img.get_width() / escala)
        nova_altura = int(img.get_height() / escala)
        self.image = pygame.transform.scale(img, (nova_largura, nova_altura))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        # Desenha o personagem na tela
        tela.blit(self.image, self.rect)


# --- CRIAÇÃO DOS PERSONAGENS E EQUIPES (O SENHOR DOS ANÉIS) ---

# Instanciando todos os heróis disponíveis com os stats que balanceamos
Aragorn = Personagem(350, 430, 'Aragorn', 250, 30, 25, 12)
Frodo = Personagem(280, 500, 'Frodo', 120, 10, 15, 20)
Legolas = Personagem(200, 430, 'Legolas', 160, 42, 15, 18)
Gandalf = Personagem(250, 380, 'Gandalf', 200, 40, 20, 8)

# Instanciando os inimigos
Sauron = Personagem(900, 360, 'Sauron', 450, 50, 30, 10)
Nazgul1 = Personagem(1100, 300, 'Nazgûl', 180, 28, 20, 16)
Nazgul2 = Personagem(1100, 550, 'Nazgûl', 180, 28, 20, 16)

# Criando as listas para a batalha
# SIMULAÇÃO DA ESCOLHA: O jogador escolheu 3 heróis para a batalha
equipe_do_jogador = [Gandalf, Aragorn, Legolas]
lista_inimigos = [Sauron, Nazgul1, Nazgul2]


# --- LOOP PRINCIPAL DO JOGO ---
rodando = True
while rodando:
    
    clock.tick(fps)

    # Desenha o cenário e o painel
    desenha_bg()
    desenha_painel(equipe_do_jogador, lista_inimigos)

    # Desenha os heróis da equipe escolhida e os inimigos
    for heroi in equipe_do_jogador:
        heroi.draw()
    for inimigo in lista_inimigos:
        inimigo.draw()
    
    # Gerenciador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    
    # Atualiza a tela
    pygame.display.update()
            
# Encerra o Pygame
pygame.quit()