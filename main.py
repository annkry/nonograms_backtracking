'''The algorithm will initially use the AC-3 algorithm to infer as much as possible whether certain fields will need to be painted, while in the backtracking function itself,
I will use a simplified version of inference (without putting it into a queue).

In the inference function, I will not recursively call settings that are inconsistent with the current setting.'''

import random
import copy


# reading data from input and initialization of initial values
plik = open('zad_input.txt')
p = 0
a = 0
b = 0
i = []
j = []
for linia in plik:
    lista = linia.split()
    num = [int(s) for s in lista if s.isdigit()]
    if p == 0:
        a = num[0]
        b = num[1]
    elif p <= a:
        i.append(num)
    else:
        j.append(num)
    p += 1
tab = [[0] * b for i in range(a)]
zafiks = [[0] * b for i in range(a)]


prefkol = [[0] * a for k in range(b)]
for u in range(b):
    prefkol[u][0] = j[u][0]
for d in range(0, b):
    for c in range(1, len(j[d])):
        prefkol[d][c] = prefkol[d][c-1]+j[d][c]

prefwie = [[0] * b for k in range(a)]
for u in range(a):
    prefwie[u][0] = i[u][0]
for d in range(0, a):
    for c in range(1, len(i[d])):
        prefwie[d][c] = prefwie[d][c-1]+i[d][c]

sumakol = []
sumawie = []
for k in range(a):
    sumawie.append(sum(i[k]))
for k in range(b):
    sumakol.append(sum(j[k]))

# returns the intersection of two sets
def intersection(lst1, lst2):
    return list(set(lst1).intersection(set(lst2)))

# returns whether a new setting is legal in accordance with the existing setting in the list
def spr_z_zafiks(bit, lista, wsp, tab, zafiks, aa, bb, nb, l_b):
    if nb != l_b-1:
        if bit == 0:
            for i in range(aa, bb):
                if zafiks[wsp][i] == 1 and tab[wsp][i] != lista[i]:
                    return False
            if bb <= len(lista)-1 and zafiks[wsp][bb] == 1 and tab[wsp][bb] == 1:
                return False
        else:
            for i in range(aa, bb):
                if zafiks[i][wsp] == 1 and tab[i][wsp] != lista[i]:
                    return False
            if bb <= len(lista)-1 and zafiks[bb][wsp] == 1 and tab[bb][wsp] == 1:
                return False
        return True
    else:
        if bit == 0:
            for i in range(aa, bb):
                if zafiks[wsp][i] == 1 and tab[wsp][i] != lista[i]:
                    return False
            if bb <= len(lista)-1 and zafiks[wsp][bb] == 1 and tab[wsp][bb] == 1:
                return False
            if bb+1 <= len(lista)-1:
                for i in range(bb+1, len(lista)):
                    if zafiks[wsp][i] == 1 and tab[wsp][i] != lista[i]:
                        return False
        else:
            for i in range(aa, bb):
                if zafiks[i][wsp] == 1 and tab[i][wsp] != lista[i]:
                    return False
            if bb <= len(lista)-1 and zafiks[bb][wsp] == 1 and tab[bb][wsp] == 1:
                return False
            if bb+1 <= len(lista)-1:
                for i in range(bb+1, len(lista)):
                    if zafiks[i][wsp] == 1 and tab[i][wsp] != lista[i]:
                        return False
        return True

# returns a list with assigned field completions consistent with the request
def rekur_zap(lista, bit, wsp, bloki, nr_b, pref, suma, gdzie_konczyl_sie_wczesniejszy_blok, tab, zafiks):
    if nr_b == len(bloki):
        wyn = []
        for i in range(len(lista)):
            if lista[i] == 1:
                wyn.append((i, 1))
            else:
                wyn.append((i, 0))
        return wyn
    else:
        if nr_b != 0:
            st = gdzie_konczyl_sie_wczesniejszy_blok+1
            end = len(lista)-(suma-pref[nr_b-1])-(len(bloki)-(nr_b+1))
        else:
            st = 0
            end = len(lista)-suma-(len(bloki)-(nr_b+1))
        pierw = 1
        przeciecie = [-1]
        for i in range(st, end+1):
            lista1 = lista.copy()
            for j in range(i, i+bloki[nr_b]):
                lista1[j] = 1
            ok = spr_z_zafiks(bit, lista1, wsp, tab, zafiks,
                              st, i+bloki[nr_b], nr_b, len(bloki))
            if ok:
                if pierw == 1:
                    przeciecie = rekur_zap(
                        lista1, bit, wsp, bloki, nr_b+1, pref, suma, i+bloki[nr_b], tab, zafiks)
                    if przeciecie != [-1]:
                        pierw = 0
                else:
                    res1 = rekur_zap(lista1, bit, wsp, bloki, nr_b+1,
                                     pref, suma, i+bloki[nr_b], tab, zafiks)
                    if res1 != [-1]:
                        przeciecie = intersection(przeciecie, res1)
        return przeciecie

