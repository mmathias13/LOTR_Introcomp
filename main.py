import pygame

pygame.init()

#Definindo o fps
clock = pygame.time.Clock()
fps = 60

#Especificações da janela do jogo
PAINEL = 200
LARGURA = 1280
ALTURA = 720 + PAINEL

#Setando a tela 
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('LOTR')


#Espaço para carregar imagens

#Imagem de fundo
background_img = pygame.image.load('imagens/Fundo/Battleground1_redimensionado.png').convert_alpha()

#Imagem do painel
painel_img = pygame.image.load('imagens/painel/painel_redimensionado.png').convert_alpha()

#Função para criar o background
def desenha_bg():
    tela.blit(background_img, (0, 0))
    
#Função para criar o painel
def desenha_painel():
    tela.blit(painel_img, (0, ALTURA - PAINEL))

# Criação de personagens adiante

#Personagem
class Personagem():
    def __init__(self, x, y, nome, vida_max, força, defesa):
        self.nome = nome
        self.vida_max = vida_max
        self.força = força
        self.defesa = defesa
        self.alive = True
        img = pygame.image.load(f'imagens/Personagens/{self.nome}/0.png')
        self.image = pygame.transform.scale(img, (img.get_width() / 6, img.get_height() / 6))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        tela.blit(self.image, self.rect)

Aragorn = Personagem(300, 450, 'Aragorn', 200, 10, 20)
Sauron = Personagem(900, 450, 'Sauron', 350, 10, 20)
Nazgul1 = Personagem(1000, 300, 'Nazgûl', 150, 10, 20)
Nazgul2 = Personagem(1000, 550, 'Nazgûl', 150, 10, 20)


#Variável para sair do jogo caso atinja condição para ser falsa
rodando = True


while rodando:
    
    clock.tick(fps)
    
    #Faz o background
    desenha_bg()
    
    #Faz o painel
    desenha_painel()

    #Faz um personagem
    Aragorn.draw()
    Sauron.draw()
    Nazgul1.draw()
    Nazgul2.draw()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    
    pygame.display.update()
            
pygame.quit()