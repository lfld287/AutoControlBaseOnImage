import uiautomator2 as u2


def getRotationPos(displayHeight: int, displayWidth: int, x: int, y: int, rotation: int):
    if rotation == 0:
        x_true = x
        y_true = y
    elif rotation == 1:
        x_true = displayWidth-y
        y_true = x
    else:
        x_true = x
        y_true = y

    return x_true, y_true


def clickRotation1(d: u2.Device, x: int, y: int):
    xt,yt = getRotationPos(3120,1440,x,y,1)
    print(xt)
    print(yt)
    d.click(xt,yt)