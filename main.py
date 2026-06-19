import pygame
import sys
import json
import os
from settings import *
from blocos import jogar_blocos, carregar_records
from bolhas import jogar_bolhas
from ingles import jogar_ingles

pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("COGNIFY - Simulador de Processos Seletivos")

# --- FONTES MODERNAS ---
fonte_titulo = pygame.font.SysFont("Trebuchet MS", 70, bold=True)
fonte_sub = pygame.font.SysFont("Trebuchet MS", 26, italic=True)
fonte_botao = pygame.font.SysFont("Trebuchet MS", 28, bold=True)
fonte_recordes = pygame.font.SysFont("Courier New", 26, bold=True)
fonte_cabecalho = pygame.font.SysFont("Trebuchet MS", 22, bold=True)


def desenhar_botao(superficie, texto, x, y, w, h, cor_normal, cor_hover, mouse_pos):
    rect = pygame.Rect(x, y, w, h)
    colidiu = rect.collidepoint(mouse_pos)
    cor_atual = cor_hover if colidiu else cor_normal

    # Sombra do botão
    pygame.draw.rect(superficie, (10, 15, 25), (x + 5, y + 5, w, h), border_radius=15)
    # Corpo do botão
    pygame.draw.rect(superficie, cor_atual, rect, border_radius=15)
    # Borda iluminada se passar o mouse
    pygame.draw.rect(superficie, (100, 150, 255) if colidiu else COR_BORDA, rect, width=2, border_radius=15)

    img_texto = fonte_botao.render(texto, True, (255, 255, 255))
    superficie.blit(img_texto, img_texto.get_rect(center=rect.center))
    return colidiu


