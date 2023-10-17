import inspect
import os

class GraphNode():
    def __init__(self, input:object):

        rawName = str(type(input))
        name = rawName.replace("<class '", "").replace("'>", "")
        if('.' in name):
            name = name.rsplit('.', 1)[1]
        self.name = name
        self.children = []

    def addChild(self, child): #child should also be GraphNode
        self.children.append(child)

    def print(self, indent=0):
        for child in self.children:
            print("  " * indent +  f"{self.name} --> {child.name}")
            child.print(indent=indent+1)
            
    def getEdgeList(self):
        retList = []
        for child in self.children:
            retList.append((self.name, child.name))
            retList.extend(child.getEdgeList())
        return retList
    
    def buildDepthDict(self, dictIn, depth=0):
        if(self.name in dictIn.keys()):
            dictIn[self.name] = max(depth, dictIn[self.name])
        else:
            dictIn[self.name] = depth

        for child in self.children:
            child.buildDepthDict(dictIn, depth+1)
        



def isRobotCode(filepath):
    if(filepath is not None):
        robotRoot = os.path.abspath(os.path.dirname(__file__))
        if(robotRoot in os.path.abspath(filepath)):
            return True
        else:
            return False
        
def shouldIterate(member):
    try:
        sourceFile = inspect.getfile(type(member))
    except TypeError:
        sourceFile = None # skiperooski

    return hasattr(member, "__dict__") and hasattr(member, "__class__") and isRobotCode(sourceFile)

def iterateRecursive(parent, object):
    for objName in object.__dict__:
        member = object.__dict__[objName]

        if(type(member) is list):
            for memberItem in member:
                newNode = GraphNode(memberItem)
                parent.addChild(newNode)
                iterateRecursive(newNode, memberItem)
        elif(type(member) is dict):
            for memberItem in member.items():
                newNode = GraphNode(memberItem)
                parent.addChild(newNode)
                iterateRecursive(newNode, memberItem)
        else:
            if(shouldIterate(member)):
                newNode = GraphNode(member)
                parent.addChild(newNode)
                iterateRecursive(newNode, member)


def generate(topLevelObject):

    classStructureRoot = GraphNode(topLevelObject)

    iterateRecursive(classStructureRoot, topLevelObject)

    # build up nodes and what depth they should be drawn at
    nodeDict = {}
    classStructureRoot.buildDepthDict(nodeDict)
    nodeJs = ""
    for node in nodeDict.keys():
        level = nodeDict[node]
        codeLine = f"    {{ id: \"{node}\", color: \"red\"}},\n"
        nodeJs += codeLine

    
    # build up edges
    edgeSet = set(classStructureRoot.getEdgeList())
    edgeJs = ""
    for edge in edgeSet:
        codeLine = f"    {{ source: \"{edge[0]}\", target: \"{edge[1]}\" }},\n"
        edgeJs += codeLine

    with open("graphTemplate.html", "r", encoding="utf-8") as tmplt_file:
        with open("graphOfCLasses.html", "w", encoding="utf-8") as outf:
            for line in tmplt_file:
                line = line.replace("$[[NODES]]", nodeJs)
                line = line.replace("$[[EDGES]]", edgeJs)
                outf.write(line)



