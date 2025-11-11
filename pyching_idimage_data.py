##---------------------------------------------------------------------------##
##
## pyChing -- a Python program to cast and interpret I Ching hexagrams
##
## Copyright (C) 1999-2006 Stephen M. Gava
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be of some
## interest to somebody, but WITHOUT ANY WARRANTY; without even the 
## implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
## See the GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING or COPYING.txt. If not, 
##  write to the Free Software Foundation, Inc.,
## 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
## The license can also be found at the GNU/FSF website: http://www.gnu.org
##
## Stephen M. Gava
## <elguavas@users.sourceforge.net>
## http://pyching.sourgeforge.net
##
##---------------------------------------------------------------------------##
"""
ideogram image data return routines for pyching
each of these functions returns the image data
for one ideogram back to pyching_interface_tkinter for
display
"""

def id1data() -> str:
    return """R0lGODlhOQAyAKEAAAAAAP///////////yH+ATEAIfkEAQoAAQAsAAAAADkAMgAAAuyMjweb
7Q8jXFRWibOhwHINPlw3feG5mdGInuz6tlosqnI22sp1zzm/Y/QcvyIROAwWSTUkIhdaMpvT
pxEkDDgbJinNlaV6oTceclxNaoWxz1etvG7hXPQc7o3f1dcEWYS392YVJqPjd6iXFgXEMrg0
VGF0mNcjpaT4V/bYeDGIckcZR+ekWVcYyQZJRZcyBoOatOoRK6tai7iIR4iD27rW5/oL+5O7
iTUbdEycyLt8Gnyk60NyCTwtbOhZjAm7mfXWrKy9112CzYzuqi4ObSrNbmeH0Z4p/0movn7/
7s7IX84cqEotAg7rdVBCAQA7"""

def id2data() -> str:
    return """R0lGODlhLwAyAKEAAAAAAP///////////yH+ATIAIfkEAQoAAQAsAAAAAC8AMgAAAsqMj6kL
vQ8jbBTIi1OlmXW0OV+wjWRlnuhXpiG7mm/XujFWyxy82yJ9GwUvOdXvMZSElj1GU8mMWpCc
qUb6NB5BM2zxMFMwtbGklhr+mtVh8HBsyEmdW/JPHqVb7T21e8/lMHdVRzhRtaQHBWgV9Gb2
Fxn39JhlaPTHSAmZmXXjVRiYVAYKKPY1WWp6yInlYymayYNKBHua+ArEWRuqtzor1Juxm4Jj
Wzx8jMz7u2ws7BxBHK1IHQxtfducXc39vO0dG848zltu3FEAADs="""

def id3data() -> str:
    return """R0lGODlhNQAyAKEAAAAAAP///////////yH+ATMAIfkEAQoAAQAsAAAAADUAMgAAAsCMjwG7
6Q+jNKzOi2XdIHvPMd94hR2JQmHKJmsLc48FlxtinrV6K3mzm/1yQeFQVnQdgUnlsMl7Qp3L
KbVq1LWQh56DO/VemVBaVmQ1f8EkMjXyQom76LO2Pfe5cfnRvK+nJif2R7RFuAT4AZaoCIJo
8hZzI+W002g19pNJh1nGFxl4d6kVSiFIWlpYV8QauOaa+hg7SXvW5Ai6V7t7m5Sri4sKZ5sS
NwGMsamcrGlq0xjdLCrtuVhtPYh9nBotUQAAOw=="""

def id4data() -> str:
    return """R0lGODlhKwAyAKEAAAAAAP///////////yH+ATQAIfkEAQoAAQAsAAAAACsAMgAAAsWMj6kH
vQ+jak5aQyOtV2e4dVL4bIA4cpNJooyasKaLtLUMo2z80QFuw+R0wNPKt+LkekiQ8XZ5uqSY
Em5CLAKhC6139/pSLbJw2Tm+7Waec3LN5BWt3aB8mMWn4mj93d1GJQbY9gfW1HcYg1jH9+OX
h2dHQyg0KbKldkn2ccjmw/aF2DKjyGhmuYlEenX6qAQHySnV+pmn+fpkuncXZpjW1ev769gI
4yhqtVTsZZym2vrW5xonWEyd6eqsim2r7fwdBSxSAAA7"""

def id5data() -> str:
    return """R0lGODlhLQAyAKEAAAAAAP///////////yH+ATUAIfkEAQoAAQAsAAAAAC0AMgAAAtOMj6kI
vQ9jatTJG6umuJsNch4UhiNWiud6aOz7qZfMVkpKB9aM99P+6wltsSERtWnhGDkSqHi8NRcl
XfRBfCpN0SQUKrtaw96uGHst56bSZpbdcfEsWiSAaabXJSrTdwvH5zV21waDtxVUeMiASHjG
+FjFaDT4IhSJ1heYqdgZx2nVubZE6VAJdFIJltpWSkgl5/QK69qqKJK3iHfrGsQbG5oGdAbp
61ikuZtBRtxr7AmIzLvMvJsX3Bv8m0grmOoMKGu34geqPQsdWzP+me4OelEAADs="""

def id6data() -> str:
    return """R0lGODlhPAAyAKEAAAAAAP///////////yH+ATYAIfkEAQoAAQAsAAAAADwAMgAAAuqMjxnA
6g+jTKy2iTO2XPuPcBVIfmKJbl3KQmsLh1ZMG3NN36Wei4Byefh6Q1kQWEz5RsYj8gRa8g4v
h1Ql/UWq1mT3imVuvVnnxOsqoz3QsPqsfZrhs3Z6uhCbdHMKGs+mN7bkJyg4RmfX9NW3A0h1
aMOFwzgYSfTzKDmJydnUiALm1qko4elYGkapmUgJc7p6uQgZV0ModCgbVYZbSwsqp8b5yMqY
lCqbetc3DLq27PsbjfeWQZzLJAw7K/fJKw28Oaen3avL/eu9rdz9qR4NbV0uvXf+zlVsrPHs
hwq/7OpJoHABrRWcUAAAOw=="""

def id7data() -> str:
    return """R0lGODlhKgAyAKEAAAAAAP///////////yH+ATcAIfkEAQoAAQAsAAAAACoAMgAAAtCMH6CA
7Q/hUrHaN+ndNTMOOl5IGmPZTJKKHt6HZOh7mqxt0XS8uLKtC/IowaImZ+wZL8mbyPn8+XoR
KQYKPF6pVe4QtvKKvVNmMhsFh4vlL4zVhJ8T86mG7VaS6cfa+r13s7f2ldaWwuWEJai1wwe2
mBgHVOhmh8dXeblpSWmXJaf1ifapQ4rYN3ZXg/U4esoayNiomrr6MqTpCSp06Jp7ibvRiioa
Qqxbgvw6M1jcctplfOyMCv17zbGc/cw9XO2dHL6lNm5oLl2OzryOeFEAADs="""

def id8data() -> str:
    return """R0lGODlhNwAyAKEAAAAAAP///////////yH+ATgAIfkEAQoAAQAsAAAAADcAMgAAAtyMj6kI
vQ+jVK3Oi2W1ufu9eeIFcuO5lADKOKPKHqAIx0H5zbaBZ/1+05GEu9+EWERGlDGjJgTkMR9T
VDUFjV4ppkTW9w26vF2Z82mqtcZS1QrjdpPjcjideI+D89x8efgHMXOWE0gVlsR2hGjDKGjY
BImlCOR4SJn4ZofZKNmnGSUGyrU2Wmn4ZcnCGKZqVabkepLK6vk0+UYo+moqqtvWu4m7Jfto
qocWDDj3W8prVrfIKZ2LDDi9xGF9rWxsEb2HzQzV7D11B92d7IcuFsnergW/Heo7X59Nb1AA
ADs="""

