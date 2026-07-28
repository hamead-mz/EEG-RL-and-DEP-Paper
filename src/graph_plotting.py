import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp
from src.multiple_tests import correct_pvalues

class Color_def:

    Edge = 'k'
    Marker_Face = 'g'
    Marker_Edge = 'r'

class FigConstants:

    StaticGraph = {

        'figsize': (5, 5),
        'edgesize': 10,
        'labelsize': 6,
        'ArrowHeadWidth': 0.1,
        'ArrowBodyWidth': 0.02,
        'ArrowHeadLength': 0.1

    }

def PrepBinaryNetwork(WeMat):

    UnVals = np.sort(np.unique(WeMat))

    for UV_i, UnVal in enumerate(UnVals):

        WeMat[np.where(WeMat == UnVal)] == int(UV_i)

    return WeMat

def isDirected(WeMat):

    for time_i in range(WeMat.shape[2]):

        tWeMat = WeMat[:, :, time_i]

        if not np.all(tWeMat == tWeMat.T):

            return True

    return False

def isWeighted(WeMat):

    if not len(np.unique(WeMat)) == 2:

        return True

    else:

        return False

def NetBasixByWeMat(WeMat):

    assert WeMat.shape[0] == WeMat.shape[1], "Weights must be square Matrix!"

    Static = True

    if WeMat.ndim == 3:

        if WeMat.shape[2] > 1:

            Static = False

    else:

        WeMat = np.reshape(WeMat, WeMat.shape + (1, ))

    Directed = isDirected(WeMat)
    Weighted = isWeighted(WeMat)

    if not Weighted:

        WeMat = PrepBinaryNetwork(WeMat)

    return WeMat, Static, Directed, Weighted
    
class network_graph:

    # WeMat (Weight Matrix) must be NxNxTimeWindow (N: number of nodes)

    def __init__(self, w_mat):

        self.weights, self.Static, self.Directed, self.Weighted = NetBasixByWeMat(w_mat)

    def SetCoords(self, coords = None): # it must be possible to define other forms of node coordinations

        if np.any(coords == None):

            coords = np.random.uniform(low = -1, high = 1, size = (self.weights.shape[1], 2))
        
        assert len(coords) == self.weights.shape[1], 'Coordinations must be available for each Node'

        self.coords = np.array(coords)

    def SetTimes(self, times):

        assert self.weights.shape[2] == len(times), 'time vector must has same length as number of temporal evolving matrices'

        self.t_ = times

    def SetLabels(self, labels):

        assert self.weights.shape[1] == len(labels), "Label numbers must be equal to number of nodes"

        self.labels = labels

    def DrawStaticGraph(self, VisThresh: int, window = 0, ax = None, show_labels = False, xlims = [-1, 1], ylims = [-1, 1], DirectionBias = 0.5, Colors = Color_def, FigConstants = FigConstants):

        # ISSUES: 
        # - isn't better way to plot DIRECTED graphs? (:|)

        # Draws a time sample,
        # win_number -> number of intended window
        # VisThresh -> Threshold to Consider Edge (it is useful to increase the sparsity of graph)

        if ax == None:

            fig, ax = plt.subplots(1, 1, layout = 'constrained', figsize = FigConstants.StaticGraph['figsize'], dpi = 200)

        x = self.coords[:, 0]
        y = self.coords[:, 1]

        assert type(window) in [int, list, np.ndarray], "Invalid Window Type"

        PlotMatW8s = self.weights[:, :, window]

        if not self.Directed:

            for i in range(len(x)):

                for j in range(i + 1, len(x)):

                    color_num = PlotMatW8s[i, j]

                    if color_num < 0:

                        color_num = 0

                    elif color_num > 1:

                        color_num = 1

                    if color_num > VisThresh:

                        ax.plot([x[i], x[j]], [y[i], y[j]], alpha = color_num, color = Colors.Edge)

        else:

            for i in range(len(x)):

                for j in range(len(x)):

                    if i != j:

                        color_num = PlotMatW8s[i, j]

                        if color_num < 0:

                            color_num = 0

                        elif color_num > 1:

                            color_num = 1

                        if color_num > VisThresh:

                            bias = DirectionBias * FigConstants.StaticGraph['ArrowHeadWidth']

                            if x[j] == x[i]:

                                if y[j] > y[i]:

                                    delta = np.pi / 2

                                else:

                                    delta = -1 * np.pi / 2

                            else:

                                delta = np.arctan((y[j] - y[i]) / (x[j] - x[i]))

                            cos = np.cos(delta) * np.sign(j - i)
                            sin = np.sin(delta)

                            cbias = bias * cos
                            sbias = bias * -1 * sin

                            ax.arrow(x[i] + sbias, y[i] + cbias, (x[j] - x[i]) / 2, (y[j] - y[i]) / 2, alpha = color_num, color = Colors.Edge,
                            head_width = FigConstants.StaticGraph['ArrowHeadWidth'], width = FigConstants.StaticGraph['ArrowBodyWidth'],
                            length_includes_head = False,
                            head_length = FigConstants.StaticGraph['ArrowHeadLength'])
                            ax.plot([x[i], x[j]], [y[i], y[j]], alpha = color_num, color = Colors.Edge)

        for i in range(len(x)):

            ax.plot(x[i], y[i], marker="o", markersize = FigConstants.StaticGraph['edgesize'], markeredgecolor = Colors.Marker_Edge, markerfacecolor = Colors.Marker_Face, alpha = FigConstants.MarkerAlpha)

            if show_labels:

                ax.text(x[i] + FigConstants.XBias[i], y[i] + FigConstants.YBias[i], str(self.labels[i]), fontsize = FigConstants.StaticGraph['labelsize'], horizontalalignment = 'center', verticalalignment = 'center')

        ax.axis(False)
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)

