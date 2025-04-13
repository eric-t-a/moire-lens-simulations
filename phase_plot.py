import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons

limit = 2
a = 5
two_pi = np.pi * 2

data_amount = int(limit * 2 / 0.01)

xx_data = []
xx_row = np.arange(-limit, limit, 0.01)

for i in range(data_amount):
    xx_data.append(xx_row)
xx = np.array(xx_data)

yy_data = []
yy_col = np.arange(limit, -limit, -0.01)

for y in yy_col:
    yy_row = [y] * data_amount
    yy_data.append(yy_row)
yy = np.array(yy_data)

def setup():
    t1_data = getMatrixData(xx, yy, a = a)
    axes[0].imshow(t1_data, cmap="gray")
    axes[0].axis("off")

    t2_data = getMatrixData(xx, yy, a = a, correspondent=True)
    axes[1].imshow(getMatrixData(xx, yy, a = a, correspondent=True), cmap="gray")
    axes[1].axis("off")

    t_result = getResultingMatrix(t1_data, t2_data)
    axes[2].imshow(t_result, cmap="gray")
    axes[2].axis("off")

    a_slider_position = plt.axes([0.25, 0, 0.65, 0.03])  # [left, bottom, width, height]
    a_slider = Slider(a_slider_position, "Arbitrary parameter", 1, 10.0, valinit=a)

    theta_slider_position = plt.axes([0.25, 0.05, 0.65, 0.03])  # [left, bottom, width, height]
    theta_slider = Slider(theta_slider_position, "Theta", -np.pi, np.pi, valinit=0)

    rounded_checkbox_position = plt.axes([0.75, 0.1, 0.1, 0.03])
    rounded_checkbox = CheckButtons(rounded_checkbox_position, ['Rounded'], [False])

    return a_slider, theta_slider, rounded_checkbox

def rotate(xx, yy, theta):
    x_new = xx * np.cos(theta) - yy * np.sin(theta)
    y_new = xx * np.sin(theta) + yy * np.cos(theta)
    return x_new, y_new

def getMatrixData(xx, yy, theta = 0, a = 1, correspondent = False, rounded = False):
    xx, yy = rotate(xx, yy, theta)
    rr_2 = xx**2 + yy**2
    phi = np.arctan2(yy, xx)
    arg = rr_2*phi*a
    if rounded:
        arg = np.ceil(rr_2*a)*phi

    result = arg % two_pi

    if correspondent:
        result = - result

    result = np.where(rr_2 > limit*2, 0, result)

    return result

def getResultingMatrix(t1_data, t2_data):
    t_result = (t1_data + t2_data) % two_pi
    return t_result

def onThetaUpdate(val):
    a = a_slider.val
    theta = theta_slider.val
    rounded = rounded_checkbox.get_status()[0]

    t1_data = getMatrixData(xx, yy, a = a, rounded=rounded)

    t2_data = getMatrixData(xx, yy, theta = theta, a = a, correspondent = True, rounded=rounded)
    axes[1].imshow(t2_data, cmap="gray")

    t_result = getResultingMatrix(t1_data, t2_data)
    axes[2].imshow(t_result, cmap="gray")
    fig.canvas.draw_idle()

def onAUpdate(val):
    a = a_slider.val
    theta = theta_slider.val
    rounded = rounded_checkbox.get_status()[0]

    t1_data = getMatrixData(xx, yy, a = a, rounded=rounded)
    axes[0].imshow(t1_data, cmap="gray")

    t2_data = getMatrixData(xx, yy, theta = theta, a = a, correspondent = True, rounded=rounded)
    axes[1].imshow(t2_data, cmap="gray")

    axes[2].imshow(getResultingMatrix(t1_data, t2_data), cmap="gray")
    fig.canvas.draw_idle()

def toggleRounded(obj):
    rounded = rounded_checkbox.get_status()[0]
    a = a_slider.val
    theta = theta_slider.val

    t1_data = getMatrixData(xx, yy, a = a, rounded=rounded)
    axes[0].imshow(t1_data, cmap="gray")

    t2_data = getMatrixData(xx, yy, theta = theta, a = a, correspondent = True, rounded=rounded)
    axes[1].imshow(t2_data, cmap="gray")

    axes[2].imshow(getResultingMatrix(t1_data, t2_data), cmap="gray")
    fig.canvas.draw_idle()

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

a_slider, theta_slider, rounded_checkbox = setup()

a_slider.on_changed(onAUpdate)
theta_slider.on_changed(onThetaUpdate)
rounded_checkbox.on_clicked(toggleRounded)

plt.show()