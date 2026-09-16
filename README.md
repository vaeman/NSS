# NSS
Approximating the behaviour of fluids in an incompressible fluid medium by implementing the logic given by the Navier stokes equation.

<img width="947" height="620" alt="image" src="https://github.com/user-attachments/assets/1880bd6a-ee6f-4b16-ab3d-c3dca7190e1f" />
<img width="925" height="617" alt="image" src="https://github.com/user-attachments/assets/848ca1e5-196d-43f8-b4d6-da3852800515" />

<h1>How it works</h1>
The simulation works on the same principles provided by the Navier Stokes equation, which was one of the seven <a href = "https://en.wikipedia.org/wiki/Millennium_Prize_Problems">Millenium Prize Problems</a>. Coincidentally it got solved while I was researching on this topic. The equations and the methods used in this code are from the paper <a href = "https://www.mikeash.com/pyblog/fluid-simulation-for-dummies.html">Fluid Simulation for Dummies</a> which was based on another paper <a href = "https://www.dgp.toronto.edu/public_user/stam/reality/Research/pdf/GDC03.pdf">Real time fluid dynamics for games</a>
<h2>Navier stokes equation for velocity: </h2>

$$
\frac{\partial \vec{v}}{\partial t} = -(\vec{v}\cdot\nabla)\vec{v} + \nu\nabla^2\vec{v} + \vec{f}
$$

$$
\nabla \cdot \vec{v} = 0
$$

Where $$ \vec{v} $$ is the velocity field, $$ \nu $$ is viscosity and $$ \vec{f} $$ is some external force. 
