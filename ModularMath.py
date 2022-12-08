# Reconstructs the constant of a polynomial using the computationally efficient method outlined in:
# https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing#Reconstruction
def reconstructConstant(pairs, polynomialDegree, p):
    if len(pairs) != polynomialDegree + 1:
        raise ValueError("Degree must be one less than number of input/output pairs")

    sum = 0
    for j in range(len(pairs)):
        yj = pairs[j][1]

        prod = 1
        for m in range(len(pairs)):
            if m == j:
                continue

            xm = pairs[m][0]
            xj = pairs[j][0]

            # Add p to the diff, since python does not correctly compute the modulus of negative numbers
            diff = xm - xj + p
            prod *= (xm * pow(diff, -1, p)) % p

        sum += (yj * prod) % p

    return sum % p


def evaluatePolynomial(coefficients, x, p):
    sum = coefficients[0]
    for i in range(1, len(coefficients)):
        sum += (coefficients[i] * pow(x, i, p)) % p

    return sum % p


# Find the prime number that is greater than or equal to N
def nextPrime(N):
    def isPrime(n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    while not isPrime(N):
        N += 1
    return N
