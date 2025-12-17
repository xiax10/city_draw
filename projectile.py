'''Draw the trajectory of a body in projectile motion'''

import matplotlib.pyplot as plt
import math

def frange(start, final, increment):
    numbers = []
    while start < final:
        numbers.append(start)
        start = start + increment

    return numbers

def draw_graph(x, y):
    plt.plot(x, y)
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.title('Projectile motion of a body')

def draw_trajectory(u, theta):
    theta = math.radians(theta)
    g = 9.8

    t_flight = 2 * u * math.sin(theta) / g
    intervals = frange(0, t_flight, 0.01)

    x = []
    y = []

    for t in intervals:
        x.append(u * math.cos(theta) * t)
        y.append(u * math.sin(theta) * t - 0.5 * g * t**2)
    
    draw_graph(x, y)

""" if __name__ == '__main__':
    try:
        u = float(input('Enter the initial velocity (m/s): '))
        theta = float(input('Enter the angle of projection (degrees):'))
    except ValueError:
        print('you entered an invalid input.')
    else:
        draw_trajectory(u, theta)
        plt.show() """

if __name__ == '__main__':
    u_list = [20]
    theta_list = [15, 30, 45, 60, 75]

    for u in u_list:
        for theta in theta_list:
            draw_trajectory(u, theta)

    # plt.legend(['20', '40', '60'])
    plt.show()