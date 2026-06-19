import pygame
import sys
import random
import json
import os
from settings import *

pygame.font.init()
fonte_jornal = pygame.font.SysFont("Georgia", 24, bold=False)
fonte_jornal_destaque = pygame.font.SysFont("Georgia", 24, bold=True)
fonte_hud = pygame.font.SysFont("Arial", 26, bold=True)
fonte_pontos = pygame.font.SysFont("Trebuchet MS", 40, bold=True)
fonte_dica = pygame.font.SysFont("Arial", 16, bold=True)
fonte_relatorio = pygame.font.SysFont("Courier New", 16, bold=True)

# =======================================================
# 📚 MEGA BANCO DE FRASES (Agora com 15 opções por nível!)
# =======================================================
BANCO_DE_FRASES = {
    1: [
        {"f": "I is a new developer here.", "erro": "is", "corr": "am", "dica": "Usa-se 'am' com o pronome 'I'.",
         "tipo": "Gramática"},
        {"f": "She make new codes every day.", "erro": "make", "corr": "makes",
         "dica": "Adiciona-se 'S' no verbo para He/She/It.", "tipo": "Conjugação"},
        {"f": "We has a big problem.", "erro": "has", "corr": "have",
         "dica": "Has é apenas para He/She/It. We usa Have.", "tipo": "Gramática"},
        {"f": "The softwares are broken.", "erro": "softwares", "corr": "software",
         "dica": "Software é incontável (não tem S).", "tipo": "Plural"},
        {"f": "The code wich I wrote works.", "erro": "wich", "corr": "which", "dica": "Falta a letra H (Which).",
         "tipo": "Ortografia"},
        {"f": "They goes to the office.", "erro": "goes", "corr": "go", "dica": "O pronome They não leva 'S' no verbo.",
         "tipo": "Conjugação"},
        {"f": "I did it becouse I wanted to.", "erro": "becouse", "corr": "because",
         "dica": "A grafia correta é Because.", "tipo": "Ortografia"},
        {"f": "The mouses are on the desk.", "erro": "mouses", "corr": "mice",
         "dica": "O plural de mouse pode ser mice.", "tipo": "Plural Irregular"},
        {"f": "It is verry important.", "erro": "verry", "corr": "very", "dica": "Very se escreve com apenas um R.",
         "tipo": "Ortografia"},
        {"f": "You is completely right.", "erro": "is", "corr": "are", "dica": "Usa-se 'are' com o pronome 'You'.",
         "tipo": "Gramática"},
        {"f": "I wants to learn Python.", "erro": "wants", "corr": "want", "dica": "O pronome I não leva 'S'.",
         "tipo": "Conjugação"},
        {"f": "He dont like to program.", "erro": "dont", "corr": "doesn't",
         "dica": "He/She/It na negativa usa doesn't.", "tipo": "Gramática"},
        {"f": "We needs to fix this bug.", "erro": "needs", "corr": "need", "dica": "O pronome We não leva 'S'.",
         "tipo": "Conjugação"},
        {"f": "The childs are playing.", "erro": "childs", "corr": "children", "dica": "O plural de child é children.",
         "tipo": "Plural Irregular"},
        {"f": "It happen all the time.", "erro": "happen", "corr": "happens",
         "dica": "Adiciona-se 'S' no verbo para o pronome It.", "tipo": "Conjugação"}
    ],
    2: [
        {"f": "I am waiting at the morning.", "erro": "at", "corr": "in",
         "dica": "Períodos do dia usam 'in' (in the morning).", "tipo": "Preposições"},
        {"f": "This is better then Java.", "erro": "then", "corr": "than",
         "dica": "Then=Então. Than=Do que (Comparação).", "tipo": "Conectivos"},
        {"f": "Did you recieve the email?", "erro": "recieve", "corr": "receive",
         "dica": "I antes de E, exceto após C (Receive).", "tipo": "Ortografia"},
        {"f": "The project was a huge sucess.", "erro": "sucess.", "corr": "success.",
         "dica": "Success possui dois C's e dois S's.", "tipo": "Ortografia"},
        {"f": "She runs fastly to the meeting.", "erro": "fastly", "corr": "fast",
         "dica": "A palavra 'fast' não aceita 'ly'.", "tipo": "Advérbios"},
        {"f": "We have a new buisness model.", "erro": "buisness", "corr": "business",
         "dica": "A letra I vem depois do S (Bus-i-ness).", "tipo": "Ortografia"},
        {"f": "Please send it to my adress.", "erro": "adress.", "corr": "address.",
         "dica": "Address escreve-se com dois D's e dois S's.", "tipo": "Ortografia"},
        {"f": "He is married with a designer.", "erro": "with", "corr": "to",
         "dica": "Diz-se casado 'para' alguém (married to).", "tipo": "Preposições"},
        {"f": "I am good in programming.", "erro": "in", "corr": "at", "dica": "Ser bom em algo é 'Good at'.",
         "tipo": "Preposições"},
        {"f": "I agree with you in this.", "erro": "in", "corr": "on", "dica": "Concordar com algo é 'Agree on'.",
         "tipo": "Preposições"},
        {"f": "He traveled to London in Monday.", "erro": "in", "corr": "on",
         "dica": "Dias da semana exigem 'on' (on Monday).", "tipo": "Preposições"},
        {"f": "I am tired to write codes.", "erro": "to", "corr": "of", "dica": "A expressão correta é 'Tired of'.",
         "tipo": "Preposições"},
        {"f": "She is interesting in the project.", "erro": "interesting", "corr": "interested",
         "dica": "Interested = Interessado (Sentimento).", "tipo": "Vocabulário"},
        {"f": "We arrived at Paris yesterday.", "erro": "at", "corr": "in",
         "dica": "Chegar a uma cidade ou país exige 'in'.", "tipo": "Preposições"},
        {"f": "He speaks english very good.", "erro": "good.", "corr": "well.",
         "dica": "Good é adjetivo. Well é advérbio (fala bem).", "tipo": "Advérbios"}
    ],
    3: [
        {"f": "I pretend to apply for this job.", "erro": "pretend", "corr": "intend",
         "dica": "Pretend=Fingir. Intend=Pretender.", "tipo": "Falsos Cognatos"},
        {"f": "Actually, I am working remotely.", "erro": "Actually,", "corr": "Currently,",
         "dica": "Actually=Na verdade. Currently=Atualmente.", "tipo": "Falsos Cognatos"},
        {"f": "We need to setup the enviroment.", "erro": "enviroment.", "corr": "environment.",
         "dica": "Esqueceu do N silencioso (Environ-ment).", "tipo": "Ortografia"},
        {"f": "The developement phase is over.", "erro": "developement", "corr": "development",
         "dica": "Não tem a letra E no meio (Develop-ment).", "tipo": "Ortografia"},
        {"f": "I losted my root password.", "erro": "losted", "corr": "lost",
         "dica": "Lost é irregular, não leva 'ed'.", "tipo": "Tempos Verbais"},
        {"f": "We must seperate the files.", "erro": "seperate", "corr": "separate",
         "dica": "A grafia correta possui dois A's (SepArate).", "tipo": "Ortografia"},
        {"f": "Can you support the door?", "erro": "support", "corr": "hold",
         "dica": "Support=Apoiar(ideia). Hold=Segurar(físico).", "tipo": "Vocabulário"},
        {"f": "I have 30 years old.", "erro": "have", "corr": "am", "dica": "Você 'é' velho, não 'tem' anos (I am).",
         "tipo": "Tradução Direta"},
        {"f": "The grammer in this code is bad.", "erro": "grammer", "corr": "grammar",
         "dica": "Grammar termina com A, e não com E.", "tipo": "Ortografia"},
        {"f": "Please explain me the code.", "erro": "explain", "corr": "explain to",
         "dica": "O verbo Explain exige 'to'.", "tipo": "Regras de Verbo"},
        {"f": "Please, resume the meeting details.", "erro": "resume", "corr": "summarize",
         "dica": "Resume=Retomar. Summarize=Resumir.", "tipo": "Falsos Cognatos"},
        {"f": "Did you assist the class yesterday?", "erro": "assist", "corr": "attend",
         "dica": "Assist=Ajudar. Attend=Assistir/Comparecer.", "tipo": "Falsos Cognatos"},
        {"f": "My boss is very comprehensive.", "erro": "comprehensive.", "corr": "understanding.",
         "dica": "Comprehensive=Abrangente. Understanding=Compreensivo.", "tipo": "Falsos Cognatos"},
        {"f": "I am making my homework.", "erro": "making", "corr": "doing",
         "dica": "Tarefas e deveres usam o verbo 'do'.", "tipo": "Make vs Do"},
        {"f": "We will have a notice board.", "erro": "notice", "corr": "bulletin",
         "dica": "Notice board existe, mas no meio tech usa-se dashboard ou bulletin.", "tipo": "Vocabulário"}
    ],
    4: [
        {"f": "I will advice you later.", "erro": "advice", "corr": "advise",
         "dica": "Advice=Conselho. Advise=Aconselhar(Verbo).", "tipo": "Ortografia"},
        {"f": "The bug will effect the system.", "erro": "effect", "corr": "affect",
         "dica": "Affect=Afetar(Verbo). Effect=Efeito(Substantivo).", "tipo": "Vocabulário"},
        {"f": "Can you accomodate the guests?", "erro": "accomodate", "corr": "accommodate",
         "dica": "Possui dois C's e dois M's.", "tipo": "Ortografia"},
        {"f": "I recomend this new software.", "erro": "recomend", "corr": "recommend",
         "dica": "Recommend possui dois M's.", "tipo": "Ortografia"},
        {"f": "Please, reply the email.", "erro": "reply", "corr": "reply to",
         "dica": "O verbo Reply exige a preposição 'to'.", "tipo": "Preposições"},
        {"f": "The comittee approved the change.", "erro": "comittee", "corr": "committee",
         "dica": "Committee tem 2 M's, 2 T's e 2 E's.", "tipo": "Ortografia"},
        {"f": "I look forward to hear from you.", "erro": "hear", "corr": "hearing",
         "dica": "'Look forward to' exige ING no próximo verbo.", "tipo": "Expressões"},
        {"f": "He gave a strong argumment.", "erro": "argumment.", "corr": "argument.",
         "dica": "Argument possui apenas um M.", "tipo": "Ortografia"},
        {"f": "It depends on how much does it cost.", "erro": "does", "corr": "---",
         "dica": "Frases indiretas não invertem verbo.", "tipo": "Estrutura de Frase"},
        {"f": "Remind to lock the door.", "erro": "Remind", "corr": "Remember",
         "dica": "Remind=Lembrar alguém. Remember=Lembrar de algo.", "tipo": "Vocabulário"},
        {"f": "Everyone was there, accept John.", "erro": "accept", "corr": "except",
         "dica": "Accept=Aceitar. Except=Exceto.", "tipo": "Ortografia"},
        {"f": "We need to discuss about the budget.", "erro": "about", "corr": "---",
         "dica": "Discuss já significa 'falar sobre', não usa 'about'.", "tipo": "Redundância"},
        {"f": "I lost the bus this morning.", "erro": "lost", "corr": "missed",
         "dica": "Missed=Perder(evento/transporte). Lost=Perder(objeto).", "tipo": "Vocabulário"},
        {"f": "Despite of the rain, we worked.", "erro": "of", "corr": "---",
         "dica": "Despite não leva 'of' (In spite of leva).", "tipo": "Preposições"},
        {"f": "He is doing a great job untill now.", "erro": "untill", "corr": "until",
         "dica": "Until tem apenas um L (diferente de Till).", "tipo": "Ortografia"}
    ],
    5: [
        {"f": "Their are thousands of active users.", "erro": "Their", "corr": "There",
         "dica": "Their=Deles (Posse). There are=Existem/Há.", "tipo": "Ortografia"},
        {"f": "We definitly need to launch.", "erro": "definitly", "corr": "definitely",
         "dica": "A grafia correta possui um 'E': Definitely.", "tipo": "Ortografia"},
        {"f": "It is absolutely neccessary.", "erro": "neccessary.", "corr": "necessary.",
         "dica": "Necessary tem apenas um C e dois S's.", "tipo": "Ortografia"},
        {"f": "It was an unexpected ocurrence.", "erro": "ocurrence.", "corr": "occurrence.",
         "dica": "Occurrence possui dois C's e dois R's.", "tipo": "Ortografia"},
        {"f": "The informations are clear.", "erro": "informations", "corr": "information",
         "dica": "Information é incontável.", "tipo": "Plural Irregular"},
        {"f": "He is an excellent profissional.", "erro": "profissional.", "corr": "professional.",
         "dica": "Em inglês escreve-se com E e dois S's.", "tipo": "Ortografia"},
        {"f": "She is one of the only person.", "erro": "person.", "corr": "people.",
         "dica": "Expressão 'One of the...' exige plural.", "tipo": "Concordância"},
        {"f": "Between you and I, this is wrong.", "erro": "I,", "corr": "me,",
         "dica": "Após preposição usa-se pronome objeto (me).", "tipo": "Pronomes"},
        {"f": "It is a privilege to work here.", "erro": "priviledge", "corr": "privilege",
         "dica": "Escreve-se sem a letra D no meio.", "tipo": "Ortografia"},
        {"f": "I prefer coffee than tea.", "erro": "than", "corr": "to",
         "dica": "O verbo Prefer exige a preposição 'to'.", "tipo": "Preposições"},
        {"f": "Its a great day for coding.", "erro": "Its", "corr": "It's",
         "dica": "Its=Posse. It's=Contração de It is.", "tipo": "Ortografia"},
        {"f": "He is a independent professional.", "erro": "a", "corr": "an",
         "dica": "Usa-se 'an' antes de palavras com som de vogal.", "tipo": "Artigos"},
        {"f": "I could of done it better.", "erro": "of", "corr": "have",
         "dica": "Could've vem de Could Have, não 'of'.", "tipo": "Erro Nativo"},
        {"f": "The code who I wrote works.", "erro": "who", "corr": "which",
         "dica": "Who é para pessoas. Coisas usa-se Which/That.", "tipo": "Pronomes Relativos"},
        {"f": "I am used to work late.", "erro": "work", "corr": "working",
         "dica": "I am used to + Verbo com ING (Estar acostumado a).", "tipo": "Expressões"}
    ]
}