def id9data() -> str:
    return """R0lGODlhaQAyAKEAAAAAAP///////////yH+ATkAIfkEAQoAAQAsAAAAAGkAMgAAAv6Mj6nL
7Q+BhLTai6vcM/sPftwWYmSJNmOXOmsLH2+szjTK3a6ti+cDaK2CPVCOMUzxipeh8xlawp7U
qvXokSqv3C42o91eEWHkL/u9Qc3nAKs4YhrabKKMTovLLemy+L23A5gElxa40KfHpHhYR8ZY
iLfnJUlhZ2k4SRkFKNipUAnmRSZ6CZSZgIr2ZRgK+llnGitkCjln+wqLqPrIa4RKWKObO9zr
WtrBdVpsLCt8/EwZvAt9W+3m5zlGHO08y4eLWbXsje3b3BQurr6rXU78Ts0smM7LDm9yjjP+
XD+feq0XvE3U8gW0Fi9WF4D6wB289WvhwBj3dNgKV9Hgv2A8dOIMamimWUKLHdeYG+kJ4UaK
J5SdRNktWySVSzKSm9bopAyd8mC6A8nxIyybEZzkNMbQG9B1K9UIJdJyaVGpLN+MCuqTpDSq
5I4OrCkTjVd5TMfmrEbU7NG0as8yKwAAOw=="""

def id10data() -> str:
    return """R0lGODlhOAAyAKEAAAAAAP///////////yH+AjEwACH5BAEKAAEALAAAAAA4ADIAAAL+jI+p
ywbfopztWUizdrfjDR7e6IURRpLBaDJp55atklLyTFsgjC98dunFdBOWMEdMvJJH0fIJaCqh
QWklWEUwnZ/er8sB33DZlZhY82a/1GOZ97SaP+yo3LdObsPgWd4eppVGVrUX1aZGt6XCB+i3
2PXD5dhSNheJBmFpYilZs7nz1mkEuiFqiNpnekrJN7W3iql6OQkLxFR6OcipJym49KjoW/sa
bJfZ2sgYUig8BBw6O4fHmiyRC3szZmMb+Hq4yy1N+wu4rNHtOvk9/nzd27ddlK6+ef7erjvN
rmtdPK8j3p9c+wCq2nbPCbpUtsLxokRQ2TBTiV7cuWXxojgDFgUAADs="""

def id11data() -> str:
    return """R0lGODlhMQAyAKEAAAAAAP///////////yH+AjExACH5BAEKAAEALAAAAAAxADIAAALFjI+J
wOoPY2IUyItdbbnnbXliVI3mU57qkU5rRy1g+KLzTdcGzudiD9LZgEJTrPg77jZIDZDTDDxb
r6mv2YvClFoJdYkrWsOqcdZr/srUk/FaOGtfuV02G05fX/FQZ59Pk3d3QqXGpFOoxHG48tVy
FEQoqAjJ6FHSl8IYt9VwWJkYScLFdDMkqmAYY+lnKrcnFTKo5zoICgYbG3b3uIhKW3maQ8oq
6fj3a6Q6N9vJYmHX/BGYjKtV3fWam/38x52a992GVAAAOw=="""

def id12data() -> str:
    return """R0lGODlhNAAyAKEAAAAAAP///////////yH+AjEyACH5BAEKAAEALAAAAAA0ADIAAALJjI+p
ywnfopzh2WupVrj7vC3fSEJaiaYAo6aRx7am0YUNetd2fFHwDuT8gpteZUg84ZK7ETP4eRKR
0iK1OnFildFtluSVLA+zcA3jMFZ/aERpqjuC0uAQsi2q++I0Ne+a50cmGAjohkdX9tJVqHg4
t4c4KJnYRMn3t2Kp+QiZ45hE+ck5SfrleeqSaiomg9qZ6arFsjgmhGkzWytqx9v42ks4Cpwr
HLtmfEu8Cdro5dvJygRdKh2a3IcNl7Gi+izbPA0eVk1eTF4AADs="""

def id13data() -> str:
    return """R0lGODlhbAAyAKEAAAAAAP///////////yH+AjEzACH5BAEKAAEALAAAAABsADIAAAL+jI+p
i+AMo5y02uWyfrf7D27iCJYmBCTjypLna7Yyp7jw3c1ZvuEM7TvYSqJgDRjU4IrGxq6pvDGb
hunyCetRhVpftNLlYrfD7Bi1OiKhVvO6qks538mwdBz/iuVk+x3YAnZm5PfHJ/ahR1jodvii
WAdp6DVIWTl5RdfoGMkpcSlp6Jk5quYX2rgFBzgno3L5iIoZkGcnS1RmycfyqngbksYGCNv2
66FlfIxHDJlsEeb8vAzaDAt8Fk2hxyjJmNidjYZN/ebNE2ouPV4Obn1hnq7ti8VrWvr+G/85
H4cRbq9O0wRbefy5kyfQ3r0I7RYaTDjwoMJvdCA+dMjwX65jfRbxSfzxb1W0kOI6Aoyx8WEn
jCdP1CvJMmDMPTM5pqRFEuTHPYtetqoZcSdOkx5d0VwpSOi5GSKB9hqaLCdCHVBRBkKoimYg
qUazKrta1aVPr2xISSWL9mfatanYusX11kcBADs="""

def id14data() -> str:
    return """R0lGODlhYgAyAKEAAAAAAP///////////yH+AjE0ACH5BAEKAAEALAAAAABiADIAAAL+jI9p
AOoPozyszTsrw7w77YWLZolmRJ4dWaruCL5ZLL9sjdL4ee+f7vP0gokUMWQ8IpJKDBCyUTGb
kumSFRVZqQqs91vRhrkBsPm8rY596LZ7zXnK3mW5Gu7Ed03fX5YM01Jkd/c3qMdFc3ZEqPSW
JoUI4/KIxmYYKPlQiXmlyVcZ10fR2MTZublV6uiV+tkleIhqOuQ6K7a605pzi4QFODpJ2isU
lmtjPDZ0fGH0iqxsNhzLo0hcvSY9jQP0jPtXylwY673S/SoOZVc+g9gtO7eeDisZs8yu/gk5
zhs8L0sNIK52uwJF8lbLSZ6AnhgSdAjwmi+IdSTSs5gJYzNNdPMSLvyXj2I6jx9B+oG4LyLF
fik/8nuo8eSvgyhXkQQFBmevliZDBhOFRxsgmQWBChI6lOi/ekWTUpnV1KnUafim0opplVHV
rKwwFAAAOw=="""

def id15data() -> str:
    return """R0lGODlhOQAyAKEAAAAAAP///////////yH+AjE1ACH5BAEKAAEALAAAAAA5ADIAAAL+jI8J
m+2x2JvUxFjVlbnDDXgWKHZkeZZUOl7NppouAoY0Fmfwu7e5jOMFg79VT3ggFh812+v2mS1b
x0lTibrqrtht08j9cTnMMdkTFrGk53JVUSGnt/FukmOe1qzmN/orNOfnJRU4JKf157Ti0xiV
OOV211eIUkcJqdiV9xgJOOZYmbU3iXHoJKo2CHGDimcXyecKGAvUV3vJiduqQRq121oZ0gNb
NFc6uxiDqUyV3GZb+JZCO9pc5YuzKqssbPr63AzWraQNvrgdGMwbWs7CjTzJ3hmc/niCdSqe
aYh4re/gWC9obpIVTDXPVilgKly8Y5jrnjiIBZ1RVBXvYo4GYhrrxCgAADs="""

def id16data() -> str:
    return """R0lGODlhOgAyAKEAAAAAAP///////////yH+AjE2ACH5BAEKAAEALAAAAAA6ADIAAAL+jI+p
awAMo5zKPYqztA51DQYcw5VjuJmXp6qo2MZJbL50e9R5+cI8e/KtGsFe5Ef8AIdGSNGyeEKb
O2XqxrRNKdgt5udddl0aWfQ2Q2bMFV5RaAWR29bwG0U+eff3HnqLRVU11iVIeJhVhpOkp0OF
JpZ2F3YkAzipxph4JgX1NjcYV0niGGpX6pcJqSnIarrYZ4QEFtgKxLKkuflIGQonatsL9yvM
mxhUGyyKXKjMxOz5AZr6PES7woYH7JskubhWrHaafLWpCtxcTrcsvJrL6H1cTGxOE8m5q50X
C29L3z2Imz9H7LK1ykRqmjNwqPzJaejw4byIXyZSnLAtRAEAOw=="""

