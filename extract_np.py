import smatch.amr as amr
import sys
import re
from amrdata import *
from collections import defaultdict
import copy

def _to_string(triples, root, level, last_child, seen, prefix, indexes):
    children = [t for t in triples if str(t[0]) == root.split()[0]]
    if root in seen:
        root = root.split()[0]
        children = []
    else:
        var = root
        if " / " in root:
            var = root.split()[0]
        indexes[var].append(prefix)
    if " / " in root:
        seen.append(root)
        graph = "(" + root
        if len(children) > 0:
            graph += "\n"
        else:
            graph += ")"
    else:
        graph = root
    j = 0
    for k, t in enumerate(children):
        if str(t[0]) == root.split()[0]:
            next_r = t[3]
            if t[4] != "":
                next_r += " / " + t[4]
            for i in range(0, level):
                graph += "    "
            seen2 = copy.deepcopy(seen)
            graph += t[2] + " " + _to_string(triples, next_r, level + 1, k == len(children) - 1, seen, prefix + "." + str(j), indexes)[0]
            if next_r not in seen2 or " / " not in next_r:
                j += 1
    if len(children) > 0:
        graph += ")"
    if not last_child:
        graph += "\n"

    return graph, indexes

def to_string(triples, root):
    children = [t for t in triples if str(t[0]) == root]
    if len(children) > 1:
        counter = 1
        triples2 = [("TOP","",":top","mu","multi-sentence")]
        for t in triples:
            if t[0] == "TOP":
                triples2.append(("mu", "multi-sentence", ":snt" + str(counter), t[3], t[4]))
                counter += 1
            else:
                triples2.append(t)
    else:
        triples2 = triples
    children = [t for t in triples2 if str(t[0]) == root]
    assert(len(children) == 1)
    if children[0][4] == "":
        return "(e / emptygraph)\n", defaultdict(list)
    return _to_string(triples2, children[0][3] + " / " + children[0][4], 1, False, [], "0", defaultdict(list))

def var2concept(amr):
    v2c = {}
    for n, v in zip(amr.nodes, amr.node_values):
            v2c[n] = v
    return v2c

def preprocess_constituency_tree(snt, syntax):
    for idx, word in enumerate(snt.split()):
        new_syntax = []
        done = False
        for tok in syntax.split():
            if not done and word == tok and not tok.startswith('<<'):
                new_syntax.append('<<' + str(idx) + '>>' + tok)
                done = True
            else:
                new_syntax.append(tok)
        syntax = ' '.join(new_syntax)
    return syntax

def run(prefix):
    blocks = open(prefix + ".sentences.nopars.out").read().split("\n\n")
    nps = []
    npstart = False
    par = 0
    k = -1
    sents = AMRDataset(prefix, True, False).getAllSents()
    famr = open("np_graphs.txt","w")
    fsent = open("np_sents.txt","w")
    while True:
        k += 1
        if len(blocks) == 1:
                break
        block_txt = blocks.pop(0).strip()
        block = block_txt.split("\n")
        const = "".join(block[3:])
        if blocks[0].startswith("\n"):
                b = ""
        else:
                b = blocks.pop(0)
        
        snt = ' '.join(sents[k].tokens)
        snt = snt.replace('(', '<OP>')
        snt = snt.replace(')', '<CP>')   
        
        syntax = " ".join(const.split(']')[-1].replace(')',' )').split())     
        syntax = preprocess_constituency_tree(snt, syntax)
    
        nps = []
        nps_idxs = []            
        np_flag = False
        new_np = ""
        new_np_idxs = []
        pars = 0
        
        # find all NPs
        for tok in syntax.split():
            fields = tok.split('>>')
            if len(fields) > 1:
                i = tok.split('>>')[0][2:]
                tok = tok.split('>>')[1]
            else:
                i = -1
            if '(' in tok:
                pars += 1
            elif ')' in tok:
                pars -= 1
            if np_flag:
                if tok == ')' and pars == 0:
                    np_flag = False
                    new_np += tok
                    new_np_idxs.append(i)
                    nouns = [x for x in new_np.split() if x.startswith('(N')]
                    if len(nouns) > 1:
                        nps.append(re.sub(r'\([A-Z:\-\,\.\$\'\`][A-Z:\-\,\.\$\'\`]*|\)', '', new_np).split())
                        nps_idxs.append(new_np_idxs[0:-1])
                        assert(len(nps[-1]) == len(nps_idxs[-1]))
                else:
                    new_np += ' ' + tok
                    if i != -1:
                        new_np_idxs.append(i)
            else:
                if tok == '(NP':
                    pars = 1
                    np_flag = True
                    new_np = tok
                    new_np_idxs = []

        # align NPs with tokens in text and write to file
        for n, i in zip(nps, nps_idxs):
            nodes = []
            if n == []:
                continue
            a = int(i[0])
            b = int(i[-1])
            for index in range(a, b + 1):
                nodes.extend(sents[k].alignments[index])
            if nodes == []:
                continue
                
            v2c = defaultdict(str)
            amr_annot = amr.AMR.parse_AMR_line(sents[k].graph.replace("\n",""))
            for key in var2concept(amr_annot):
                v2c[str(key)] = str(var2concept(amr_annot)[key])
                
            rels = [r for r in sents[k].relations if r[0] in nodes and r[2] in nodes]
            rels2 = [(r[0], v2c[r[0]], r[1], r[2], v2c[r[2]]) for r in rels]
            if len(rels2) > 0:
                rels2.insert(0, ("TOP", "", ":top", rels2[0][0], v2c[rels2[0][0]]))
            for node in nodes:
                if node not in [r[0] for r in rels2] and node not in [r[3] for r in rels2]:
                    rels2.insert(0, ("TOP", "", ":top", node, v2c[node]))
            amr_str = to_string(rels2, rels2[0][0])[0]
            
            famr.write(amr_str + "\n")
            fsent.write(" ".join(n).replace('<OP>', '(').replace('<CP>', ')') + "\n")
            
if __name__ == "__main__":
    run(sys.argv[1])