# def population_to_edge(Pop, Threshold = 0.5, UpperBound = -1 * np.log10(0.00001), LowerBound = -1 * np.log10(0.05)):

#     Pop = np.array(Pop)

#     _, m, n = Pop.shape

#     EdgeCIMat = np.zeros((m, n))

#     for m_ in range(m):

#         for n_ in range(n):

#             if m_ != n_:

#                 TestPop = Pop[:, m_, n_]

#                 PV = ttest_1samp(TestPop, Threshold, alternative = 'greater').pvalue * 2

#                 TmpVar = -1 * np.log10(PV + 0.000001)

#                 if np.isnan(TmpVar):

#                     print('NaN ALERT ' + str(PV) + ' ' + str(m_) + ' ' + str(n_))

#                 if TmpVar < LowerBound:

#                     EdgeCIMat[m_, n_] = 0

#                 elif TmpVar > UpperBound:

#                     EdgeCIMat[m_, n_] = 1

#                 else:

#                     EdgeCIMat[m_, n_] = TmpVar / UpperBound

#             else:

#                 EdgeCIMat[m_, n_] = 0

#     return EdgeCIMat

def population_to_edge(
        Pop,
        Threshold=0.5,
        UpperBound=-1 * np.log10(0.00001),
        LowerBound=-1 * np.log10(0.05),
        correction="none",
):

    Pop = np.asarray(Pop)

    _, m, n = Pop.shape

    EdgeCIMat = np.zeros((m, n))

    tests = []

    # -----------------------------
    # Collect all p-values
    # -----------------------------
    for m_ in range(m):

        for n_ in range(n):

            if m_ == n_:
                continue

            TestPop = Pop[:, m_, n_]

            p = ttest_1samp(
                TestPop,
                Threshold,
                alternative="greater"
            ).pvalue * 2

            tests.append((m_, n_, p))

    raw_p = [x[2] for x in tests]

    corrected_p = correct_pvalues(
        raw_p,
        method=correction,
    )

    # -----------------------------
    # Fill EdgeCIMat
    # -----------------------------
    for (m_, n_, _), p in zip(tests, corrected_p):

        TmpVar = -np.log10(p + 1e-6)

        if np.isnan(TmpVar):
            print(f"NaN ALERT {p} {m_} {n_}")

        if TmpVar < LowerBound:

            EdgeCIMat[m_, n_] = 0

        elif TmpVar > UpperBound:

            EdgeCIMat[m_, n_] = 1

        else:

            EdgeCIMat[m_, n_] = TmpVar / UpperBound

    return EdgeCIMat