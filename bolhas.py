import pygame
import sys
import random
import math
import json
import os
from settings import *

# --- FONTES LOCAIS AJUSTADAS ---
pygame.font.init()
fonte_bolha = pygame.font.SysFont("Trebuchet MS", 28, bold=True)
fonte_alvo_label = pygame.font.SysFont("Trebuchet MS", 32, bold=True)
fonte_alvo_num = pygame.font.SysFont("Trebuchet MS", 80, bold=True)
fonte_hud = pygame.font.SysFont("Arial", 30, bold=True)
fonte_pontos = pygame.font.SysFont("Trebuchet MS", 45, bold=True)
fonte_relatorio = pygame.font.SysFont("Courier New", 18, bold=True)


def salvar_record_bolhas(pontuacao):
    arquivo = "records.json"
    records = {}
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            records = json.load(f)

    bateu_recorde = False
    if "bolhas" not in records or not isinstance(records["bolhas"], dict):
        records["bolhas"] = {"melhor": pontuacao, "ultimo": pontuacao}
        bateu_recorde = True
    else:
        records["bolhas"]["ultimo"] = pontuacao
        if pontuacao > records["bolhas"]["melhor"]:
            records["bolhas"]["melhor"] = pontuacao
            bateu_recorde = True

    with open(arquivo, "w") as f:
        json.dump(records, f)
    return bateu_recorde


class Bolha:
    def __init__(self, x, y, equacao, e_correta, tempo_vida_segundos):
        self.x = int(x)
        self.y = int(y)
        self.raio_atual = 55
        self.equacao = equacao
        self.e_correta = e_correta
        self.status = "ativa"
        self.cor_base = random.choice(
            [(0, 200, 255), (255, 100, 200), (100, 255, 100), (200, 150, 255), (255, 200, 50)])
        self.timer_animacao = 15
        self.tempo_vida = tempo_vida_segundos * 60
        self.idade = 0

    def atualizar(self):
        if self.status == "ativa":
            self.idade += 1
            if self.idade >= self.tempo_vida:
                self.status = "morta_tempo"

    def desenhar(self, tela):
        if self.status in ["morta", "morta_tempo"]: return
        px, py = self.x, self.y
        cor_atual = self.cor_base

        if self.status == "ativa":
            frames_restantes = self.tempo_vida - self.idade
            if frames_restantes < 120:
                intensidade = 5 if frames_restantes < 60 else 2
                px += random.randint(-intensidade, intensidade)
                py += random.randint(-intensidade, intensidade)
        elif self.status == "explodindo_certa":
            self.raio_atual += 5
            cor_atual = (50, 255, 50)
            self.timer_animacao -= 1
            if self.timer_animacao <= 0: self.status = "morta"
        elif self.status == "explodindo_errada":
            self.raio_atual += 5
            cor_atual = (255, 50, 50)
            self.timer_animacao -= 1
            if self.timer_animacao <= 0: self.status = "morta"

        surf_bolha = pygame.Surface((self.raio_atual * 2, self.raio_atual * 2), pygame.SRCALPHA)
        r, g, b = cor_atual
        pygame.draw.circle(surf_bolha, (r, g, b, 80), (self.raio_atual, self.raio_atual), self.raio_atual)
        pygame.draw.circle(surf_bolha, (r, g, b, 255), (self.raio_atual, self.raio_atual), self.raio_atual, 3)
        rect_brilho = pygame.Rect(self.raio_atual * 0.3, self.raio_atual * 0.2, self.raio_atual * 0.8,
                                  self.raio_atual * 0.4)
        pygame.draw.ellipse(surf_bolha, (255, 255, 255, 160), rect_brilho)
        tela.blit(surf_bolha, (px - self.raio_atual, py - self.raio_atual))

        txt = fonte_bolha.render(self.equacao, True, (255, 255, 255))
        sombra = fonte_bolha.render(self.equacao, True, (0, 0, 0))
        tela.blit(sombra, sombra.get_rect(center=(px + 2, py + 2)))
        tela.blit(txt, txt.get_rect(center=(px, py)))

    def clicou(self, mouse_pos):
        if self.status != "ativa": return False
        return math.hypot(self.x - mouse_pos[0], self.y - mouse_pos[1]) <= self.raio_atual


