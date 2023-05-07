import math

class CacheBlock:
    def __init__(self, tag):
        self.tag = tag
        self.valid = False
        self.data = None
        self.access_count = 0

class AssociativeCache:
    def __init__(self, num_blocks, num_sets, replace_policy):
        self.num_blocks = num_blocks
        self.num_sets = num_sets
        self.replace_policy = replace_policy
        self.blocks = [[CacheBlock(None) for _ in range(num_blocks)] for _ in range(num_sets)]

    def read(self, address):
        tag, set_idx, block_idx = self._decode_address(address)
        block = self.blocks[set_idx][block_idx]

        if block.valid and block.tag == tag:
            # Cache hit
            self._update_block_access_count(set_idx, block_idx)
            return block.data
        else:
            # Cache miss
            block = self._find_victim_block(set_idx)
            block.tag = tag
            block.valid = True
            block.data = self._fetch_data_from_memory(address)
            self._update_block_access_count(set_idx, block_idx)
            return block.data

    def _decode_address(self, address):
        offset_bits = int(math.log2(self.num_blocks))
        set_bits = int(math.log2(self.num_sets))
        tag_bits = 32 - offset_bits - set_bits

        offset = address & (self.num_blocks - 1)
        set_idx = (address >> offset_bits) & (self.num_sets - 1)
        tag = address >> (offset_bits + set_bits)

        return tag, set_idx, offset

    def _fetch_data_from_memory(self, address):
        # Replace with actual implementation of fetching data from memory
        return address

    def _find_victim_block(self, set_idx):
        if self.replace_policy == 'LRU':
            return self._find_lru_block(set_idx)
        elif self.replace_policy == 'LFU':
            return self._find_lfu_block(set_idx)
        elif self.replace_policy == 'FIFO':
            return self._find_fifo_block(set_idx)
        else:
            raise ValueError(f'Invalid replace policy: {self.replace_policy}')

    def _find_lru_block(self, set_idx):
        min_access_count = float('inf')
        min_access_count_block = None

        for block in self.blocks[set_idx]:
            if not block.valid:
                return block

            if block.access_count < min_access_count:
                min_access_count = block.access_count
                min_access_count_block = block

        return min_access_count_block

    def _find_lfu_block(self, set_idx):
        min_access_count = float('inf')
        min_access_count_block = None

        for block in self.blocks[set_idx]:
            if not block.valid:
                return block

            if block.access_count < min_access_count:
                min_access_count = block.access_count
                min_access_count_block = block

        min_access_count_block.access_count += 1

        return min_access_count_block

    def _find_fifo_block(self, set_idx):
        for block in self.blocks[set_idx]:
            if not block.valid:
                return block

        return self.blocks[set_idx][0]

    def _update_block_access_count(self, set_idx, block_idx):
        block = self.blocks[set_idx][block_idx]
        block.access_count += 1

cache = AssociativeCache(num_blocks=2, num_sets=4, replace_policy='LRU')

# Read data from memory addresses
addresses = [0x1234, 0x5678, 0x9012, 0x3456, 0x7890]
for address in addresses:
    data = cache.read(address)
    print(f'Read address {address:04X} from cache, data={data}')

def create_cache(cache_size, num_blocks, replace_policy):
    block_size = 4  # Assume block size of 4 bytes
    num_sets = cache_size // (num_blocks * block_size)
    return AssociativeCache(num_blocks=num_blocks, num_sets=num_sets, replace_policy=replace_policy)

cache_size = 64  # 64 bytes
num_blocks = 2
replace_policy = 'LRU'

cache = create_cache(cache_size, num_blocks, replace_policy)

# Example to compare hit rates for different replace policies

cache_size = 8  # 8 bytes
num_blocks = 2

# Exemplo 1 - Política LRU
cache_size = 16 # Tamanho da cache em bytes
block_size = 4 # Tamanho de cada bloco em bytes
num_blocks = cache_size // block_size # Número de blocos na cache
cache = [[] for _ in range(num_blocks)] # Inicializa a cache com blocos vazios
mem_accesses = [0x00, 0x04, 0x08, 0x0C, 0x00, 0x10, 0x14, 0x18, 0x0C, 0x08, 0x1C] # Sequência de acessos à memória
hits = 0 # Contador de hits
misses = 0 # Contador de misses

for access in mem_accesses:
    block_index = access // block_size % num_blocks # Calcula o índice do bloco que contém o endereço
    if access in cache[block_index]: # Hit
        hits += 1
        cache[block_index].remove(access)
        cache[block_index].append(access)
    else: # Miss
        misses += 1
        if len(cache[block_index]) == block_size: # Cache cheia, substitui o bloco mais antigo
            cache[block_index] = cache[block_index][1:] + [access]
        else: # Cache com espaço livre, adiciona o novo bloco
            cache[block_index].append(access)

print(f'LRU Policy - Hits: {hits}, Misses: {misses}')


# Exemplo 2 - Política LFU
cache_size = 16 # Tamanho da cache em bytes
block_size = 4 # Tamanho de cada bloco em bytes
num_blocks = cache_size // block_size # Número de blocos na cache
cache = [[] for _ in range(num_blocks)] # Inicializa a cache com blocos vazios
mem_accesses = [0x00, 0x04, 0x08, 0x0C, 0x00, 0x10, 0x14, 0x18, 0x0C, 0x08, 0x1C] # Sequência de acessos à memória
hits = 0 # Contador de hits
misses = 0 # Contador de misses

def lfu_key(block):
    return block[1] # Retorna a frequência de acesso do bloco

for access in mem_accesses:
    block_index = access // block_size % num_blocks # Calcula o índice do bloco que contém o endereço
    block_found = False
    for block in cache[block_index]:
        if block[0] == access: # Hit
            hits += 1
            block[1] += 1 # Incrementa a frequência de acesso do bloco
            block_found = True
            break
    if not block_found: # Miss
        misses += 1
        if len(cache[block_index]) == num_blocks: # Cache cheia, substitui o bloco menos frequentemente acessado
            cache[block_index].sort(key=lfu_key)
            cache[block_index].pop(0)
        cache[block_index].append([access, 1]) # Adiciona o novo bloco com frequência de acesso 1

print(f'LFU Policy - Hits: {hits}, Misses: {misses}')

#Exemplo 3 - Política FIFO
cache_size = 16 # Tamanho da cache em bytes
block_size = 4 # Tamanho de cada bloco em bytes
num_blocks = cache_size // block_size # Número de blocos na cache
cache = [[] for _ in range(num_blocks)] # Inicializa a cache com blocos vazios
mem_accesses = [0x00, 0x04, 0x08, 0x0C, 0x00, 0x10, 0x14, 0x18, 0x0C, 0x08, 0x1C] # Sequência de acessos à memória
hits = 0 # Contador de hits
misses = 0 # Contador de misses

for access in mem_accesses:
    block_index = access // block_size % num_blocks # Calcula o índice do bloco que contém o endereço
    if access in cache[block_index]: # Hit
        hits += 1
    else: # Miss
        misses += 1
        cache[block_index] = [access] + cache[block_index][:-1] # Substitui o bloco mais antigo pelo novo

print(f'FIFO Policy - Hits: {hits}, Misses: {misses}')
