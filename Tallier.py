def tally(shareVectors):
    return [
        sum([
            shareVector[i] for shareVector in shareVectors
        ])
        for i in range(len(shareVectors[0]))
    ]