# --- FRASES DE PREENCHIMENTO (Expandido para dar mais variedade aos parágrafos) ---
FRASES_PREENCHIMENTO = [
    "The team had a quick daily scrum meeting.",
    "Our goal is to deliver high-quality software.",
    "The deployment will happen on Friday night.",
    "We need to check the server logs.",
    "Please review the pull request when possible.",
    "The client requested a new dashboard feature.",
    "Agile methodologies help us work faster.",
    "Data analysis is crucial for this step."
]


def gerar_texto_aleatorio(nivel):
    nivel_banco = min(nivel, 5)

    # 1. Pega todas as 15 frases do nível atual e SORTEIA APENAS 10!
    todas_frases_do_nivel = BANCO_DE_FRASES[nivel_banco]
    frases_com_erro = random.sample(todas_frases_do_nivel, 10)

    # 2. Pega 2 ou 3 frases limpas sorteadas para o texto não ficar tão artificial
    qtd_limpas = random.randint(2, 3)
    frases_limpas = random.sample(FRASES_PREENCHIMENTO, qtd_limpas)

    todas_as_frases = []
    erros_finais = {}

    for item in frases_com_erro:
        todas_as_frases.append(item["f"])
        erros_finais[item["erro"]] = {"corr": item["corr"], "dica": item["dica"], "tipo": item["tipo"]}

    for item in frases_limpas:
        todas_as_frases.append(item)

    # 3. Embaralha tudo para que o jogador nunca saiba onde os erros estão
    random.shuffle(todas_as_frases)

    texto_final = ""
    for i, frase in enumerate(todas_as_frases):
        texto_final += frase + " "
        # Quebra de linha a cada 4 ou 5 frases para não ficar um paredão de texto
        if (i + 1) % 4 == 0 and i < len(todas_as_frases) - 1:
            texto_final += "\n\n"

    return {"nivel": nivel, "texto": texto_final.strip(), "erros": erros_finais}