# The AC-3 algorithm for the old, determines whether at the input we can infer about painting some fields
def START(tab, zafiks):
    kolejka = []
    wynik_przypisania = []
    for h in range(0, a):
        kolejka.append((0, h))
    for h in range(0, b):
        kolejka.append((1, h))
    while kolejka != []:
        bit, wsp = kolejka.pop(0)
        if bit == 0:
            lis = []
            for ff in range(b):
                lis.append(0)
            res = rekur_zap(
                lis, bit, wsp, i[wsp], 0, prefwie[wsp], sumawie[wsp], 0, tab, zafiks)
            if res != []:
                for ind, var in res:
                    if zafiks[wsp][ind] != 1:
                        tab[wsp][ind] = var
                        zafiks[wsp][ind] = 1
                        wynik_przypisania.append((wsp, ind, var))
                        if (1, ind) not in set(kolejka):
                            kolejka.append((1, ind))
        else:
            lis = []
            for ff in range(a):
                lis.append(0)
            res = rekur_zap(
                lis, bit, wsp, j[wsp], 0, prefkol[wsp], sumakol[wsp], 0, tab, zafiks)
            if res != []:
                for ind, var in res:
                    if zafiks[ind][wsp] != 1:
                        tab[ind][wsp] = var
                        zafiks[ind][wsp] = 1
                        wynik_przypisania.append((ind, wsp, var))
                        if (0, ind) not in set(kolejka):
                            kolejka.append((0, ind))
    return wynik_przypisania

# during the operation of the backtrack we will want to carry out simplified inference
def infer(tab1, zafiks1, un_assign, un_lista, un_len_lista):
    kolejka = []
    wynik_przypisania = []
    for h in range(0, a):
        kolejka.append((0, h))
    for h in range(0, b):
        kolejka.append((1, h))
    l1 = [0]*b
    l2 = [0]*a
    while kolejka != []:
        bit, wsp = kolejka.pop(0)

        if bit == 0:
            lis = l1.copy()
            res = rekur_zap(
                lis, bit, wsp, i[wsp], 0, prefwie[wsp], sumawie[wsp], 0, tab1, zafiks1)
            if res != [-1]:
                for ind, var in res:
                    if zafiks1[wsp][ind] != 1:
                        tab1[wsp][ind] = var
                        zafiks1[wsp][ind] = 1
                        un_assign[(wsp, ind)] = var
                        if un_lista.count((wsp, ind)) > 0:
                            un_lista.remove((wsp, ind))
            else:
                return [0]
        else:
            lis = l2.copy()
            res = rekur_zap(
                lis, bit, wsp, j[wsp], 0, prefkol[wsp], sumakol[wsp], 0, tab1, zafiks1)
            if res != [-1]:
                for ind, var in res:
                    if zafiks1[ind][wsp] != 1:
                        tab1[ind][wsp] = var
                        zafiks1[ind][wsp] = 1
                        un_assign[(ind, wsp)] = var
                        if un_lista.count((ind, wsp)) > 0:
                            un_lista.remove((ind, wsp))
            else:
                return [0]
    return 1

# main function for backtracking
def backtracck(assignment, lista, zafikss, tabb, len_lista):
    if lista == []:
        return tabb

    x, y = lista.pop(0)
    wart = []
    pierw = random.randint(0, 1)
    wart.append(pierw)
    wart.append(1-pierw)
    for t in wart:
        un_tab = copy.deepcopy(tabb)
        un_zafiks = copy.deepcopy(zafikss)
        un_assign = assignment.copy()
        un_lista = lista.copy()
        un_len_lista = len_lista.copy()
        un_assign[(x, y)] = t
        un_tab[x][y] = t
        un_zafiks[x][y] = 1
        inferences = infer(un_tab, un_zafiks, un_assign,
                           un_lista, un_len_lista)
        if inferences != [0]:
            result = backtracck(un_assign, un_lista,
                                un_zafiks, un_tab, un_len_lista)
            if result != -1:
                return result
    return -1


assignment = {}
len_war = a*b

war = []
for f in range(0, a):
    for h in range(0, b):
        assignment[(f, h)] = -1
        war.append((f, h))

assign = START(tab, zafiks)
if assign != []:
    for id1, id2, var in assign:
        len_war -= 1
        war.remove((id1, id2))
        assignment[(id1, id2)] = var
result = backtracck(assignment, war, zafiks, tab, [len_war])

file = open("zad_output.txt", "w")
for q in range(0, a):
    for g in range(0, b):
        if result[q][g] == 1:
            print('#', end='', file=file)
        else:
            print('.', end='', file=file)
    print('', file=file)

file.close()
