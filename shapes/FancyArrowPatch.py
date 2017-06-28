import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

"""
Curve	-
CurveB	->
BracketB	-[
CurveFilledB	-|>
CurveA	<-
CurveAB	<->
CurveFilledA	<|-	
CurveFilledAB	<|-|>
BracketA	]-
BracketAB	]-[
Fancy	fancy
Simple	simple
Wedge	wedge
BarAB	|-|
"""

class FancyArrowPatch:
    def __init__(self, posA=None, posB=None, path=None, arrowstyle='simple', connectionstyle='bar', props={}, figure=None):
        self.posA = posA
        self.posB = posB
        self.path = path
        self.arrowstyle = arrowstyle
        self.connectionstyle = connectionstyle
        self.props = props
        self.figure = figure

        fancyArrow = patches.FancyArrowPatch(posA, posB, path, arrowstyle, connectionstyle, **self.props)
        self.matplotlib_obj = fancyArrow

    def __draw__(self, zorder=1):
        p = self.figure.ax.add_patch(self.matplotlib_obj)
        p.set(zorder=zorder)
