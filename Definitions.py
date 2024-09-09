import sys, math
import pyray as rlib
def clamp(x,a,b):
	return max(a, min(x, b))

ventx, venty = 800, 800
cx = ventx//2 
cy = venty//2 
unit = 30 
zoom_step = 5 
dragging = False

#--Convertidores--#
xtm = lambda x: (x-cx)/unit
ytm = lambda y: -(y-cy)/unit
def xytm(x, y): return (xtm(x), ytm(y))

xtc = lambda x: int(clamp(x*unit+cx, -2**30, 2**30))
ytc = lambda y: int(clamp(-y*unit+cy, -2**30, 2**30))
def xytc(x, y): return (xtc(x), ytc(y))

#--Controles--#
def basic_controls():
    global dragging, zoom_step, cx, cy
    def zoom(step):
        global cx, cy, unit
        if unit + step <= 0: return
        opx, opy = xytm(ventx//2, venty//2)
        unit += step
        opx, opy = xytc(opx, opy)
        dx, dy = ventx//2-opx, venty//2-opy
        cx, cy = cx+dx, cy+dy

    #Quit
    if rlib.window_should_close():
        sys.exit()

	#Mouse
    if rlib.is_mouse_button_pressed(2): #Central Click
        dragging = True
    elif rlib.is_mouse_button_released(2):
        dragging = False
    zoom(zoom_step*rlib.get_mouse_wheel_move())

    #Drag
    rel = rlib.get_mouse_delta()
    if dragging:
        cx += rel.x
        cy += rel.y

#--- Implicit Function ---#
implicit_LOT = [
	(),          ((2,1),),      ((2,0),),      ((0,1),),
	((1,3),),    ((2,3),),      ((2,0),(1,3)), ((0,3),),
	((0,3),),    ((2,0),(1,3)), ((2,3),),      ((1,3),),
	((0,1),),    ((2,0),),      ((2,1),),      ()
]

def bisection_find_root(f, p1, p2, iters = 5):
	if f(p1) == 0:
		return p1
	if f(p2) == 0:
		return p2
	if not ((f(p1) < 0 and f(p2) > 0) or (f(p1) > 0 and f(p2) < 0)):
		return 0

	if f(p1) > 0:
		t = p1
		p1 = p2
		p2 = t
	
	for i in range(iters):
		p3 = (p1+p2)/2
		if f(p3) > 0:
			p2 = p3
		elif f(p3) < 0:
			p1 = p3
		else:
			return p3

	return (p1+p2)/2


def draw_implicit(f, region_size, cuts, border = True, interior = False, border_color = (255,0,0), interior_color = (100,100,100)):
    find_root = bisection_find_root

    for i in range(1, cuts+1):
        for j in range(1, cuts+1):
            a = ((2*(i-1)/cuts - 1)*region_size, (2*(j-1)/cuts - 1)*region_size)
            b = ((2*(i-1)/cuts - 1)*region_size, (2*j/cuts - 1)*region_size)
            c = ((2*i/cuts - 1)*region_size, (2*(j-1)/cuts - 1)*region_size)
            d = ((2*i/cuts - 1)*region_size, (2*j/cuts - 1)*region_size)
            
            fa, fb, fc, fd = f(a[0], a[1]), f(b[0], b[1]), f(c[0], c[1]), f(d[0], d[1])

            #if interior and fa < 0 and fb < 0 and fc < 0 and fd < 0:
            #	pygame.draw.polygon(vent, interior_color, (xytc(a[0], a[1]), xytc(b[0], b[1]), xytc(d[0], d[1]), xytc(c[0], c[1])))

            if border:
                fxt = lambda x: f(x,b[1])
                fxb = lambda x: f(x,a[1])
                fyl = lambda y: f(a[0],y)
                fyr = lambda y: f(c[0],y)

                pt = (find_root(fxt, b[0], d[0]), b[1])
                pd = (find_root(fxb, a[0], c[0]), a[1])
                pl = (a[0], find_root(fyl, a[1], b[1]))
                pr = (c[0], find_root(fyr, c[1], d[1]))

                p_list = [pt, pd, pl, pr]

                i_LOT = int(fd < 0)*2**3+int(fc < 0)*2**2+int(fb < 0)*2**1+int(fa < 0)*2**0

                for l in implicit_LOT[i_LOT]:
                    initial = xytc(p_list[l[0]][0], p_list[l[0]][1])
                    final = xytc(p_list[l[1]][0], p_list[l[1]][1])
                    rlib.draw_line(initial[0], initial[1], final[0], final[1], rlib.GREEN)

def draw_parametric(f, ti, tf, t_count, cyclic = True, color = (255,255,255)):
    f_prev = (0,0)
    try:
        f_prev = f(ti)
    except:
        pass
    f_now = f_prev

    for i in range(1, t_count-1):
        try:
            f_now = f((tf-ti)*(i/t_count) + ti)
            initial = xytc(f_now[0], f_now[1])
            final = xytc(f_prev[0], f_prev[1])
            rlib.draw_line(initial[0], initial[1], final[0], final[1], color)
            f_prev = f_now
        except:
            pass

    if cyclic:
        try:
            f_prev = f(ti)
            initial = xytc(f_now[0], f_now[1])
            final = xytc(f_prev[0], f_prev[1])
            rlib.draw_line(initial[0], initial[1], final[0], final[1], color)
        except:
            pass