def id17data() -> str:
    return """R0lGODlhMgAyAKEAAAAAAP///////////yH+AjE3ACH5BAEKAAEALAAAAAAyADIAAAL9jI+p
Cb0PozStzotVtfnuuQGdFDrRNy5leHJUCa1yawZyzcAwfbOqawPmeroYUBgkpl41JHO1PKCS
mCnD48I5rU/cI9vkonogrUgqJDp/ZyZiqhwd02izF9tO5od8DQm8leZwY0SmYae2V0fYp5eo
6OboNbdWFmbFFdUYWfe2uMNTNpRo6TGqVvpTCKn3d+fI5vPkujdzSsm62AX6iUu7m9nKZnkG
+LUW/Bb4Kmn8e8jMSPUMDQmlnKt7fFeZrB0LvUo9vInN/E2eY+7dRYMnu315/X7e3iwdnw17
TxpOmxftUQd4GR4pIZjCIJRKCRUWqxdFICdN+YJBpHihAAA7"""

def id18data() -> str:
    return """R0lGODlhLAAyAKEAAAAAAP///////////yH+AjE4ACH5BAEKAAEALAAAAAAsADIAAALbjI+J
AOoPo2FM2ptowzzq3m2ZRorgUqbpqajfQbJoBVMzLU94YNd9rjO5TEDeMFYcHXdJI83GbD6g
P6lD5ZT9lqvTy+VzEjEf5Cg4vlTJUbZofcWqwWhu+rmsd82+rrgfhhaH9/byFyQ4RSg2ZpeG
yGjYNySR1yLXpvSVyVMTOFf4iAIIGulBaYHqKDlx01OG+jnJlxX5CGc6p3vJCSqaxAUCu0pb
SazZy9uwvMVUElLVTFScuiOtyRJNOI1bLbR4o3VdS+p1PRzrS0xnZLvu6L6KTJkO5NdtVVEA
ADs="""

def id19data() -> str:
    return """R0lGODlhNAAyAKEAAAAAAP///////////yH+AjE5ACH5BAEKAAEALAAAAAA0ADIAAALzjI+p
Cb0PozytzothtbkjoG2g14mLOJIBx6BOu6mrS8fwq9hP7Ybsh9rxfjmdgefDBYXKYar4M52c
0kh1hoMOS0YjsCfDPsXM8DRL1prVXylxfYxSJUs6dUvBJ+8j/vX8d0Vzg8YG+OTVVniz19Zo
txhXmCgZ6cg0lkZ4Qal5qZgJiImpZ/UmFopag+H3KNOqAacKJjtR9Vc7+lkbSNQJRVrn9Vvp
t9SFbHyHujs7R9iXPNY7qBUt90Kbl/12K410meit7MshrkMuvT39fQrz2a6Yobe8nnpY5yxI
bL3vlonLlKU4rPjlEnjvIKSECk019FAAADs="""

def id20data() -> str:
    return """R0lGODlhMwAyAKEAAAAAAP///////////yH+AjIwACH5BAEKAAEALAAAAAAzADIAAAL+jI95
wOoP42NN2mvApLjvilCaRy5icpZqmnHq6rYN+0q0iI91mINBT9v9gDxNzhKL4Ia6obJJJMWS
KGBPCvIprCYqUpdleWXNizU6Zpar5/YoHWSfuGTZ5wvliMNXJr7YVUe25GfjM9U3WJbGpvY2
d6gViEeoBgEn6UAXJ+jCeUmot3Zm2eF2g8a4darF+amZpOqqWrSY2YV6KwdGh7un62vUtnpU
+pSSqClofEdFu1z48WhbLNcoHTxsjfJU2wv7ahYrm4wVqQsJbHguzDe9ZurJ6o4kPT8OX2Uf
V21nCJ7vmkBQAP+AW1fwGKiA0BoOJLYOHiN1zLxJpEiJ1SoNIYrccIyo7SPISgEKAAA7"""

def id21data() -> str:
    return """R0lGODlhawAyAKEAAAAAAP///////////yH+AjIxACH5BAEKAAEALAAAAABrADIAAAL+jI+p
y+0PF5ix2jjB3TBTDh7a443hWX6n5ZHtGqbw9TLlHNe4mzX3vvkBHUKFbojpIYlKSXOZTKmg
R8RxCrVKn0hu4inrarfenU5FDgPT2GxAGWaXZ+l1Vf6WunmmFXmsl0dRlUMzF8VmUDQmclih
xufU17gl2BRICThpI+dIafL3dffSU7RpiUgKKdm5SfiD5onaUbb62domyCoCGPWYC9uZc0qo
eEoHXKNWTEssy5rL5Bwt+sFcLckRytL2rHz9WX2sWWc4CW48tbjbe4s7Li3e7IqO516JwyVb
ayuOz9juizZ14MBs43SNXzd099ZZegcv3bxzXhwi/EcOU7qziEH0VWQYLhUzaiAWXQGZ6Ve9
Lh+xoLTSkWOeIevOPNvT0MwogiRx4oKB8Vu/JfY2yvQRSqhGZHhsvgyoyprUpxNN8rxp5OpG
Xe5oGsR2a1jWEUsfsuxjEBRViRK6srODlmfYkjILHjWnNm7enpxU3j2rJeSsPSP/xgSY1jDd
qxaByuU62CvEoX70so3MbfJklozeZRZWVXFozXyNrqWZkXRjJzhjqm7V2k2iYaVjV8Z6oQAA
Ow=="""

def id22data() -> str:
    return """R0lGODlhLwAyAKEAAAAAAP///////////yH+AjIyACH5BAEKAAEALAAAAAAvADIAAAK3jI+p
AOoPI2JU2rsow/zq3YXO14jm8Z1qQJIr1Mbla8j2TLM3no+4NuHRQEGiTriqFH/KHBBlPCJV
z+MyM7VUEztXpwvecsPkMviKTZ2bWFPqEYXGh1tbT06+S8N6ts//AjgmSEXkJUZ3I6W357XY
N4d2R4jH2PU4uYPZo7npFFkJmVVDecJ2Wuqm6JlohxgI0kIK2mr0+qkkyzib6ygaFfM7Fdwq
QWx6O5hsvPxHG5EKE707G1EAADs="""

def id23data() -> str:
    return """R0lGODlhMQAyAKEAAAAAAP///////////yH+AjIzACH5BAEKAAEALAAAAAAxADIAAALtjI+p
ywrfYnhASkqty5ph2BlYuHxgNx4c+oXm1LqpZdYnveJ2rM2XX5PdGj5RUVeJvBA8YbK0VB17
uUSQOUUSd1GHsorlgsOesTSXPT/Da6eaDR1SIbb3Rv4TP6fpux7ul7cjGNcGo2dYqIgICKMY
yPV42MbHcRWndlM5RLe117SZOHlnBBRaZtqVKem3pmo11pdqVooqipXZxIJnC/L6xdvq+2ur
dZi7Gzz5eaLriXc5aofkWtdYO8f5enTbCsvdRx1YSpycqF2e3c0W/m2trizsDBxfmM7qNE9P
wk67xe+uHkBzAwuOM4jQkYECADs="""

def id24data() -> str:
    return """R0lGODlhNQAyAKEAAAAAAP///////////yH+AjI0ACH5BAEKAAEALAAAAAA1ADIAAALvjI+J
AOoPo2Qt0SqzDheb7m3i0lnXiH6gVz5UaoIxo6ywetb5sb6o7egJfSKZa9hKGY80TvM2wzxJ
IWhw6gztrljr1oi08pI45BYGHKezVSW5DDm75Wxmd7ScqeHQfFRGt+H3lxOo8aYjZziBqMfV
lrH2ODk3SNUwVMlnF4ZHtGhGdCgqShnjiVWamKoad9caVXbHxRQZagu5yGbmBSvrY4kKucvS
+APbozZ7/HrirFtUSpYspnxZFYxWGJhdWYEs2eurHK49TixbbYx+LcZt3M3YVU6+HPEVT3xO
mx4tFG3hBq9qzP4RFEbtoD8ZBQAAOw=="""

