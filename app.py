import numpy as np
from matplotlib import pyplot as plt
from scipy import stats
import panel as pn

LTPD = np.linspace(0,1,1001) #the range of potential defect rates in the lot
Pa = lambda c,n: stats.binom.cdf(c,n,LTPD)

def plot(c,n,AQL,RQL,x_range, y_range):
    Pa1 = Pa(c,n)
    plt.clf()
    plt.plot(LTPD, Pa1)
    plt.xlabel('LTPD [%]')
    plt.ylabel('Pa [%]')
    
    # Set axis limits based on sliders
    x_min, x_max = x_range
    y_min, y_max = y_range
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    producers_risk = Pa1[max(np.where(LTPD<=AQL)[0])]
    consumers_risk = LTPD[min(np.where(Pa1<=1-RQL)[0])]
    plt.title(f'Operating Characteristic Curve\n (c={c}, n={n})')
    plt.vlines(x=AQL, ymin=min(Pa1), ymax=min(Pa1[np.where(LTPD<=AQL)[0]]), color='purple', linestyle=':', label=f'AQL: {np.round(AQL*100,2)}%')
    plt.hlines(y=producers_risk, xmin=0, xmax=AQL, color='purple', linestyle=':', label=f'Producer\'s Risk:{np.round(100*(1-producers_risk),1)}%') 
    
    
    plt.hlines(y=1-RQL, xmin=min(LTPD), xmax=consumers_risk, color='orange', linestyle=':', label=f'RQL:{np.round(100*(1-RQL),2)}%')
    plt.vlines(x=consumers_risk, ymin=0, ymax=1-RQL, color='orange', linestyle=':', label=f'Consumer\'s Risk:{np.round(100*consumers_risk,1)}%')


    plt.legend()
    return pn.pane.Matplotlib(plt.gcf(), tight=True)

def summary_text(c, n, AQL, RQL):
    # Calculate producer's and consumer's risks (example)
    Pa1 = stats.binom.cdf(c, n, LTPD)
    producers_risk = Pa1[max(np.where(LTPD <= AQL)[0])]
    consumers_risk = LTPD[min(np.where(Pa1 <= 1 - RQL)[0])]

    text = f""" <div align="center">
    <h2>Summary</h2>
    <p style="font-size:18px">There is a  {100 * (1 - RQL):.2f}% chance the producer (Starlight) will reject the lot if its percentage defective is greater than {100*(1-AQL):.2f}%.<br>   
    There is a {100 * consumers_risk:.2f}% chance the customer will accept the lot if it's quality if its percent defective is greater than {100*(1-RQL):.2f}% </p></div>
    """
    return text

x_range_slider = pn.widgets.RangeSlider(name='X-axis range', start=0, end=1, step=0.01, value=(0, 0.4))
y_range_slider = pn.widgets.RangeSlider(name='Y-axis range', start=0, end=1, step=0.05, value=(0, 1))
c_slider = pn.widgets.IntSlider(name='c:', start=0, end=10, step=1, value=0)
n_slider = pn.widgets.IntSlider(name='n:', start=0, end=100, step=1, value=29)
AQL_slider = pn.widgets.DiscreteSlider(name='AQL:',
                                       options=[.0001, .00015, .00025, .00065, .001, .0015, 
                                                .0025, .004, .0065,.01,.015,.025,.04,.065,.1],
                                       value=.04)
RQL_slider = pn.widgets.FloatSlider(name='RQL:', start=0.5, end=0.99, step=0.1, value=.9)
interactive_plot = pn.bind(plot, c=c_slider, n=n_slider, AQL=AQL_slider, RQL=RQL_slider, x_range=x_range_slider, y_range=y_range_slider)

summary_pane = pn.bind(summary_text, c=c_slider, n=n_slider, AQL=AQL_slider, RQL=RQL_slider)
summary_md = pn.pane.Markdown(summary_pane, width=300)

sliders = pn.Column(c_slider, n_slider, AQL_slider, 
                    RQL_slider, x_range_slider, y_range_slider,
                    width=250,
                    sizing_mode='fixed',
                    margin=(10, 20))
plot_and_text = pn.Column(interactive_plot, summary_md, sizing_mode='stretch_width',margin=(10, 10))

app=pn.Row(sliders, 
           plot_and_text,
           sizing_mode='stretch_width',
           margin=10)
app.servable()
