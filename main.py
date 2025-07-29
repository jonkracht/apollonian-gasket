import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Circle:
    def __init__(self, x, y, r, is_interior):
        self.x = x
        self.y = y
        self.z = complex(x, y)
        self.r = r

        if is_interior:
            self.k = r ** -1  # curvature k = 1/r
        else:
            self.k = -(r ** -1)

        self.kz = self.k * self.z

    def __str__(self):
        return f"Circle with radius {round(self.r, 2)} centered at ({round(self.x, 2)}, {round(self.y, 2)})"


def generate_initial_circles():
    """Circles with which to instantiate fractal."""

    c1 = Circle(0, 0, 100, False)
    c2 = Circle(-50, 0, 50, True)
    c3 = Circle(0, 200 / 3, 100 / 3, True)

    return [c1, c2, c3]


def compute_tangent_circles(C1, C2, C3):
    """Takes three circle objects and returns both mutually tangent circles."""
    print("\n*** Computing tangent circles ***")

    # Compute radii
    sum_term = C1.k + C2.k + C3.k
    sqrt_term = 2 * np.sqrt(C1.k * C2.k + C1.k * C3.k + C2.k * C3.k)

    print(f"Sum term is:  {sum_term}")
    print(f"Sqrt term is:  {sqrt_term}")

    k4_plus = sum_term - sqrt_term
    k4_minus = sum_term + sqrt_term

    # Compute circles' centers
    print("\n*** Computing circles' centers ***")
    z_sum_term = C1.kz + C2.kz + C3.kz
    z_sqrt_term = 2 * np.sqrt(C1.kz * C2.kz + C1.kz * C3.kz + C2.kz * C3.kz)

    print(f"Zsum term is:  {z_sum_term}")
    print(f"Zsqrt term is:  {z_sqrt_term}")

    zp = (z_sum_term + z_sqrt_term) / k4_plus
    zm = (z_sum_term - z_sqrt_term) / k4_minus

    C4 = Circle(np.real(zp), np.imag(zp), k4_plus ** -1, True)
    C5 = Circle(np.real(zm), np.imag(zm), k4_minus ** -1, True)

    return [C4, C5]


def print_circle_object(circle):
    """"""
    print(circle)
    for attr in dir(circle):
        print(f"{attr}: {getattr(circle, attr)}")


def draw_circles(circles):
    """Plot a list of circle objects."""

    fig, ax = plt.subplots()
    for c in circles:
        # print(c)
        circle = patches.Circle(
            (c.x, c.y), radius=c.r, color="blue", fill=True, alpha=0.5
        )
        ax.add_patch(circle)

    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_aspect("equal", adjustable="box")  # Ensures the circle is round
    plt.show()

    return


initial_circles = generate_initial_circles()
c1, c2, c3 = initial_circles

print("\n\nInitial circles:")
for circle in initial_circles:
    print(circle)

c4, c5 = compute_tangent_circles(c1, c2, c3)
print(f"c4 is:  {c4}")
print(f"c5 is:  {c5}")

draw_circles([c1, c2, c3, c4, c5])
c6, c7 = compute_tangent_circles(c1, c2, c4)


draw_circles([c1, c2, c3, c4, c5, c6, c7])