def id25data() -> str:
    return """R0lGODlhaQAyAKEAAAAAAP///////////yH+AjI1ACH5BAEKAAEALAAAAABpADIAAAL+jI+p
y+3fgIS02our3DP7D3ocF5YJaX4jkIIr2lprTL12R0PjMqv3D8s9UECWqCgsFV8uWDApW9p8
uMMTGpD+slZjc4PYYbvI8Sl4xd7METSYbdjCFe7qnOy9x6tiPd5PFvZGN5iUBldY12NYqJeo
ZRdziJdnArnGaFdmeTmV2VkZtQRICBraBkR5eieXginIRJqVN5nRVxorCxupRnKrO9s4RlTL
WsxD1XGM6LS6t6gxuMymeCnqNW1mmqrzyMu8LTVUB24dLLyLTnnm/GWK237m8Busgsr9fEqf
rP/dfb8vzb4j6tT9m+fvHI+BGBgaHBcPIi+GFyg+RBgRYx9Qite6JWTAMdordxmzrWsxkuBH
VRVDtoTW8CI8mPlcikxJLdzKGjtwDgvn6pbPn+ZC5Eons1crkgk9ARNyVGPSp9emsqQa1Co8
rFzzde16sQAAOw=="""

def id26data() -> str:
    return """R0lGODlhaAAyAKEAAAAAAP///////////yH+AjI2ACH5BAEKAAEALAAAAABoADIAAAL+jI95
wOoPo0yszYurxbw7XXkiAgLjmZUmyqns+7jwVc72At5Src95D+EBXxqarziEIXGqEOqXFDWn
1BM0qqBqt9fWEsgNW8QrT1dHLgtTZfN3OA1+nckzfCOnG95oPnbyttan99GGFSh4YxeQeIcn
4zjGdajXeJRmOYI5iFllk8bSyRf3GXeFR6PFhPpHcUrICBvRlOXXykTitxjDmit7y/sLqbQL
vJcjpphJKbrsNXy76dur6WRbtwVI7UZ3HemdpVy5jW2o/cvNCm5MRjS67m7ebP5MDR8qPU0+
611MLNTIWTB0x/bF62XLXx6DAp/IKoJKYSGC+uhdkkcqFsVgWvcKbqwmKZtGg646evwoJYQn
fR0acpTYslvAe9BiumRjKCG8mwN58osorF9NkENBlnRRrKiVlQ4bdPpJMl1GoqJ2MFO1dKhS
YGGyWjz61dhJn9NSoRTbI+xLtGy5TSgAADs="""

def id27data() -> str:
    return """R0lGODlhMwAyAKEAAAAAAP///////////yH+AjI3ACH5BAEKAAEALAAAAAAzADIAAAL+jI+p
ywz/mpzUwAuqnrjDHWCUR34jmZTq1ayfa3Jwh6zgHDmmuOFZRdPwaizg8BQ7HCVL5I+YZEYt
OUUR+pRVqc3Q9KrllqzfKdHry6LVaOXChd2uU2N6RK5cgtceO5scVYSD5QRow/e0l7SHqAcm
GDTnxyiWBZOHRxk3Gck3qSXX96aoiRlqtkkIamiVagrKBsnjiFdZdkj7M8Mp6hm3y1ubqwJb
/JvT9Wqs7Dq69Zdr+Kc87CctRWyqxphs2xttDftNmrkYi3zEfZvNGa6qzW7rxiWd9jzUe+zz
y1uP2qIJhTYQzfwlKoWtVj8xBH0ZmfVPR0RnMSa6I4hvWsMHGxY3YvxRAAA7"""

def id28data() -> str:
    return """R0lGODlhdAAyAKEAAAAAAP///////////yH+AjI4ACH5BAEKAAEALAAAAAB0ADIAAAL+jI+p
y+0PowFUWkbB3byHDGoeFI7mOYUluqgiCzvuHCdujWYIna54r/uNZiCFSng4IjvEhhL5XO6i
wJezKKVmm0ns1Qv1Sati8VQrNI+JViwbvFSPye0gTf7Dzz/BboXfB/i3BrdHYhcoaBVXaCjT
l6hXI+loAzkIZEiJuecVmcgI6ica6mfJGcr5tljac4YatsplQupqW5UUKzvLhAZoOnqTs0tM
K3w6Suf7RQybx2OE2Fz72qzJW80W3XgKjTunnfn2QBnsXM4iXRcegd5F7h4Dely97Wwcn44q
562Ig72FVYld3VidGEhtEiw3K8zka8fwnkKDEddhengoELeXiQLVvSr4D85GeZ8GjatHUtRI
fRov9RMUkhTGC2BqbpzJ7B5OCSWntAA4RNKyYR0hvvQwlM6zpD+ZWnBKD99Jnk6NJsxmMOO0
cjsLZs0pEcNURUczEb1qL19Zr1G/bqiaVi1atuzgNV0Jb22aravYno1KiC80wEj7VhLsiXBQ
w4f5mnO7mHFjyd/2yqpEVydkGJQxV2ZQAAA7"""

def id29data() -> str:
    return """R0lGODlhOwAyAKEAAAAAAP///////////yH+AjI5ACH5BAEKAAEALAAAAAA7ADIAAALpjI+p
i+AMo5zKPYrztFf7b3AASGbiWC4ceabM+rVuJXrynNxbjdMwxevlgjuL0GfE/I4HXYTIDECf
yWhzKcFetSauSnuq2rzIYZgMmX7PbDVVnG5f2GPjtI1Ev+Rm1BvehbeF4pdXCMRXFtLRABiX
uFeIpTcoGCm55PhYRQZIxJjSCSpFyaK5OdoDdth4OpN56obzI+r6OocmO3uWVWrqtGYbCmyY
ultKdxSGmKQb6EvK6NxLfHk43besxIVd2R1tDB5erOFcHcz6l05udV68XuL+Pv5Mby2vDs8M
WQSNyrtNWEB+VNrhKQAAOw=="""

def id30data() -> str:
    return """R0lGODlhOQAyAKEAAAAAAP///////////yH+AjMwACH5BAEKAAEALAAAAAA5ADIAAAL+jI8G
C+kPo3yszsOuhtXevoVY13ygKJ5KdHooZ5GUp74Jid+ubCM479vVUr+MRAXUFJOwRdCoXCpc
M2hgyMrpnEfrlWribsXV0tP8tWm/aHbb7SZHgV7vtIjCw+/tpTz0s9ciBSgXSANCSMQFxeiY
KAY212AnyMSXthHzJhPo4Dl51ukkqRfqN0jmV2iaEWlkuojlaoa4Jkv5l/XG1tO7FzdW9quG
WlsZi9tqhTrBvIYEuxqWjGkdV7mL18itK6ktXQL56p09JnTYzft9jp7jPrzlM/JIc/1t/Gdb
96yfbxhuXb9/yaiUU0WwGjtsCG8V08XH4MKHXWpg8UWsyUAcXhg5ChOFMSSniSEfQizZgyTK
POZWUnS5sqWGAgA7"""

def id31data() -> str:
    return """R0lGODlhMwAyAIAAAAAAAP///yH+AjMxACH5BAEKAAEALAAAAAAzADIAAALejI+ZwOoPo2OU
yotftbn3DSiNRx6gWJXkNp3qxbbxC81oSke4tudyqBv5eMIacEg8GmzIJMjVvD2fUcT0yslk
rditrwvtfcG/KhXmHRclYrUSrUx/5Fzgrq2lB2I9PPy9FJblxzZ4VXdEGNRwKGWitxgClbSn
aLSG0VgCufRjSelUdLaZhrXANAc2Wcl5qckKiJrHiFf6SfSIKTaammgrOrUCrLtl2nK61ndn
KJdM3BU4bFvnKfj8HO0KCBuaa4eZixs5ksIJDi5lcRsFXfW36h66bhYc/95qH42fn10AADs="""

def id32data() -> str:
    return """R0lGODlhNAAyAKEAAAAAAP///////////yH+AjMyACH5BAEKAAEALAAAAAA0ADIAAALVjB+g
gO0PI1xU2ovpwrwjzXjiBY6mpJ2qU61JK8InqMSbTcvZPeU+z9E1fj6TcFhysYDKXcgAezYj
wEpq2pP+VFJqDbrt0CwtIon4fZSvH7Q7+z26o+w2Tz4m1w/s4yt9hnfHxEfo5UcHaKdYt2e3
CBeSU+gHFxn2Z3jYtTjZicNJGYpUaWmK4qin+Imq2Tqa2WUGujnnuvlqa3SLmRq4Sqq6e4uV
WzwMfKya7FIKRqxm65oUK627ZJ3tSarNXE0tWlPU7EgNXeyr/KpOyy527l4YD1EAADs="""

