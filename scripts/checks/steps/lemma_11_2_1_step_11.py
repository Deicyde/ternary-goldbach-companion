# Lemma 11.2.1 (optcoor.tex 300-305): 13/4 log(x^{1/3}/3)+7.82 = 13/12 log x + (7.82-13/4 log 3);
# 13.66 log(x^{1/3}/3)+37.55 = (13.66/3) log x + 37.55-13.66 log 3. Exit 0 if constants match the log-x reading.
from math import log
import sys
c1 = 7.82 - 13/4*log(3); c2 = 13.66/3; c3 = 37.55 - 13.66*log(3)
print("7.82-13/4 log3 =", c1, "(4.25)", "; 13.66/3 =", c2, "(4.56)", "; 37.55-13.66 log3 =", c3, "(22.55)")
sys.exit(0 if c1 <= 4.25 and c2 <= 4.56 and c3 <= 22.55 else 1)
