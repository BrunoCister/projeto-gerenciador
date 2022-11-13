
import psutil, pygame, cpuinfo

# interface pygame
largura_tela = 800  # dimensoes da tela
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Informações')  # escrito no topo da janela
pygame.display.init()

pygame.font.init()
font = pygame.font.Font(None, 28)  # configura a fonte

clock = pygame.time.Clock()  # clock
cont = 60  # contador

info_cpu = cpuinfo.get_cpu_info()  # dados cpu

# cores
preto = (0, 0, 0)
branco = (255, 255, 255)
cinza = (128, 128, 128)
verde = (0, 100, 0)
vermelho = (255, 0, 0)

# surfaces
s1 = pygame.surface.Surface((largura_tela, altura_tela / 3))
s2 = pygame.surface.Surface((largura_tela, altura_tela / 3))
s3 = pygame.surface.Surface((largura_tela, altura_tela / 3))


def memoria():  # define a funçao que mostra os dados da memoria
    mem = psutil.virtual_memory()  # dados sobre a memória
    porcento = mem.percent
    usado = mem.used / 1024 ** 3
    largura_barra = largura_tela - 2 * 20
    pygame.draw.rect(s1, cinza, (20, 50, largura_barra, 10))
    tela.blit(s1, (0, 0))
    largura_barra *= mem.percent / 100
    pygame.draw.rect(s1, verde, (20, 50, largura_barra, 10))
    tela.blit(s1, (0, 0))
    total = mem.total / 1024 ** 3
    texto_barra = f'Uso da memória: {usado:.2f}GB ({porcento}%) | Total: {total:.2f}GB'
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, 10))  # texto, posiçao x, posiçao y


def cpu(l_cpu_percent):  # define a funçao q mostra os dados da cpu
    freq = psutil.cpu_freq().current
    proc = info_cpu['brand_raw']
    arquit = info_cpu['arch']
    bits = info_cpu['bits']
    nucleosl = psutil.cpu_count()
    nucleosf = psutil.cpu_count(logical=False)
    tela.blit(s2, (0, altura_tela / 3))
    texto_barra = (f'Nome do processador: {proc}')
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, 75))
    texto_barra = (f'Arquitetura: {arquit}')
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, 100))
    texto_barra = (f'Palavra (bits): {bits}')
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, 125))
    texto_barra = (f'Frequência (MHz): {freq}')
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (400, 100))
    texto_barra = (f'Núcleos (físicos): {nucleosl} ({nucleosf})')
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (400, 125))

    num_cpu = len(l_cpu_percent)
    x = y = 10
    desl = 10
    alt = s2.get_height() - 2 * y
    larg = (s2.get_width() - 2 * y - (num_cpu + 1) * desl) / num_cpu
    d = x + desl
    for i in l_cpu_percent:
        pygame.draw.rect(s2, verde, (d, y, larg, alt))
        pygame.draw.rect(s2, cinza, (d, y, larg, (1 - i / 100) * alt))
        d = d + larg + desl
    tela.blit(s2, (0, altura_tela / 3))
    cont_cpu = 0
    cpu_x = desl + larg / 2
    titulo_core = 'Percentual de uso de cada núcleo:'
    text = font.render(titulo_core, 1, branco)
    tela.blit(text, (20, 150))
    for i in l_cpu_percent:
        perc_core = f'{l_cpu_percent[cont_cpu]}%'
        cont_cpu += 1
        text = font.render(perc_core, 1, branco)
        tela.blit(text, (cpu_x, 175))
        cpu_x += larg + desl


def disco():  # define a funçao q mostra os dados da cpu
    disco = psutil.disk_usage('.')
    porcento = disco.percent
    usado = disco.used / 1024 ** 3
    larg = largura_tela - 2 * 20
    pygame.draw.rect(tela, cinza, (20, 450, larg, 10))
    larg = larg * disco.percent / 100
    pygame.draw.rect(tela, verde, (20, 450, larg, 10))
    total = round(disco.total / (1024 * 1024 * 1024), 2)
    texto_barra = f'Uso de disco: {usado:.2f}GB ({porcento}%) | Total: {total:.2f}GB'
    text = font.render(texto_barra, 1, branco)
    tela.blit(text, (20, 410))


terminou = False
while not terminou:
    for event in pygame.event.get():  # checar os eventos
        if event.type == pygame.QUIT:  # clicar no x termina
            terminou = True
    if cont == 60:
        tela.fill(preto)
        memoria()
        cpu(psutil.cpu_percent(interval=0.1, percpu=True))
        disco()
        cont = 0
    pygame.display.update()  # atualiza tela
    clock.tick(60)  # 60 fps
    cont += 1
pygame.display.quit()  # finaliza
quit()