def id33data() -> str:
    return """R0lGODlhNAAyAKEAAAAAAP///////////yH+Dk1hZGUgd2l0aCBHSU1QACH5BAEKAAEALAAA
AAA0ADIAAAL+jI+pywffolSgvXunXtjhn20iSJaVaJlZiQYf8xox0m0kDHkhvWs3ldNxej4Q
8CRM1FpGZVD2hCJbrmXyKp1Sq8Nnz8rddnXImVR8/DWx6CqLRW6TT6tczYz+Rt10om/MxieI
grcDZsJUaGelQviTtYY4IgkZ0wGGoxLUVLe41xVixhiJaUN0Oro2GYWqpbmq5eY0pekHOIs7
52nLE3vWW2lYCpyGu6T3mUsMjKycwrq3MuuaPB0oWyx2HG07bFrmhZfVFgq9XeE9ccctrJoI
nknrDpMt4Tefhi6Ok19Uu//MF6h/j/h9i0DQoJx4rxbCIthwIcRaDntN5CVxYkUHdRE3+sNY
AAA7"""

def id34data() -> str:
    return """R0lGODlhbQAyAKEAAAAAAP///////////yH+AjM0ACH5BAEKAAEALAAAAABtADIAAAL+jI95
wOoPo5y02sDy3bz7mmnfiDXk6YQiuqnsW7qwJU/AHKk3TtWPz1uEgqAhRLcjxkzK3OqHbAJ5
TyHzqJMatddlbzoD43xbZ5l6DpKr0HTYPS7DE2JY3S7vYtlxfj9p4Jci+HJXWEVIl4hSZ2jz
NKe4eOKGpHcxFPU1OWLpmcXxyemFJmoKWGSaeklz6mrZAUr6yCdr9Xpn29oViVAjKunpO6o2
iWurqdDbNHt7DDvMuiTNPP3ccBqqW+38ecvlWLyz3VxKrhQeSKwtskwJvYn6tuLO7r1KBFRv
dr+/b48q3R545fiJuySwTbKCA82xSjgInr91q+RFo9Ziy0RzjLEMQRyYZKPFTo7OZbwiEk89
kxUv7gr5kaWyjy5rxgNWcSRIitOCzbxWkubClz9hAh0ajKc6mT6TXmS6dKfOl+lqpeEIUGnS
oAj/eSD47l5RhVNZQD0pNhpIZl4xubLCryw3Rtncyp1LF+cuvHzN3j1RAAA7"""

def id35data() -> str:
    return """R0lGODlhMgAyAKEAAAAAAP///////////yH+Dk1hZGUgd2l0aCBHSU1QACH5BAEKAAEALAAA
AAAyADIAAALLjI+pa+DOopztWUtzgPX6r03fSAKhVILnSnbcCm+Yizzx8daznO+sz3sBgaFL
YjckapJCm84Jg+KgTNNNSusolMtcNhjkUqrWsCo2G01LN7P6C76mmuVp2/wsY+/H+ne/5SXH
YeSS0jaXWDim2Oj46GEImci3JhlZ2YX5A5gZOOc5uXnXuCZ20hIxSnpq6sfa2RcbRYTUimqL
uVhZaujptnqLO2v6G5YhXCScrCm4wIx8u8vbuson6gwLaQwsZU09O51JfMw9bE57UgAAOw=="""

def id36data() -> str:
    return """R0lGODlhaAAyAKEAAAAAAP///////////yH+AjM2ACH5BAEKAAEALAAAAABoADIAAAL+jI+p
y+2vgIS02oup3CD7D34cF5ZXZz4jmnqbM7bMKrsvssY1Tu7LFMkJdT5iwmgD8oZMnwEZGMKU
UWEwd4S2mNwGl7akXsXbr3Rmvh20614yDZ+q2/NnPXuHwPMiN53sN9aH9fcz+BNYRRYWwucH
drKYqMgyVrmzF3lpJ6k2N2myt+jVWWrFuakZhzqKVjkx2YXamGaJUWsZCGoBSWmr2iRI2hr6
ySanE8tHmarRzBqsKoz37JuRKJqEaDpMjIxLpz3N6Ord/aVnzrmdagx0rAIFehrffhdDuFvf
3LMqx54LDDxk5UQRA/eH0Kw3Yc5QW8bMYSGC1zLt84ZwYbeYN+jSQdTIitpFjm70QfMIkNw5
kq+QKOkFo5zKlQwfUpFFS+TIGhIl8lQ3sOLLmwp/AjV565GnoDU9quN1b+lTodUaypBXsioI
pAnLOOJKayqzFPBgXv1Y5WSJoGaLHaU36GnRtWgTgmUnFm7cpG2d3bUrdkbcur9YBvb6NyJd
n04eAtNaIWNja04PX4w2mTBlTGYme3bbqwAAOw=="""

def id37data() -> str:
    return """R0lGODlhZAAyAKEAAAAAAP///////////yH+AjM3ACH5BAEKAAEALAAAAABkADIAAAL+jI8Z
wOoPo5y0Koab3bx7l2XfSJZgCJjq+oXsC0tuTHtaJJ5ozS+pjgoKbz3W8IgUGn+x5G4yXOWW
s1JUVcViqEEu0zoFK73SMMn8eoqJOHUx4T5vH873BT2aG5zxdxZ712dHh1fzN0jI1iO491V0
aAh5oPdIuViIIEnmhzmpWabYNAZkCcMI+iN5itqZp9e3qrXVavM16lNKM0UrNzv3yQWXK6tx
xVnKyzFze+zoGep6czTYCUyRhdQMlZxIFDXMes0tzJZjDt4LTeosY7n7Or6Nvm4SZm9dEd+I
T0ruGCtPXcB4h9B0qTVvYMJnoQwyEyfQgjEIqoZNbBdxw7Q7fhTBZeu4UOJHhuxIttnoT1cd
WsDqZMoYLVvJQBmTICJ5EGROjPxu5rvoM+jLnkKbwSxKLSTSpEvtFAAAOw=="""

def id38data() -> str:
    return """R0lGODlhNgAyAKEAAAAAAP///////////yH+AjM4ACH5BAEKAAEALAAAAAA2ADIAAAL+jI+p
mwAMo2xOuTqzvhhxDS7c6JFhOKbld4Ipa6gt+gRmDM/tnXf6FXnlbD6XzCKsrYqWQ5JJxNyi
wOAzifOxXpIj9Up5ZqrLBzY8nZCdW295x+Sll3Alez1EQq014HQNMRfI9benZ9dFiGcoktcI
AwmY6Bh2mIV4Fyd4Zxn1mMfFIPlBdoX5JemJVgomKrQqVpZ6eGRquAlr8kp5efppisbH+BtK
J+w6fNmJXHQ2qMloW/y5TCx9nFklbXu8/aqTu60MLsudTV75xoxOQfusNIseP4Q7Mz9az57J
HK+PO63vnLB+4HhlS3Yin6yAX2gYdOhrEkI1BLHJi2hkQgEAOw=="""

def id39data() -> str:
    return """R0lGODlhMAAyAKEAAAAAAP///////////yH+AjM5ACH5BAEKAAEALAAAAAAwADIAAALWjI+Z
AOoP42JM2usoxRzr1oXQJ5ZZFX2oOamuO67PS9MxWL+pOuea8duRFLZA8HAkwpQyxMapAyZP
TeTTWMR6ri0fKDSF1ljSVc76JXOz2KUoTW1HyT02vbu88uhzL5zvF8bidUflJlcodyj2V7LH
1ZUY2YIoWYbjYxm4aDJ22TA0uDep2HhBAtmGZyqEAhnGeQPnOsooSIoW+3kbasu62jv1WlGb
+5haudt7ipxcenvTymhpaFZFbdOceKRbKFy83Tx3B62szfwLPC5xze5Hrb4Mn4tRAAA7"""

