# Exercice ex01 :  L'INTRICATION QUANTIQUE (ÉTAT DE BELL)

## Sujet : 
Écrivez un programme qui produira un circuit quantique avec deux qubits afin d'obtenir cet état $\frac{1}{\sqrt{2}}(|0.0\rangle + |1.1\rangle)$ en utilisant le principe de superposition et d'intrication quantique.

## Analyse:
L'état quantique $|\psi\rangle$ appelé **2-qubit** est la réunion de 2 qubit  et est défini par la superposition : 
$$
|\psi\rangle = \alpha|0.0\rangle + \beta|0.1\rangle + \gamma|1.0\rangle + \delta|1.1\rangle~~~~(1)
$$
avec $\alpha,\beta,\gamma,\delta \in \mathbb{C}$

$|\psi\rangle$ à par convention une **norme** égale à **1** donc : 

$$
|\alpha|^2 + |\beta|^2 + |\gamma|^2 + |\delta|^2 = 1
$$

La mesure d'un 2-qubit, donne 2 bits classique:
- [0.0] avec une probabilité $|\alpha|^2$.
- [0.1] avec une probabilité $|\beta|^2$.
- [1.0] avec une probabilité $|\gamma|^2$.
- [1.1] avec une probabilité $|\delta|^2$.

Pour l'état demandé dans le sujet, on a:

$|\psi\rangle = \frac{1}{\sqrt{2}}(|0.0\rangle + |1.1\rangle) <=> \frac{1}{\sqrt{2}}|0.0\rangle + \frac{1}{\sqrt{2}}|1.1\rangle$

qui peut s'écrire : 

$$
|\psi\rangle = \frac{1}{\sqrt{2}}|0.0\rangle + 0|0.1\rangle + 0|1.0\rangle + \frac{1}{\sqrt{2}}|1.1\rangle
$$

Donc $|\psi\rangle$ s'écrit bien comme $(1)$ avec $\alpha = \frac{1}{\sqrt{2}}$, $\beta = 0$, $\gamma = 0$ et $\delta = \frac{1}{\sqrt{2}}$

La mesure de ce 2-qubit donne:
- [0.0] avec une probabilité $|\alpha|^2 = |\frac{1}{\sqrt{2}}|^2 = \frac{1}{2}$.
- [0.1] avec une probabilité $|\beta|^2$ = 0.
- [1.0] avec une probabilité $|\gamma|^2$ = 0.
- [1.1] avec une probabilité $|\delta|^2| = |\frac{1}{\sqrt{2}}|^2 = \frac{1}{2}$.

On a aucune chance d'avoir [0.1] ou [1.0] et une chance sur 2 d'avoir [0.0] ou [1.1]

### Analogie des 2 pièces de Monnaie:

En lançant 2 pièces de monnaie qui ont soit **P**ile, soit **F**ace, tant qu'elles sont en l'air on a 4 états possibles à l'arrivée.([**F**,**F**], [**F**,**P**], [**P**,**F**], [**P**,**P**])? Les 4 états ont la même chance de se produire, et c'est biensur que lorsque les pièces sont tombées (Mesure), que l'on a l'état définitf. Mais avec *l'intrication quantique* les deux pièces peuvent être *liée* fortement entre elles et tomber dans le même état. Si l'une est côté **P**ile, l'autre aussi.

Cela revient à obtenir un ***etat de Bell*** pour un 2-quBit, et que l'on note $|\Phi^+\rangle$

Pour obtenir **l'état de Bell**, on a besoin de la porte ***CNOT***

## Porte *CNOT*

La porte *CNOT* est une porte qui a en entrée et en sortie e2 qubits:

```text
     q0 ───●────
           │
     q1 ───⊕────
```

Le principe de cette porte est de changer le second qubit en fonction de l'état du premier:


```text
 |0> ───●──> |0>   |0> ───●──> |0>   |1> ───●──> |1>   |1> ───●──> |1> 
        │                 │                 │                 │       
 |0> ───⊕──> |0>   |1> ───⊕──> |1>   |0> ───⊕──> |1>   |1> ───⊕──> |0> 
```
On notera :
- Le premier qubit ne change jamais
- Si le premier qubit est $|0\rangle$, le second ne varie pas.
- Si le premier qubit est $|1\rangle$, alors le second qubit change par une porte **X** : $|0\rangle \to |1\rangle$ et $|1\rangle \to |0\rangle$ 

## Solution

Pour l'obtention de *l'état de Bell* nous devons utiliser le circuit suivant:

```text
         ┌───┐    
q0 ──────┤ H ├─────●────────
         └───┘     │
q1 ────────────────⊕────────
```

Reprenons le calcul en détails (notation verticale) à partir de l’entrée :

$$
|0.0\rangle = \begin{matrix}|0\rangle\\ \otimes \\ |0\rangle\end{matrix}
$$


Tout d’abord le premier qubit (celui du haut) passe par une porte \(H\),  
le second qubit reste inchangé :


$$
\begin{array}{ccc}
|0\rangle & \xrightarrow{H} & H(|0\rangle) \\
\otimes    &                 & \otimes      \\
|0\rangle &                 & |0\rangle
\end{array}
$$

ce qui donne :

$$
\begin{array}{ccc}
\frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle \\
\otimes\\
|0\rangle
\end{array} = \frac{1}{\sqrt{2}}\begin{array}{cc} |0\rangle \\ \otimes \\|0\rangle\end{array} + \frac{1}{\sqrt{2}} \begin{array}{cc}|1\rangle \\ \otimes \\|0\rangle \end{array}
$$

---

Ensuite ce résultat intermédiaire passe par la porte CNOT.  
On regarde d’abord indépendamment chaque terme :

- **Premier terme** :

$$
\begin{array}{c}|0\rangle \\ \otimes \\|0\rangle \end{array}
\;\xrightarrow{\text{CNOT}}\;
\begin{array}{c}|0⟩ \\ \otimes \\ |0⟩ \end{array}
$$

- **Second terme** :

$$
\begin{array}{c} |1⟩ \\ \otimes \\|0⟩ \end{array}
\;\xrightarrow{\text{CNOT}}\;
\begin{array}{c} |1⟩ \\ \otimes \\|1⟩ \end{array}
$$

---

Ainsi par linéarité :

$$
\begin{array}{ccc}
H(|0\rangle) \\
\otimes      \\
|0\rangle
\end{array}\;\xrightarrow{\text{CNOT}} \frac{1}{\sqrt{2}} \begin{array}{c}|0\rangle\\ \otimes \\ |0\rangle \end{array} + \frac{1}{\sqrt{2}}\begin{array}{c} |1\rangle \\ \otimes \\ |1\rangle\end{array}
 = \frac{1}{\sqrt{2}}\big(|0.0⟩ + |1.1⟩\big)
$$

qui est bien l'état de *Bell* $|\Phi\rangle ^+$.

