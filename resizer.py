from PIL import Image

# --- CONFIGURAÇÕES ---
# 1. Coloque o nome da sua imagem original aqui
NOME_ARQUIVO_ORIGINAL = 'imagens/painel/sauron.png'

# 2. Escolha as novas dimensões (ex: 1280x720)
NOVA_LARGURA = 600
NOVA_ALTURA = 200

# 3. Dê um nome para o novo arquivo que será criado
NOME_ARQUIVO_NOVO = 'imagens/Personagens/Sauron/0.png'
# ---------------------

try:
    # Abre a imagem original
    img = Image.open(NOME_ARQUIVO_ORIGINAL)

    # Redimensiona a imagem
    print(f"Redimensionando '{NOME_ARQUIVO_ORIGINAL}' para {NOVA_LARGURA}x{NOVA_ALTURA}...")
    imagem_redimensionada = img.resize((NOVA_LARGURA, NOVA_ALTURA), Image.Resampling.LANCZOS)

    # Salva a nova imagem
    imagem_redimensionada.save(NOME_ARQUIVO_NOVO)

    print(f"Sucesso! Nova imagem salva como '{NOME_ARQUIVO_NOVO}'")

except FileNotFoundError:
    print(f"Erro: O arquivo '{NOME_ARQUIVO_ORIGINAL}' não foi encontrado. Verifique o caminho e o nome do arquivo.")