#!/usr/bin/env python
#coding=utf-8

'''
Computes AMR scores for concept identification, named entity recognition, wikification,
negation detection, reentrancy detection and SRL.

@author: Marco Damonte (m.damonte@sms.ed.ac.uk)
@since: 03-10-16
'''

import sys
import smatch.amr as amr
import smatch.smatch_fromlists as smatch
from collections import defaultdict
from utils import *

pred = open(sys.argv[1]).read().strip().split("\n\n")
gold = open(sys.argv[2]).read().strip().split("\n\n")

inters = defaultdict(int)
golds = defaultdict(int)
preds = defaultdict(int)
reentrancies_pred = []
reentrancies_gold = []
srl_pred = []
srl_gold = []

k = 0
tot = 0
correct = 0
for amr_pred, amr_gold in zip(pred, gold):
    amr_pred1 = amr_pred
    amr_pred = amr.AMR.parse_AMR_line(amr_pred.replace("\n","")) 
    dict_pred = var2concept(amr_pred)
    triples_pred = []
    for t in amr_pred.get_triples()[1] + amr_pred.get_triples()[2]:
        if t[0].endswith('-of'):
            triples_pred.append((t[0][:-3], t[2], t[1]))
        else:
            triples_pred.append((t[0], t[1], t[2]))

    amr_gold = amr.AMR.parse_AMR_line(amr_gold.replace("\n",""))
    dict_gold = var2concept(amr_gold)
    triples_gold = []
    for t in amr_gold.get_triples()[1] + amr_gold.get_triples()[2]:
        if t[0].endswith('-of'):
            triples_gold.append((t[0][:-3], t[2], t[1]))
        else:
            triples_gold.append((t[0], t[1], t[2]))
    
    list_pred = disambig(concepts(dict_pred))
    list_gold = disambig(concepts(dict_gold))
    inters["Concepts"] += len(list(set(list_pred) & set(list_gold)))
    preds["Concepts"] += len(set(list_pred))
    golds["Concepts"] += len(set(list_gold))
    list_pred = disambig(namedent(dict_pred, triples_pred))
    list_gold = disambig(namedent(dict_gold, triples_gold))
    inters["Named Ent."] += len(list(set(list_pred) & set(list_gold)))
    preds["Named Ent."] += len(set(list_pred))
    golds["Named Ent."] += len(set(list_gold))
    list_pred = disambig(negations(dict_pred, triples_pred))
    list_gold = disambig(negations(dict_gold, triples_gold))
    inters["Negations"] += len(list(set(list_pred) & set(list_gold)))
    preds["Negations"] += len(set(list_pred))
    golds["Negations"] += len(set(list_gold))

    list_pred = disambig(wikification(triples_pred))
    list_gold = disambig(wikification(triples_gold))
    inters["Wikification"] += len(list(set(list_pred) & set(list_gold)))
    preds["Wikification"] += len(set(list_pred))
    golds["Wikification"] += len(set(list_gold))

    reentrancies_pred.append(reentrancies(dict_pred, triples_pred))
    reentrancies_gold.append(reentrancies(dict_gold, triples_gold))
    
    srl_pred.append(srl(dict_pred, triples_pred))
    srl_gold.append(srl(dict_gold, triples_gold))

for score in preds:
    print score, "->",
    if preds[score] > 0:
        pr = inters[score]/float(preds[score])
    else:
        pr = 0
    if golds[score] > 0:
        rc = inters[score]/float(golds[score])
    else:
        rc = 0
    if pr + rc > 0:
        f = 2*(pr*rc)/(pr+rc)
        print 'P: %.2f, R: %.2f, F: %.2f' % (float(pr), float(rc), float(f))
    else: 
        print 'P: %.2f, R: %.2f, F: %.2f' % (float(pr), float(rc), float("0.00"))

pr, rc, f = smatch.main(reentrancies_pred, reentrancies_gold, True)
print 'Reentrancies -> P: %.2f, R: %.2f, F: %.2f' % (float(pr), float(rc), float(f))
pr, rc, f = smatch.main(srl_pred, srl_gold, True)
print 'SRL -> P: %.2f, R: %.2f, F: %.2f' % (float(pr), float(rc), float(f))
