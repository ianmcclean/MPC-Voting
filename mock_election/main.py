import json
import os.path

import ResultsComputer
import Tallier
import Voter
from ModularMath import nextPrime

global numVoters, numCandidates, numTalliers, votes, voterOutputs, tallierOutputs


def main():
    global numVoters, numCandidates, numTalliers, votes, voterOutputs, tallierOutputs
    while True:
        paramsExist = os.path.exists('params.txt')
        votesExist = os.path.exists('votes.txt')
        voterOutputsExist = os.path.exists('voterOutputs.txt')
        tallierOutputsExist = os.path.exists('tallierOutputs.txt')

        # reload parameters
        if paramsExist:
            paramsFile = open('params.txt', 'r')
            [numVoters, numCandidates, numTalliers] = paramsFile.read().split(' ')
            [numVoters, numCandidates, numTalliers] = [int(numVoters), int(numCandidates), int(numTalliers)]
            paramsFile.close()

        if votesExist:
            # reload votes
            votesFile = open('votes.txt', 'r')
            votes = [int(vote) for vote in votesFile.read().split(' ') if vote != '']
            votesFile.close()

        if voterOutputsExist:
            # reload voter outputs
            voterOutputsFile = open('voterOutputs.txt', 'r')
            voterOutputs = json.loads(voterOutputsFile.read())
            voterOutputsFile.close()

        if tallierOutputsExist:
            # reload voter outputs
            tallierOutputsFile = open('tallierOutputs.txt', 'r')
            tallierOutputs = json.loads(tallierOutputsFile.read())
            tallierOutputsFile.close()

        print('\nOptions:')
        print('0. Exit')
        print('1. Create parameters.')
        print('2. Create votes')
        print('3. Compute vote-shares')
        print('4. Generate tallies')
        print('5. Compute election results')
        userInput = input('\n')

        if userInput == '0':
            return
        elif userInput == '1':
            createParameters()
        elif userInput == '2':
            if not paramsExist:
                print('Parameters have not been initialized yet.')
                continue
            generateVotes()
        elif userInput == '3':
            if (not paramsExist) or (not votesExist):
                print('Parameters or votes have not been initialized yet.')
                continue
            computeVoteShares()
        elif userInput == '4':
            if (not voterOutputsExist) or (not paramsExist):
                print('The voter outputs/shares or parameters have not been calculated yet.')
                continue
            generateTallies()
        elif userInput == '5':
            if (not tallierOutputsExist) or (not paramsExist):
                print('The tallier outputs or parameters have not been calculated yet.')
                continue
            computeElectionResults()
        else:
            print('Invalid input.')


def generateVotes():
    file = open('votes.txt', 'w')

    for i in range(numVoters):
        vote = input(f'Vote {i + 1}: ')
        if int(vote) < 0 or int(vote) >= numCandidates:
            print('Invalid vote.')
            file.close()
            os.remove('votes.txt')
            return
        file.write(vote + ' ')

    file.close()


def createParameters():
    global numVoters, numCandidates, numTalliers

    numVoters = input('How many voters: ')
    numCandidates = input('How many candidates: ')
    numTalliers = input('How many talliers: ')

    parameters = open('params.txt', 'w')
    parameters.write(f'{numVoters} {numCandidates} {numTalliers}')

    parameters.close()


def computeVoteShares():
    global voterOutputs

    p = nextPrime(numVoters)

    voterOutputs = [
        Voter.generateBallotShareVectors(numCandidates, vote, numTalliers, p) for vote in votes
    ]

    voterOutputsFile = open('voterOutputs.txt', 'w')
    voterOutputsFile.write(json.dumps(voterOutputs))
    voterOutputsFile.close()


def generateTallies():
    global tallierOutputs

    tallierInputs = [
        [
            voterOutputs[voter][tallier] for voter in range(numVoters)
        ]
        for tallier in range(numTalliers)
    ]

    tallierOutputs = [
        Tallier.tally(tallierInput) for tallierInput in tallierInputs
    ]

    tallierOutputsFile = open('tallierOutputs.txt', 'w')
    tallierOutputsFile.write(json.dumps(tallierOutputs))
    tallierOutputsFile.close()


def computeElectionResults():
    superTallierInputs = [
        (numTallier, tallierOutputs[numTallier]) for numTallier in range(numTalliers)
    ]

    p = nextPrime(numVoters)

    totalVotes = ResultsComputer.getTotalVotes(superTallierInputs, numCandidates, numTalliers, p)
    print(f'Election Results: {totalVotes}')


if __name__ == '__main__':
    main()