# =======================================================
# 📊 TELA DE RECORDES DINÂMICA
# =======================================================
def tela_recordes(modo_jogo):
    rodando = True
    records = carregar_records()

    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        tela.fill(COR_FUNDO)

        # Efeitos de fundo
        pygame.draw.circle(tela, (20, 25, 45), (LARGURA_TELA // 2, 0), 400)

        titulo_texto = f"DESEMPENHO: {modo_jogo.upper()}"
        titulo = fonte_titulo.render(titulo_texto, True, (255, 215, 0))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, 80)))

        start_y = 210

        # Mostra recordes dos BLOCOS
        if modo_jogo == "blocos":
            cabecalho = fonte_cabecalho.render("FASES (EXPERT)        MELHOR TEMPO        ÚLTIMA TENTATIVA", True,
                                               (200, 200, 200))
            tela.blit(cabecalho, cabecalho.get_rect(center=(LARGURA_TELA // 2, 160)))
            pygame.draw.line(tela, (100, 150, 255), ((LARGURA_TELA // 2) - 350, 180), ((LARGURA_TELA // 2) + 350, 180),
                             2)

            for i in range(1, 11):
                chave = f"expert_{i}"
                if chave in records and isinstance(records[chave], dict):
                    melhor = records[chave]["melhor"]
                    ultimo = records[chave]["ultimo"]
                    str_melhor = f"{melhor // 60:02d}:{melhor % 60:02d}"
                    str_ultimo = f"{ultimo // 60:02d}:{ultimo % 60:02d}"
                    cor_texto = (50, 255, 150)
                else:
                    str_melhor = "--:--"
                    str_ultimo = "--:--"
                    cor_texto = (100, 100, 100)

                linha = f"NÍVEL {i:02d} ............. {str_melhor} ............. {str_ultimo}"
                img_linha = fonte_recordes.render(linha, True, cor_texto)
                tela.blit(img_linha, img_linha.get_rect(center=(LARGURA_TELA // 2, start_y + (i * 35))))

        # Mostra recordes das BOLHAS
        elif modo_jogo == "bolhas":
            if "bolhas" in records and isinstance(records["bolhas"], dict):
                melhor = records["bolhas"]["melhor"]
                ultimo = records["bolhas"]["ultimo"]

                txt_m = fonte_titulo.render(f"RECORDE MÁXIMO: {melhor} Pts", True, (50, 255, 150))
                txt_u = fonte_botao.render(f"Última tentativa: {ultimo} Pts", True, (200, 200, 200))

                tela.blit(txt_m, txt_m.get_rect(center=(LARGURA_TELA // 2, 300)))
                tela.blit(txt_u, txt_u.get_rect(center=(LARGURA_TELA // 2, 380)))
            else:
                txt_vazio = fonte_botao.render("Nenhum treinamento realizado ainda.", True, (150, 150, 150))
                tela.blit(txt_vazio, txt_vazio.get_rect(center=(LARGURA_TELA // 2, 300)))

        clicou_voltar = desenhar_botao(tela, "VOLTAR", (LARGURA_TELA // 2) - 150, 600, 300, 60, (50, 60, 80),
                                       (80, 90, 120), mouse_pos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if clicou_voltar:
                    return

        pygame.display.flip()


# =======================================================
# 📁 SUB-MENUS DOS JOGOS
# =======================================================
def menu_blocos():
    rodando = True
    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        tela.fill(COR_FUNDO)
        pygame.draw.circle(tela, (25, 30, 50), (0, 0), 400)

        titulo = fonte_titulo.render("LÓGICA ESPACIAL (BLOCOS)", True, (0, 150, 255))
        subtitulo = fonte_sub.render("Treine seu raciocínio geométrico e encaixe de padrões.", True, (200, 200, 200))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, 120)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA_TELA // 2, 180)))

        b_w, b_h, b_x = 420, 60, (LARGURA_TELA // 2) - 210

        btn_treino = desenhar_botao(tela, "1. PRATICAR LIVREMENTE", b_x, 280, b_w, b_h, (40, 50, 70), (60, 80, 120),
                                    mouse_pos)
        btn_expert = desenhar_botao(tela, "2. SIMULADO CRONOMETRADO", b_x, 360, b_w, b_h, (150, 40, 60),
                                    (255, 50, 80), mouse_pos)
        btn_records = desenhar_botao(tela, "3. VER DESEMPENHO", b_x, 440, b_w, b_h, (180, 140, 20), (255, 200, 50),
                                     mouse_pos)
        btn_voltar = desenhar_botao(tela, "VOLTAR AO INÍCIO", b_x, 560, b_w, b_h, (50, 50, 50), (100, 100, 100),
                                    mouse_pos)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if btn_treino:
                    jogar_blocos("treino")
                elif btn_expert:
                    jogar_blocos("expert")
                elif btn_records:
                    tela_recordes("blocos")
                elif btn_voltar:
                    rodando = False

        pygame.display.flip()


def menu_bolhas():
    rodando = True
    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        tela.fill(COR_FUNDO)
        pygame.draw.circle(tela, (25, 30, 50), (LARGURA_TELA, 0), 400)

        titulo = fonte_titulo.render("FOCO E CÁLCULO (BOLHAS)", True, (0, 255, 150))
        subtitulo = fonte_sub.render("Teste sua atenção concentrada sob forte pressão de tempo.", True,
                                     (200, 200, 200))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, 120)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA_TELA // 2, 180)))

        b_w, b_h, b_x = 420, 60, (LARGURA_TELA // 2) - 210

        btn_jogar = desenhar_botao(tela, "1. INICIAR BATERIA DE TREINO", b_x, 300, b_w, b_h, (40, 150, 120),
                                   (50, 255, 180), mouse_pos)
        btn_records = desenhar_botao(tela, "2. VER DESEMPENHO", b_x, 380, b_w, b_h, (180, 140, 20), (255, 200, 50),
                                     mouse_pos)
        btn_voltar = desenhar_botao(tela, "VOLTAR AO INÍCIO", b_x, 500, b_w, b_h, (50, 50, 50), (100, 100, 100),
                                    mouse_pos)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if btn_jogar:
                    jogar_bolhas()
                elif btn_records:
                    tela_recordes("bolhas")
                elif btn_voltar:
                    rodando = False

        pygame.display.flip()


def menu_ingles():
    rodando = True
    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        tela.fill(COR_FUNDO)
        pygame.draw.circle(tela, (25, 30, 50), (LARGURA_TELA // 2, ALTURA_TELA), 400)

        titulo = fonte_titulo.render("INGLÊS TÉCNICO (TEXTOS)", True, (180, 80, 255))
        subtitulo = fonte_sub.render("Encontre os erros ocultos em textos de vivência corporativa.", True,
                                     (200, 200, 200))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, 120)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA_TELA // 2, 180)))

        b_w, b_h, b_x = 420, 60, (LARGURA_TELA // 2) - 210

        btn_jogar = desenhar_botao(tela, "1. INICIAR SIMULADO (READING)", b_x, 320, b_w, b_h, (100, 50, 150), (180, 80, 255),
                                   mouse_pos)
        btn_voltar = desenhar_botao(tela, "VOLTAR AO INÍCIO", b_x, 440, b_w, b_h, (50, 50, 50), (100, 100, 100),
                                    mouse_pos)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if btn_jogar:
                    jogar_ingles()
                elif btn_voltar:
                    rodando = False

        pygame.display.flip()


# =======================================================
# 🌐 MENU PRINCIPAL HUB
# =======================================================
def menu_principal():
    rodando = True
    while rodando:
        mouse_pos = pygame.mouse.get_pos()
        tela.fill(COR_FUNDO)

        # Formas geométricas modernas no fundo
        pygame.draw.circle(tela, (25, 30, 50), (LARGURA_TELA, 0), 500)
        pygame.draw.circle(tela, (20, 25, 45), (0, ALTURA_TELA), 400)

        titulo = fonte_titulo.render("TREINOS COGNITIVOS", True, (255, 255, 255))
        subtitulo = fonte_sub.render("Simulador Prático para Processos Seletivos", True, (200, 200, 200))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA // 2, 130)))
        tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA_TELA // 2, 190)))

        b_w, b_h = 440, 70  # Botões maiores para o menu principal
        b_x = (LARGURA_TELA // 2) - (b_w // 2)

        btn_blocos = desenhar_botao(tela, "🧩 TREINO DE LÓGICA (Blocos)", b_x, 280, b_w, b_h, (40, 50, 70), (0, 150, 255),
                                    mouse_pos)
        btn_bolhas = desenhar_botao(tela, "⏱️ TREINO DE FOCO (Bolhas)", b_x, 370, b_w, b_h, (40, 150, 120),
                                    (50, 255, 180), mouse_pos)
        btn_ingles = desenhar_botao(tela, "🇬🇧 INGLÊS TÉCNICO (Textos)", b_x, 460, b_w, b_h, (100, 50, 150),
                                    (180, 80, 255), mouse_pos)

        pygame.draw.line(tela, (60, 70, 90), (b_x, 560), (b_x + b_w, 560), 2)
        btn_sair = desenhar_botao(tela, "ENCERRAR SIMULADOR", b_x + 50, 590, b_w - 100, 50, (50, 50, 50), (200, 50, 50),
                                  mouse_pos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if btn_blocos:
                    menu_blocos()
                elif btn_bolhas:
                    menu_bolhas()
                elif btn_ingles:
                    menu_ingles()
                elif btn_sair:
                    rodando = False

        pygame.display.flip()


menu_principal()
pygame.quit()
sys.exit()