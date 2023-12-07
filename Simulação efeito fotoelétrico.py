
from vpython import *

scene = canvas(title='Simulação - Efeito fotoelétrico para ascender uma lâmpada', width=800, height=600)
scene.background = vector(0.5, 0.8, 1)

#### Objetos #####

#Paredes

parade_1 = box(pos=vector(30, 0, 15), size=vector(0.5, 50, 70), color=color.white)
parade_2 = box(pos=vector(5, 0, 50), size=vector(50, 50, 0.5), color=color.white)
parade_3 = box(pos=vector(5, 0, -20), size=vector(50, 50, 0.5), color=color.white)
chao = box(pos=vector(5, -25, 15), size=vector(50, 0.5, 70), color=color.white)



# Placa
placa = box(pos=vector(0, 0, 0), size=vector(15, 0.5, 15), color=color.gray(0.5))
placa.rotate(angle=radians(20), axis=vector(0, 0, 0), origin=vector(0, 0, 0))

# Fios
fio1 = box(pos=vector(0, -5, 0), size=vector(1.5, -10, 1), color=color.gray(0.5))
#fio2 = box(pos=vector(0, -10, 14.5), size=vector(1, 1, 30), color=color.gray(0.5))
fiolamp = box(pos=vector(0, -5, 29), size=vector(1.5, -10, 1), color=color.gray(0.5))

# Lugar em que os elétrons vão pasar 
fioe_1 = box(pos=vector(0, -8, 14.5), size=vector(1.5, 0.1, 30), color=color.gray(0.5))
fioe_2 = box(pos=vector(0.9, -9, 14.5), size=vector(0.1, 2, 30), color=color.gray(0.5))
fioe_3 = box(pos=vector(0, -10, 14.5), size=vector(1.5, 0.1, 30), color=color.gray(0.5))
#fioe_4 = box(pos=vector(-0.8, -9, 14.5), size=vector(0.1, 2, 30), color=color.gray(0.5),opacity=0.1)


# lâmpada 
base_lamp = cylinder(pos=vector(0, 0, 29), axis=vector(0, 3, 0), radius=1.5, color=color.gray(0.8))
corpo_lamp = cylinder(pos=vector(0, 3, 29), axis=vector(0, 1, 0), radius=1.5, color=color.gray(0.8))
bulbo_lamp = sphere(pos=vector(0, 6, 29), radius=2.5, color=color.yellow * 0.8)
luz = False


luz_cima_esquerda =  local_light(pos=vector(-5, 10, 10), color=color.white * 0.1)
luz_cima_direita =  local_light(pos=vector(-5, 10, 20), color=color.white * 0.1)
#luz_cima_onde_que_ela_ta? = sphere(pos=vector(-5, 30, 15), radius=2.5, color=color.yellow)


# Lista para armazenar as bolas (fótons)
bolas = []

# Lista para armazenar os elétrons

eletrons = []


### Condições para o funcionamento do código ####

### Definindo a função para determinar a seção de choque
def sig(Z, E):
    E_ev = E * 1000000 
    sigma = Z**4/E_ev**3
    ## tornando a unidade própria para análise clássica
    sig_prop = sigma * 0.0000001
    return sig_prop

## entrada

Z = -1
while Z < 1:
    Z = int(input('Insira o número atômico do elemento do qual a placa é feito:'))

E = -1
while E < 1:
    E = float(input('Insira o valor da energia da radiação incidente, em Mev: '))


sec_choque = sig(Z, E)
escalar_choque = 1 + sec_choque  
energia_rad = 1 + E

deltat = 0.01
t = 0
tfinal = 1000
intervalo_criacao = 1/E  
tempo_ate_proxima_bola = 0

intervalo_criacao_e = 1 / escalar_choque*2
tempo_ate_proximo_e = 0

### Loop ###

while t < tfinal:
    rate(100)

    # Atualizar a posição e verificar colisões para cada bola
    for bola in bolas:
        # Verificar colisão com a placa
        if bola.pos.y - bola.radius * 2 < placa.pos.y + placa.size.y / 2:
            bolas.remove(bola)
            bola.visible = False
            
        # Atualizar a posição da bola
        bola.pos = bola.pos + bola.velocidade * deltat

    # Verificar se é hora de criar uma nova bola
    if tempo_ate_proxima_bola >= intervalo_criacao:
        nova_bola = sphere(pos=vector(-7, 10, 0), radius=0.5, color=color.yellow * 0.8)
        nova_bola.velocidade = vector(5, -5, 0) * energia_rad
        bolas.append(nova_bola)
        
        # Resetar o contador de tempo para a próxima bola
        tempo_ate_proxima_bola = 0


#### determinar a corrente elétrica
    
    for eletron in eletrons:
        # Verificar colisão com fiolamp
        if eletron.pos.z - eletron.radius * 2 < fiolamp.pos.z + fiolamp.size.z / 2:
            eletron.velocidade.y = -1 * eletron.velocidade.y
        
        # Verificar colisão com parade fiolamp
        if eletron.pos.z + eletron.radius > fiolamp.pos.z + fiolamp.size.z  / 2:
            eletrons.remove(eletron)
            eletron.visible = False
            
            # Ascender a Lâmpada
            if not luz:
                luz = True
                luz = local_light(pos=vector(0, 6, 29), color=color.yellow * 0.5)
                
        # Atualizar a posição do eletron
        eletron.pos = eletron.pos + eletron.velocidade * deltat

    # Verificar se é hora de criar um novo eletron
    if tempo_ate_proximo_e >= intervalo_criacao_e:
        novo_eletron = sphere(pos=vector(0, -9, 0), radius=0.5, color=color.red)
        novo_eletron.velocidade = vector(0, 0, 5) * (escalar_choque**10)
        eletrons.append(novo_eletron)

        # Resetar o contador de tempo para o proximo eetron
        tempo_ate_proximo_e = 0

    # Incrementar o tempo
    t += deltat
    tempo_ate_proxima_bola += deltat
    tempo_ate_proximo_e += deltat
