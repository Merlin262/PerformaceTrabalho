# Exemplo 1 - Política LRU
tamanhoCache = 16 # Tamanho da cache em bytes
tamanhoBloco = 4 # Tamanho de cada bloco em bytes
numeroBlocos = tamanhoCache // tamanhoBloco # Número de blocos na cache
cache = [[] for _ in range(numeroBlocos)] # Inicializa a cache com blocos vazios
acessoMemoria = [0x00, 0x04, 0x08, 0x0C, 0x00, 0x10, 0x14, 0x18, 0x0C, 0x08, 0x1C] # Sequência de acessos à memória
hits = 0 # Contador de hits
misses = 0 # Contador de misses

for acesso in acessoMemoria:
    blocoIndex = acesso // tamanhoBloco % numeroBlocos # Calcula o índice do bloco que contém o endereço
    if acesso in cache[blocoIndex]: # Hit
        hits += 1
        cache[blocoIndex].remove(acesso)
        cache[blocoIndex].append(acesso)
    else: # Miss
        misses += 1
        if len(cache[blocoIndex]) == tamanhoBloco: # Cache cheia, substitui o bloco mais antigo
            cache[blocoIndex] = cache[blocoIndex][1:] + [acesso]
        else: # Cache com espaço livre, adiciona o novo bloco
            cache[blocoIndex].append(acesso)

print(f'Tamanho da Cache em bytes: {tamanhoCache}')
print(f'Tamanho do bloco em bytes: {tamanhoBloco}')
print(f'Numero de blocos: {numeroBlocos}')
print(f'Algoritmo LRU - Hits: {hits}, Misses: {misses}')
print(f'')

# Exemplo 2 - Política LFU
tamanhoCache = 16 # Tamanho da cache em bytes
tamanhoBloco = 4 # Tamanho de cada bloco em bytes
numeroBlocos = tamanhoCache // tamanhoBloco # Número de blocos na cache
cache = [[] for _ in range(numeroBlocos)] # Inicializa a cache com blocos vazios
acessoMemoria = [0x00, 0x04, 0x08, 0x0C, 0x00, 0x10, 0x14, 0x18, 0x0C, 0x08, 0x1C] # Sequência de acessos à memória
hits = 0 # Contador de hits
misses = 0 # Contador de misses

def lfu_key(bloco):
    return bloco[1] # Retorna a frequência de acesso do bloco

for acesso in acessoMemoria:
    blocoIndex = acesso // tamanhoBloco % numeroBlocos # Calcula o índice do bloco que contém o endereço
    blocoAchado = False
    for bloco in cache[blocoIndex]:
        if bloco[0] == acesso: # Hit
            hits += 1
            bloco[1] += 1 # Incrementa a frequência de acesso do bloco
            blocoAchado = True
            break
    if not blocoAchado: # Miss
        misses += 1
        if len(cache[blocoIndex]) == numeroBlocos: # Cache cheia, substitui o bloco menos frequentemente acessado
            cache[blocoIndex].sort(key=lfu_key)
            cache[blocoIndex].pop(0)
        cache[blocoIndex].append([acesso, 1]) # Adiciona o novo bloco com frequência de acesso 1

print(f'Tamanho da Cache em bytes: {tamanhoCache}')
print(f'Tamanho do bloco em bytes: {tamanhoBloco}')
print(f'Numero de blocos: {numeroBlocos}')
print(f'Algoritmo LFU - Hits: {hits}, Misses: {misses}')
print(f'')

#Exemplo 3 - Política FIFO
tamanhoCache = 16 # Tamanho da cache em bytes
tamanhoBloco = 4 # Tamanho de cada bloco em bytes
numeroBlocos = tamanhoCache // tamanhoBloco # Número de blocos na cache
cache = [[] for _ in range(numeroBlocos)] # Inicializa a cache com blocos vazios
acessoMemoria = [0x00, 0x04, 0x08, 0x0C, 0x00, 0x10, 0x14, 0x18, 0x0C, 0x08, 0x1C] # Sequência de acessos à memória
hits = 0 # Contador de hits
misses = 0 # Contador de misses

for acesso in acessoMemoria:
    blocoIndex = acesso // tamanhoBloco % numeroBlocos # Calcula o índice do bloco que contém o endereço
    if acesso in cache[blocoIndex]: # Hit
        hits += 1
    else: # Miss
        misses += 1
        cache[blocoIndex] = [acesso] + cache[blocoIndex][:-1] # Substitui o bloco mais antigo pelo novo

print(f'Tamanho da Cache em bytes: {tamanhoCache}')
print(f'Tamanho do bloco em bytes: {tamanhoBloco}')
print(f'Numero de blocos: {numeroBlocos}')
print(f'Algoritmo FIFO  - Hits: {hits}, Misses: {misses}')