# =======================================================
# 🧠 O MOTOR DE TEXTO CLICÁVEL E HOVER
# =======================================================
class PalavraClicavel:
    def __init__(self, texto, x, y, eh_erro, info_erro):
        self.texto_original = texto
        self.texto_atual = texto
        self.rect = pygame.Rect(x, y, 0, 0)
        self.eh_erro = eh_erro
        self.info_erro = info_erro
        self.status = "normal"
        self.piscar_dica = 0


def renderizar_paragrafo(tela, palavras, margem_x, margem_y, max_w, mouse_pos):
    x, y = margem_x, margem_y
    for p in palavras:
        if p.texto_original == "\n\n":
            x = margem_x
            y += 40
            continue

        fonte = fonte_jornal_destaque if p.status == "descoberto" else fonte_jornal

        cor_texto = (30, 30, 30)
        cor_fundo = None

        if p.status == "normal":
            if p.rect.collidepoint(mouse_pos) and p.texto_original != "\n\n":
                cor_fundo = (220, 225, 230)
        elif p.status == "descoberto":
            cor_texto = (0, 150, 0)
        elif p.status == "erro_clique":
            cor_texto = (200, 0, 0)

        if p.piscar_dica > 0:
            cor_fundo = (255, 255, 100)
            p.piscar_dica -= 1

        txt_img = fonte.render(p.texto_atual, True, cor_texto)
        w, h = txt_img.get_size()

        if x + w > margem_x + max_w:
            x = margem_x
            y += 35

        p.rect = pygame.Rect(x, y, w, h)

        if cor_fundo:
            pygame.draw.rect(tela, cor_fundo, p.rect, border_radius=4)

        tela.blit(txt_img, (x, y))
        x += w + 8


