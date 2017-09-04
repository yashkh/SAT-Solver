import random
import copy

finalclause = []
onepatleastonetable = []
clauseonetablep1 = []
clauseonetablep2 = []
clausefriend = []
clauseenemy = []
f_c1 = ""
f_c2 = ""
e_c1 = ""
e_c2 = ""

dict_clauses = {}

with open("./data/input1.txt", "r") as finp:
    nguest = -1
    relationship = {}
    enemy = []
    flag_1 = 0
    flag_2 = 0
    for line in finp:

        if nguest == -1:
            nguest, ntable = map(int, line.strip().split(" "))
            if ntable > nguest:
                ntable = nguest
            indifferent_guest = []
            for i in xrange(1, nguest+1):
                indifferent_guest.append(i)
        else:
            person1, person2, relation = line.strip().split(" ")
            if int(person1) in indifferent_guest:
                indifferent_guest.remove(int(person1))
            if int(person2) in indifferent_guest:
                indifferent_guest.remove(int(person2))
            if flag_1 == 0 and relation == "E":
                e_c1 = person1
                e_c2 = person2
                flag_1 = 1

            if flag_2 == 0 and relation == "F":
                f_c1 = person1
                f_c2 = person2
                flag_2 = 1

            if relation in relationship:
                relationship[relation].append([int(person1), int(person2)])
            else:
                relationship[relation] = [[int(person1), int(person2)]]

if "F" in relationship and "E" in relationship:
    for fvalue in relationship["F"]:
        for evalue in relationship["E"]:
            print evalue
            if fvalue == evalue or fvalue == list(reversed(evalue)):
                nguest = 0
                ntable = 0

for i in xrange(nguest):
    templist = []
    for j in xrange(ntable):
        a = str(i+1)+ str("_") + str(j+1)
        templist.append(a)
    clauseonetablep1.append(templist)
    finalclause.append(templist)

for k in xrange(nguest):
    for i in xrange(ntable):
        j = i + 1
        while j < (ntable):
            a = "-" + str(k+1) + str("_") + str(i+1)
            b = "-" + str(k+1) + str("_") + str(j+1)
            clauseonetablep2.append([a, b])
            finalclause.append([a, b])
            j=j+1

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
        i = i + 1


j = 0
if 'E' in relationship:
    while j < len(relationship["E"]):
        for i in xrange(ntable):
            a1 = "-" + str(relationship["E"][j][0]) + "_" + str(i + 1)
            b1 = "-" + str(relationship["E"][j][1]) + "_" + str(i + 1)
            clauseenemy.append([a1, b1])
            finalclause.append([a1, b1])
        j = j + 1

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


def WalkSAT(clauses):
    dict = {}
    for individual_clause in clauses:
        for plsymbol in individual_clause:
            if '-' in plsymbol:
                plsymbol = plsymbol[1:]
            if plsymbol in dict:
                continue
            else:
                dict[plsymbol]= random.choice([True, False])
    while 1:
        satisfied, unsatisfied = [], []
        for clause in clauses:
            if pl_true(clause, dict):
                satisfied.append(clause)
            else:
                unsatisfied.append(clause)
        if not unsatisfied:
            return dict
        random_clause = random.choice(unsatisfied)
        random_symbol = random.choice(random_clause)
        if "-" in random_symbol:
            dict[random_symbol[1:]] = not dict[random_symbol[1:]]
        else:
            dict[random_symbol] = not dict[random_symbol]


def reduceFriendClause(c1, c2, ntable, clause):
    t = []
    f = []
    t.append(c1+"_1")
    t.append(c2+"_1")
    f.append("-" + c1 + "_1")
    f.append("-" + c2 + "_1")
    for i in xrange(2, ntable+1):
        t.append("-" + c1 + "_" + str(i))
        t.append("-" + c2 + "_" + str(i))
        f.append(c1 + "_" + str(i))
        f.append(c2 + "_" + str(i))

    temp = []
    for i in clause:
        tem = []
        for j in i:
            if j in t:
                tem = []
                break
            elif j in f:
                continue
            else:
                tem.append(j)
        if len(tem) != 0:
            temp.append(tem)

    return temp

def reduceEnemyClause(c1, c2, ntable, clause):
    t = []
    f = []
    t.append(c1 + "_1")
    t.append(c2 + "_2")
    f.append("-" + c1 + "_1")
    f.append("-" + c2 + "_2")

    for i in xrange(1, ntable+1):
        if i != 2:
            t.append("-" + c2 + "_" + str(i))
            f.append(c2 + "_" + str(i))
        if i != 1:
            t.append("-" + c1 + "_" + str(i))
            f.append(c1 + "_" + str(i))

    temp = []
    for i in clause:
        tem = []
        for j in i:
            if j in t:
                tem = []
                break
            elif j in f:
                continue
            else:
                tem.append(j)
        if len(tem) != 0:
            temp.append(tem)

    return temp, t, f

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
            if sym in model:
                if "-" not in literal and model[sym]:
                    num_not_in_model = 0
                    break
                elif "-" in literal and not model[sym]:
                    num_not_in_model = 0
                    break
                elif "-" in literal and model[sym]:
                    continue
                elif "-" not in literal and not model[sym]:
                    continue
            else:
                num_not_in_model +=1
                P, value = sym, (literal[0] != '-')
        if num_not_in_model == 1:
            return P, value
    return None, None

