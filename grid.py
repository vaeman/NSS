import pygame
import numpy
import colorsys

# CONSTANTS

WIDTH, HEIGHT = 768,768
BLOCK_SIZE = 8
GRID_SIZE = int(WIDTH/BLOCK_SIZE)


# storing density and velocity

vxo = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))
vyo = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))

vx = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))
vy = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))

d = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))
do = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))

# colors (rgb channels same logic as d do)

rc = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))
rco = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))

gc = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))
gco = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))

bc = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))
bco = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))

hue = 0.0

# controls properties of wada
dt = 0.12
iters = 200
diff = 0.000005
visc = 0.000000000005
# visc = 0.002

# divergence
div = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))
p = numpy.zeros((GRID_SIZE+2, GRID_SIZE+2))
prev_mouse = (0, 0)

a = dt * diff * GRID_SIZE * GRID_SIZE

#init

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

r = True

# shiii

def get_grid_coords():
    x,y = pygame.mouse.get_pos()
    return (x//BLOCK_SIZE, y//BLOCK_SIZE)

# def draw():
#     for i in range(1, GRID_SIZE+1):
#         for j in range(1, GRID_SIZE+1):
#             c = int(d[i][j])
#             if c != 0:
#                 pygame.draw.rect(screen, pygame.Color(c,c,c) ,((i-1)*BLOCK_SIZE,(j-1)*BLOCK_SIZE,BLOCK_SIZE, BLOCK_SIZE)) 




# vectorization: instead of using for loops, we do operations on the whole array at once (numpy does it in c)

def draw():
    # for i in range(1, GRID_SIZE+1):
    #     for j in range(1, GRID_SIZE+1):
    #         c = int(d[i][j])
    #         if c != 0:
    #             pygame.draw.rect(screen, pygame.Color(c,c,c) ,((i-1)*BLOCK_SIZE,(j-1)*BLOCK_SIZE,BLOCK_SIZE, BLOCK_SIZE)) 

    #vectorisation instead of for loops cuz faster

    # d[1:-1, 1:-1] means entire grid
    arr = numpy.clip(d[1:-1, 1:-1]*1000, 0, 1)

    r = numpy.clip(rc[1:-1, 1:-1]*50, 0,255)
    g = numpy.clip(gc[1:-1, 1:-1]*50, 0,255)
    b = numpy.clip(bc[1:-1, 1:-1]*50, 0,255)


    rgb = numpy.stack([r,g,b], axis=-1).astype(numpy.uint8)

    # instead of each grid cell being rendered individually, we make a surface 
    surf = pygame.surfarray.make_surface(rgb)
    surf = pygame.transform.scale(surf, (WIDTH, HEIGHT))
    screen.blit(surf, (0, 0))

# need this in my life

def add_color(x,y, col):

    d[x+1][y+1] = min(d[x+1][y+1] + a, 255)
    rc[x+1][y+1] += col[0]
    gc[x+1][y+1] += col[1]
    bc[x+1][y+1] += col[2]

# reflection from boundary
# i copied this bc how

def set_bnd(b, x):
    x[0, 1:-1] = -x[1, 1:-1] if b == 1 else x[1, 1:-1]
    x[-1, 1:-1] = -x[-2, 1:-1] if b == 1 else x[-2, 1:-1]
    x[1:-1, 0] = -x[1:-1, 1] if b == 2 else x[1:-1, 1]
    x[1:-1, -1] = -x[1:-1, -2] if b == 2 else x[1:-1, -2]

    x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
    x[0, -1] = 0.5 * (x[1, -1] + x[0, -2])
    x[-1, 0] = 0.5 * (x[-2, 0] + x[-1, 1])
    x[-1, -1] = 0.5 * (x[-2, -1] + x[-1, -2])


# take weighted average of the 4 cells around ith cell

def diffuse(b, f, fo, rate):
    a = dt * rate * GRID_SIZE * GRID_SIZE
    for _ in range(iters):
        f[1:-1,1:-1] = (fo[1:-1,1:-1] + a * (f[:-2,1:-1] + f[2:,1:-1] +
                                              f[1:-1,:-2] + f[1:-1,2:])) / (1 + 4*a)
        set_bnd(b, f)
    

    


# unholy amount of math going on here something something linear interpolation (we know the previous point and the current point so we can approximate the next point)


ix, iy = numpy.meshgrid(numpy.arange(1,GRID_SIZE+1), numpy.arange(1,GRID_SIZE+1), indexing="ij")

def advect(b, f, fo, vx, vy):
    dt0 = dt * GRID_SIZE


    x = numpy.clip(ix - dt0 * vx[1:-1,1:-1], 0.5, GRID_SIZE + 0.5)
    y = numpy.clip(iy - dt0 * vy[1:-1,1:-1], 0.5, GRID_SIZE + 0.5)


    i0 = x.astype(int); i1 = i0 + 1
    j0 = y.astype(int); j1 = j0 + 1
    s1 = x - i0; s0 = 1 - s1
    t1 = y - j0; t0 = 1 - t1

    f[1:-1,1:-1] = (s0 * (t0 * fo[i0,j0] + t1 * fo[i0,j1]) +
                     s1 * (t0 * fo[i1,j0] + t1 * fo[i1,j1]))

    set_bnd(b,f)

def add_vel(x,y, a,b):
    vx[x+1][y+1] += a
    vy[x+1][y+1] += b

def obstacle(ox,oy,radius):
    mask = (ix - ox)**2 + (iy - oy)**2 < radius**2
    vx[1:-1,1:-1][mask] = 0
    vy[1:-1,1:-1][mask] = 0
    d[1:-1,1:-1][mask] =  0
    rc[1:-1,1:-1][mask] = 0
    gc[1:-1,1:-1][mask] = 0
    bc[1:-1,1:-1][mask] = 0


# ensures law of convesraitionaotnaoo of mass is conserved

# def project():
#     h = 1.0/GRID_SIZE

#     for i in range(1, GRID_SIZE+1):
#         for j in range(1, GRID_SIZE+1):
#             div[i][j] = -0.5 * h *(vx[i+1][j] - vx[i-1][j] + vy[i][j+1] - vy[i][j-1]) # weighted average returns
#             p[i][j] = 0

#     for z in range(iters):
#         for i in range(1, GRID_SIZE+1):
#             for j in range(1, GRID_SIZE+1):
#                 p[i][j] = (div[i][j] + p[i-1][j] + p[i+1][j] + p[i][j-1] + p[i][j+1]) / 4
#         set_bnd(0,p)

#     for i in range(1,GRID_SIZE+1):
#         for j in range(1, GRID_SIZE+1):
#             vx[i][j] -= 0.5 * (p[i+1][j] - p[i-1][j]) / h
#             vy[i][j] -= 0.5 * (p[i][j+1] - p[i][j-1]) / h 

#     set_bnd(1, vx)
#     set_bnd(2, vy)

def project():
    h = 1.0 / GRID_SIZE    
    div[1:-1,1:-1] = -0.5 * h * (vx[2:,1:-1] - vx[:-2,1:-1] +
                                  vy[1:-1,2:] - vy[1:-1,:-2])
    p[:] = 0
    set_bnd(0, div)
    set_bnd(0, p)

    for _ in range(iters):
        p[1:-1,1:-1] = (div[1:-1,1:-1] + p[:-2,1:-1] + p[2:,1:-1] +
                         p[1:-1,:-2] + p[1:-1,2:]) / 4
        set_bnd(0, p)

    vx[1:-1,1:-1] -= 0.5 * (p[2:,1:-1] - p[:-2,1:-1]) / h
    vy[1:-1,1:-1] -= 0.5 * (p[1:-1,2:] - p[1:-1,:-2]) / h
    set_bnd(1, vx)
    set_bnd(2, vy)



while r:

    gx, gy = get_grid_coords()

    gx = max(min(gx,GRID_SIZE-1), 0)
    gy = max(min(gy,GRID_SIZE-1), 0)

    mousecoords= font.render(f"{gx,gy}",False, "green")
    frames= font.render(f"{int(clock.get_fps())}",False, "green")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             r = False
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            r = False


    if pygame.mouse.get_pressed()[0]:
        hue += 0.01
        h = 1.0 / GRID_SIZE
        col = [int(c*255) for c in colorsys.hsv_to_rgb(hue, 1, 1)]
            
        add_color(gx, gy, col)
        mx, my = pygame.mouse.get_pos()
        pmx, pmy = prev_mouse
        # adding delta v
        add_vel(gx, gy, (mx - pmx) * 0.3, (my - pmy) * 0.3)
    elif pygame.mouse.get_pressed()[2]:
        mx, my = pygame.mouse.get_pos()
        pmx, pmy = prev_mouse
        # adding delta v
        add_vel(gx, gy, (mx - pmx) * 0.3, (my - pmy) * 0.3)
    prev_mouse = pygame.mouse.get_pos()
    

    screen.fill((0,0,0))

    draw()

    vxo = vx.copy()
    vyo = vy.copy()

    diffuse(1, vx, vxo, visc)
    diffuse(2, vy, vyo, visc)
    project()

    vxo = vx.copy()
    vyo = vy.copy()

    advect(1, vx, vxo, vxo, vyo)
    advect(2, vy, vyo, vxo, vyo)
    project()

    rco = rc.copy(); diffuse(0, rc, rco, diff)
    rco = rc.copy(); advect(0, rc, rco, vx, vy)
    rc *= 0.99

    gco = gc.copy(); diffuse(0, gc, gco, diff)
    gco = gc.copy(); advect(0, gc, gco, vx, vy)
    gc *= 0.99

    bco = bc.copy(); diffuse(0, bc, bco, diff)
    bco = bc.copy(); advect(0, bc, bco, vx, vy)
    bc *= 0.99


    do = d.copy()
    diffuse(0, d, do, diff)
    do = d.copy()
    advect(0, d, do, vx, vy)

    # adding different sources
    
    add_color(10,10, (255,100,100))
    add_vel(10,10,10,10)

    add_color(88,88, (100,100,255))
    add_vel(88,88,-10,-10)

    # obstacle(40,40,10)
    # x,y = 60,60
    # add_vel(x+5, y, 0, -10)
    # add_vel(x+5, y, -2, 0)
    # add_vel(x, y+5, 10, 0)
    # add_vel(x, y+5, 0, -2)
    # add_vel(x-5, y, 0, 10)
    # add_vel(x-5, y, 2, 0)
    # add_vel(x, y-5, -10, 0)
    # add_vel(x, y-5, 0, 2)
    # add_color(x+5,y, (1,1,20))



    d *= 0.99

    screen.blit(frames, (10,10))
    screen.blit(mousecoords, (10, HEIGHT - 20))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()


