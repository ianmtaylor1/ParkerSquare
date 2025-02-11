# ParkerSquare
Searching for magic-squares-of-squares

## Background

This repository contains code to search for magic squares of squares. These squares were made popular recently by a series of Numberphile videos starting in [2016](https://www.youtube.com/watch?v=aOT_bG-vWyg) where one failed attempt was cristened the "Parker square". The topic was [revisted](https://www.youtube.com/watch?v=stpiBy6gWOA) in 2025 and a US \$10,000 bounty was placed on the first successful finding of such a square. (Note, however, that many mathematicians suspect these squares do not exist.)

Magic squares are $3 \times 3$ grids of positive integers,
```math
\begin{matrix}
x_{11} & x_{12} & x_{13} \\
x_{21} & x_{22} & x_{23} \\
x_{31} & x_{32} & x_{33}
\end{matrix}
```
where all integers are unique and the three rows, three columns, and two main diagonals have the same sum, $T$. Magic squares of squares have the additional property that each $x_{ij}$ is also a square, $x_{ij} = r_{ij}^2$ for $r_{ij} \in \mathbb{N}$.

## The search

### The main idea ($k$)

The search employed here revolves around the central value, $x_{22}$, and its square root, $r_{22}$. Consider all sums passing through $x_{22}$: the second row, second column, and both diagonals. Subtracting $x_{22}$ from each reveals a common constant we call $k$,

$$
k = x_{11} + x_{33} = x_{12} + x_{32} = x_{13} + x_{31} = x_{21} + x_{23}.
$$

We note several interesting and useful properties of $k$. 

First, directly from the above equation, $k$ must be expressable as the sum of two squares in at least four unique ways.

Second, $k = 2r_{22}^2$. Consider the relationship between $k$ and the common sum of the square, $T$. The first and third rows of the magic square, together, comprise exactly three copies of $k$ and exactly two copies of $T$. Therefore $T = 3k/2$. Now considering one sum containing $x_{22}$, we see

$$
T = x_{11} + x_{22} + x_{33} = x_{22} + k.
$$

Therefore $x_{22} = k/2$ and $k$ must also be twice a perfect square, specifically, $k = 2r_{22}^2$.

Third, with $r_{22}$, $k$, and all pairs of square numbers which sum to $k$, it is relatively easy to try all permutations and check for the desired magic square. All eight values on the permiter of the magic square are involved in a sum with its opposite to equal $k$.

### Details of the search algorithm

The algorithm has the following general steps:

For $r_{22} = 1,2,\dots$
1. Set $k = 2r_{22}^2$.
2. Determine if $k$ can be written as a sum of squares in at least 4 unique ways.
    - If not, continue to next $r_22$.
3. Find all $(a_i, b_i)$ with $0 < a_i < b_i$, with $a_i,b_i$ square, and $a_i + b_i = k$.
4. Try combinations of $(a_i, b_i)$ for the diagonal and second column sums to complete the top and bottom rows with common sum $T$.
    - If unsuccessful, continue to next $r_{22}$.
5. With a completed top and bottom row, and known $T$, fill in the middle row so each column sums to $T$ and check if the filled in values are perfect squares.
    - If unsuccessful, continue to next $r_{22}$.
    - If successful, you've won \$10,000.
  
#### Steps 2 and 3 - finding Quad Sums of Squares (QSS)

#### Steps 4 and 5 - filling in the magic square
