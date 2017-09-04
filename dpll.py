import random
import copy

finalclause = []
onepatleastonetable = []
clauseonetablep1 = []
clauseonetablep2 = []
clausefriend = []
clauseenemy = []

dict_clauses = {}

def remove_dup(clause):
    tautology = {}
    temp = []
    for i in clause:
        if i in tautology:
            #print clause
            #print "AD"
            tautology[i]+=1
        else:
            tautology[i] = 1
    for i in tautology:
        temp.append(i)

    return temp

def reduceset(clause):
    #return False
    if len(clause) == 1:
        return False

    tautology = {}
    for i in clause:
        if i in tautology:
            tautology[i]+=1
        else:
            tautology[i] = 1

    for i in clause:
        if ("-" + i) in tautology:
            return True

    return False

with open("./data/input5.txt") as finp:
    nguest = 0
    relationship = {}
    enemy = []
    relationship = {}
    for line in finp:
        if nguest == 0:
            nguest, ntable = map(int, line.strip().split(" "))
        else:
            person1, person2, relation = line.strip().split(" ")
            if relation in relationship:
                relationship[relation].append([int(person1), int(person2)])
            else:
                relationship[relation] = [[int(person1), int(person2)]]

#print relationship["F"][0][1]

for i in xrange(nguest):
    templist = []
    for j in xrange(ntable):
        a = str(i+1)+ str("_") + str(j+1)
        templist.append(a)
    clauseonetablep1.append(templist)
    finalclause.append(templist)
print "C1", clauseonetablep1

for k in xrange(nguest):
    #templistp2 = []
    for i in xrange(ntable):
        j = i + 1
        while j < (ntable):
            a = "-" + str(k+1) + str("_") + str(i+1)
            b = "-" + str(k+1) + str("_") + str(j+1)
            clauseonetablep2.append([a, b])
            finalclause.append([a, b])
            j=j+1

print "C2", clauseonetablep2


i=0
if 'F' in relationship:
    while i < len(relationship["F"]):
        for j in xrange(ntable):
            a1 = str(relationship["F"][i][0]) + "_" + str(j + 1)
            b1 = str(relationship["F"][i][1]) + "_" + str(j + 1)
            clausefriend.append(["-" + a1, b1])
            clausefriend.append([a1, "-" + b1])
            finalclause.append(["-" + a1, b1])
            finalclause.append([a1, "-" + b1])
        # clausefriend.append(templist3)
        i = i + 1
print "C3", clausefriend


j = 0
if 'E' in relationship:
    while j < len(relationship["E"]):
        for i in xrange(ntable):
            a1 = "-" + str(relationship["E"][j][0]) + "_" + str(i + 1)
            b1 = "-" + str(relationship["E"][j][1]) + "_" + str(i + 1)
            clauseenemy.append([a1, b1])
            finalclause.append([a1, b1])
        j = j + 1
print "C4", clauseenemy

#print finalclause

for clause in finalclause:
    for i in xrange(len(clause)):
        if clause[i] in dict_clauses:
            dict_clauses[clause[i]].append(clause)
        else:
            dict_clauses[clause[i]] = [clause]

print dict_clauses

def removeall(P, symbols):
    new_set_symbol = copy.deepcopy(symbols)
    new_set_symbol.remove(P)
    return new_set_symbol

def extend(model, P, value):
    new_model = copy.deepcopy(model)
    new_model[P] = value
    return new_model

def literal_symbol(literal):
    if '-' in literal:
        return literal[1:]
    else:
        return literal

def find_pure_symbol(symbols, unknown_clauses):
    for s in symbols:
        found_pos, found_neg = False, False
        for c in unknown_clauses:
            if not found_pos and s in c: found_pos = True
            if not found_neg and ("-" + s) in c: found_neg = True
        if found_pos != found_neg: return s, found_pos
    return None, None

def find_unit_clause(clauses, model):
    for clause in clauses:
        num_not_in_model = 0
        for literal in clause:
            sym = literal_symbol(literal)
            if sym not in model:
                num_not_in_model += 1
                P, value = sym, (literal[0] != '-')
        if num_not_in_model == 1:
            return P, value
    return None, None

def pl_true(clause, dict):
    flagnone = 0
    for iclause in clause:
        if '-' in iclause:
            if iclause[1:] in dict:
                if not dict[iclause[1:]]:
                    return True
            else:
                flagnone = 1
        else:
            if iclause in dict:
                if dict[iclause]:
                    return True
            else:
                flagnone = 1
    if flagnone == 1:
        return None
    else:
        return False

#print "dD", pl_true(['1_1'], {'1_1': True})

def dpll(clauses, symbols, model):
    "See if the clauses are true in a partial model."
    print model
    unknown_clauses = [] ## clauses with an unknown truth value
    for c in clauses:
        #print c, model
        val =  pl_true(c, model)
        #print val
        if val == False:
            return False
        if val != True:
            unknown_clauses.append(c)
    #print "sdSD", unknown_clauses

    if not unknown_clauses:
        return model
    P, value = find_pure_symbol(symbols, unknown_clauses)
    #print "sad", P
    if P:
        return dpll(clauses, removeall(P, symbols), extend(model, P, value))
    print clauses
    P, value = find_unit_clause(clauses, model)
    print P,value

    if P:
        return dpll(clauses, removeall(P, symbols), extend(model, P, value))

    if len(symbols) >= 1:
        P = symbols.pop()
        return (dpll(clauses, symbols, extend(model, P, True)) or
                dpll(clauses, symbols, extend(model, P, False)))



total_symbols = []
for key in dict_clauses:
    if '-' in key:
        key = key[1:]
    if key not in total_symbols:
        total_symbols.append(key)

print "adaf", total_symbols
print finalclause
print dpll(finalclause, total_symbols, {})

def WalkSAT(clauses, max_flips):
    dict = {}
    for individual_clause in clauses:
        for plsymbol in individual_clause:
            if '-' in plsymbol:
                plsymbol = plsymbol[1:]
            if plsymbol in dict:
                continue
            else:
                dict[plsymbol]= random.choice([True, False])
    #print dict
    for i in xrange(max_flips):
        satisfied, unsatisfied = [], []
        for clause in clauses:
            if pl_true(clause, dict):
                satisfied.append(clause)
            else:
                unsatisfied.append(clause)
        if not unsatisfied:
            return dict
        #print unsatisfied
        random_clause = random.choice(unsatisfied)
        random_symbol = random.choice(random_clause)
        #print random_symbol
        if "-" in random_symbol:
            dict[random_symbol[1:]] = not dict[random_symbol[1:]]
        else:
            dict[random_symbol] = not dict[random_symbol]

#print WalkSAT(finalclause, 100000)