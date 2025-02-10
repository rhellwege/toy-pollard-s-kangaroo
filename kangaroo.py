import math
import random
r = math.ceil(random.random() * 1000)

# pseudorandom deterministic function should be uniform
# cannot return 0
def rand(n, upper):
    return (hash(n + r) % (upper-1)) + 1

# find x such that alpha ^ x = beta modulo n where x is in range a, b
def kangaroo(alpha, beta, n, a, b):
    # these parameters can change
    trapSteps = math.floor(math.sqrt((b-a)/2)) # heuristic tame trap steps
    upperStep = math.floor(math.sqrt((b-a)/2))   # the output of the random number generator for steps
    # tame
    xTame = pow(alpha, b, n)     # trap
    dTame = 0                    # distance traveled (sum of steps)
    for i in range(0,trapSteps):
        step = rand(xTame, upperStep) # random step
        xTame = (xTame * pow(alpha, step, n)) % n
        dTame += step
    # wild
    yWild = beta # start at beta so we can write alpha in terms of beta and solve for x
    dWild = 0 # distance traveled
    i = 0
    while dWild <= b - a + dTame: # heuristic stopping point so it doesn't run forever
        step = rand(yWild, upperStep) # random step
        yWild = (yWild * pow(alpha, step, n)) % n
        dWild += step
        if yWild == xTame: # wild kangaroo trapped
            print(f"wild took {i} steps.")
            print(dTame, dWild)
            ans = (b + dTame - dWild) % n
            # ad hoc fix for off by one error
            if pow(alpha, ans, n) == beta:
                return ans
            else:
                return ans + 1
        i += 1
    raise Exception("failed to reach trap.")

if __name__ == "__main__":
    g = 3
    n = 4567
    secret = 4000
    beta = pow(g, secret, n)
    print("beta = ", beta)
    try:
        print(kangaroo(g, beta, n, 0, n))
    except:
        print("failed.")