def tela_relatorio_ingles(tela, historico_erros, nivel, concluiu):
    frames = 0
    while frames < 60 * 25:
        frames += 1
        tela.fill(COR_FUNDO)
        margem_x, margem_y = 40, 60
        pygame.draw.rect(tela, (250, 250, 245),
                         (margem_x, margem_y, LARGURA_TELA - (margem_x * 2), ALTURA_TELA - (margem_y * 2)),
                         border_radius=10)

        titulo = f"NÍVEL {nivel} CONCLUÍDO!" if concluiu else "TEMPO ESGOTADO! ESTUDE SEUS ERROS:"
        txt_t = fonte_pontos.render(titulo, True, (30, 150, 30) if concluiu else (200, 50, 50))
        tela.blit(txt_t, txt_t.get_rect(center=(LARGURA_TELA // 2, margem_y + 35)))
        pygame.draw.line(tela, (200, 200, 200), (margem_x + 40, margem_y + 70),
                         (LARGURA_TELA - margem_x - 40, margem_y + 70), 2)

        y_linha = margem_y + 90
        for erro_original, dados in historico_erros.items():
            if dados.get('achou', False):
                texto = f"✅ Você corrigiu: '{dados['corr']}' (O erro era '{erro_original}') ➔ {dados['dica']}"
                cor = (0, 120, 0)
            else:
                texto = f"❌ Passou batido: O correto era '{dados['corr']}' (Não '{erro_original}') ➔ {dados['dica']}"
                cor = (180, 0, 0)

            img_r = fonte_relatorio.render(texto, True, cor)
            tela.blit(img_r, (margem_x + 30, y_linha))
            y_linha += 35

        tela.blit(fonte_relatorio.render("Pressione [ESPAÇO] para o próximo desafio.", True, (150, 150, 150)),
                  (LARGURA_TELA // 2 - 250, ALTURA_TELA - margem_y - 25))

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE: return
            if ev.type == pygame.MOUSEBUTTONDOWN: return

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# =======================================================
# 👨‍🏫 AVALIAÇÃO FINAL: COM DIAGNÓSTICO CATEGORIZADO
# =======================================================
def tela_diagnostico_final(tela, pontuacao, total_cliques_errados, total_deixou_passar, categorias_perdidas):
    tela.fill(COR_FUNDO)
    margem_x, margem_y = 150, 100
    pygame.draw.rect(tela, (250, 250, 245),
                     (margem_x, margem_y, LARGURA_TELA - (margem_x * 2), ALTURA_TELA - (margem_y * 2)),
                     border_radius=15)

    # CORREÇÃO AQUI: Troquei fonte_alvo_num (que não existe) por fonte_pontos!
    txt_v = fonte_pontos.render("DIAGNÓSTICO FINAL", True, (0, 100, 200))
    tela.blit(txt_v, txt_v.get_rect(center=(LARGURA_TELA // 2, margem_y + 60)))

    erros_totais = total_cliques_errados + total_deixou_passar
    if erros_totais <= 5:
        opiniao, cor_op = "IMPECÁVEL! Seu inglês técnico é Nível Nativo.", (0, 150, 0)
    elif erros_totais <= 15:
        opiniao, cor_op = "MUITO BOM! Fluência garantida. Requer revisões leves.", (150, 150, 0)
    elif erros_totais <= 25:
        opiniao, cor_op = "INTERMEDIÁRIO. Entende o contexto, mas falta precisão.", (200, 100, 0)
    else:
        opiniao, cor_op = "ATENÇÃO! Sua atenção visual e gramática precisam de revisão profunda.", (200, 50, 50)

    ponto_fraco = max(categorias_perdidas,
                      key=categorias_perdidas.get) if categorias_perdidas else "Nenhum (Você é impecável)"

    tela.blit(fonte_hud.render(f"Cliques errados (Precipitação): {total_cliques_errados}", True, (50, 50, 50)),
              (margem_x + 80, margem_y + 160))
    tela.blit(fonte_hud.render(f"Erros que passaram batido: {total_deixou_passar}", True, (50, 50, 50)),
              (margem_x + 80, margem_y + 210))

    txt_fraco = fonte_hud.render(f"Ponto fraco para estudar: {ponto_fraco}", True, (200, 50, 50))
    tela.blit(txt_fraco, (margem_x + 80, margem_y + 260))

    tela.blit(fonte_pontos.render(opiniao, True, cor_op), (margem_x + 80, margem_y + 340))
    tela.blit(fonte_pontos.render(f"PONTUAÇÃO TOTAL: {pontuacao} Pts", True, (0, 0, 0)),
              (margem_x + 80, margem_y + 420))

    pygame.display.flip()
    pygame.time.delay(10000)


def desenhar_botao_dica(superficie, x, y, mouse_pos):
    rect = pygame.Rect(x, y, 160, 40)
    colidiu = rect.collidepoint(mouse_pos)
    cor = (200, 150, 0) if colidiu else (180, 120, 0)
    pygame.draw.rect(superficie, cor, rect, border_radius=8)
    txt = fonte_dica.render("💡 DICA (-5s)", True, (255, 255, 255))
    superficie.blit(txt, txt.get_rect(center=rect.center))
    return colidiu


# =======================================================
# MOTOR DO JOGO PRINCIPAL
# =======================================================
def jogar_ingles():
    tela = pygame.display.get_surface()
    clock = pygame.time.Clock()

    pontuacao = 0
    nivel_atual = 1
    total_cliques_errados = 0
    total_deixou_passar = 0
    categorias_perdidas = {}

    while nivel_atual <= 5:
        dados = gerar_texto_aleatorio(nivel_atual)
        palavras_obj = []
        partes = dados["texto"].replace("\n\n", " \n\n ").split(" ")
        for p in partes:
            eh_erro = p in dados["erros"]
            info = dados["erros"][p] if eh_erro else None
            palavras_obj.append(PalavraClicavel(p, 0, 0, eh_erro, info))

        tempo_maximo = 90.0 - ((nivel_atual - 1) * 5.0)
        tempo_restante_float = tempo_maximo
        erros_restantes = 10
        dicas_flutuantes = []

        combo_atual = 1
        mostrar_combo_timer = 0

        rodando_nivel = True
        while rodando_nivel:
            dt = clock.tick(60) / 1000.0
            tempo_restante_float -= dt
            if tempo_restante_float < 0: tempo_restante_float = 0

            mouse_pos = pygame.mouse.get_pos()

            btn_dica_x, btn_dica_y = LARGURA_TELA - 200, 100
            hover_dica = pygame.Rect(btn_dica_x, btn_dica_y, 160, 40).collidepoint(mouse_pos)

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:

                    if hover_dica and tempo_restante_float > 5:
                        tempo_restante_float -= 5
                        pontuacao -= 10
                        combo_atual = 1
                        nao_descobertas = [p for p in palavras_obj if p.eh_erro and p.status != "descoberto"]
                        if nao_descobertas:
                            random.choice(nao_descobertas).piscar_dica = 60
                        continue

                    for p in palavras_obj:
                        if p.rect.collidepoint(mouse_pos) and p.texto_original != "\n\n":
                            if p.eh_erro and p.status != "descoberto":
                                p.status = "descoberto"
                                p.texto_atual = p.info_erro["corr"]
                                pts_ganhos = 20 * combo_atual
                                pontuacao += pts_ganhos
                                combo_atual += 1
                                mostrar_combo_timer = 90

                                erros_restantes -= 1
                                dados['erros'][p.texto_original]['achou'] = True
                                dicas_flutuantes.append(
                                    {"txt": f"+{pts_ganhos} (Dica: {p.info_erro['dica']})", "x": p.rect.x,
                                     "y": p.rect.y, "timer": 100})

                            elif not p.eh_erro and p.status == "normal":
                                p.status = "erro_clique"
                                combo_atual = 1
                                pontuacao -= 5
                                tempo_restante_float -= 2.0
                                total_cliques_errados += 1

                                categorias_perdidas["Atenção Visual / Leitura"] = categorias_perdidas.get(
                                    "Atenção Visual / Leitura", 0) + 1
                            break

            if erros_restantes <= 0 or tempo_restante_float <= 0:
                for erro, infos in dados['erros'].items():
                    if 'achou' not in infos:
                        infos['achou'] = False
                        total_deixou_passar += 1
                        cat = infos["tipo"]
                        categorias_perdidas[cat] = categorias_perdidas.get(cat, 0) + 1

                tela_relatorio_ingles(tela, dados['erros'], nivel_atual, (erros_restantes <= 0))
                nivel_atual += 1
                break

            # --- RENDERIZAÇÃO ---
            tela.fill(COR_FUNDO)
            pygame.draw.rect(tela, (20, 25, 45), (0, 0, LARGURA_TELA, 80))
            pygame.draw.line(tela, (100, 150, 255), (0, 80), (LARGURA_TELA, 80), 3)

            tela.blit(fonte_hud.render(f"SYNTAX HACKER | NÍVEL {nivel_atual}", True, (0, 255, 150)), (40, 22))

            cor_pts = (255, 255, 255) if combo_atual == 1 else (50, 255, 100)
            tela.blit(fonte_pontos.render(f"PONTOS: {pontuacao}", True, cor_pts), (LARGURA_TELA // 2 - 100, 15))

            cor_t = (255, 50, 50) if tempo_restante_float <= 15 else (255, 255, 0)
            tela.blit(fonte_hud.render(f"TEMPO: {int(tempo_restante_float):02d}s", True, cor_t),
                      (LARGURA_TELA - 200, 22))
            tela.blit(fonte_hud.render(f"BUGS ESCONDIDOS: {erros_restantes}/10", True, (255, 100, 100)),
                      (LARGURA_TELA // 2 - 160, 100))

            desenhar_botao_dica(tela, btn_dica_x, btn_dica_y, mouse_pos)

            margem_folha_x, margem_folha_y = 80, 150
            w_folha, h_folha = LARGURA_TELA - (margem_folha_x * 2), ALTURA_TELA - margem_folha_y - 20
            pygame.draw.rect(tela, (250, 250, 245), (margem_folha_x, margem_folha_y, w_folha, h_folha), border_radius=5)
            pygame.draw.line(tela, (150, 150, 150), (margem_folha_x + w_folha, margem_folha_y + 10),
                             (margem_folha_x + w_folha, margem_folha_y + h_folha), 3)

            renderizar_paragrafo(tela, palavras_obj, margem_folha_x + 30, margem_folha_y + 30, w_folha - 60, mouse_pos)

            if mostrar_combo_timer > 0 and combo_atual > 1:
                txt_combo = fonte_pontos.render(f"COMBO {combo_atual - 1}X!", True, (0, 200, 0))
                tela.blit(txt_combo, (margem_folha_x + 30, 95))
                mostrar_combo_timer -= 1

            for d in dicas_flutuantes:
                if d["timer"] > 0:
                    d["y"] -= 1.0
                    d["timer"] -= 1
                    txt_d = fonte_dica.render(d["txt"], True, (200, 100, 0))
                    tela.blit(txt_d, (d["x"], d["y"] - 20))

            pygame.display.flip()

    tela_diagnostico_final(tela, pontuacao, total_cliques_errados, total_deixou_passar, categorias_perdidas)