def gerar_equacao(alvo, nivel, e_correta, equacoes_existentes):
    if nivel <= 2:
        operacoes, negativos, faixa_erro = ['+', '-'], False, 2
    elif nivel <= 5:
        operacoes, negativos, faixa_erro = ['+', '-', '*', '/'], False, 3
    else:
        operacoes, negativos, faixa_erro = ['+', '-', '*', '/'], True, 5
    alvo_real = alvo if e_correta else alvo + random.choice([i for i in range(-faixa_erro, faixa_erro + 1) if i != 0])

    for _ in range(100):
        op = random.choice(operacoes)
        if op == '+':
            a = random.randint(-5 if negativos else 1, alvo_real + 5)
            b = alvo_real - a
            if b < 0 and not negativos: continue
            eq = f"{a} + ({b})" if b < 0 else f"{a} + {b}"
        elif op == '-':
            b = random.randint(-5 if negativos else 1, 15)
            a = alvo_real + b
            eq = f"{a} - ({b})" if b < 0 else f"{a} - {b}"
        elif op == '*':
            divs = [i for i in range(1, abs(alvo_real) + 1) if i != 0 and alvo_real % i == 0]
            a = random.choice(divs) if divs else 1
            b = alvo_real // a
            if negativos and random.choice([True, False]): a, b = -a, -b
            eq = f"{a} x {b}"
        elif op == '/':
            b = random.randint(2, 5)
            a = alvo_real * b
            eq = f"{a} / {b}"

        if eq not in equacoes_existentes:
            return eq

    return f"{alvo_real - 1} + 1"


