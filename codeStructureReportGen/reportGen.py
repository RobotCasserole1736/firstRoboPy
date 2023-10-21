import inspect
import os

class GraphNode():
    def __init__(self, rootNode:object):

        rawName = str(type(rootNode))
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
        robotRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return (robotRoot in os.path.abspath(filepath))
    else:
        return False

def shouldIterate(member):
    try:
        sourceFile = inspect.getfile(type(member))
    except TypeError:
        sourceFile = None # skiperooski

    return hasattr(member, "__dict__") and hasattr(member, "__class__") and isRobotCode(sourceFile)

def iterateRecursive(parent, inputObj):
    for objName in inputObj.__dict__:
        member = inputObj.__dict__[objName]

        if(isinstance(member, list)):
            for memberItem in member:
                newNode = GraphNode(memberItem)
                parent.addChild(newNode)
                iterateRecursive(newNode, memberItem)
        elif(isinstance(member, dict)):
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
    for node in nodeDict:
        codeLine = f"    {{ id: \"{node}\", color: \"red\"}},\n"
        nodeJs += codeLine

    # build up edges
    edgeSet = set(classStructureRoot.getEdgeList())
    edgeJs = ""
    for edge in edgeSet:
        codeLine = f"    {{ source: \"{edge[0]}\", target: \"{edge[1]}\" }},\n"
        edgeJs += codeLine

    with open("./codeStructureReportGen/graphTemplate.html", "r", encoding="utf-8") as tmpltf:
        with open("docs/graphOfClasses.html", "w", encoding="utf-8") as outf:
            for line in tmpltf:
                line = line.replace("$[[NODES]]", nodeJs)
                line = line.replace("$[[EDGES]]", edgeJs)
                outf.write(line)
