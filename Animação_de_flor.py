from turtle import Screen, Turtle, done
import colorsys
import math
import time


PETALS = 14
PETAL_SIZE = 130
PETAL_ARC = 70
CENTER_RADIUS = 0
CENTER_OFFSET = 0
PEN_WIDTH = 2


FPS = 40
STEM_SECONDS = 1.2
LEAF_SECONDS = 1.0
BLOOM_SECONDS = 3.0
FINAL_SWAY_SECONDS = 6.0

STEM_FRAMES = int(FPS * STEM_SECONDS)
LEAF_FRAMES = int(FPS * LEAF_SECONDS)
BLOOM_FRAMES = int(FPS * BLOOM_SECONDS)
SWAY_FRAMES = int(FPS * FINAL_SWAY_SECONDS)

TOTAL_FRAMES = STEM_FRAMES + LEAF_FRAMES + BLOOM_FRAMES + SWAY_FRAMES

screen = Screen()
screen.bgcolor("black")
screen.colormode(1.0)
screen.tracer(0, 0)


stem_t = Turtle()
petal_t = Turtle()
center_t = Turtle()
leaf_t = Turtle()

for tt in (stem_t, petal_t, center_t, leaf_t):
    tt.hideturtle()
    tt.speed(0)
petal_t.width(PEN_WIDTH)
center_t.width(1)
stem_t.width(8)
leaf_t.width(2)

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def push_state(t):
    return (t.position(), t.heading())

def pop_state(t, state):
    t.penup()
    t.goto(state[0])
    t.setheading(state[1])
    t.pendown()

def draw_stem(progress):
    stem_t.clear()
    stem_t.penup()
    stem_t.home()
    stem_t.setheading(270)
    stem_t.pendown()
    stem_t.pencolor((0.06, 0.5, 0.12))
    stem_t.pensize(8)
    length = 260
    drawn = int(length * progress)
    #  crescimento
    stem_t.penup()
    stem_t.home()
    stem_t.setheading(270)
    stem_t.forward(0)
    stem_t.pendown()
    seg = 6
    steps = max(1, drawn // seg)
    for i in range(steps):
        stem_t.forward(seg)
    rest = drawn - steps * seg
    if rest > 0:
        stem_t.forward(rest)

def draw_leaf(progress, side=1):
    leaf_t.clear()
    leaf_t.penup()
    leaf_t.home()
    leaf_t.setheading(270)
    leaf_t.forward(140)  
    base = leaf_t.position()
    base_heading = 270
    leaf_t.goto(base)
    leaf_t.setheading(base_heading + side * 40)
    leaf_t.pendown()
    leaf_t.fillcolor((0.06, 0.55, 0.15))
    leaf_t.pencolor((0.02, 0.35, 0.08))
    leaf_t.begin_fill()   
    size = 40 * progress
    leaf_t.circle(size, 90)
    leaf_t.left(90)
    leaf_t.circle(size, 90)
    leaf_t.end_fill()

def draw_petal_at(angle, scale, hue, sway=0.0):  
    petal_t.penup()
    petal_t.home()
    petal_t.setheading(angle + sway)
    petal_t.forward(CENTER_OFFSET)
    base = petal_t.position()
    start_state = push_state(petal_t)
    petal_t.setheading(angle + sway)
    petal_t.pendown()
    r, g, b = colorsys.hsv_to_rgb(hue, 0.85, 1.0)
    petal_t.fillcolor((r, g, b))
    petal_t.pencolor((max(0, r * 0.85), max(0, g * 0.85), max(0, b * 0.85)))
    petal_t.begin_fill()
    petal_t.left(90)
    petal_t.circle(PETAL_SIZE * scale, PETAL_ARC)
    petal_t.left(180 - PETAL_ARC)
    petal_t.circle(PETAL_SIZE * scale, PETAL_ARC)
    petal_t.left(90)
    petal_t.end_fill()
    pop_state(petal_t, start_state)

def draw_center(scale):
    center_t.clear()
    center_t.penup()
    center_t.home()
    center_t.pendown()
    center_r, center_g, center_b = colorsys.hsv_to_rgb(0.12, 0.9, 1.0)
    center_t.fillcolor((center_r, center_g, center_b))
    center_t.pencolor("black")
    center_t.begin_fill()
    center_t.circle(CENTER_RADIUS * scale)
    center_t.end_fill()

start_time = time.time()
for frame in range(TOTAL_FRAMES + 1):
    t = frame 
    petal_t.clear()
    center_t.clear()
    leaf_t.clear() 

    if t <= STEM_FRAMES:
        frac = clamp(t / STEM_FRAMES)
        draw_stem(ease_out_cubic(frac))
    else:
        draw_stem(1.0)

    leaf_phase = max(0, t - STEM_FRAMES)
    if leaf_phase <= LEAF_FRAMES:
        lp = clamp(leaf_phase / LEAF_FRAMES)
        draw_leaf(ease_out_cubic(lp), side=-1)
        draw_leaf(ease_out_cubic(lp * 0.9), side=1)
    else:
        draw_leaf(1.0, side=-1)
        draw_leaf(1.0, side=1)
    
    bloom_phase = max(0, t - STEM_FRAMES - LEAF_FRAMES)
    
    for i in range(PETALS):
        petal_offset_frames = int((i / PETALS) * (BLOOM_FRAMES * 0.7))
        local = bloom_phase - petal_offset_frames
        local_scale = clamp(local / (BLOOM_FRAMES * 0.4))
        local_scale = ease_out_cubic(local_scale)
       
        sway_phase = max(0, t - (STEM_FRAMES + LEAF_FRAMES + BLOOM_FRAMES))
        sway = 0.0
        if sway_phase > 0:
            sway = 4.0 * math.sin((sway_phase / FPS) * 2.0 + i * 0.3)
        hue = (i / PETALS) * 0.9
        draw_petal_at(360 * i / PETALS, local_scale, hue, sway)

    center_local = clamp(bloom_phase / BLOOM_FRAMES)
    draw_center(0.2 + 0.8 * ease_out_cubic(center_local))
 
    final_phase = t - (STEM_FRAMES + LEAF_FRAMES + BLOOM_FRAMES)
    if final_phase > 0:
        sway_global = 6.0 * math.sin(final_phase / FPS * 1.6)
        
        petal_t.clear()
        for i in range(PETALS):
            hue = (i / PETALS) * 0.9
           
            draw_petal_at(360 * i / PETALS, 1.0, hue, sway_global + 2.0 * math.sin(frame * 0.06 + i))

        pulse = 1.0 + 0.03 * math.sin(frame * 0.12)
        draw_center(pulse)

    screen.update()
    time.sleep(1.0 / FPS)

petal_t.clear()
center_t.clear()
leaf_t.clear()
stem_t.clear()
draw_stem(1.0)
draw_leaf(1.0, side=-1)
draw_leaf(1.0, side=1)
for i in range(PETALS):
    hue = (i / PETALS) * 0.9
    draw_petal_at(360 * i / PETALS, 1.0, hue, 0.0)
draw_center(1.0)

screen.update()
screen.tracer(1, 10)
screen.exitonclick()
done()