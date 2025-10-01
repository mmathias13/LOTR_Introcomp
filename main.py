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

#Variável para sair do jogo caso atinja condição para ser falsa
rodando = True


while rodando:
    
    clock.tick(fps)
    
    #Faz o background
    desenha_bg()
    
    #Faz o painel
    desenha_painel()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    
    pygame.display.update()
            
pygame.quit()