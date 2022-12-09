import random
from math import floor

from ModularMath import reconstructConstant


def getTotalVotes(tallyVectorPairs, numCandidates, numTalliers, p):
    # the tally vectors are secrets to the total weigh vector

    numSubsetNeeded = floor((numTalliers + 1) / 2)  # D'
    polynomialDegree = numSubsetNeeded - 1

    voteTotals = [0] * numCandidates
    # loop through all candidates
    for candidate in range(numCandidates):
        pairs = [
            (tallierNum + 1, tally[candidate]) for (tallierNum, tally) in tallyVectorPairs
        ]

        # we only need D'=numSubsetNeeded of the pairs
        pairs = random.sample(pairs, numSubsetNeeded)

        voteTotals[candidate] = reconstructConstant(pairs, polynomialDegree, p)

    return voteTotals
