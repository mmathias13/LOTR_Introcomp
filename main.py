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

fonte = pygame.font.SysFont('Times New Roman', 26)
fonte_grande = pygame.font.SysFont('Times New Roman', 60)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)

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
    # Coluna 1: Heróis
    for i, heroi in enumerate(equipe_do_jogador):
        desenha_textos(f'{heroi.nome.upper()} | VIDA: {int(heroi.vida)}/{heroi.vida_max}', fonte, verde, 100, ALTURA - 200 + 30 + (i * 50))
    # Coluna 2: Turno e Ações
    lutador_da_vez = lista_lutadores[lutador_atual]
    desenha_textos(f"TURNO DE {lutador_da_vez.nome.upper()}", fonte, branco, 520, ALTURA - 200 + 15)
    # Mostra o menu de ações apenas se não houver uma animação acontecendo
    if lutador_da_vez in equipe_do_jogador and estado_batalha == 'selecionando_acao' and not acao_em_andamento:
        x_acao, y_acao_base = 540, ALTURA - 200 + 60
        desenha_textos('ATACAR', fonte, vermelho, x_acao, y_acao_base)
        desenha_textos('DEFENDER', fonte, vermelho, x_acao, y_acao_base + 40)
        cor_habilidade = vermelho if lutador_da_vez.habilidade_cooldown == 0 else cinza
        desenha_textos(lutador_da_vez.nome_habilidade, fonte, cor_habilidade, x_acao, y_acao_base + 80)
        y_offset_seta = 5
        if acao_selecionada == 0: tela.blit(arrow_img, (x_acao - 40, y_acao_base + y_offset_seta))
        elif acao_selecionada == 1: tela.blit(arrow_img, (x_acao - 40, y_acao_base + 40 + y_offset_seta))
        elif acao_selecionada == 2: tela.blit(arrow_img, (x_acao - 40, y_acao_base + 80 + y_offset_seta))
    # Coluna 3: Inimigos
    for i, inimigo in enumerate(lista_inimigos):
        desenha_textos(f'{inimigo.nome.upper()} | VIDA: {int(inimigo.vida)}/{inimigo.vida_max}', fonte, vermelho, 900, ALTURA - 200 + 30 + (i * 50))