def id40data() -> str:
    return """R0lGODlhMAAyAKEAAAAAAP///////////yH+AjQwACH5BAEKAAEALAAAAAAwADIAAALsjI8A
yO0PnVqx2jrp3Tsro11eKI4ZZHpcqgbsW76fmyZtdI+2fvDoxLgFTz3ib1YEPowg5ZFEQzaY
TenUWoXuSNSrBDucabodU3hs5iTT1a3zKSO+s+BrjR79zp/JNW1JBojkFOi3Qji4d6YliHaH
o9gYxWJBCWdmZBUHyZYZ56PXl7VmWeZoOIpaifg4uXUoBqNaaEfJdMtKVerq9ynEZui72cYo
LLSDfHlMG8bJ+FqGEQm9+pzqbCpdRy0tyItd3cj8Dek8reptbn39U73NvWS6Pjmvdo6nlg+n
z19b328OoMBjAvONK3jkQgEAOw=="""

def id41data() -> str:
    return """R0lGODlhLwAyAKEAAAAAAP///////////yH+AjQxACH5BAEKAAEALAAAAAAvADIAAALwjI8B
m+0P4ZogWsMuolU33nmgCI7klFBKyYYXl7YZBp8ubX6qt84bGqnZHjsikFeM+ZTL15FpfA6j
IRkPV5HKckjWz3r9crG38AGsC5Z1XjN5uZVqtud2ciOO14W9dbzKt+Jw9yZHNvREyLZGlXSX
aNgIB1SyxzgY2NeG1dVU6Km46NlnkSk6+ugTahlalLOKxtRiiRmbN0ZYSVoLSznLWTvnqwvM
9rX4qSQxE+ia2UpHe4zMu7krjGq7Sm2syV0Ke0hTDB7JenupaXqOrmYtW52uPkouK0/8HV8e
uV2472fOnhOA9KoJ6xamnxsSAQoAADs="""

def id42data() -> str:
    return """R0lGODlhOgAyAKEAAAAAAP///////////yH+AjQyACH5BAEKAAEALAAAAAA6ADIAAALTjI+p
u+DAooxvpletblljvIXGF36dKJnQpq4o07qW+sItatbXXZP6SPsFQDoeS4ZwCIkeo7AUcz6b
0dwUWmVescqt9/s9gZdiRXdsKyet6AOb8wYHKfNwPe3zSlNxcv7456clEtjTh6NGWFiE9LJo
2Ih4Bnnn6Jg1OIZZJbjZV6m4OZQ5eggYtTPpZnp6NlgIGirzqsbKtaaaaXuLm9q4e+rba0bK
OKlVm2g826FbvIzr4qxMGb2aJeepvUe37W30Hb5d+j0l/miXE9M2kUfN3hBQAAA7"""

def id43data() -> str:
    return """R0lGODlhNgAyAKEAAAAAAP///////////yH+AjQzACH5BAEKAAEALAAAAAA2ADIAAAK6jI+p
wKAPo5StzYtvtbl7sznfqG3kSXHomlTse7jwK89rbZ91KOYpH/JFgEQh8Ri8IZMIHmvJjEV1
U5zUilK1tKCpsMtYmL7i8JZLBvfU5nSTO363Z3H20jaGFp/6PrUPuDYUOFIXCGQEdSaIhwhR
l4NVJuk2SVnJBob5uDO3GWB4+YUFmVYKKkp3edqItsjY6mkJS5NqR/snO+hFwrrrmwH8Kzyc
6+RB/HNU4lroZxl7J6erpPdWeVcAADs="""

def id44data() -> str:
    return """R0lGODlhNQAyAKEAAAAAAP///////////yH+AjQ0ACH5BAEKAAEALAAAAAA1ADIAAALyjI+p
ywHfonpQMlptxFkfDngXKH5kmZwi2KEOV7KtC3vyjNbW7U76xuotfiOVMIUZ8o4N4ivIBFJ8
yeiuipxaJVgqbmv6PsXgbpZsdSLM4HDI0GUXtdclnD435mVu7w3vFqTzR1jIFxhI6HNnuIb1
lyOINwgoBBj3WNl2Oam5hdmJdhTaIqf0Voc6pjqWKroaQqTWKHXoaAipYZuYC8ta+0vr97vH
mmR6+8r4c4wMa2NH56x2CkGSSUZ9ptqcMe28bAy1XMs1a4Ss/dwEShzODm7mpJfsnjxcOKdb
iZsO/dVPGTyAntq0KmJQ34aE7BgeKAAAOw=="""

def id45data() -> str:
    return """R0lGODlhLQAyAKEAAAAAAP///////////yH+AjQ1ACH5BAEKAAEALAAAAAAtADIAAAKxjI+p
CrAP42tN2ptoxZFe7XCTJpEiBHbeOa6LCYas+cYpG9CMrYt3xnOVghugDJcj1o5IItMgREKL
yeSGKkWFYtkTF4HtGis88c4ZxaHLM+dYHGw91bLeNNz9HezwtBUvxRfXpwPD58OGpedVZLM0
h6G4uAcZ+QhoJmfxFbiydqjyuaYlWmpKBSqHptk5eVbJAfuaGetH+3j7YZsLtst7J8ub+jss
7Et8bIz5a8U8lFUAADs="""

def id46data() -> str:
    return """R0lGODlhMAAyAKEAAAAAAP///////////yH+AjQ2ACH5BAEKAAEALAAAAAAwADIAAALBjI+p
Cr0Po2xU2ugWrbefrW2AR4ohR17imJiptWYf+GIxO6N1e5/4nltBaMDA7ecrGo8T3Uu4lCWV
DGJVSjW4plmElYfN7b5e1DHcdAbPWxWNDVc/4vTYvF4hX7V4uX7Yh1SGBsgUVEiIKMiX2Jbl
OJg49he1qAS51nWoqMlo6flZg5mpSQlaaloZmpKq2jUaudoBG/so5yMLc4t7ucsLRHslmZYL
Nowo2ipcvPx0bOPbaczcGSwdeT0bnc3IrU1SAAA7"""

def id47data() -> str:
    return """R0lGODlhLAAyAKEAAAAAAP///////////yH+AjQ3ACH5BAEKAAEALAAAAAAsADIAAALhjI+p
u+DAomSv1omN3fzl04WiE0DKiKZq93FlCprfe9FbU2e3TUY79rNMfsOcsOjRGXM+puTIAzqb
ySiyJ61CqVhN16udnsJEqHgMi5FlTxXCXEW7E/Avz6Vcg1GzuolFdCXDFBfYtsZGZ8g1GCe3
qKhHkYYjWTn3tmS3B7bn5Hf5h8WiNupoRRNZqJloU/qYacn5Khdr2vUptlrDCpt329iKKkhb
wthydKYqHFrKbPu8LHp6icyrrNiXjD3zOL0puCN+tkJZfk56hx6Epw5pvRvdDc1GPT/pKH8P
vd+fGlAAADs="""

def id48data() -> str:
    return """R0lGODlhLwAyAKEAAAAAAP///////////yH+AjQ4ACH5BAEKAAEALAAAAAAvADIAAAK3jI+p
CbAPY2xU2rtowxxr14XPJ0KVRJaZNrHqesLbK4NKSt8x87m5z+vtVEChMRcwKnu0pfLnHA5L
0dEMerTakAhgkKu7hsFjLflrlhHFQZAz5D1Es5e5HWe6C8NTg37P8ccm15dXFedXaIiXuNW2
Zrh4RujYpfiC2FiJlJnUubZJOdh0yYgVqokq8ul5Cedqijnaptrhmgp22zr7Wivqa6GLC2XL
WtfLO2kpfBarXPaMkhxN2FEAADs="""

def id49data() -> str:
    return """R0lGODlhLQAyAKEAAAAAAP///////////yH+AjQ5ACH5BAEKAAEALAAAAAAtADIAAAKvjI+p
Cb0P42tO2lMjzVdvuHHdEgLgN3rUhKbnSn6hy8B1OdMGzvem6+MFcJ2gaHgEBmM/HcbWQtic
LFGOWvVhJcut6iptem/i0lhhjBbF4XTya0SD10I1cpqa3+Xvix6vl4e39zSoZBW35WbmlXjG
V9b3yGcRePizKAmXadnG6Xa3GOr3mWQnyPjC5qRZuDrJ9ApLNst1WrtjiJvbCnu7+4sbXDtM
3Ot7PKm7u4NVAAA7"""

