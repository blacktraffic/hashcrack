from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import viridis
from bokeh.models.mappers import LinearColorMapper
from bokeh.models import Range1d, LinearAxis
from bokeh.plotting import figure,save
import sys
import re
import math 

#bits liberally borrowed from bokeh example code

# need:
# pip install bokeh

# takes pot file or other output file, so hash:password or pwdump style uname:uid:foo:hash:password and makes a graph
# as long as

def big_palette(size, palette_func):
    if size < 256:
        return palette_func(size)
    p = palette_func(256)
    out = []
    for i in range(size):
        idx = int(i * 256.0 / size)
        out.append(p[idx])
    return out

output_file(sys.argv[1]+"q.html")

maxh=0
maxlen=0


freq=[]
pos=[]
tick=0
total=0
maximv=0
total=0
imv=0
itv=0

#parse our input file to get max
with open(sys.argv[1], encoding="iso-8859-1") as inf:
    for line in inf:
        ans=line.rstrip()
        m = re.search(r'.+,(\d+)',ans)                   
        if m.group(1):
            mv=m.group(1)
            imv = math.log(int(mv),10)

        if maximv<imv:
            maximv=imv
                               
imv=0

#parse our input file
with open(sys.argv[1], encoding="iso-8859-1") as inf:
    for line in inf:
        ans=line.rstrip()
        m = re.search(r'.+,(\d+)',ans)                   
        if m.group(1):
            mv=m.group(1)                            
            imv = math.log(int(mv),10)

            freq.append(imv)
            pos.append(tick)
            tick=tick+1

#get an appropriate palette, and reverse the order
cm = big_palette(tick, viridis)
mcm = cm[::-1]

msource = ColumnDataSource(data=dict(ticks=pos, cracked=freq, color=mcm ))

p = figure(x_range=(0,tick), y_range=(0,maximv), plot_height=600, title="How Often the Rules Fired on Our Test Data", toolbar_location=None, tools="")

p.xaxis.axis_label='Rule rank (best to worst) '
p.yaxis.axis_label='How often it fired, log_10'

p.vbar(x='ticks', top='cracked', width=1, color='color', legend=False, source=msource)

p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

show(p)
#save(p)
