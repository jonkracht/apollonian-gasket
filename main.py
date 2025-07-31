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

    c1 = Circle(0, 0, 100, False)  # bounding circle
    
    # Equally-divided
    #c2, c3 = Circle(-50, 0, 50, True). Circle(50, 0, 50, True)

    # Unequal sizes
    c2, c3 = Circle(-40, 0, 60, True), Circle(60, 0, 40, True)

    return [c1, c2, c3]


def draw_circles(circles_1, circles_2, title):
    """Plot a list of circle objects."""

    fig, ax = plt.subplots(figsize=(15, 15))
    
    for c in circles_1:
        # print(c)
        circle = patches.Circle(
            (c.x, c.y), radius=c.r, color="blue", fill=True, alpha=0.1
        )
        ax.add_patch(circle)
    
    for c in circles_2:
        # print(c)
        circle = patches.Circle(
            (c.x, c.y), radius=c.r, color="red", fill=True, alpha=0.5
        )
        ax.add_patch(circle)


    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)
    ax.set_aspect("equal", adjustable="box")  # Ensures the circle is round
    ax.set_title(title)
    plt.axis("off")
    plt.show()

    return




def compute_tangent_circles(circle_list):
    """Takes three circle objects and returns both mutually tangent circles."""

    # print("\n*** Computing tangent circles ***")

    C1, C2, C3 = circle_list

    # Compute radii
    sum_term = C1.k + C2.k + C3.k

    # Handle negative numbers in square root
    val = C1.k * C2.k + C1.k * C3.k + C2.k * C3.k
    if val < 0:
        sqrt_term = 0
    else:
        sqrt_term = 2 * np.sqrt(val)

    # print(f"Sum term is:  {sum_term}")
    # print(f"Sqrt term is:  {sqrt_term}")

    k4_plus = sum_term - sqrt_term
    k4_minus = sum_term + sqrt_term

    # Compute circles' centers
    # print("\n*** Computing circles' centers ***")
    z_sum_term = C1.kz + C2.kz + C3.kz
    z_sqrt_term = 2 * np.sqrt(C1.kz * C2.kz + C1.kz * C3.kz + C2.kz * C3.kz)

    # print(f"Zsum term is:  {z_sum_term}")
    # print(f"Zsqrt term is:  {z_sqrt_term}")

    zp = (z_sum_term + z_sqrt_term) / k4_plus
    zm = (z_sum_term - z_sqrt_term) / k4_minus

    C4 = Circle(np.real(zp), np.imag(zp), k4_plus ** -1, True)
    C5 = Circle(np.real(zm), np.imag(zm), k4_minus ** -1, True)

    return [C4, C5]


def main(): 
    
    circles = generate_initial_circles()
    #draw_circles(circles, "Initial circles")

    triples = [circles.copy()]


    print(f"\nInitial triples:\n{triples}")

    while True:

        new_triples = []
        print(40 *'-')
        
        for triple in triples:

            print(f"\nTriple is of length {len(triple)}.")
            print(triple)

            tangent_circles = compute_tangent_circles(triple)

            #print(f"\nTangent circles:\n{tangent_circles}")

            for circle in tangent_circles:

                print(f"\nExamining candidate circle:  {circle}")

                # Check if circle is new
                eps = 0.1
                new_circle = True
                for c in circles:
                    if abs(c.x - circle.x) < eps and abs(c.y - circle.y) < eps and abs(c.r - circle.r) < eps:
                        new_circle = False
                 
                if new_circle:
                    circles.append(circle)

                    #print(circle)
                    #print(triple)

                    new_triples.append([circle, triple[0], triple[1]])
                    new_triples.append([circle, triple[0], triple[2]])
                    new_triples.append([circle, triple[1], triple[2]])

                    print(f"\nCircle triple:")
                    for c in triple:
                        print(c)

                    draw_circles(triple, [circle], "Mon")
                    #f = input()
        
        triples = new_triples

            


    return


if __name__ == "__main__":
    main()

