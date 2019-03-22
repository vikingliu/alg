# coding=utf-8
# 使用文本注解绘制树形图
import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


# 上面三行代码定义文本框和箭头格式
# 定义决策树决策结果的属性，用字典来定义，也可写作 decisionNode={boxstyle:'sawtooth',fc:'0.8'}
# 其中boxstyle表示文本框类型，sawtooth是波浪型的，fc指的是注释框颜色的深度
# arrowstyle表示箭头的样式

def plotNode(nodeTxt, centerPt, parentPt, nodeType):  # 该函数执行了实际的绘图功能
    # nodeTxt指要显示的文本，centerPt指的是文本中心点，parentPt指向文本中心的点
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


# 获取叶节点的数目
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]  # 字典的第一个键，也就是树的第一个节点
    secondDict = myTree[firstStr]  # 这个键所对应的值，即该节点的所有子树。
    for key in secondDict.keys():
        if type(secondDict[key]) == dict:  # 测试节点的数据类型是否为字典
            numLeafs += getNumLeafs(secondDict[key])  # 递归,如果是字典的话，继续遍历
        else:
            numLeafs += 1  # 如果不是字典型的话，说明是叶节点，则叶节点的数目加1
    return numLeafs


# 获取树的层数
def getTreeDepth(myTree):  # 和上面的函数结果几乎一致
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])  # 递归
        else:
            thisDepth = 1  # 一旦到达叶子节点将从递归调用中返回，并将计算深度加1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth


# 可视化
def plotMidText(cntrPt, parentPt, txtString):  # 计算父节点和子节点的中间位置，并在父子节点间填充文本信息
    # cntrPt文本中心点   parentPt 指向文本中心的点
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)


def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)  # 调用getNumLeafs（）函数计算叶子节点数目（宽度）
    depth = getTreeDepth(myTree)  # 调用getTreeDepth（），计算树的层数（深度）
    firstStr = myTree.keys()[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)  # plotTree.totalW表示树的深度
    plotMidText(cntrPt, parentPt, nodeTxt)  # 调用 plotMidText（）函数，填充信息nodeTxt
    plotNode(firstStr, cntrPt, parentPt, decisionNode)  # 调用plotNode（）函数，绘制带箭头的注解
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    # 因从上往下画，所以需要依次递减y的坐标值，plotTree.totalD表示存储树的深度
    for key in secondDict.keys():
        nodeTxt = '%s' % key
        if type(secondDict[key]) is dict:
            plotTree(secondDict[key], cntrPt, nodeTxt)  # 递归
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, nodeTxt)
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD  # h绘制完所有子节点后，增加全局变量Y的偏移。


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')  # 绘图区域为白色
    fig.clf()  # 清空绘图区
    axprops = dict(xticks=[], yticks=[])  # 定义横纵坐标轴
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    # 由全局变量createPlot.ax1定义一个绘图区，111表示一行一列的第一个，frameon表示边框,**axprops不显示刻度
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()


class Node:
    def __init__(self, val, feature=None, children=None, sample=None, gt=None):
        self.val = val
        self.feature = feature
        self.children = children
        self.sample = sample
        self.gt = gt

    def dump(self):
        if not self.children:
            return self.val
        rst = {self.val: {}}
        for key, child in self.children.items():
            rst[self.val][key] = child.dump()
        return rst

    def show(self, inTree=None):
        if not inTree:
            inTree = self.dump()
        createPlot(inTree)
