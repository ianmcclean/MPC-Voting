import unittest

import SuperTallier
import Tallier
import Voter
from ModularMath import evaluatePolynomial, nextPrime, reconstructConstant
from Tallier import tally


def assertShape(lis, shape, assertEquals):
    assertEquals(len(lis), shape[0])

    if len(shape) == 1:
        return

    for subLis in lis:
        assertShape(subLis, shape[1:], assertEquals)


class TestModularMath(unittest.TestCase):

    def testEvaluatePolynomial(self):
        self.assertEqual(evaluatePolynomial([2, 14, 17], 9, 31), 17)
        self.assertEqual(evaluatePolynomial([2, 10, 17], 0, 31), 2)
        self.assertEqual(evaluatePolynomial([2, 3, 19, 30], 21, 31), 20)
        self.assertEqual(evaluatePolynomial([1, 89, 300, 14, 7], 3, 107), 61)

    def testNextPrime(self):
        self.assertEqual(nextPrime(30), 31)
        self.assertEqual(nextPrime(3), 3)
        self.assertEqual(nextPrime(15), 17)

    def testReconstructConstant(self):
        primes = [107, 109, 113, 127]
        tests = [
            [1, 89, 300, 14, 7],
            [98, 35, 39, 100, 94],
            [7, 3, 2]
        ]

        for test in tests:
            for p in primes:
                degree = len(test) - 1
                pairs = [(d, evaluatePolynomial(test, d, p)) for d in range(1, degree + 2)]
                self.assertEqual(reconstructConstant(pairs, degree, p), test[0])


class TestTallier(unittest.TestCase):

    def testTally(self):
        vectors = [
            [1, 4, 7, 8],
            [3, 9, 1, 0],
            [8, 5, 6, 5]
        ]

        expected = [12, 18, 14, 13]
        self.assertEqual(tally(vectors), expected)


class IntegrationTest(unittest.TestCase):
    def test(self):
        # run multiple iterations since we use random numbers
        for testIterations in range(100):
            numCandidates = 10
            numTalliers = 8

            voteFile = open("testVotes.txt", 'r')
            votes = [
                int(line.strip()) for line in voteFile
            ]
            voteFile.close()

            numVoters = len(votes)

            p = nextPrime(numVoters)

            voterOutputs = [
                Voter.generateBallotShareVectors(numCandidates, vote, numTalliers, p) for vote in votes
            ]

            assertShape(voterOutputs, [numVoters, numTalliers, numCandidates], self.assertEqual)

            tallierInputs = [
                [
                    voterOutputs[voter][tallier] for voter in range(numVoters)
                ]
                for tallier in range(numTalliers)
            ]

            assertShape(tallierInputs, [numTalliers, numVoters, numCandidates], self.assertEqual)

            tallierOutputs = [
                Tallier.tally(tallierInput) for tallierInput in tallierInputs
            ]

            assertShape(tallierOutputs, [numTalliers, numCandidates], self.assertEqual)

            superTallierInputs = [
                (numTallier, tallierOutputs[numTallier]) for numTallier in range(numTalliers)
            ]

            totalVotes = SuperTallier.getTotalVotes(superTallierInputs, numCandidates, numTalliers, p)

            # find actual sum:
            actualVoteTotals = [
                len([
                    vote for vote in votes if vote == candidateNum
                ])
                for candidateNum in range(numCandidates)
            ]

            self.assertEqual(totalVotes, actualVoteTotals)


if __name__ == '__main__':
    unittest.main()
