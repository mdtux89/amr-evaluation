# amr-evaluation

Evaluation metrics to compare AMR graphs based on Smatch and relies on https://github.com/nschneid/amr-hackathon. 
evaluation.sh computes a set of metrics between AMR graphs in addition to the traditional Smatch code:

* Unlabeled: Smatch score computed on the predicted graphs after removing all edge labels
* No WSD. Smatch score while ignoring Propbank senses (e.g., duck-01 vs duck-02)
* Named Ent. F-score on the named entity recognition (:name roles)
* Wikification. F-score on the wikification (:wiki roles)
* Negations. F-score on the negation detection (:polarity roles)
* Concepts. F-score on the concept identification task
* Reentrancy. Smatch computed on reentrant edges only
* SRL. Smatch computed on :ARG-i roles only

**Installation:** ./download.sh

**Usage:** ```./evaluation.sh <filea> <fileb>```,
where <filea> and <fileb> are two files which contain multiple AMRs. A blank line is used to separate two AMRs (same format required by Smatch).

References
-------
Smatch: http://amr.isi.edu/evaluation.html
AMR API: https://github.com/nschneid/amr-hackathon
