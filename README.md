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

Where $\vec{v}$ is the velocity field, $\nu$ is viscosity and $\vec{f}$ is some external force. The $\nabla \cdot \vec{v} = 0$ means that the given fluid is not compressible. The fluid is incompressible in the sim because of complexity.

**The equation has 3 variables which help in calculating the velocity.**
<ul>
  <li> $(\vec{v}\cdot\nabla)\vec{v}$ (Advectation): Accounts for the movement of the velocity.</li>
  <li> $\nu\nabla^2\vec{v}$ (Diffusion): Diffusion of our fluid / dye into the medium.</li>
  <li> $\vec{f}$ (External Forces): Forces acting on the fluid that affect the flow.</li>
</ul>
<h2>Implementing the equation into code</h2>

Since calculating each of these terms for every single pixel on the screen involves a lot of computational power, we use a grid, with each cell having its own density, velocity, and color of dye. The clicking of the mouse adds some amount of dye/fluid into the system, then for each frame the terms per grid cell are calculated.

<h3>Diffuse</h3>
The function iterates through the grid and takes a weighted average of the 4 cells around it to essentially diffuse the values of one cell into another. This is the same as watching a drop of paint spread out onto the surface of water.

<h2>Advect</h2>
Advect uses linear interpolation to approximate where the fluid will go. Linear interpolation traces the grid cell backwards in the velocity field then takes a weighted average to find out where the next point will land. It's a stable and cheap way for the job, although the weighted average in the function smooths out the finer details of the fluid.

<h2>Project</h2>
It's a function that keeps the fluid "incompressible" by making sure the law of conservation of mass is followed during the execution of above functions. 

