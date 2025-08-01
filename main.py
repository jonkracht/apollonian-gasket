import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import pickle


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
        return f"Circle with radius {round(self.r, 2)} centered at ({round(self.x, 2)}, {round(self.y, 2)} {self.k})"


def generate_initial_circles(R=100):
    """Circles with which to instantiate fractal."""

    c1 = Circle(0, 0, R, False)  # bounding circle
    
    # Equally-divided
    #c2, c3 = Circle(-50, 0, 50, True), Circle(50, 0, 50, True)

    # Unequal sizes
    #c2, c3 = Circle(-40, 0, 60, True), Circle(60, 0, 40, True)

    # Randomized radius and angle
    r2, theta = random.uniform(20, 90), random.uniform(0, 2*np.pi)
    r3 = R - r2

    c2 = Circle((R-r2)*np.cos(theta), (R-r2)*np.sin(theta), r2, True) 
    c3 = Circle((R - r3)*np.cos(theta + np.pi), (R - r3)*np.sin(theta + np.pi), r3, True)

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
            (c.x, c.y), radius=c.r, color="red", fill=True, alpha=0.3
        )
        ax.add_patch(circle)

    window = 100
    ax.set_xlim(-window, window)
    ax.set_ylim(-window, window)
    ax.set_aspect("equal", adjustable="box")  # Ensures the circle is round
    ax.set_title(title, size = 30)
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

    k4_1 = sum_term - sqrt_term
    k4_2 = sum_term + sqrt_term

    # Compute circles' centers
    # print("\n*** Computing circles' centers ***")
    z_sum_term = C1.kz + C2.kz + C3.kz
    z_sqrt_term = 2 * np.sqrt(C1.kz * C2.kz + C1.kz * C3.kz + C2.kz * C3.kz)

    z1 = (z_sum_term + z_sqrt_term) / k4_1
    z2 = (z_sum_term - z_sqrt_term) / k4_1
    z3 = (z_sum_term + z_sqrt_term) / k4_2  
    z4 = (z_sum_term - z_sqrt_term) / k4_2

    C4 = Circle(np.real(z1), np.imag(z1), k4_1 ** -1, True)
    C5 = Circle(np.real(z2), np.imag(z2), k4_1 ** -1, True)
    C6 = Circle(np.real(z3), np.imag(z3), k4_2 ** -1, True)
    C7 = Circle(np.real(z4), np.imag(z4), k4_2 ** -1, True)

    return [C4, C5, C6, C7]


def print_triple(triple, msg):
    print(f"\n{msg}")
    for t in triple:
        print(f" * {t}")

    return

def are_circles_tangent(c1, c2, eps=0.1):
    """Determine if two circles are tangent to one another."""

    # Compute distance between circles' centers
    d = np.sqrt((c1.x - c2.x)**2 + (c1.y - c2.y)**2)

    # Circles abut
    if d - (c1.r + c2.r) < eps:
        return True

    # One circle inside another
    if d - abs(c1.r - c2.r) < eps:
        return True

    return False
    

def valid_circle(circle, triple):
    valid = True

    if circle.r < 0:
        return False

    if circle.x ** 2 + circle.y ** 2 > 100 ** 2:        
        return False

    for t in triple:
        if are_circles_tangent(circle, t):
            continue
        else:
            return False

    return valid

def save_option(circles):
    if input("\nSave file?  ") == 'y':
        name = input("Enter file name:  ")
        save_file = open("./data/" + name, 'ab')
        pickle.dump(circles, save_file)
        save_file.close()
    return
 

def main(): 
    
    circles = generate_initial_circles()
    generation = 0

    #draw_circles(circles, [], f"Generation {generation}")

    triples = [circles.copy()]

    #print_triple(triples[0], "Initial configuration:")

    while generation < 8:

        generation += 1

        new_circles, new_triples = [], []
        #print(60 * '*')
        
        for triple in triples:

            #print_triple(triple, "Triple under consideration:")

            tangent_circles = compute_tangent_circles(triple)

            for candidate in tangent_circles:

                #print(f"\nCandidate:  {candidate}")

                if not valid_circle(candidate, triple):
                    continue

                # Check if candidate was already found
                eps = 0.1
                new_circle = True
                for c in circles:
                    if abs(c.x - candidate.x) < eps and abs(c.y - candidate.y) < eps and abs(c.r - candidate.r) < eps:
                        new_circle = False
                 
                if new_circle:
                    circles.append(candidate)
                    new_circles.append(candidate)

                    new_triples.append([candidate, triple[0], triple[1]])
                    new_triples.append([candidate, triple[0], triple[2]])
                    new_triples.append([candidate, triple[1], triple[2]])

                else:
                    pass
                    #print("Circle existed previously.  Skipping.")

        
        #draw_circles(circles, new_circles, f"Generation {generation}")
        
        triples = new_triples
    
    #draw_circles(circles, [], "Generation")
    save_option(circles)
       
    return


if __name__ == "__main__":
    main()

