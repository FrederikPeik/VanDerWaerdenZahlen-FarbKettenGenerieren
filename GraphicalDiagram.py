import turtle

def open(chains, colors):
    turtle.title("Wegdiagramm")

    colorcodes = {
        "R":(255, 0, 0),
        "B":(0, 0, 255),
        "G":(0, 150, 0),
        "Y":(255, 255, 0),
        "A":(100, 100, 255),
        "C":(0, 200, 200),
        "O":"orange",
        "W":(255, 255, 255),
        "L":(0, 255, 0),
        "P":(200, 0, 200),
    }

    angles = {}
    ind = 0
    dis = 360 / len(colors)
    for color in colors:
        angles[color] = dis * ind

        ind += 1

    turtle.colormode(255)
    turtle.bgcolor("#19232d")
    turtle.shape("circle")
    turtle.shapesize(0.5)
    turtle.width(5)
    turtle.speed(0)

    xgridsize = 5
    ygridsize = int(len(chains) / xgridsize - 1)
    distance = 200
    xind = 0
    yind = 0
    for chain in chains:
        xstart = xind * distance
        ystart = yind * distance

        turtle.up()
        turtle.setpos(xstart - xgridsize * distance / 2, ystart - ygridsize * distance / 2)
        turtle.down()

        for element in chain:
            turtle.color(colorcodes[element])
            turtle.setheading(angles[element])
            turtle.forward(20)

        turtle.up()
        turtle.forward(5)
        turtle.color("white")
        turtle.shape("classic")
        turtle.shapesize(1)
        turtle.stamp()
        turtle.setpos(xstart - xgridsize * distance / 2, ystart - ygridsize * distance / 2)
        turtle.shape("circle")
        turtle.shapesize(0.5)
        turtle.stamp()
        turtle.down()

        xind += 1
        if xind > xgridsize:
            xind = 0
            yind += 1

    turtle.exitonclick()