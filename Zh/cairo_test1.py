import cairo

surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 300, 200)
ctx = cairo.Context(surface)

ctx.rectangle(25, 50, 50, 120)
ctx.set_source_rgb(1, 0, 0)
ctx.fill()

surface.write_to_png('rectangle.png')
