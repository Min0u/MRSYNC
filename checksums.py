import hashlib
import os


def split_blocks(file_path, block_size, beg):
    """renvoie la liste de tuples (contenu, hash, taille), beg étant la taille du premier bloc (~ offset)"""
    blocks = []
    with open(file_path, 'rb') as f:
        block = f.read(beg)
        blocks.append((block, hashlib.md5(block).hexdigest(), len(block)))
        while True:
            block = f.read(block_size)
            if not block:
                break
            blocks.append((block, hashlib.md5(block).hexdigest(), len(block)))
    return blocks


def split_light(file_path, block_size, beg):
    """comme split_blocks mais renvoie que la liste de hash, beg étant la taille du premier bloc (~ offset)"""
    hashes = []
    with open(file_path, 'rb') as f:
        # lis le premier bloc
        block = f.read(beg)
        hashes.append(hashlib.md5(block).hexdigest())
        while True:
            block = f.read(block_size)
            if not block:
                break
            hashes.append(hashlib.md5(block).hexdigest())
    return hashes


def extract_block(file_path, start, block_size):
    """Extrait un bloc de taille n à partir d'un offset donné"""
    with open(file_path, 'rb') as f:
        f.seek(start)
        block = f.read(block_size)
        md5 = hashlib.md5(block).hexdigest()
        size = len(block)
    return (block, md5, size)



def generate_blocks(file_path, block_size):
    """Genere tous les blocks possibles de taille n (qui se chevauchent)"""
    blocks = []
    with open(file_path, 'rb') as f:
        data = f.read()
        for i in range(len(data) - block_size + 1):
            block = data[i:i+block_size]
            md5 = hashlib.md5(block).hexdigest()
            blocks.append((block, md5, block_size))
    return blocks



def associate_blocks(file_a,b_hashes,block_size):
    """Associe (si possible) chaque bloc de B avec un bloc de A"""
    #les blocks possibles de taille n dans a
    a_blocks= generate_blocks(file_a, block_size)
    c=0
    match=[]
    for tuple in a_blocks:
        if tuple[1] in b_hashes:
            offset=c%block_size
            i=((c-offset)//block_size)+1
            if offset != 0:
                #l'indice est décalé pour compter le premier bloc de taille offset
                i+=1
            else:
                offset= block_size
            #print("Match!!  Le",b_hashes.index(tuple[1])+1, "ème bloc de b correspond au ",i, "ème bloc de a dont le 1er bloc est de taille", offset)    
            match.append([b_hashes.index(tuple[1]),i-1,offset])
        c+=1
    return match




def organize(file_a, b_hashes, block_size):
    """associer chaque bloc de B à une position dans A"""
    # récupération de la liste des correspondances entre les blocs de file_a et ceux de file_b
    matches = associate_blocks(file_a, b_hashes, block_size)
    m=[]
    for elt in matches:
        offset=elt[2]
        if offset==block_size:
            offset=0
            m.append([elt[0],offset+ elt[1]*block_size])  #[indice bloc b, la position du bloc dans a]
        else:
            m.append([elt[0],offset+ (elt[1]-1)*block_size])  #[indice bloc b, la position du bloc dans a]
    return m


def find_blocks(file_a, b_hashes, block_size):
    """Cherche les blocks de A qui ne sont pas dans B"""
    size_a = os.path.getsize(file_a)
    matches = organize(file_a, b_hashes, block_size)
    result=[]
    cpt=0
    curseur=0
    seq=[]
    if matches == []:  ##Pas de blocs communs entre A et B
        return False
    else:
        if matches[0][1]==0:
            seq.append("B")
            cpt+=1
            curseur+=block_size
        while cpt< len(matches):
            if matches[cpt][1]-curseur != 0:
                result.append(extract_block(file_a, curseur , matches[cpt][1]-curseur))
                seq.append("A")
                curseur=curseur + matches[cpt][1]-curseur
            seq.append("B")
            curseur+=block_size
            cpt+=1
        if curseur < size_a:
            result.append(extract_block(file_a, curseur , size_a-curseur))
            seq.append("A")
    return seq, result, [s[0] for s in matches]



def rebuild2(seq, A,B_ind,B_blocks):  #(Blocks de A nécessaire, blocks B)
    """Contruit une liste de sous-listes, chaque sous-listes correspond à soit un bloc de A (taille non fixe) ou de B (taille fixe)"""
    B=[B_blocks[i] for i in B_ind]
    C=[]
    (i,j,k)= (0,0,0)
    while i < len(seq):
        if seq[i] == "A":
            C.append(A[j])
            j+=1
        elif seq[i] == "B":
            C.append(B[k])
            k+=1
        i+=1
    return C


def write_blocks(blocks, output_file_path):   #écrit le fichier ouput_file_path grace aux blocs de données de rebuild2
    with open(output_file_path, 'wb') as f:
        for block in blocks:
            f.write(block[0])
            
            
"""usage: soit A -> B
B doit envoyer son split_light vers A, et avec cela , A va utiliser find_blocks pour reconstruire A avec des blocs à lui et de B. Il renvoie le tout à 
B et B peux utiliser rebuild2 pour reécrire le fichier A. """