def desenha_menu():
    # ... (sem alterações)
    tela.blit(menu_bg_img, (0, 0))
    desenha_textos('ESCOLHA SUA EQUIPE', fonte_grande, branco, LARGURA // 2 - 350, 100)
    y_pos_herois = 380
    for i, heroi in enumerate(personagens_disponiveis):
        x_pos = 200 + i * 250; tela.blit(heroi.image, (x_pos, y_pos_herois))
        texto_nome = fonte.render(heroi.nome, True, branco)
        texto_x = x_pos + (heroi.image.get_width() / 2) - (texto_nome.get_width() / 2)
        texto_y = y_pos_herois + heroi.image.get_height() + 15
        tela.blit(texto_nome, (texto_x, texto_y))
        if i == cursor_menu:
            pygame.draw.rect(tela, branco, (x_pos - 10, y_pos_herois - 10, heroi.image.get_width() + 20, heroi.image.get_height() + 20), 3)
    desenha_textos('Equipe selecionada:', fonte, branco, 100, 750)
    for i, heroi in enumerate(equipe_do_jogador):
        desenha_textos(heroi.nome, fonte, verde, 400 + i * 180, 750)

class Personagem():
    def __init__(self, x, y, nome, vida_max, força, defesa, velocidade, escala_img=6):
        self.nome = nome; self.vida_max = vida_max; self.vida = vida_max; self.força_base = força; self.força = força
        self.defesa_base = defesa; self.defesa = defesa; self.velocidade = velocidade
        self.defendendo = False; self.invulneravel = False; self.critico_garantido = False; self.vivo = True
        self.habilidade_cooldown = 0; self.ataque_debuff_turns = 0; self.defesa_buff_turns = 0
        img = pygame.image.load(f'imagens/Personagens/{self.nome}/0.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() / escala_img), int(img.get_height() / escala_img)))
        self.rect = self.image.get_rect(); self.rect.center = (x, y)
        
        self.posicao_original = (x, y)
        self.estado_animacao = 'parado'
        self.animation_start_time = 0
        self.alvo_da_animacao = None
        self.hit_registrado = False # Para garantir que o dano seja aplicado só uma vez

        self.definir_habilidade()

    def definir_habilidade(self):
        # ... (sem alterações)
        if self.nome == 'Gandalf': self.nome_habilidade = 'LUZ DE ISTARI'; self.habilidade_cooldown_max = 3
        elif self.nome == 'Aragorn': self.nome_habilidade = 'GRITO DO REI'; self.habilidade_cooldown_max = 3
        elif self.nome == 'Legolas': self.nome_habilidade = 'CHUVA DE FLECHAS'; self.habilidade_cooldown_max = 3
        elif self.nome == 'Frodo': self.nome_habilidade = 'DESAPARECER'; self.habilidade_cooldown_max = 4
        elif self.nome == 'Sauron': self.nome_habilidade = 'OLHO DO TERROR'; self.habilidade_cooldown_max = 4
        elif self.nome == 'Nazgûl': self.nome_habilidade = 'GRITO SOMBRIO'; self.habilidade_cooldown_max = 3
        else: self.nome_habilidade = 'NENHUMA'; self.habilidade_cooldown_max = 0

    def atacar(self, alvo):
        # ... (sem alterações)
        if alvo.invulneravel: return 0, False
        multiplicador_critico = 2.0 if self.critico_garantido else 1.0; self.critico_garantido = False
        defesa_alvo = alvo.defesa * 2 if alvo.defendendo else alvo.defesa
        dano = (self.força * (50 / (50 + defesa_alvo))) * multiplicador_critico
        alvo.vida -= dano
        if alvo.vida < 1:
            alvo.vida = 0; alvo.vivo = False; return dano, True
        return dano, False

    def defender(self): self.defendendo = True
    
    def usar_habilidade(self, alvos_inimigos, alvos_aliados):
        # ... (sem alterações)
        dano_total = 0
        if self.habilidade_cooldown == 0:
            self.habilidade_cooldown = self.habilidade_cooldown_max + 1
            if self.nome == 'Gandalf':
                for inimigo in alvos_inimigos:
                    dano, _ = self.atacar_com_força(inimigo, self.força * 0.75); dano_total += dano
            # ... (resto da lógica de habilidades)
            elif self.nome == 'Aragorn':
                for aliado in alvos_aliados: aliado.defesa_buff_turns = 3
            elif self.nome == 'Legolas':
                for _ in range(3):
                    if alvos_inimigos:
                        dano, _ = self.atacar_com_força(random.choice(alvos_inimigos), self.força * 0.6); dano_total += dano
            elif self.nome == 'Frodo':
                self.invulneravel = True; self.critico_garantido = True
            elif self.nome == 'Sauron':
                if alvos_aliados:
                    dano, _ = self.atacar_com_força(random.choice(alvos_aliados), self.força * 1.5); dano_total += dano
            elif self.nome == 'Nazgûl':
                for aliado in alvos_aliados: aliado.ataque_debuff_turns = 3
        return dano_total

    def atacar_com_força(self, alvo, força):
        # ... (sem alterações)
        if alvo.invulneravel: return 0, False
        defesa_alvo = alvo.defesa * 2 if alvo.defendendo else alvo.defesa
        dano = (força * (50 / (50 + defesa_alvo)))
        alvo.vida -= dano
        if alvo.vida < 1:
            alvo.vida = 0; alvo.vivo = False; return dano, True
        return dano, False
        
    def iniciar_animacao_ataque(self, alvo):
        self.estado_animacao = 'atacando'
        self.alvo_da_animacao = alvo
        self.animation_start_time = pygame.time.get_ticks()
        self.hit_registrado = False # Reseta o controle de dano

    def draw(self):
        if self.vivo: tela.blit(self.image, self.rect)

# --- CRIAÇÃO DOS PERSONAGENS ---
Aragorn = Personagem(350, 500, 'Aragorn', 250, 30, 25, 12)
Gandalf = Personagem(250, 420, 'Gandalf', 200, 40, 20, 8)
Legolas = Personagem(250, 580, 'Legolas', 160, 42, 15, 18)
Frodo = Personagem(400, 580, 'Frodo', 120, 10, 15, 20, escala_img=9)
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
texto_de_acao = ""; timer_texto_de_acao = 0
acao_em_andamento = False # Controla se uma ação (animação) está acontecendo

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
        # --- LÓGICA DE BATALHA REESTRUTURADA PARA ANIMAÇÃO ---

        # 1. Desenha tudo
        desenha_bg(); desenha_painel()
        for personagem in equipe_do_jogador + lista_inimigos: personagem.draw()
        if estado_batalha == 'selecionando_alvo':
            alvos_vivos = [i for i in lista_inimigos if i.vivo];
            if alvos_vivos:
                if alvo_selecionado >= len(alvos_vivos): alvo_selecionado = 0
                alvo = alvos_vivos[alvo_selecionado]
                tela.blit(arrow_img, (alvo.rect.centerx - (arrow_img.get_width() / 2), alvo.rect.top - arrow_img.get_height()))
        if timer_texto_de_acao > 0:
            if pygame.time.get_ticks() - timer_texto_de_acao < 2000:
                texto_img = fonte.render(texto_de_acao, True, branco)
                pos_x = LARGURA // 2 - texto_img.get_width() // 2
                tela.blit(texto_img, (pos_x, ALTURA - 240))
            else:
                timer_texto_de_acao = 0
        if jogo_acabou:
            if vitoria == 1: tela.blit(vitoria_img, (LARGURA // 2 - vitoria_img.get_width() // 2, ALTURA // 2 - vitoria_img.get_height() // 2))
            elif vitoria == -1: tela.blit(derrota_img, (LARGURA // 2 - derrota_img.get_width() // 2, ALTURA // 2 - derrota_img.get_height() // 2))

        # 2. Processa eventos e lógica de turno
        if not jogo_acabou and not acao_em_andamento:
            lutador_da_vez = lista_lutadores[lutador_atual]
            if lutador_da_vez.vivo:
                if 'turno_iniciado' not in locals() or turno_iniciado != lutador_atual:
                    # Lógica de início de turno
                    lutador_da_vez.defendendo = False; lutador_da_vez.invulneravel = False
                    if lutador_da_vez.habilidade_cooldown > 0: lutador_da_vez.habilidade_cooldown -= 1
                    turno_iniciado = lutador_atual
                
                if lutador_da_vez in equipe_do_jogador:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: rodando = False
                        if event.type == pygame.KEYDOWN:
                            if estado_batalha == 'selecionando_acao':
                                if event.key == pygame.K_UP: acao_selecionada = (acao_selecionada - 1) % 3
                                if event.key == pygame.K_DOWN: acao_selecionada = (acao_selecionada + 1) % 3
                                if event.key == pygame.K_z:
                                    if acao_selecionada == 0: estado_batalha = 'selecionando_alvo'
                                    elif acao_selecionada == 1:
                                        lutador_da_vez.defender(); texto_de_acao = f"{lutador_da_vez.nome} se defendeu!"; timer_texto_de_acao = pygame.time.get_ticks()
                                        acao_em_andamento = True # Inicia uma "ação" para criar uma pausa
                                    elif acao_selecionada == 2 and lutador_da_vez.habilidade_cooldown == 0:
                                        # Habilidades ainda acontecem instantaneamente por simplicidade
                                        dano_total = lutador_da_vez.usar_habilidade([i for i in lista_inimigos if i.vivo], [h for h in equipe_do_jogador if h.vivo])
                                        if dano_total > 0: texto_de_acao = f"{lutador_da_vez.nome} usou {lutador_da_vez.nome_habilidade} e causou {int(dano_total)} de dano!"
                                        else: texto_de_acao = f"{lutador_da_vez.nome} usou {lutador_da_vez.nome_habilidade}!"
                                        timer_texto_de_acao = pygame.time.get_ticks(); acao_em_andamento = True
                            elif estado_batalha == 'selecionando_alvo':
                                alvos_vivos = [i for i in lista_inimigos if i.vivo]
                                if alvos_vivos:
                                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN: alvo_selecionado = (alvo_selecionado + 1) % len(alvos_vivos)
                                    if event.key == pygame.K_x: estado_batalha = 'selecionando_acao'
                                    if event.key == pygame.K_z:
                                        alvo = alvos_vivos[alvo_selecionado]
                                        lutador_da_vez.iniciar_animacao_ataque(alvo)
                                        acao_em_andamento = True
                else: # Turno do Inimigo
                    alvos_vivos = [h for h in equipe_do_jogador if h.vivo]
                    if alvos_vivos:
                        alvo = random.choice(alvos_vivos)
                        lutador_da_vez.iniciar_animacao_ataque(alvo)
                        acao_em_andamento = True
            else: # Pula o turno do lutador morto
                lutador_atual = (lutador_atual + 1) % len(lista_lutadores)

        # 3. Gerenciador de Animação (executa a cada frame)
        if acao_em_andamento:
            atacante = lista_lutadores[lutador_atual]
            if atacante.estado_animacao == 'atacando':
                duracao_total = 600 # 0.6 segundos
                tempo_passado = pygame.time.get_ticks() - atacante.animation_start_time
                
                # Fase 1: Avançar
                if tempo_passado < duracao_total / 2:
                    atacante.rect.centerx += 8
                # Fase 2: Registrar o dano no meio do caminho
                elif tempo_passado >= duracao_total / 2 and not atacante.hit_registrado:
                    dano_causado, alvo_foi_derrotado = atacante.atacar(atacante.alvo_da_animacao)
                    if alvo_foi_derrotado: texto_de_acao = f"{atacante.alvo_da_animacao.nome} foi derrotado!"
                    else: texto_de_acao = f"{atacante.nome} atacou {atacante.alvo_da_animacao.nome} e causou {int(dano_causado)} de dano!"
                    timer_texto_de_acao = pygame.time.get_ticks()
                    atacante.hit_registrado = True
                # Fase 3: Voltar
                elif tempo_passado > duracao_total / 2 and tempo_passado < duracao_total:
                     atacante.rect.centerx -= 8
                # Fase 4: Fim da animação
                else:
                    atacante.estado_animacao = 'parado'
                    atacante.rect.center = atacante.posicao_original
                    acao_em_andamento = False
                    lutador_atual = (lutador_atual + 1) % len(lista_lutadores)
                    estado_batalha = 'selecionando_acao'
            else: # Para ações que não são ataque (Defender, Habilidades)
                pygame.display.update(); pygame.time.delay(1000)
                acao_em_andamento = False
                lutador_atual = (lutador_atual + 1) % len(lista_lutadores)
        
        # Verifica Condição de Fim de Jogo
        vivos_herois = sum(1 for h in equipe_do_jogador if h.vivo); vivos_inimigos = sum(1 for i in lista_inimigos if i.vivo)
        if vivos_herois == 0: vitoria = -1; jogo_acabou = True
        elif vivos_inimigos == 0: vitoria = 1; jogo_acabou = True
        
        # Se o jogo acabou, só verifica o evento de fechar
        if jogo_acabou:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: rodando = False

    pygame.display.update()
            
pygame.quit()