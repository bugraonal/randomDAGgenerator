import random
import math
import graphviz


diag = graphviz.Digraph()
nodeID = 0


class Node:
    """
    Graph node. Holds the function name, ID, callees. Also used to generate the
    graphviz dot.

    Parameters
    ----------
    name :
        name
    level :
        level
    """

    def __init__(self, name, level):
        global nodeID
        self.name = name
        self.level = level
        self.callees = []
        self.program = 0
        self.vars = (0, 0, 0)
        self.ID = str(nodeID)
        nodeID += 1
        diag.node(self.ID, self.name)

    def calls(self, other):
        """
        Add a function call

        Parameters
        ----------
        other : Node
            The callee node
        """
        global diag
        self.callees.append(other)
        diag.edge(self.ID, other.ID)


class DAGgen:

    def __init__(self, numNodes=15, numLevels=6, saturationFraction=2/3):
        self.numNodes = numNodes
        self.numLevels = numLevels
        self.saturationFraction = saturationFraction

    def generate(self):
        dist = self.distrubute(self.numNodes, self.numLevels, self.saturationFraction)
        print(dist)
        levels = self.firstPass(self.numNodes, self.numLevels, dist)
        self.secondPass(levels)
        diag.render('graph.gv', view=True)

    def distrubute(self, numNodes, numLevels, saturationFraction):
        """
        This function will distrubute the nodes to the levels.
        A partial function is used for distrubution. The function
        parts include a linear part and a constant part.

        Parameters
        ----------
        numNodes : int
            Number of total nodes
        numLevels : int
            Number of levels
        saturationFraction : int
            The fraction of the total number of nodes where the linear
            function will end and constant function will begin
        """
        N = numNodes - 1
        L = numLevels - 1
        f = saturationFraction
        coA = -f**2 * L**2 / 2 + f * L**2 - f * L
        coB = L - 1
        a = 3/2
        b = (N - coA * a) / coB

        dist = [1]
        for i in range(1, math.ceil(L * f)):
            dist.append(round(a * i + b))
        for i in range(math.ceil(L * f), L+1):
            dist.append(round(a * f * L + b))

        subProb = 0.05
        sub = 0
        numPasses = 1
        for _ in range(numPasses):
            for d in dist[1:]:
                r = random.random()
                if r < subProb:
                    if d > 1:
                        d -= 1
                        sub += 1
        for _ in range(sub):
            ind = random.randrange(1, L+1)
            dist[ind] += 1
        return dist

    def randPDF(self, pdf):
        choices = []
        for index, value in enumerate(pdf):
            choices.extend(index for _ in range(value))
        return random.choice(choices)

    def firstPass(self, numNodes, numLevels, dist):
        """
        The first pass while generating the graph. The nodes will be placed on
        the levels and will be connected to a single node from the previous level.
        The connections are random, and it is ensured that each function will have
        at least one callee (Leaf nodes not included).

        Parameters
        ----------
        numNodes : int
            Total number of nodes
        numLevels : int
            Number of levels
        dist : list(int)
            The distrubution list
        """
        levels = [[] for _ in range(numLevels)]
        levels[0].append(Node('main', 0))

        nameNum = 1

        for i, d in enumerate(dist[1:], start=1):
            # free = [f for f in range(len(levels[i-1]))]
            pdf = [d for _ in range(len(levels[i-1]))]
            for _ in range(d):
                node = Node('f' + str(nameNum), i)
                levels[i].append(node)
                nameNum += 1
                # if len(free) > 0:
                #     callerInd = random.choice(free)
                #     free.remove(callerInd)
                # else:
                #     callerInd = random.randrange(len(levels[i-1]))
                callerInd = self.randPDF(pdf)
                pdf[callerInd] -= 1
                caller = levels[i - 1][callerInd]
                caller.calls(node)
        return levels

    def secondPass(self, levels):
        """
        The second pass of the graph where the nodes will be randomly
        connected to nodes on lower levels.

        Parameters
        ----------
        levels : list(Node)
            The levels containing the function Nodes
        """
        initProb = 0.7
        prob = initProb
        decr = 0.7 / self.numLevels
        for i, l in enumerate(levels[:-1]):
            for n in l:
                prob = initProb
                while True:
                    roll = random.random()
                    if roll < prob:
                        randLevel = random.choice(levels[i+1:])
                        randNode = random.choice(randLevel)
                        if randNode not in n.callees:
                            n.calls(randNode)
                        prob -= decr
                    else:
                        break
            initProb -= decr

