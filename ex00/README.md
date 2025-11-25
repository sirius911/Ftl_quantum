# EXERCICE ex00 : LA SUPERPOSITION QUANTIQUE

## Sujet

Écrivez un programme qui produira un circuit quantique avec un seul qubit pour obtenir cet état: $\frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$ en utilisant le principe de superposition quantique.


## Théorie


l'etat : $|\psi\rangle =  \frac{1}{\sqrt{2}}(|0\rangle + |1\rangle)$ peut s'écrire

$$
|\psi\rangle =  \frac{1}{\sqrt{2}}|0\rangle + \frac{1}{\sqrt{2}}|1\rangle
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
|\psi\rangle = \alpha|0\rangle + \beta|1\rangle~~avec~~\alpha \in \mathbb{C}~~et~~\beta \in \mathbb{C}

</div>
<br><br>
</div>


Pour notre état $|\psi\rangle$, $\alpha = \beta = \frac{1}{\sqrt{2}}$

La norme de $|ψ\rangle$ noté $||\psi||$ est $|\alpha|^2 + |\beta|^2$ soit

$$||\psi|| = |{\frac{1}{\sqrt{2}}}| ^ 2 + |\frac{1}{\sqrt{2}}| ^ 2 = \frac{1}{2} + \frac{1}{2} = 1
$$

Comme $|\psi\rangle$ a une norme de 1, on peut *mesurer* l'état quantique à la sortie du circuit, avec une probabilité pour:
- **1** : de $|\alpha|^2$ soit $\frac{1}{2}$
- **2** : de $|\beta|^2$ soit $\frac{1}{2}$

## Solution

Pour avoir cet état, on va utiliser un circuit avec une *porte* de ***Hadamard***

```text
         ┌───┐    
q0 ──────┤ H ├───┤M├──>
         └───┘ 
```

Ce circuit applique la porte Hadamard sur un qubit initialement dans l'état \( |0\rangle \).

Nous aurons en sortie :
- **50%** de chance d'avoir **1** et
- **50%** de chance d'avoir **0**

