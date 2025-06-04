import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import panel as pn
LTPD = np.linspace(0,1,1001) #the range of potential defect rates in the lot
Pa = lambda c,n: stats.binom.cdf(c,n,LTPD)

def plot(c,n,AQL,RQL):
    Pa1 = Pa(c,n)
    plt.plot(LTPD, Pa1)
    plt.xlabel('LTPD [%]')
    plt.ylabel('Pa [%]')
    plt.xlim(0,.4)
    producers_risk = Pa1[max(np.where(LTPD<=AQL)[0])]
    consumers_risk = LTPD[min(np.where(Pa1<=1-RQL)[0])]
    plt.title(f'Operating Characteristic Curve\n (c={c}, n={n})')
    plt.vlines(x=AQL, ymin=min(Pa1), ymax=min(Pa1[np.where(LTPD<=AQL)[0]]), color='gray', linestyle=':', label=f'AQL: {np.round(AQL*100,2)}%')
    plt.hlines(y=producers_risk, xmin=0, xmax=AQL, color='gray', linestyle=':', label=f'Producer\'s Risk:{np.round(100*(1-producers_risk),1)}%') 
    plt.hlines(y=1-RQL, xmin=min(LTPD), xmax=consumers_risk, color='gray', linestyle=':', label=f'RQL:{np.round(100*(1-RQL),2)}%')
    plt.vlines(x=consumers_risk, ymin=0, ymax=1-RQL, color='gray', linestyle=':', label=f'Consumer\'s Risk:{np.round(100*consumers_risk,1)}%')
    plt.legend()
    return pn.pane.Matplotlib(plt.gcf(), tight=True)

c_slider = pn.widgets.IntSlider(name='c:', start=0, end=10, step=1)
n_slider = pn.widgets.IntSlider(name='n:', start=0, end=100, step=1)
AQL_slider = pn.widgets.DiscreteSlider(name='AQL:',
                                       options=[.0001, .00015, .00025, .00065, .001, .0015, 
                                                .0025, .004, .0065,.01,.015,.025,.04,.065,.1],
                                       value=.04)
RQL_slider = pn.widgets.FloatSlider(name='RQL:', start=0, end=0.5, step=0.1)
interactive_plot = pn.bind(plot, c=c_slider, n=n_slider, AQL=AQL_slider, RQL=RQL_slider)
app = pn.Column(c_slider, n_slider, AQL_slider, RQL_slider, interactive_plot)
app.servable()
