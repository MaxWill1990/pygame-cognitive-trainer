# settings.py
import random

# --- Configurações da Janela ---
LARGURA_TELA = 1280  # Tela Widezona HD!
ALTURA_TELA = 720
TAMANHO_BLOCO = 50

# --- Paleta de Cores da UI (Tema Midnight Moderno) ---
COR_FUNDO = (15, 20, 35)       # Fundo azul marinho muito escuro
COR_TABULEIRO = (60, 70, 90)   # Cinza-azulado para a área de jogo
COR_BORDA = (200, 200, 200)    # Bordas claras para destacar
COR_VERDE = (0, 255, 150)      # Verde Neon super vivo

# ... (MANTENHA O RESTO DO ARQUIVO INTACTO: CORES_VIBRANTES, PALETA_EXPERT, ETC) ...

# --- Sorteio de Cores ---
CORES_VIBRANTES = [
    (255, 165, 0), (255, 50, 50), (50, 255, 50), (255, 255, 0),
    (0, 100, 255), (200, 0, 255), (0, 255, 255), (255, 20, 147)
]
PALETA_EXPERT = [
    (255, 50, 50), (150, 0, 255), (255, 165, 0), (255, 255, 0), (0, 255, 255)
]

# --- As Formas Geométricas ---
PECA_QUADRADO = [[1, 1], [1, 1]]
PECA_PONTO = [[1]]
PECA_RETA3 = [[1, 1, 1]]

# As 7 Peças Clássicas do Tetris (Para o Expert)
PECA_I = [[1, 1, 1, 1]]
PECA_O = [[1, 1], [1, 1]]
PECA_T = [[1, 1, 1], [0, 1, 0]]
PECA_S = [[0, 1, 1], [1, 1, 0]]
PECA_Z = [[1, 1, 0], [0, 1, 1]]
PECA_L = [[1, 0], [1, 0], [1, 1]]
PECA_J = [[0, 1], [0, 1], [1, 1]]

# ==========================================
# 🟢 MODO TREINO: OS 3 NÍVEIS
# ==========================================
MAPA_TREINO_1 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
PECAS_TREINO_1 = [
    {"matriz": PECA_QUADRADO, "cor": random.choice(CORES_VIBRANTES), "x": 50, "y": 200, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_L,        "cor": random.choice(CORES_VIBRANTES), "x": 600, "y": 200, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_PONTO,    "cor": random.choice(CORES_VIBRANTES), "x": 350, "y": 450, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0}
]

MAPA_TREINO_2 = [[1, 1, 1], [1, 1, 1], [0, 1, 0]]
PECAS_TREINO_2 = [
    {"matriz": PECA_T,     "cor": random.choice(CORES_VIBRANTES), "x": 50, "y": 200, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_RETA3, "cor": random.choice(CORES_VIBRANTES), "x": 600, "y": 200, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0}
]

MAPA_TREINO_3 = [[1, 1, 1], [1, 1, 1], [1, 1, 0]]
PECAS_TREINO_3 = [
    {"matriz": PECA_L,       "cor": random.choice(CORES_VIBRANTES), "x": 50, "y": 200, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_QUADRADO,"cor": random.choice(CORES_VIBRANTES), "x": 600, "y": 200, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0}
]

NIVEIS_TREINO = [
    {"mapa": MAPA_TREINO_1, "pecas": PECAS_TREINO_1},
    {"mapa": MAPA_TREINO_2, "pecas": PECAS_TREINO_2},
    {"mapa": MAPA_TREINO_3, "pecas": PECAS_TREINO_3}
]


# ==========================================
# 🔥 MODO EXPERT: NÍVEIS PROGRESSIVOS
# ==========================================
MAPA_EXP_1 = [
    [1, 1, 1, 0, 0],
    [0, 1, 0, 1, 1],
    [0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 1, 1]
]
PECAS_EXP_1 = [
    {"matriz": PECA_T, "cor": random.choice(PALETA_EXPERT), "x": 50, "y": 100, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_O, "cor": random.choice(PALETA_EXPERT), "x": 600, "y": 150, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_L, "cor": random.choice(PALETA_EXPERT), "x": 50, "y": 300, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_Z, "cor": random.choice(PALETA_EXPERT), "x": 600, "y": 350, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0}
]

MAPA_EXP_2 = [
    [1, 1, 1, 1, 0, 0],
    [1, 1, 0, 1, 1, 0],
    [1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 1],
    [0, 0, 1, 0, 1, 1]
]
PECAS_EXP_2 = [
    {"matriz": PECA_I, "cor": random.choice(PALETA_EXPERT), "x": 50, "y": 100, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_O, "cor": random.choice(PALETA_EXPERT), "x": 600, "y": 100, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_S, "cor": random.choice(PALETA_EXPERT), "x": 50, "y": 200, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_J, "cor": random.choice(PALETA_EXPERT), "x": 600, "y": 250, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_T, "cor": random.choice(PALETA_EXPERT), "x": 350, "y": 450, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0}
]

MAPA_EXP_3 = [
    [1, 0, 0, 0, 1, 0],
    [1, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 1, 1],
    [0, 1, 1, 1, 1, 0]
]
PECAS_EXP_3 = [
    {"matriz": PECA_L, "cor": random.choice(PALETA_EXPERT), "x": 50, "y": 100, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_L, "cor": random.choice(PALETA_EXPERT), "x": 600, "y": 100, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_O, "cor": random.choice(PALETA_EXPERT), "x": 50, "y": 300, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_Z, "cor": random.choice(PALETA_EXPERT), "x": 600, "y": 300, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0},
    {"matriz": PECA_S, "cor": random.choice(PALETA_EXPERT), "x": 350, "y": 450, "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0}
]

NIVEIS_EXPERT = [
    {"mapa": MAPA_EXP_1, "pecas": PECAS_EXP_1},
    {"mapa": MAPA_EXP_2, "pecas": PECAS_EXP_2},
    {"mapa": MAPA_EXP_3, "pecas": PECAS_EXP_3}
]