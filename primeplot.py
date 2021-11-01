import numpy as np
import random
import os
from matplotlib import pyplot as plt

import argparse
parser = argparse.ArgumentParser(description='Plot density of primes.')
parser.add_argument('--output_path', '-o', default='./', help='where to store outputs')
parser.add_argument('--max_power', '-m', type=int, default=6)

def miller_rabin_prime_test(n, k=5):
    '''
    Uses miller-rabin randomized primality test to compute if n is prime.
    Will never have a false negative (if it says n is not prime, then it is not)
    Will have a false positive with probabilty at most 4^-k
    So with k=10, we have <1000 correct answers for every mistake.
    '''
    n = int(n)
    # 2 and 3 are prime
    if n == 2 or n == 3:
        return True

    if n == 1:
        return False

    #other even numbers are not prime
    if n % 2 == 0:
        return False

    # n-1 is even.
    # Compute highest power of two that divides n-1:
    # Write n-1 = s * 2^r for an odd number s.
    r = 0
    s = n - 1
    while s % 2 == 0:
        r += 1
        s //= 2


    for _ in range(k):
        # We try the following procedure k times.
        # Due to some beautiful number theory, if n is not prime it will
        # detect this with probability at least 1/2.

        # The central observation is that n is prime if and only if
        # the only square roots of 1 mod n are 1 and -1.
        # Further, if n is not prime, there are at least 4 square roots of 1.
        # So we will try to guess a square root of 1 that is not 1 or -1.

        a = int(random.randrange(2, n-1)) # choose random number mod n other than 1 or -1.
        x = pow(a, s, n) # raise to s^th power mod n.
        # By LaGrange theorem, we now have x^(2^r) = 1 mod n.
        # Thus, x^(2^k) is a square root of n for some k <= r

        if x == 1 or x == n - 1:
            continue # x is already -1 or 1, didn't find a new square root.

        # find smallest k such that x^(2^k) is a square root of n.
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
            if x == 1:
                # x wasn't 1 or -1, but when squared was 1!
                return False
        else:
            # at this point x should be a^(s * 2^(r-1)), which is a square root of 1, and is not -1 or 1.
            return False
    return True


def estimate_probability(n, num_samples):
    '''
    estimates probability that a randomly selected number x < n will be a prime.

    args:
        n: range of random numbers to test primality
        num_samples: number of samples used to compute the estimate
    '''
    tests = np.random.randint(1, n, num_samples)

    prime_test = [miller_rabin_prime_test(p) for p in tests]

    average = np.mean(prime_test)

    return average

def plot_primes(max_power, path):
    '''
    plots probably of a randomly selected number <n being prime.
    will test n = 100, 1000, ..., 10^(1+maxpower)
    output will be saved in path/probfig.png
    '''
    n = 100
    probabilities = []
    n_values = []
    for r in range(max_power):
        print(' computing with n: {}'.format(n))
        probabilities.append(estimate_probability(n,n))
        n_values.append(n)
        n *= 10
    plt.plot(n_values, probabilities)
    plt.title("probability of a random x<n being prime")
    plt.xlabel("n")
    plt.ylabel("prob")
    plt.savefig(os.path.join(path, "probfig.png"))


def plot_primes_log(max_power, path):
    '''
    plots probably of a randomly selected number <n being prime.
    will test n = 100, 1000, ..., 10^(1+maxpower)
    output will be saved in path/probfig.png as log plot on x axis
    '''
    n = 100
    probabilities = []
    n_values = []
    for r in range(max_power):
        print(' computing with n: {}'.format(n))
        probabilities.append(estimate_probability(n,n))
        n_values.append(n)
        n *= 10
    plt.plot(n_values, probabilities)
    plt.title("probability of a random x<n being prime")
    plt.xlabel("n")
    plt.ylabel("prob")
    plt.xscale('log')
    plt.savefig(os.path.join(path, "probfig.png"))



def plot_primes_log_confidence(max_power, path):
    '''
    plots probably of a randomly selected number <n being prime.
    will test n = 100, 1000, ..., 10^(1+maxpower)
    output will be saved in path/probfig.png
    also computes confidence intervals and saves as a log plot.
    '''
    n = 100
    probabilities = []
    n_values = []
    for r in range(max_power):
        print(' computing with n: {}'.format(n))
        probabilities.append(estimate_probability(n,2*n))
        n_values.append(n)
        n *= 10
    probabilities = np.array(probabilities)
    n_values = np.array(n_values)
    confidence_interval = np.sqrt((probabilities - probabilities**2)*np.log(max_power/0.025)/n_values) + 7.0*np.log(max_power/0.025)/(3.0 * (2*n_values-1.0))

    # subtract 1.0/1024.0 from the lower confidnece bound due to bias in primality test.
    plt.plot(n_values, 1.0/(np.maximum(1e-100,probabilities-confidence_interval-1.0/1024.0)), '--',color='red')
    plt.plot(n_values, 1.0/(np.minimum(1.0, probabilities+confidence_interval)), '--', color='red')
    plt.plot(n_values, 1.0/probabilities, color='blue')
    plt.title("(inverse) probability of a random x<n being prime")
    plt.xlabel("n")
    plt.ylabel("1.0/prob")
    plt.xscale('log')
    plt.savefig(os.path.join(path, "probfig.png"))
    print(probabilities)


if __name__ == '__main__':
    args = parser.parse_args()
    plot_primes_log_confidence(args.max_power, args.output_path)
