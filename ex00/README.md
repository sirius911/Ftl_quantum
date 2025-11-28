---
pdf-engine: xelatex
monofont: "DejaVu Sans Mono"
geometry: "top=1.5cm,bottom=1.5cm,left=2cm,right=2cm"
---

# EXERCICE ex00 : LA SUPERPOSITION QUANTIQUE

## Sujet

Écrivez un programme qui produira un circuit quantique avec un seul qubit pour obtenir cet état: $\frac{1}{\sqrt{2}}(\lvert0\rangle + \lvert1\rangle)$ en utilisant le principe de superposition quantique.


## Théorie


l'etat : $\lvert\psi\rangle =  \frac{1}{\sqrt{2}}(\lvert0\rangle + \lvert1\rangle)$ peut s'écrire

$$
\lvert\psi\rangle =  \frac{1}{\sqrt{2}}\lvert0\rangle + \frac{1}{\sqrt{2}}\lvert1\rangle
$$

ou encore :

<div style="text-align:center;">
<div style="
    display: inline-block;
    border: 1px solid #aaa;
    padding: 10px;
    border-radius: 8px;
">

$$
\lvert\psi\rangle = \alpha\lvert0\rangle + \beta\lvert1\rangle~~avec~~\alpha \in \mathbb{C}~~et~~\beta \in \mathbb{C}
$$
</div>
<br><br>
</div>


Pour notre état $\lvert\psi\rangle$, $\alpha = \beta = \frac{1}{\sqrt{2}}$

La norme de $\lvert\psi\rangle$ noté $\lvert\lvert\psi\lvert\lvert$ est $\lvert\alpha\lvert^2 + \lvert\beta\lvert^2$ soit

$$\lvert\lvert\psi\lvert\lvert = \lvert{\frac{1}{\sqrt{2}}}\lvert ^ 2 + \lvert\frac{1}{\sqrt{2}}\lvert ^ 2 = \frac{1}{2} + \frac{1}{2} = 1
$$

Comme $\lvert\psi\rangle$ a une norme de 1, on peut *mesurer* l'état quantique à la sortie du circuit, avec une probabilité pour:

- **0** : de $\lvert\alpha\lvert^2$ soit $\frac{1}{2}$

- **1** : de $\lvert\beta\lvert^2$ soit $\frac{1}{2}$

## Solution

Pour avoir cet état, on va utiliser un circuit avec une *porte* de ***Hadamard***

```text
         ┌───┐    
q0 ──────┤ H ├───┤M├──>
         └───┘ 
```

Ce circuit applique la ***porte Hadamard*** sur un qubit initialement dans l'état $\lvert0\rangle$.

Nous aurons en sortie :

- **50%** de chance d'avoir **1** et

- **50%** de chance d'avoir **0**