def id50data() -> str:
    return """R0lGODlhLwAyAKEAAAAAAP///////////yH+AjUwACH5BAEKAAEALAAAAAAvADIAAALgjI+p
CL0P42qUyvuq3g57w3XB9nlaZpVYBbHqKiruK6UjO9Nt6OT6xGHYfkDALkZMDJXIJc15WPpe
Npd0WuIZb9sodlI8eWPiy7Ura37TaC5KjYzkzr41G60tg6BvfJ6eRabH1WbHxnTEFCe3mCjU
GJZE+DEHBccXxqOYR/l3FxI4M0VCFDeKKXnaGKSiWqhlBrr5N7jHOQsa5GnbNvnYyyvLe7fZ
Z1FpCthSPNZbh0rcHC1tovzLDHM5PZzt7PQMeb3NTc24+m3dd+StbW7O/ho+AlM0LplWf08l
r4/yUAAAOw=="""

def id51data() -> str:
    return """R0lGODlhLwAyAKEAAAAAAP///////////yH+AjUxACH5BAEKAAEALAAAAAAvADIAAALajI+p
Cg0Lo0Su1omT3fzl34XeB4bkiV3ouqgsM06WJkpOKuYNdOl+Dfu5ZJvgrHUzJI3D42EZUDkp
HOruWYwms0pTF6qVLqdT65V2bYJxZ2J6nRmG22K4OzY/u8px/FcPJfdihfUmOIiUg5gotPiV
x+WIdtgm+edXZXkJGSk5o6j5RxFqY3dpSiL4syjUwbpa6LdS5zHGd6I2cpP5kmt2mwoWCIy7
ZktcYmzYiUJZGctye7gZ/FxINYkqGnHMZA3NvWvnFe3KA1qNzMkcrr7uHvvNyF6qTXqtWQAA
Ow=="""

def id52data() -> str:
    return """R0lGODlhMQAyAKEAAAAAAP///////////yH+AjUyACH5BAEKAAEALAAAAAAxADIAAALLjI+p
Br0P42q0Oomj3Tb7wIXcp4jUE5LlKLHqcX7pC8eZS4OVh9PdvcnVbAhiUMjYDZU6ptB0PCKb
poQUOUP9pluNE/vVEsFj8WVKBbS63HLxig6n2W1oFj3vJdX4u5lPRrciR7JDuHfIY+MmUgdI
9eb3UqbUGHcWqVc3oek4KHiJ2QEX+gjyaeq5lqjCuoT5BDuIKNvqhph5C1QLadW5mgpqKWME
SkvKuWj8+nvcnFvlG01sVzldWJ2dSq2dV2p3jIcLvC2OoWv+UAAAOw=="""

def id53data() -> str:
    return """R0lGODlhNAAyAKEAAAAAAP///////////yH+AjUzACH5BAEKAAEALAAAAAA0ADIAAAL+jI9p
wKAPo4StzYtvdbkvK22etzFUpZljySXi9JIxgsL1etNltI9B/uk9hD4Oa+Yi+oJKRXN5YIWA
UJ7q18JeqzbTDsTFHJEdqnMsLSrRLZS5C6zd5Ntkbn2dg6hju9cB9pW3x1a3x3SkFVX4pGLU
p9WG5mTDZBm5CFnmSJh2iSnzyKgzWJeSqUlKmpWSlWjlCia21Qkba2oL+3mHm3vSx8s6hcuI
JAuHOIlqt1ks/AnaCih0DB2NfG0WV60T+bx8JvyW3Gt9be5X7u03xL2qbtw7njxMWz6PWC/5
jR7Ov75AWhk4//yFYZeBTBh37RhCUeev4MFZECcKtFjFIcYEWRMKAAA7"""

def id54data() -> str:
    return """R0lGODlhZAAyAKEAAAAAAP///////////yH+AjU0ACH5BAEKAAEALAAAAABkADIAAAL+jI8B
m+0Po5y0moWt3rxHzHjiSD4g0GXlFq4KyJ6t+8GrPck6OUNyqbr0dLCf55RDiopGIe7QTD1N
Uw1zV4lytA1lLAgF+7hbL7Vnqb6GRPIX3RWnq/K2ealO5CnTPCoOVxaol4ElYWPIN/imaPdX
08YIJAfo+Di2h2B5icdm2UmI9nkjOnoUQhS66CTo8ERpNcp5lpiECrvG81rouYkbGgYbdAcJ
6OTo6gacWslsq3rs3Lwa7WZ62GK0K0ycHLlmd/oNDp2cpT08Lk5c9wtpuA1OHQcVbKwqrWm6
V2vLyRvI1yx5KtIFzIetFw5k+tqBQYQr3DmF/9Qd81HporeeKwPPAPPIqtwcawA1PmuIyZ7I
kdxuuaQWT17IXCtZDlxocNU2MwbvCRKzM1imgv16viD3E2evht0I8ssGMBMtcuyASpOYUqOy
qdU60hHoTiVSmRNnNDXJlGNYfUyFsvSWsCMmuW/FJtQ1j0ZNvVTa8q37d+7WwH4JC15LWKrh
foYzNn6XN7DixpMXI7b82F/mzXjpcv6cFbToOaNXFAAAOw=="""

def id55data() -> str:
    return """R0lGODlhKAAyAKEAAAAAAP///////////yH+AjU1ACH5BAEKAAEALAAAAAAoADIAAALSjI9p
wOoPHWtoxisnqBarnVFL5x3aRwZaeq3Jaa4idlK1zLa42uCz7tuwYCUfBxQjApU85MhVevKk
zV20askaY5EgVYZyJsHJ16/afELLR5fXDOsEezcxlj6vg+Jb7XqsdjczdEaUB4eYSMXGKEi2
CJk3dwQnCfZoaGnXhqTJZFLJafUwOiWaM1ZK+ul5FlL5eLVUiCq7umULO5l72Jar5hr4+xf6
K6xrDLib7KjKG0v8nBMtbUdtS/xprMS66ZGpGdW6fDpO3hwLoXouG6zNHFAAADs="""

def id56data() -> str:
    return """R0lGODlhOwAyAKEAAAAAAP///////////yH+AjU2ACH5BAEKAAEALAAAAAA7ADIAAAL+jI+p
a+AMo5zJWUCzfPNaDSIeFo1cqJkkY6KhCo3u27LX7Mr2h6NefFvwepWg4nfUERvD5OmgWi2N
w2DUOL0GrtGliAuWer/h7phsZj5ISiLYKd4ifeWnWtimvOVYrHqul/Yn1jRol1FTVHiYSBcH
BbhTVegGg9cXObMH6ZenuenZmEP1Y8mZSfNUt2L62dRVl7XoxyfYQ0tb64kTicrllenLgYEK
IkzJp4iMiFzcWbyx7Ey5W7JcC3Soq33JDZ27zX0Kqfz4l109ZwWuS3aa92yLxqq61yz/3j4P
I94Kt7sJHbtw/fD9E0fQ3BhoCc9ki1bNoTGGEpldq5jiIsYEjGcKAAA7"""

def id57data() -> str:
    return """R0lGODlhNQAyAKEAAAAAAP///////////yH+AjU3ACH5BAEKAAEALAAAAAA1ADIAAALYjI+Z
AOrcnJwSwmkv3TXH5WncGIplNlKnZYSBm3Ym2zKgGKc0tuc6/uj5OEIFavizyYDIWgS2Yjaj
H5d0Crt9mpuilkuSKr3gL4LmJcd2Ryd164tqqdiT8a0c2oN0cPZ+VfZSwpcnCOhReIhx0Na4
sjh31hfphqeGdLlX9jYZyLn5aFj56IZI2jU6qMoDCrf6isi6ptqjWTen6Zike8vTG+sJTOkH
bIpquftXmbhU+7lImIsMS7YseJ0bnLn726337Q2diik+Sz6uEq5eHpYues4dD4g8H1AAADs="""

