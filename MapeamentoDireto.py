def inicializarCache(tamanhoCache):
    chaves = []
    valores = []
    for i in range(tamanhoCache):
        chave = i
        valor = -1
        chaves.append(chave)
        valores.append(valor)
    cache = {}
    for chave, valor in zip(chaves, valores):
        cache[chave] = valor
    return cache

def imprimirCacheInicial(cache):
    print("Cache inicial")
    print("Tamanho cache: " + str(tamanhoCache))
    print("Pos cache |Posição Memória")
            
    for chave, valor in cache.items():
        print("         " + str(chave)+"|","            " +  str(valor))


def mapeamentoDireto(tamanhoCache, posMemoria):
    hit = 0
    miss = 0
    
    for posicoes in range(len(posMemoria)):
        posicaoCache = posMemoria[posicoes] % tamanhoCache
        if cache[posicaoCache] == posMemoria[posicoes]:
            hit+=1
            print(f"Linha {posicoes} Status: Hit")
        else:
            miss+=1
            print(f"Linha {posicoes} Status: Miss")
        cache[posicaoCache] = posMemoria[posicoes]
        
        print("Linha : " + str(posicoes) + "| posição de memória desejada: " + str(posMemoria[posicoes]))
        print("Pos cache |Posição Memória")
            
        for chave, valor in cache.items():
            print("         " + str(chave)+"|","            " +  str(valor))
            
    
    resultado = 100*hit/(len(posMemoria))
    
    print("\n")
    print("Conectividade em sistemas Cíberfísicos - Mapeamento Direto - Guilherme")
    print("*--------------------------------------------------------------------*")
    print("Memorias acessadas: " + str(len(posMemoria)))    
    print("Numero de Hits: " + str(hit))
    print("Numero de Miss: " + str(miss))
    print(f"Taxa de acertos (hits): {resultado:.2f}%")

posMemoria = [0,1,2,2,22,32,42,20,1,10,11,12,13]
tamanhoCache = 5

inicializarCache(tamanhoCache)
print("\n")
cache = inicializarCache(tamanhoCache)
imprimirCacheInicial(cache)
print("\n")
mapeamentoDireto(tamanhoCache, posMemoria)
