import pygame
import sys
import random
import json
import os
from settings import *

# --- ARQUIVO DE BANCO DE DADOS (JSON) ---
ARQUIVO_RECORDS = "records.json"


def carregar_records():
    if os.path.exists(ARQUIVO_RECORDS):
        with open(ARQUIVO_RECORDS, "r") as f:
            return json.load(f)
    return {}


def salvar_record(chave_fase, tempo_gasto):
    records = carregar_records()
    bateu_recorde = False

    # Se a fase nunca foi jogada, cria o histórico "melhor" e "ultimo"
    if chave_fase not in records or not isinstance(records[chave_fase], dict):
        records[chave_fase] = {"melhor": tempo_gasto, "ultimo": tempo_gasto}
        bateu_recorde = True
    else:
        # Atualiza a última partida sempre
        records[chave_fase]["ultimo"] = tempo_gasto

        # Verifica se bateu o recorde
        if tempo_gasto < records[chave_fase]["melhor"]:
            records[chave_fase]["melhor"] = tempo_gasto
            bateu_recorde = True

    # Salva no JSON
    with open(ARQUIVO_RECORDS, "w") as f:
        json.dump(records, f)

    return bateu_recorde


# --- PALETA DE CORES ÚNICAS ---
CORES_DISTINTAS = [
    (255, 50, 50), (50, 255, 50), (50, 100, 255), (255, 255, 0),
    (255, 165, 0), (200, 0, 255), (0, 255, 255), (255, 20, 147),
    (139, 69, 19), (0, 250, 154)
]


def desenhar_grade(superficie, matriz, pos_x, pos_y, cor_preenchimento, cor_borda):
    for linha in range(len(matriz)):
        for coluna in range(len(matriz[linha])):
            if matriz[linha][coluna] == 1:
                x = pos_x + (coluna * TAMANHO_BLOCO)
                y = pos_y + (linha * TAMANHO_BLOCO)
                pygame.draw.rect(superficie, cor_preenchimento, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))
                pygame.draw.rect(superficie, cor_borda, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO), 2)


def desenhar_texto_centro(tela, texto, fonte, cor, y):
    img = fonte.render(texto, True, cor)
    rect = img.get_rect(center=(LARGURA_TELA / 2, y))
    tela.blit(img, rect)


