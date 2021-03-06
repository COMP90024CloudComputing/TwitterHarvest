# from : http://matplotlib.org/users/path_tutorial.html
#draw a polygon by all coordinate points then put into path.
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

verts = [
    (1,1),
    (1,3),
    (2,4),
    (3,3.5),
    (4,4),
    (4,1),

    ]

codes = [Path.MOVETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.LINETO,
         Path.CLOSEPOLY,
         ]

path = Path(verts, codes)

fig = plt.figure()
ax = fig.add_subplot(111)
patch = patches.PathPatch(path, facecolor='orange', lw=2)
ax.add_patch(patch)
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
plt.show() # delete it if don't need to output plot
print path.contains_point((3,3.75))
