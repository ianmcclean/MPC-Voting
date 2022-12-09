import random
from math import floor

from ModularMath import evaluatePolynomial

sysRandom = random.SystemRandom()


# Generates a ballot share vector for each tallier
# The returned vector is a numTallier length vector, representing the shareVector to send to each tallier
# Each shareVector is a vector of length numCandidates
def generateBallotShareVectors(numCandidates, candidateToVoteFor, numTalliers, p):
    polynomialDegree = floor((numTalliers + 1) / 2) - 1

    randomPolynomials = [
        [1 if candidateToVoteFor == candidate else 0] +
        [
            sysRandom.randint(0, p - 1) for degree in range(1, polynomialDegree + 1)
        ]
        for candidate in range(numCandidates)
    ]

    return [
        [
            evaluatePolynomial(randomPolynomials[candidate], tallierNum + 1, p)
            for candidate in range(numCandidates)
        ]
        for tallierNum in range(numTalliers)
    ]
