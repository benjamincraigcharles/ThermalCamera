import time
import board
import busio
import adafruit_mlx90640
import matplotlib.colors as cpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as image


i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = [0] * 768
heatArray = [[0] * 32]*24

while True:
    try:
        mlx.getFrame(frame)

    except ValueError:
        # these happen, no biggie - retry
        continue

    for h in range(24):
        for w in range(32):
            t = frame[h*32 + w]
            t = ((9.0 / 5.0) * t) + 32
            print("%0.1f, " % t, end="")

        print()

    print()

    for i in range(len(frame)):
        frame[i] = (frame[i] *1.8) + 32

    vMax = None
    for i in frame:
        if(vMax is None or i > vMax):
            vMax = i

    vMin = None
    for i in frame:
        if(vMin is None or i < vMin):
            vMin = i

    ##print(vMax)
    ##print(vMin)
    ##print(frame)

    data = np.resize(frame, (24,32))


    ##print(data)

    vMax = str(vMax)
    vMin = str(vMin)

    ##norm = cpl._make_norm_from_scale(vmin='vMin', vmax='vMax', clip='False')

    plt.imshow( data, cmap="viridis", aspect="equal", interpolation="bicubic")

    plt.text(1, 1, ("Max Temp: " + vMax), color="white",
             fontdict={"fontsize": 8, "fontweight": 'bold', "ha": "left", "va": "baseline"})

    plt.text(1, 2, ("Min Temp: " + vMin), color="white",
             fontdict={"fontsize": 8, "fontweight": 'bold', "ha": "left", "va": "baseline"})

    ##plt.colorbar.set_label('Degrees Fahrenheit')





    plt.colorbar(label = 'Degrees Fahrenheit', spacing = 'proportional')

    plt.show()








    ##print(heatArray)
    ##plt.imshow(heatArray, cmap='hot', interpolation='nearest')
   ## plt.show()
    time.sleep(5)