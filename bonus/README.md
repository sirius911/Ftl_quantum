---
pdf-engine: xelatex
monofont: "DejaVu Sans Mono"
geometry: "top=1.5cm,bottom=1.5cm,left=2cm,right=2cm"
---
# Algorithme de Shor

### Objectif :

Factoriser un grand nombre $M$.
(Nous suivront la démonstration avec un exemple concret : $15$)

La **factorisation** consiste à trouver les facteurs premiers $p$ et $q$ d'un nombre composé $M$ tel que $M=p\cdot q$.

L'algorithme réalise ceci en convertissant la factorisation en un problème de **Recherche de Période** d'une fonction exponentielle spécifique.

**A. Partie Classique (L'Enrobage)**

Cette partie utilise la théorie des nombres pour transformer le problème $M=p\cdot q$ en un problème de période.

1. **Choisir un nombre aléatoire** $a$ tel que $1<a<M$.

2. **Calculer le $PGCD$ (Plus Grand Commun Diviseur)** entre $a$ et $M$.

- Si $PGCD~(a,M) \neq 1$, alors nous avons trouvé un facteur ! (C'est rare, mais possible.)

3. **Trouver la période** $r$ (le plus petit entier positif) de la fonction périodique :
$$
f(x)=a^x~mod~M
$$

C'est-à-dire, trouver le plus petit $r$ tel que $a^r \equiv 1 ~(mod~M)$.

4. **Calculer les facteurs.** Une fois $r$ trouvé (et si $r$ est pair et $a^{r/2} \not\equiv −1~(mod~M)$), les facteurs de $M$ sont donnés par :
$$
PGCD ~ (a^{r/2} \pm 1,~M)
$$

**B. Partie Quantique (Le Cœur Accélérateur)**

La seule étape qui requiert un ordinateur quantique: **Trouver la période** $r$ de la fonction $f(x)=a^x~mod~M$.

Nous allons nous concentrer sur la partie que vous pouvez implémenter avec Qiskit, la Recherche de Période Quantique (QPF).

Par exemple, factoriser $15$ revient à trouver $3$ et $5$.

**Pourquoi cet algorithme est révolutionnaire ?**

La sécurité de la cryptographie actuelle (comme **RSA**) repose sur le fait que la factorisation des très grands nombres est extrêmement difficile et longue pour les ordinateurs classiques (complexité *quasi-exponentielle*). L'algorithme de Shor, grâce à la mécanique quantique, peut réaliser cette factorisation en temps **polynomial**, rendant la cryptographie RSA obsolète à l'arrivée d'un ordinateur quantique à grande échelle.

L'algorithme est hybride : il utilise de la théorie des nombres classique et une sous-routine quantique appelée **Recherche de Période (QPF)**.

## 1. Détermination des Tailles de Registres ($n_c, n_d$):

Dans l'algorithme de *Shor*, le circuit est divisé en deux sections principales, chacune nécessitant un certain nombre de qubits, et la taille totale du circuit est la somme de ces deux tailles :

$$
Taille ~ totale ~ du ~ circuit ~ (en ~ qubits)=n_c​+n_d​
$$
**1. Registre de Compteur ($n_c$​)**

* **Taille** : $n_c​$ qubits.

* **Rôle** : Ce registre sert de compteur. Il est mis en superposition et passe par la Transformée de Fourier Quantique (QFT). Il est essentiel pour trouver la période $r$.

* **Fonction dans le Circuit** : Il contient les entrées $x$ de la fonction $f(x)= a^x ~ mod ~ M$.

**2. Registre de Données ($n_d$​)**

* **Taille** : $n_d$​ qubits.

* **Rôle** : Ce registre sert à stocker le résultat de l'exponentiation modulaire $a^x ~ mod ~ M$.

* **Fonction dans le Circuit** : Il contient la valeur $f(x)$ et doit être suffisamment grand pour contenir toutes les valeurs possibles de $0$ à $M−1$.


La taille des registres dépend du nombre $M$ que vous souhaitez factoriser.

**3. Calculs pour l'Exemple $M=15$**

1. **Taille du Registre de Données ($n_d$​) :**

$$
n_d​=⌈log_2 ​(15)⌉ = ⌈3.906\dots⌉ = 4 ~ qubits
$$
(Car $2^3=8$ n'est pas assez, $2^4=16$ est suffisant).

2. **Taille du Registre de Compteur ($n_c$​) :**
La règle standard pour la QFT est $n_c \geq 2n_d$​.

$$n_c ​\geq 2 \times 4 = 8 ~ qubits$$

---

## 2. Partie Classique (L'Enrobage)

La partie classique est exécutée par le code Python standard. Elle sert à **transformer le problème de factorisation en un problème périodique** que le quantique peut résoudre.

1. Choisir la base $a$: On sélectionne un nombre aléatoire a tel que $1 < a < M$ et $PGCD(a,M)=1$.

2. Trouver la Période $r$ : La partie quantique (QPF) trouvera la période r de la fonction f(x)=axmodM.

3. Calculer les Facteurs : Une fois $r$ trouvée, on revient au classique pour calculer les facteurs de $M$ grâce à la propriété mathématique : $PGCD(a^{r/2} \pm 1,M)$.

[Pour notre exemple : $M=15$ et $a=7$.
Notre objectif quantique est de trouver $r$ tel que $7^r \equiv 1(mod15)$]

---

## 3. Partie Quantique : Recherche de période (QPF)


### Pourquoi l’oracle n’est codé que pour (M = 15) ?

Dans la version complète de l’algorithme de Shor, l’**oracle** doit implémenter l’opération :

$$
[
\lvert x \rangle \lvert y \rangle \longmapsto \lvert x \rangle \lvert y \cdot a^x \bmod M \rangle
]
$$

pour un **M quelconque**.
En pratique, cela demande :

* de construire des circuits quantiques d’**arithmétique modulaire** (addition, multiplication, exponentiation mod (M)),
* avec beaucoup de qubits auxiliaires et un **nombre de portes très important**,
* ce qui devient vite lourd, difficile à lire, et presque inutilisable sur un simulateur.

Pour garder le projet **pédagogique et manipulable**, j’ai fait un choix :

* **Ne coder un oracle “réel” que pour le cas (M = 15)** (et (a = 2) dans les exemples),
* et garder un **oracle abstrait** (symbolique) pour les autres valeurs, qui sert uniquement à montrer la structure du circuit.

Ainsi :

* on a **un vrai exemple quantique complet** (superposition + oracle concret + IQFT + mesure) pour (M = 15),
* tout en évitant la complexité technique d’une implémentation générale, qui n’apporterait pas grand-chose de plus au niveau compréhension pour un premier contact avec l’algorithme de Shor.


La partie quantique utilise deux registres et se déroule en trois étapes :

#### a. Étape 1 : Initialisation des États

Nous créons une superposition uniforme sur le Registre de Compteur et initialisons le Registre de Données à $∣1\rangle$.

1. **Registre de compteur : ($n_c$ qubits):**
- **Action** : Application de la porte de **Hadamard ($\mathbf{H}$)** sur chaque qubit.
- **Résultat** : Le registre entre dans une superposition uniforme, représentant toutes les entrées x possibles :
$$
\sum _{x=0} ^{2^{n_c} - 1}~|x\rangle
$$

2. **Registre de Données ($n_d$​ qubits) :**
- **Action**:Application de la porte $\mathbf{X}$ **(NOT)** sur le qubit le moins significatif (LSB) de ce registre.
- **Résultat**: Le registre est initialisé à l'état de base $∣1\rangle$.

#### b. Étape 2 : L'Oracle d'Exponentiation Modulaire Contrôlée ($U_f$​):

C'est l'étape qui requiert l'accélération quantique.
L'Oracle implémente la fonction périodique $f(x)=a^x ~mod~M$.

- **Opération** : L'Oracle effectue l'opération contrôlée suivante :
$$
U_f​∣x\rangle∣y\rangle \rightarrow ∣x\rangle∣(y \cdot a^x)~mod ~ M\rangle
$$

- **Effet** : Comme le Registre de Données ($∣y\rangle$) est initialisé à $∣1\rangle$, le résultat est :
$∣x\rangle∣a^xmod~M\rangle$.
Le registre de compteur $∣x\rangle$ contrôle l'exponentiation.

- **Implémentation** : Cette opération est extrêmement complexe. Elle requiert des circuits quantiques pour l'addition et la multiplication modulaires, souvent en utilisant un **Registre Auxiliaire** ($n_a$​) pour les calculs intermédiaires. Dans notre implémentation, nous utilisons le bloc ModularExponentiation de Qiskit, qui encapsule tous les milliers de portes élémentaires nécessaires.

- **sPour notre exemple** ($M=15,~a=7$): Le circuit quantique réalise la transformation : $\sum_ x ​∣x\rangle∣1\rangle \rightarrow \sum_x​∣x\rangle∣7^x ~ mod ~ 15\rangle$.

*Exemple des premiers états*:
$$
\begin{array}{l}
∣0\rangle ∣1\rangle \rightarrow~∣0\rangle∣7^0~mod~15\rangle=∣0\rangle∣1\rangle\\
∣1\rangle ∣1\rangle \rightarrow~∣1\rangle ~|~7^1~mod~15⟩=∣1\rangle∣7\rangle\\
∣2\rangle ∣1\rangle \rightarrow~∣2\rangle~|~7^2~mod~15⟩=∣2\rangle∣4\rangle\\
\end{array}
$$

#### c. La Simulation Quantique (L'Oracle Concret et l'étape simulée)

L'Oracle (la boîte $U_{a}^x \pmod M$) est un circuit gigantesque qui effectue l'exponentiation modulaire en superposition.

**L'Oracle n'est pas abstrait :**

-   Dans notre code, la primitive Qiskit `ModularExponentiation` **n'est pas une abstraction théorique** (comme une "boîte noire"), mais une **implémentation concrète** des milliers de portes (Toffoli, CNOT) nécessaires à l'arithmétique modulaire quantique.
-   Elle est affichée comme une seule boîte dans la représentation textuelle pour la lisibilité, mais un appel à `qiskit.transpile` (comme dans `main.py`) la décomposerait en un circuit de plusieurs milliers d'opérations élémentaires. 

**La simulation de l'étape de mesure :**

-   Étant donné la complexité de simuler l'intégralité de ce circuit sur de petits simulateurs locaux, notre code remplace la phase de *mesure quantique* par une valeur prédéterminée, $m$.
    -   **Théorie :** La valeur mesurée $m$ doit être très proche de $\frac{s}{r} \cdot 2^{n_c}$.
    -   **Pratique :** Nous calculons classiquement la vraie période $r$, puis nous déduisons l'état idéal $m$ qui serait le plus probable à être mesuré (le pic de probabilité). Cela nous permet de garantir le succès de la phase classique finale (Fractions Continues) et de valider l'architecture de l'algorithme.

**

#### d. Étape 3 : Transformée de Fourier Quantique Inverse (IQFT)

- **Opération** : L'IQFT est appliquée au **Registre de Compteur** ($n_c$​).
- **Rôle** : Elle transforme la périodicité encodée dans les phases des états quantiques en un pic de probabilité mesurable, permettant de déterminer la fraction $\frac{s}{r}$.

#### e. Étape 4 : Mesure

- **Opération** : Mesure du registre de compteur $n_c$​.
- **Résultat** : Une valeur classique $m$ est obtenue.

---

## D. Phase Classique (Post-Traitement)

Cette phase utilise le résultat de la mesure quantique, $m$, pour déterminer la période $r$ et, finalement, les facteurs de $M$.

**1. Algorithme des Fractions Continues :**

-   La mesure $m$ nous donne une approximation : $\frac{m}{2^{n_c}} \approx \frac{s}{r}$.
-   Nous appliquons l'algorithme des **Fractions Continues** sur $\frac{m}{2^{n_c}}$ pour trouver la meilleure approximation irréductible $\frac{s}{r}$. Le dénominateur $r$ est notre **candidat pour la période**.

**2. Vérification et Calcul des Facteurs :**

-   **Vérification :** On confirme que $a^r \equiv 1 \pmod{M}$.
-   **Calcul des Facteurs :** Si la période $r$ est valide, on obtient les facteurs de $M$ par $PGCD(a^{r/2} \pm 1, M)$.

---

## E. Conclusion : L'Avantage Quantique - La course contre RSA

L'impact de l'Algorithme de Shor se résume à une question de **Complexité**.

| Caractéristique | Algorithme Classique (Factorisation par Crible) | Algorithme Quantique (Shor) |
| :--- | :--- | :--- |
| **Complexité (temps)** | **Quasi-Exponentielle** $O(e^{(L^{1/3})})$ | **Polynomiale** $O(L^3)$ |
| **Croissance** | **Explosive** (impossible à maîtriser) | **Contrôlée** (prévisible, linéaire-cubique) |
| **Durée (Exemple $L=2048$ bits)** | Des milliards d'années | Quelques heures/jours |

Où $L$ est la taille du nombre $M$ en bits.

**Code *Classique* VS *quantique* :**

1.  **Le Classique (Attaque RSA Actuelle) :** Pour chaque bit que vous ajoutez au nombre $M$ (pour le rendre plus sûr), le temps nécessaire à la factorisation **double**. C'est une croissance exponentielle. 

[Image of Exponential vs Polynomial Growth]


2.  **Le Quantique (Shor) :** Pour chaque bit que vous ajoutez, le temps nécessaire **augmente juste un peu** (de manière cubique, $L^3$). C'est une croissance contrôlée, ce qui rend la factorisation réalisable sur un grand nombre.

**Le Secret : La QFT**

Le Quantique ne factorise pas plus vite ; il a simplement transformé le problème le plus difficile (la factorisation) en un problème plus simple (la recherche de période) grâce à la **Transformée de Fourier Quantique (QFT)**. Cette opération quantique exploite :

-   La **superposition** pour tester *tous* les exposants $x$ de la fonction $a^x \pmod M$ simultanément.
-   L'**interférence** pour faire ressortir la période $r$ (l'information utile) sous forme de pics de probabilité mesurables.

**Conséquence :** L'Algorithme de Shor est la menace la plus grave pour la cryptographie actuelle, car il annule l'hypothèse de base de RSA : que la factorisation est *difficile*.

---

### Pour le Bonus j'ai codé un veritable circuit quantique fonctionnant pour $M=15$:

Intuition de ce qui est vraiment quantique dans ce projet

Dans ce projet, la partie vraiment « quantique » est la recherche de période (QPF : Quantum Period Finding).
L’idée clé : on exploite un registre en superposition pour évaluer une fonction sur tous les inputs à la fois, puis on utilise des interférences pour faire ressortir l’information sur la période.

1. **Superposition du registre compteur**

On utilise ici 
$n_c=8$ qubits pour le registre « compteur ».
Après les portes Hadamard, ce registre est dans l’état :

$$
\frac{1}{\sqrt{2^{n_c}}} \sum_{x=0} ^{2^{n_c}-1}|x\rangle
$$

Concrètement :

il est en même temps dans tous les états de 0 à 255 (les 256 valeurs possibles sur 8 bits).

Le registre de données est initialisé à $∣1\rangle$

2. **Oracle : calcul de $a^x~mod ~M$ sur tous les états à la fois**

Pour $M=15$ et $a=2$, l’oracle applique :

$$
∣x \rangle∣1\rangle \rightarrow ∣x\rangle∣2^x~mod~15\rangle
$$

Grâce à la superposition, ce n’est **pas** fait pour un seul $x$, mais pour **tous les** $x$ en **parallèle** :

$$
\frac{1}{\sqrt{2^{n_c}}} \sum_{x=0} ^{2^{n_c}-1}|x\rangle|1\rangle ~ \xrightarrow{\text{oracle}}~ \frac{1}{\sqrt{2^{n_c}}} \sum_{x=0} ^{2^{n_c}-1}|x\rangle|2^x ~mod~15\rangle
$$

Pour $M=15, a=2$,  la fonction $2^x ~ mod ~ 15$ est **périodique** avec une période $r=4$.

Cette périodicité est maintenant « encodée » dans l’état quantique complet.

3. **IQFT + mesure : faire ressortir la période**

On applique ensuite la **QFT inverse (IQFT)** sur le registre compteur uniquement.
La QFT inverse transforme la structure périodique en une **distribution de probabilités avec des pics** aux positions :

$$
m \approx k \cdot \frac{2^{n_c}}{r}
$$

Dans notre exemple :

- $2^{n_c} = 256$

- $r = 4$

- On obtient des pics pour $m \approx 0,64,128,192$

C’est exactement ce que montrent les résultats de mesure du registre compteur, où les bitstrings :

- $00000000 ~ (0)$

- $01000000 ~ (64)$

- $10000000 ~ (128)$

- $11000000 ~ (192)$

apparaissent avec des probabilités élevées.

À partir de la valeur mesurée $m$, la partie **classique** (fractions continues + PGCD) reconstruit la période $r=4$, puis les facteurs $3$ et $5$ de $15$.

En résumé :

- La **superposition** permet de traiter **tous les** $x$ en même temps.

- L’**oracle** encode la **périodicité** de $a^x mod~ M$ dans l’état quantique.

- L’**IQFT** transforme cette périodicité en **pics de probabilité** mesurables.

- La factorisation finale reste un **post-traitement classique**.