def dpll(clauses, symbols, model):
    unknown_clauses = []
    for c in clauses:
        val =  pl_true(c, model)
        if val == False:
            return False
        if val != True:
            unknown_clauses.append(c)

    if not unknown_clauses:
        return model
    P, value = find_pure_symbol(symbols, unknown_clauses)
    if P:
        return dpll(clauses, removeall(P, symbols), extend(model, P, value))
    P, value = find_unit_clause(clauses, model)

    if P:
        return dpll(clauses, removeall(P, symbols), extend(model, P, value))

    if len(symbols) >= 1:
        P = symbols.pop()
        return (dpll(clauses, symbols, extend(model, P, True)) or
                dpll(clauses, symbols, extend(model, P, False)))

remove_temp = []
for i in finalclause:
    f_t = 0
    for j in i:
        if '-' in j:
            j = j[1:]
            a = j.split("_")
            if int(a[0]) in indifferent_guest:
                f_t = 1
                break
        else:
            a = j.split("_")
            if int(a[0]) in indifferent_guest:
                f_t = 1
                break

    if f_t == 0:
        remove_temp.append(i)

total_symbols = []

for i in remove_temp:
    for key in i:
        if '-' in key:
            key = key[1:]
        if key not in total_symbols:
            total_symbols.append(key)

answer_dict = {}

if nguest == 0:
    with open("./output.txt", "wb") as fop:
        fop.write("no")
else:
    if len(clauseenemy) == 0:
        if ntable > 1:
            if len(clausefriend) == 0:
                result = WalkSAT(finalclause)
                print result
                for i in remove_temp:
                    if str(i) + "_1" not in result:
                        result[str(i) + "_1"] = True

                with open("./output.txt", "wb") as fop:
                    fop.write("yes \n")
                    for key in result:
                        if result[key]:
                            guest_number = key.split('_')
                            answer_dict[int(guest_number[0])] = guest_number[1]

                    for key in sorted(answer_dict):
                        fop.write(str(key) + " " + answer_dict[key] + "\n")

            else:

                final =reduceFriendClause(f_c1, f_c2, ntable, remove_temp)
                result = WalkSAT(final)
                for i in indifferent_guest:
                    if str(i) + "_1" not in result:
                        result[str(i) + "_1"] = True

                if str(f_c1) + "_1" not in result:
                    result[str(f_c1) + "_1"] = True

                if str(f_c2) + "_1" not in result:
                    result[str(f_c2) + "_1"] = True

                with open("./output.txt", "wb") as fop:
                    fop.write("yes \n")
                    for key in result:
                        if result[key]:
                            guest_number = key.split('_')
                            answer_dict[int(guest_number[0])] = guest_number[1]

                    for key in sorted(answer_dict):
                        fop.write(str(key) + " " + answer_dict[key] + "\n")

        elif ntable== 1:
            result = WalkSAT(finalclause)
            for i in indifferent_guest:
                if str(i) + "_1" not in result:
                    result[str(i) + "_1"] = True
            with open("./output.txt", "wb") as fop:
                fop.write("yes \n")
                for key in result:
                    if result[key]:
                        guest_number = key.split('_')
                        answer_dict[int(guest_number[0])] = guest_number[1]

                for key in sorted(answer_dict):
                    fop.write(str(key) + " " + answer_dict[key] + "\n")
        else:
            with open("./output.txt", "wb") as fop:
                fop.write("no")

    else:
        if ntable> 1:
            final, t, f = reduceEnemyClause(e_c1, e_c2, ntable, remove_temp)
            dict = {}
            print "t", t
            for i in t:
                if "-" in i:
                    dict[i[1:]] = False
                else:
                    dict[i] = True

            result = dpll(final, total_symbols, dict)
            print result
            with open("./output.txt", "wb") as fop:
                if result == False:
                    fop.write("no")
                else:
                    fop.write("yes \n")
                    for i in indifferent_guest:
                        if str(i) + "_1" not in result:
                            result[str(i) + "_1"] = True

                    if str(e_c1) + "_1" not in result:
                        result[str(e_c1) + "_1"] = True

                    if str(e_c2) + "_2" not in result:
                        result[str(e_c2) + "_2"] = True

                    for key in result:
                        if result[key]:
                            guest_number = key.split('_')
                            answer_dict[int(guest_number[0])] = guest_number[1]

                    for key in sorted(answer_dict):
                        fop.write(str(key) + " " + answer_dict[key] + "\n")

        else:
            with open("./output.txt", "wb") as fop:
                fop.write("no")