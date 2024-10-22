# Introduction 
In this repository, we are going to test the security of the `Diffie-Hellman Key Exchange (DHKE)` against the efficient algorithms that exist today. before getting into the attacks against the `DHKE`, let us describe the premise of the cryptosystem and what do these attacks aim to compute. 
## DHKE 
the DHKE is a public-key cryptosystem that aims for the parties involved in the communication to compute a shared secret key. this shared secret key then could be used for symmetric-key cryptography.

we shall describe the two-party setup. suppose user1 has a private key `X_1` and public key `Y_1`. similarly, user2 has a private key `X_2` and public key `Y_2`. these keys hold a special relation, precisely the following

$$
Y_i = g^{X_i} \pmod{p}, \qquad \text{where } i = 0 \text { or } 1
$$

here, $g$ is a fixed primitive element of the multiplicative group $\mathbb{F}_p^{*}$ where $p$ is a prime known publically. to compute the shared secret key between user1 and user2, user1 computes 

$$
s_1 = Y_2^{X_1} = g^{X_1 X_2} \pmod{p}
$$

and the user2 computes

$$
s_2 = Y_1^{X_2} = g^{X_1 X_2} \pmod{p}
$$

and as one can observe, both the shared secrets computed are equivalent.
# Security of DHKE
the DHKE cryptosystem is broken if an attacker can solve the discrete-logarithm problem for the group $\mathbb{F}_p^{*}$, that is computing $X_i$ from $Y_i$ and $g$. we shall now investigate various algorithms in the literature that solve the discrete-logarithm problem and compare the time required on average for these algorithms to crack the keys. the implementations of the algorithms are provided in the repository for reference.

## 1. Shank's Big-step Small-step Algorithm (BSGS)
read: https://en.wikipedia.org/wiki/Baby-step_giant-step

[*] implementation done
[*] timing measurement tests written

## 2. Pohlig-Hellman's Algorithm
read: https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm

[*] implementation done
[*] timing measurement tests written 