def tela_relatorio_nivel(tela, historico, nivel):
    clock = pygame.time.Clock()
    frames = 0
    tempo_limite = 20 * 60
    while frames < tempo_limite:
        frames += 1
        seg_exibidos = 20 - (frames // 60)
        tela.fill(COR_FUNDO)
        margem_x, margem_y = 60, 80
        pygame.draw.rect(tela, (240, 240, 245),
                         (margem_x, margem_y, LARGURA_TELA - (margem_x * 2), ALTURA_TELA - (margem_y * 2)),
                         border_radius=15)

        titulo = f"TEMPO ESGOTADO! (FIM DO NÍVEL {nivel})"
        txt_t = fonte_pontos.render(titulo, True, (200, 50, 50))
        tela.blit(txt_t, txt_t.get_rect(center=(LARGURA_TELA // 2, margem_y + 40)))

        pygame.draw.line(tela, (180, 180, 180), (margem_x + 30, margem_y + 90),
                         (LARGURA_TELA - margem_x - 30, margem_y + 90), 2)

        # Configuração das 3 Colunas
        col1_x = margem_x + 30
        col2_x = margem_x + 400
        col3_x = margem_x + 770

        tela.blit(fonte_hud.render(f"ACERTOS: {len(historico['acertos'])}", True, (0, 120, 0)),
                  (col1_x, margem_y + 110))
        tela.blit(fonte_hud.render(f"ERROS CLIQUE: {len(historico['erros'])}", True, (180, 0, 0)),
                  (col2_x, margem_y + 110))
        tela.blit(fonte_hud.render(f"DEIXOU PASSAR: {len(historico['ignoradas'])}", True, (200, 100, 0)),
                  (col3_x, margem_y + 110))

        y_linha = margem_y + 160

        for i, eq in enumerate(historico['acertos'][-14:]):
            tela.blit(fonte_relatorio.render(eq, True, (60, 60, 60)), (col1_x, y_linha + (i * 28)))

        for i, eq in enumerate(historico['erros'][-14:]):
            tela.blit(fonte_relatorio.render(eq, True, (180, 40, 40)), (col2_x, y_linha + (i * 28)))

        for i, eq in enumerate(historico['ignoradas'][-14:]):
            tela.blit(fonte_relatorio.render(eq, True, (200, 100, 0)), (col3_x, y_linha + (i * 28)))

        # --- O NOVO RODAPÉ (Mais limpo e sutil) ---
        texto_espaco = fonte_relatorio.render("Pressione [ESPAÇO] para avançar agora", True, (120, 120, 120))
        tela.blit(texto_espaco, (LARGURA_TELA // 2 - texto_espaco.get_width() // 2, ALTURA_TELA - margem_y - 35))

        texto_timer = fonte_relatorio.render(f"Avanço automático em: {seg_exibidos}s", True, (150, 150, 150))
        tela.blit(texto_timer, (LARGURA_TELA - margem_x - 280, ALTURA_TELA - margem_y - 35))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE: return
            if ev.type == pygame.MOUSEBUTTONDOWN: return

        pygame.display.flip()
        clock.tick(60)


def jogar_bolhas():
    tela = pygame.display.get_surface()
    clock = pygame.time.Clock()

    nivel_atual, pontuacao = 1, 0
    acertos_nivel = 0
    alvo = random.randint(10, 20)

    bolhas, historico = [], {"acertos": [], "erros": [], "ignoradas": []}

    tempo_restante_float = 35.0
    frames_spawn = 0

    while nivel_atual <= 10:
        dt = clock.tick(60) / 1000.0
        tempo_restante_float -= dt
        if tempo_restante_float < 0: tempo_restante_float = 0

        mouse_pos = pygame.mouse.get_pos()

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for b in bolhas:
                    if b.clicou(mouse_pos):
                        if b.e_correta:
                            b.status = "explodindo_certa"
                            pontuacao += 10
                            acertos_nivel += 1
                            historico["acertos"].append(f"{b.equacao} = {alvo}")
                        else:
                            b.status = "explodindo_errada"
                            pontuacao -= 5
                            try:
                                v_erro = eval(b.equacao.replace("x", "*"))
                            except:
                                v_erro = "?"
                            historico["erros"].append(f"{b.equacao} = {v_erro} (Não é {alvo})")
                        break

        for b in bolhas:
            b.atualizar()
            if b.status == "morta_tempo":
                if b.e_correta:
                    historico["ignoradas"].append(f"{b.equacao} = {alvo}")
                b.status = "morta"

        if tempo_restante_float <= 0:
            for b in bolhas:
                if b.status == "ativa" and b.e_correta:
                    historico["ignoradas"].append(f"{b.equacao} = {alvo}")

            tela_relatorio_nivel(tela, historico, nivel_atual)

            nivel_atual += 1
            acertos_nivel = 0
            historico = {"acertos": [], "erros": [], "ignoradas": []}

            if nivel_atual > 10: break

            tempo_restante_float = 35.0
            alvo = random.randint(10 + (nivel_atual * 2), 30 + (nivel_atual * 5))
            bolhas.clear()
            frames_spawn = 0
            continue

        frames_spawn += 1
        max_bolhas_tela = min(3 + nivel_atual, 12)
        spawn_rate = max(20, 80 - (nivel_atual * 6))

        if frames_spawn >= spawn_rate and len([b for b in bolhas if b.status == "ativa"]) < max_bolhas_tela:
            e_correta = random.random() < 0.38
            eqs_ativas = [b.equacao for b in bolhas if b.status == "ativa"]
            nova_eq = gerar_equacao(alvo, nivel_atual, e_correta, eqs_ativas)
            t_vida = 10 if nivel_atual <= 3 else (6 if nivel_atual <= 6 else 4)

            for _ in range(40):
                nx, ny = random.randint(150, LARGURA_TELA - 150), random.randint(120, ALTURA_TELA - 250)
                if not any(math.hypot(nx - b.x, ny - b.y) < 120 for b in bolhas if b.status == "ativa"):
                    bolhas.append(Bolha(nx, ny, nova_eq, e_correta, t_vida))
                    frames_spawn = 0
                    break

        bolhas = [b for b in bolhas if b.status != "morta"]

        tela.fill(COR_FUNDO)
        pygame.draw.rect(tela, (20, 25, 45), (0, 0, LARGURA_TELA, 80))
        pygame.draw.line(tela, (100, 150, 255), (0, 80), (LARGURA_TELA, 80), 3)

        txt_n = fonte_hud.render(f"NÍVEL {nivel_atual}", True, (0, 255, 150))
        tela.blit(txt_n, (40, 22))

        txt_meta = fonte_hud.render(f"ACERTOS: {acertos_nivel}", True, (200, 200, 200))
        tela.blit(txt_meta, (250, 22))

        txt_p = fonte_pontos.render(f"PONTOS: {pontuacao}", True, (255, 255, 255))
        tela.blit(txt_p, (LARGURA_TELA // 2 - 120, 15))

        cor_t = (255, 50, 50) if tempo_restante_float <= 10 else (255, 255, 0)
        txt_tm = fonte_hud.render(f"TEMPO: {int(tempo_restante_float):02d}s", True, cor_t)
        tela.blit(txt_tm, (LARGURA_TELA - 220, 22))

        painel_w, painel_h = 500, 120
        px_painel, py_painel = (LARGURA_TELA // 2) - (painel_w // 2), ALTURA_TELA - 140
        pygame.draw.rect(tela, (25, 30, 50), (px_painel, py_painel, painel_w, painel_h), border_radius=25)
        pygame.draw.rect(tela, (50, 255, 150), (px_painel, py_painel, painel_w, painel_h), 3, border_radius=25)

        tela.blit(fonte_alvo_label.render("SOMA ALVO:", True, (200, 200, 200)), (px_painel + 20, py_painel + 35))
        tela.blit(fonte_alvo_num.render(str(alvo), True, (50, 255, 150)), (px_painel + 320, py_painel + 15))

        for b in bolhas: b.desenhar(tela)
        pygame.display.flip()

    bateu_rec = salvar_record_bolhas(pontuacao)
    tela.fill(COR_FUNDO)

    txt_v = fonte_alvo_num.render("TREINAMENTO CONCLUÍDO!", True, (0, 255, 150))
    tela.blit(txt_v, txt_v.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 60)))

    txt_f = fonte_pontos.render(f"PONTUAÇÃO TOTAL: {pontuacao} Pts", True, (255, 255, 255))
    tela.blit(txt_f, txt_f.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 30)))

    if bateu_rec:
        txt_r = fonte_pontos.render("NOVO RECORDE ALCANÇADO!", True, (255, 215, 0))
        tela.blit(txt_r, txt_r.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 90)))

    pygame.display.flip()
    pygame.time.delay(5000)