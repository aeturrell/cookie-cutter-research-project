import numpy as np
import matplotlib.pyplot as plt

from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

github_url = 'https://github.com/google/fonts/blob/main/ofl/tomorrow/Tomorrow-Bold.ttf'

url = github_url + '?raw=true'  # You want the actual file, not some html

response = urlopen(url)
f = NamedTemporaryFile(delete=False, suffix='.ttf')
f.write(response.read())
f.close()

prop = fm.FontProperties(fname=f.name)

# Create figure and axis
fig, ax = plt.subplots(figsize=(5, 4))
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')

# Draw cookie base with a wobbly edge
angles = np.linspace(0, 2 * np.pi, 100)
radii = 1 + 0.05 * np.sin(10 * angles) * (1 + 0.5 * np.cos(angles))  # Add some waviness to the edge
x = radii * np.cos(angles)
y = radii * np.sin(angles)
ax.fill(x, y, color='none', edgecolor='#ff7161', linewidth=7)

# Draw chocolate chips with improved distribution
np.random.seed(2)  # For reproducibility
num_chips = 15
chip_sizes = np.random.uniform(0.08, 0.13, num_chips)
colors = ['#2c75ff']

def generate_distributed_points(n, min_r=0.0, max_r=0.9):
    points = []
    for i in range(n):
        # Improved radius distribution: more chips towards the center
        r = np.sqrt(np.random.uniform(min_r**2, max_r**2))

        # Improved angle distribution: try to keep them spaced
        theta = np.random.uniform(0, 2 * np.pi) #random angle.
        if i>0:
          min_dist = 0.2 #minimum angle distance.
          too_close = True
          while too_close:
            too_close = False
            for prev_x, prev_y in points:
              prev_theta = np.arctan2(prev_y, prev_x)
              if prev_theta<0:
                prev_theta+= 2*np.pi
              curr_theta = np.arctan2(r*np.sin(theta), r*np.cos(theta))
              if curr_theta <0:
                curr_theta+= 2*np.pi

              dist = abs(curr_theta - prev_theta)
              if dist > np.pi:
                dist = 2*np.pi - dist

              if dist < min_dist:
                theta = np.random.uniform(0, 2*np.pi)
                too_close = True
                break

        x = r * np.cos(theta)
        y = r * np.sin(theta)
        points.append((x, y))
    return np.array(points)

chip_points = generate_distributed_points(num_chips)

for i in range(num_chips):
    ax.add_patch(plt.Circle(chip_points[i], chip_sizes[i], facecolor=np.random.choice(colors), edgecolor="k"))

ax.set_title("cookiecutter\n        research project", fontproperties=prop, size=25, loc="left", color="#ff7161")
plt.tight_layout()
plt.savefig("cookiecutter_logo.svg", transparent=True)
# Show the drawing
plt.show()