def tela_instrucoes(tela, modo):
    fonte_titulo = pygame.font.SysFont("Arial", 40, bold=True)
    fonte_texto = pygame.font.SysFont("Arial", 22)
    fonte_botao = pygame.font.SysFont("Arial", 28, bold=True)
    botao_start = pygame.Rect((LARGURA_TELA // 2) - 150, 420, 300, 60)

    if modo == "treino":
        titulo, cor_titulo = "COGNIFY: MODO TREINO", (50, 255, 50)
    else:
        titulo, cor_titulo = "COGNIFY: MODO EXPERT", (255, 50, 50)

    while True:
        tela.fill(COR_FUNDO)
        desenhar_texto_centro(tela, titulo, fonte_titulo, cor_titulo, 100)
        desenhar_texto_centro(tela, "O objetivo é preencher toda a área cinza o mais rápido possível.", fonte_texto,
                              (200, 200, 200), 180)
        desenhar_texto_centro(tela, "Você tem 5 MINUTOS. Se falhar, a solução será revelada.", fonte_texto,
                              (255, 255, 0), 240)
        desenhar_texto_centro(tela, "Clique ESQUERDO para arrastar. Clique RÁPIDO para girar.", fonte_texto,
                              (200, 200, 200), 280)

        pygame.draw.rect(tela, (0, 150, 255), botao_start, border_radius=8)
        img_start = fonte_botao.render("INICIAR JOGO", True, (0, 0, 0))
        tela.blit(img_start, img_start.get_rect(center=botao_start.center))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: pygame.quit(); sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_start.collidepoint(evento.pos): return
        pygame.display.flip()


# =======================================================
# 🦠 CÉREBRO: AGENTE ORGÂNICO COM MEMÓRIA DE SOLUÇÃO
# =======================================================
def rotacionar_matriz(matriz):
    return [list(linha) for linha in zip(*matriz[::-1])]


def gerar_fase_organica(nivel):
    banco_pecas = [
        [[1, 1], [1, 1]], [[1, 1, 1, 1]], [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 0], [0, 1, 1]], [[0, 1, 1], [1, 1, 0]],
        [[1, 0], [1, 0], [1, 1]], [[0, 1], [0, 1], [1, 1]]
    ]

    qtd_pecas = min(3 + (nivel // 2), 8)
    tamanho_limite = 30
    grid = [[0 for _ in range(tamanho_limite)] for _ in range(tamanho_limite)]
    pecas_usadas = []

    for i in range(qtd_pecas):
        peca = random.choice(banco_pecas)
        for _ in range(random.randint(0, 3)): peca = rotacionar_matriz(peca)

        if i == 0:
            origem_r, origem_c = 15, 15
            for r in range(len(peca)):
                for c in range(len(peca[0])):
                    if peca[r][c] == 1: grid[origem_r + r][origem_c + c] = i + 1
            pecas_usadas.append({"matriz": peca, "id": i + 1, "orig_r": origem_r, "orig_c": origem_c})
        else:
            posicionado = False
            tentativas = 0
            while not posicionado and tentativas < 500:
                tentativas += 1
                existentes = [(r, c) for r in range(tamanho_limite) for c in range(tamanho_limite) if grid[r][c] != 0]
                er, ec = random.choice(existentes)

                blocos_nova = [(r, c) for r in range(len(peca)) for c in range(len(peca[0])) if peca[r][c] == 1]
                pr, pc = random.choice(blocos_nova)

                dr, dc = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                orig_r = er + dr - pr
                orig_c = ec + dc - pc

                cabe = True
                novos_blocos_pos = []
                for r in range(len(peca)):
                    for c in range(len(peca[0])):
                        if peca[r][c] == 1:
                            curr_r, curr_c = orig_r + r, orig_c + c
                            if not (0 <= curr_r < tamanho_limite and 0 <= curr_c < tamanho_limite):
                                cabe = False;
                                break
                            if grid[curr_r][curr_c] != 0:
                                cabe = False;
                                break
                            novos_blocos_pos.append((curr_r, curr_c))
                    if not cabe: break

                if cabe:
                    todas_celulas = existentes + novos_blocos_pos
                    min_r_t = min(r for r, c in todas_celulas)
                    max_r_t = max(r for r, c in todas_celulas)
                    min_c_t = min(c for r, c in todas_celulas)
                    max_c_t = max(c for r, c in todas_celulas)
                    if (max_r_t - min_r_t + 1) > 9 or (max_c_t - min_c_t + 1) > 9:
                        cabe = False

                if cabe:
                    for r, c in novos_blocos_pos:
                        grid[r][c] = i + 1
                    pecas_usadas.append({"matriz": peca, "id": i + 1, "orig_r": orig_r, "orig_c": orig_c})
                    posicionado = True

    celulas_finais = [(r, c) for r in range(tamanho_limite) for c in range(tamanho_limite) if grid[r][c] != 0]
    min_r = min(r for r, c in celulas_finais)
    max_r = max(r for r, c in celulas_finais)
    min_c = min(c for r, c in celulas_finais)
    max_c = max(c for r, c in celulas_finais)

    w = max_c - min_c + 1
    h = max_r - min_r + 1

    mapa_final = [[0 for _ in range(w)] for _ in range(h)]
    for r, c in celulas_finais:
        mapa_final[r - min_r][c - min_c] = 1

    pecas_formatadas = []
    cores_embaralhadas = list(CORES_DISTINTAS)
    random.shuffle(cores_embaralhadas)

    for p_data in pecas_usadas:
        matriz_correta = p_data["matriz"]
        linha_correta = p_data["orig_r"] - min_r
        coluna_correta = p_data["orig_c"] - min_c

        matriz_p = p_data["matriz"]
        cor = cores_embaralhadas[(p_data["id"] - 1) % len(cores_embaralhadas)]

        for _ in range(random.randint(0, 3)): matriz_p = rotacionar_matriz(matriz_p)

        meio_lista = len(pecas_usadas) // 2
        espacamento_y = 150

        if (p_data["id"] - 1) < meio_lista:
            lado_x = 50
            pos_y = 80 + ((p_data["id"] - 1) * espacamento_y)
        else:
            lado_x = LARGURA_TELA - 200
            pos_y = 80 + ((p_data["id"] - 1 - meio_lista) * espacamento_y)

        pecas_formatadas.append({
            "matriz": matriz_p, "cor": cor,
            "x": lado_x, "y": pos_y,
            "no_tabuleiro": False, "arrastando": False, "off_x": 0, "off_y": 0,
            "matriz_correta": matriz_correta,
            "linha_correta": linha_correta,
            "coluna_correta": coluna_correta
        })

    return {"mapa": mapa_final, "pecas": pecas_formatadas, "w": w, "h": h}


# =======================================================
# MOTOR DO JOGO
# =======================================================
def jogar_blocos(modo):
    tela = pygame.display.get_surface()
    fonte_hud = pygame.font.SysFont("Arial", 28, bold=True)
    fonte_vitoria = pygame.font.SysFont("Arial", 48, bold=True)
    fonte_designer = pygame.font.SysFont("Arial", 40, bold=True, italic=True)

    tela_instrucoes(tela, modo)

    lista_fases = []
    if modo == "treino":
        for nivel in range(3): lista_fases.append(gerar_fase_organica(1))
    else:
        for nivel in range(1, 11): lista_fases.append(gerar_fase_organica(nivel))

    tempo_total = 300
    tempo_inicio = pygame.time.get_ticks()

    records_salvos = carregar_records()

    for indice, fase in enumerate(lista_fases):
        mapa_atual = fase["mapa"]
        pecas = fase["pecas"]
        w_fase, h_fase = fase["w"], fase["h"]
        chave_record = f"{modo}_{indice + 1}"

        offset_tab_x = (LARGURA_TELA - (w_fase * TAMANHO_BLOCO)) // 2
        offset_tab_y = (ALTURA_TELA - (h_fase * TAMANHO_BLOCO) + 70) // 2

        rodando_fase, venceu = True, False
        pos_clique_inicial = (0, 0)
        bateu_recorde = False

        while rodando_fase:
            tempo_atual = pygame.time.get_ticks()
            tempo_restante = tempo_total - ((tempo_atual - tempo_inicio) // 1000)
            if tempo_restante < 0: tempo_restante = 0

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: pygame.quit(); sys.exit()
                if venceu:
                    continue

                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mouse_x, mouse_y = evento.pos
                    pos_clique_inicial = evento.pos
                    for peca in reversed(pecas):
                        larg = len(peca["matriz"][0]) * TAMANHO_BLOCO
                        alt = len(peca["matriz"]) * TAMANHO_BLOCO
                        if peca["x"] <= mouse_x <= peca["x"] + larg and peca["y"] <= mouse_y <= peca["y"] + alt:
                            peca["arrastando"], peca["no_tabuleiro"] = True, False
                            peca["off_x"], peca["off_y"] = mouse_x - peca["x"], mouse_y - peca["y"]
                            pecas.remove(peca)
                            pecas.append(peca)
                            break

                elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    for peca in pecas:
                        if peca["arrastando"]:
                            peca["arrastando"] = False

                            if abs(evento.pos[0] - pos_clique_inicial[0]) < 5 and abs(
                                    evento.pos[1] - pos_clique_inicial[1]) < 5:
                                peca["matriz"] = rotacionar_matriz(peca["matriz"])

                            rel_x = peca["x"] - offset_tab_x
                            rel_y = peca["y"] - offset_tab_y
                            snap_x = round(rel_x / TAMANHO_BLOCO) * TAMANHO_BLOCO + offset_tab_x
                            snap_y = round(rel_y / TAMANHO_BLOCO) * TAMANHO_BLOCO + offset_tab_y

                            lt = int(round((snap_y - offset_tab_y) / TAMANHO_BLOCO))
                            ct = int(round((snap_x - offset_tab_x) / TAMANHO_BLOCO))

                            tab_virtual = [[0 for _ in range(w_fase)] for _ in range(h_fase)]
                            for p in pecas:
                                if p != peca and p["no_tabuleiro"]:
                                    for l in range(len(p["matriz"])):
                                        for c in range(len(p["matriz"][0])):
                                            if p["matriz"][l][c] == 1:
                                                lt_p = int(round((p["y"] - offset_tab_y) / TAMANHO_BLOCO))
                                                ct_p = int(round((p["x"] - offset_tab_x) / TAMANHO_BLOCO))
                                                if 0 <= lt_p + l < h_fase and 0 <= ct_p + c < w_fase:
                                                    tab_virtual[lt_p + l][ct_p + c] = 1

                            encaixe = True
                            for l in range(len(peca["matriz"])):
                                for c in range(len(peca["matriz"][0])):
                                    if peca["matriz"][l][c] == 1:
                                        check_r, check_c = lt + l, ct + c
                                        if not (0 <= check_r < h_fase and 0 <= check_c < w_fase):
                                            encaixe = False;
                                            break
                                        if mapa_atual[check_r][check_c] == 0 or tab_virtual[check_r][check_c] == 1:
                                            encaixe = False;
                                            break
                                if not encaixe: break

                            if encaixe:
                                peca["x"], peca["y"] = snap_x, snap_y
                                peca["no_tabuleiro"] = True
                            else:
                                peca["no_tabuleiro"] = False

                elif evento.type == pygame.MOUSEMOTION:
                    for peca in pecas:
                        if peca["arrastando"]:
                            larg_p = len(peca["matriz"][0]) * TAMANHO_BLOCO
                            alt_p = len(peca["matriz"]) * TAMANHO_BLOCO
                            nova_x = evento.pos[0] - peca["off_x"]
                            nova_y = evento.pos[1] - peca["off_y"]
                            peca["x"] = max(0, min(nova_x, LARGURA_TELA - larg_p))
                            peca["y"] = max(70, min(nova_y, ALTURA_TELA - alt_p))

            if all(p["no_tabuleiro"] for p in pecas) and not venceu:
                venceu = True
                tempo_gasto = tempo_total - tempo_restante
                bateu_recorde = salvar_record(chave_record, tempo_gasto)
                records_salvos = carregar_records()

            tela.fill(COR_FUNDO)

            LARG_ZONA = 280
            COR_ESTANTE = (20, 25, 45)

            pygame.draw.rect(tela, COR_ESTANTE, (0, 70, LARG_ZONA, ALTURA_TELA))
            pygame.draw.rect(tela, COR_ESTANTE, (LARGURA_TELA - LARG_ZONA, 70, LARG_ZONA, ALTURA_TELA))
            pygame.draw.line(tela, (80, 90, 110), (LARG_ZONA, 70), (LARG_ZONA, ALTURA_TELA), 2)
            pygame.draw.line(tela, (80, 90, 110), (LARGURA_TELA - LARG_ZONA, 70),
                             (LARGURA_TELA - LARG_ZONA, ALTURA_TELA), 2)

            texto_bg1 = fonte_designer.render("INVENTÁRIO", True, (35, 45, 65))
            texto_bg2 = fonte_designer.render("PEÇAS", True, (35, 45, 65))
            texto_bg1 = pygame.transform.rotate(texto_bg1, 90)
            texto_bg2 = pygame.transform.rotate(texto_bg2, -90)
            tela.blit(texto_bg1, (10, (ALTURA_TELA // 2) - 100))
            tela.blit(texto_bg2, (LARGURA_TELA - 60, (ALTURA_TELA // 2) - 80))

            desenhar_grade(tela, mapa_atual, offset_tab_x, offset_tab_y, COR_TABULEIRO, COR_BORDA)
            for peca in pecas: desenhar_grade(tela, peca["matriz"], peca["x"], peca["y"], peca["cor"], COR_BORDA)

            pygame.draw.rect(tela, (15, 15, 20), (0, 0, LARGURA_TELA, 70))
            pygame.draw.line(tela, COR_BORDA, (0, 70), (LARGURA_TELA, 70), 3)

            tela.blit(
                fonte_hud.render(f"NÍVEL: {indice + 1} / {len(lista_fases)} ({modo.upper()})", True, (255, 255, 255)),
                (30, 20))

            if chave_record in records_salvos and isinstance(records_salvos[chave_record], dict):
                melhor_tempo = records_salvos[chave_record]["melhor"]
                texto_recorde = f"RECORDE: {melhor_tempo // 60:02d}:{melhor_tempo % 60:02d}"
                tela.blit(fonte_hud.render(texto_recorde, True, (255, 215, 0)), (LARGURA_TELA // 2 - 100, 20))

            cor_t = (255, 50, 50) if tempo_restante <= 60 else (50, 255, 50)
            tela.blit(fonte_hud.render(f"TEMPO: {tempo_restante // 60:02d}:{tempo_restante % 60:02d}", True, cor_t),
                      (LARGURA_TELA - 220, 20))

            if tempo_restante == 0 and not venceu:
                for peca in pecas:
                    peca["matriz"] = peca["matriz_correta"]
                    peca["x"] = offset_tab_x + (peca["coluna_correta"] * TAMANHO_BLOCO)
                    peca["y"] = offset_tab_y + (peca["linha_correta"] * TAMANHO_BLOCO)

                tela.fill(COR_FUNDO)
                pygame.draw.rect(tela, COR_ESTANTE, (0, 70, LARG_ZONA, ALTURA_TELA))
                pygame.draw.rect(tela, COR_ESTANTE, (LARGURA_TELA - LARG_ZONA, 70, LARG_ZONA, ALTURA_TELA))
                desenhar_grade(tela, mapa_atual, offset_tab_x, offset_tab_y, COR_TABULEIRO, COR_BORDA)
                for peca in pecas: desenhar_grade(tela, peca["matriz"], peca["x"], peca["y"], peca["cor"], COR_BORDA)
                pygame.draw.rect(tela, (15, 15, 20), (0, 0, LARGURA_TELA, 70))

                tela.blit(fonte_vitoria.render("TEMPO ESGOTADO!", True, (255, 50, 50)), ((LARGURA_TELA // 2) - 220, 10))
                tela.blit(fonte_hud.render("Essa é a resposta certa.", True, (255, 255, 0)),
                          ((LARGURA_TELA // 2) - 160, 150))
                pygame.display.flip()

                pygame.time.delay(5000)
                return

            if venceu:
                msg = "NOVO RECORDE!!" if bateu_recorde else "PERFEITO!"
                cor_msg = (255, 215, 0) if bateu_recorde else (50, 255, 50)
                tela.blit(fonte_vitoria.render(msg, True, cor_msg), ((LARGURA_TELA // 2) - 180, 150))
                pygame.display.flip()
                pygame.time.delay(1500)
                rodando_fase = False

            pygame.display.flip()