def id58data() -> str:
    return """R0lGODlhMwAyAKEAAAAAAP///////////yH+AjU4ACH5BAEKAAEALAAAAAAzADIAAALEjI+p
Cb0PozzNzYtXrbnjzXniA1ojE04lcGqbCrZkPL+ySyv5re+UzaulfqagkIUAGo8o5DKiHAaK
T0MRWKpCVittk5ttxcBDrpgsJfo8Ztia/T46ZXEc9ZzeKm97fR4/B/UHGGhXyNOnlsj3grbI
6HhYZVY3GfaodTmYibVpmYL5tBNq5EM6k2HqqXcRlrRa43Y3BYsjEXdq6zdrxdvK62o3slhJ
6ysoFSwkElys1tFmfNwTWZ37ZY1Glw1Wyu1MqIxQAAA7"""

def id59data() -> str:
    return """R0lGODlhMwAyAKEAAAAAAP///////////yH+AjU5ACH5BAEKAAEALAAAAAAzADIAAALojI+p
C7APozytzYtftbnn7XgKWGGkmJCldKKjyoJU6Aatpsq1sUF5vrPRGL9bEFfUHYkrhHGZas6k
0CjHOqw6qTxupGfygsNPJjI7AbrGyvPYjC2m269k8uLd2odlU/0qhNaHl/UW+IdGhqUHGNj4
kSgF0/WoWDfVYgiJNEVpoUmY2EXJ6IiSJ2Sqp9oB6ln5WTkn6nkI54Fqq+n6ldu0N+kj6whs
d0ZcnCwLpjxstdr2RIcbHEoLOS2ci72NyeesDe4dJ8K7GCdeOgtbHXP9Gm5eLq92JO+dvt6a
vd+NGHTv2I58whYUAAA7"""

def id60data() -> str:
    return """R0lGODlhKAAyAKEAAAAAAP///////////yH+AjYwACH5BAEKAAEALAAAAAAoADIAAALTjI+p
B72fGoBRUijdzfMq3mGZt3DbSCIgZaqW+AaoMctrid42yIduPwPyPkINTegB4oy1Ry7GgDaJ
vtbRGMVWfNeqtuvUvGrcXzmsS6l33zXJ2nYve/JtVlnvDtOwMp+dNHSH1iGFNBgFxlYUNDZi
aKUXgkQGZealUxnXNBU5pYgoiXkGeIkXermVSXUWuYi5NEc1N8rq15bpKPhDOxmzy2vKBGl5
dVc4jOUqWmym2tvsHNH3+awG3Lf2R+hWLasdx513HT3+bR4Yji69fkLa7qJWAAA7"""

def id61data() -> str:
    return """R0lGODlhXgAyAKEAAAAAAP///////////yH+Dk1hZGUgd2l0aCBHSU1QACH5BAEKAAEALAAA
AABeADIAAAL+jI+py+2vgIS02ouR3Ln772wiyIzkeYgqmqgA+7kcrLk0Zrcvnd9PHzGhVr6G
7EckJYvI2QIYczKbk5IQdPVla1JuVdm9HXXhVDmzrWGhKcgX/DanLeMpZSSrd5bGsycPyHYx
Z5BXsUMWqEg4FOi2aNjH+AckKAeYGDKJxheg99TpJRkXJRipSZpp5UdnWbh5iQgqG5TKyeoJ
KzrKy0I7+3vH6hfKM4FL1RuLfKKLGpwLydxsq/McLf05dYZZm23XKivtnTMN/prNlmYulg4J
unq+rAjOHr5Ye+58SC+pb//IFZl/1cDgKOgL4DaEjRjKQ0cQ2sNddvZVVHjQoTwti3swavF4
b2KyeiCNaVxz8mJJYRJFYmuZEObCUypdeinWTqZKnDY3cuyZE0QBADs="""

def id62data() -> str:
    return """R0lGODlhcwAyAKEAAAAAAP///////////yH+AjYyACH5BAEKAAEALAAAAABzADIAAAL+jI+p
y+0PIwJU2lWv3jzQD3QWGIqmSaank5bry7YtjKn0Kduefh9z38llJjzgD5iQJYtLELL5eUJJ
UAjTSJX6csQh44p1artZg3ha1qbH2/MuI3Sr5ey2611SrqX7eizv1ock6FfjEkj3RFjYZEdW
uMjY5khZFyn5VokHmYjZpdk5GCrq1WgWpalR+nC5s3L0eXo3anVXi8qKu6GkgHsmNKKbK/xF
awg7KQsIHGFsZ9sAdgzmFMcc7awMje0shvjMhTa8yk1enP0IzvtHTGY+fSF93ot8ev6uvX2v
v49PDy2IyaJ65fj1i7fNm7VZtOT98/cQYixTCxm2c2cw4i6OdJsoIip1qdWzjRfvPZRVJd04
VRxT3bKl0AuxbBKnBOGQ5le4kXxavtKlc522OSUVAfXlT6QIpTDkFM3nMwZGRkIl7PwZx2hF
dARRZCW1tZtDnNd6XFVXlCnCqjfGlp2oVe1GlmczNpVLtSKbsZ7QhOVbri/Zv2zXCl5KGO+E
wzgSM36MFjDkvIUnT6ZVAAA7"""

def id63data() -> str:
    return """R0lGODlhZwAyAKEAAAAAAP///////////yH+AjYzACH5BAEKAAEALAAAAABnADIAAAL+jI+p
y+3PgJSw2ouzmxzoNn3iuHQUeXTo+pmsob5teHEybGfx7EI58sPkTg8TUWP0FJM9XTLCVIqM
uKiVJnwCr9JpjHutcVPaWwB7DlZR2mZabV5Kf2if2k2uxxWu4E7eVeX2t1dig4YHoqdCB1eY
cBiYqBj4doJF6HSkuaUHGEk05CjmCUURMmlnlac0SupqSZVpMWbJCrn5WRnLxMuDG3okmmro
2ehBc5qrCjwnDPYKlCf4hrOWJZmMCrZMuTVdHX5ZWtzFuFqISSXeCtvMPSsTvL4dpWp/3L2i
3lSvDeuOTzw249ohO4colR9d+rw4MyjoYK4yt1jtosjinym7ZXco+iHUS16wa+AsWuzRsQ6o
XSM0/ln2sY3KmBJZOmzVqVI+gTRzzuNo81c5dAE73eJnMKgmm7VsRVvoNJwdQBsaVqwQsplR
rEpdFS0a0dhMpSTfBR2VleHFRVap8STHixutSY7gXvV5Fh7YRPHsxtpYta1brmz1+e0Ld6/f
rXc36sRY8m00MVrvwQNBiWzOR46hLf3MOXMYbJorh1bLo7Tk06zTkADbOjZg2bRB1759D7fu
wLt7G8JQAAA7"""

def id64data() -> str:
    return """R0lGODlhZAAyAKEAAAAAAP///////////yH+AjY0ACH5BAEKAAEALAAAAABkADIAAAL+jI8Z
wKwPo5y02tTy3TwDDmKeE5bP+JndqLYH6l5s3M705N1KKmu6lPsZbEDfy0gLCmEUlFOnXM6c
1OfNR6wFq9Hjj8tLkoZRpPDIPRdTxkYM7FavSW0zKC23YMcL+z3ulxfhEIcWdlUoppIY+Mbn
mDjX99H1FTl5qFeJkLaJOEb1ZwdH6QlJKvpIRkfYWpqpRdo4yMgG6Dq5Glt1VgjqdvuK1iOr
qvY7hYtpvMO7DCvFw5QL11Q5LYeMOZxsao0dze0KjGS1gdfLKm1LXh5aETpbEjzULL1tmAWh
scdscrsqTCQz7yThO+iC3rIT6x5541RLoDxNbESo23LpHEGHhxNxZHxmpeO+Uar0EaP10dA8
ksbAwUs5UaRFZh/NfYOmi6FLjzB77oQ4q5jMhShxggxkMmAnkQ8R6iwI1F/HqSlnvkTnNCpF
o16Icc0HzqfXdP5m2rw5NtpXS2XtrU0lSOuKtluTqg0xtKhdS/+qzm0a9+rbunQDo4UC2LBB
xIUVryHr2HEBADs="""

### end of module
