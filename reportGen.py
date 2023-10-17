import inspect
import os

class GraphNode():
    def __init__(self, input:object):

        rawName = str(type(input))
        name = rawName.replace("<class '", "").replace("'>", "")
        self.name = name
        self.children = []

    def addChild(self, child): #child should also be GraphNode
        self.children.append(child)

    def print(self, indent=0):
        for child in self.children:
            print("  " * indent +  f"{self.name} --> {child.name}")
            child.print(indent=indent+1)



def isRobotCode(filepath):
    if(filepath is not None):
        robotRoot = os.path.abspath(os.path.dirname(__file__))
        if(robotRoot in os.path.abspath(filepath)):
            return True
        else:
            return False

def iterateRecursive(parent, object):
    for objName in object.__dict__:
        member = object.__dict__[objName]

        try:
            sourceFile = inspect.getfile(type(member))
        except TypeError:
            sourceFile = None # skiperooski

        shouldIterate = hasattr(member, "__dict__") and hasattr(member, "__class__") and isRobotCode(sourceFile)
        if(shouldIterate):
            newNode = GraphNode(member)
            parent.addChild(newNode)
            iterateRecursive(newNode, member)


def generate(topLevelObject):

    classStructureRoot = GraphNode(topLevelObject)

    iterateRecursive(classStructureRoot, topLevelObject)

    classStructureRoot.print()

    return



