import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import random



class InteractiveCircleSelector:
    def __init__(self, radius, kdtree):
        self.fig, self.ax = plt.subplots()
        self.kdtree = kdtree
        self.radius = radius
        self.ax.scatter(*zip(*points), color='blue')
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.ax.set_title(f"Please chose a center of circle with radius: {self.radius}")
        plt.show()

    def on_click(self, event):
        if event.button == 1 and event.inaxes == self.ax:
            x, y = float(event.xdata), float(event.ydata)
            kdtree.traverse_and_check_circle((x,y), self.radius)

class Node:
    def __init__(self, point, depth, left=None, right=None):
        self.point = point
        self.depth = depth
        self.left = left
        self.right = right


class KDTree:
    def __init__(self, points):
        self.root = self.build_kdtree(points)

    def build_kdtree(self, points, depth=0):
        if not points:
            return None

        k = len(points[0])
        axis = depth % k
        points.sort(key=lambda point: point[axis])
        median = len(points) // 2

        return Node(
            points[median],
            depth,
            self.build_kdtree(points[:median], depth + 1),
            self.build_kdtree(points[median + 1:], depth + 1)
        )

    def _distance(self, point1, point2):
        return sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2))

    def is_point_in_circle(self, center, radius, point):
        return self._check_point_in_circle(self.root, center, radius, point, 0)

    def _check_point_in_circle(self, node, center, radius, point, depth):
        if node is None:
            return False

        axis = depth % len(point)
        distance = (point[axis] - center[axis]) ** 2
        if point[axis] < center[axis]:
            if distance <= radius ** 2:
                return True
            return self._check_point_in_circle(node.left, center, radius, point, depth + 1)
        else:
            if distance <= radius ** 2:
                return True
            return self._check_point_in_circle(node.right, center, radius, point, depth + 1)

    def inorder_traversal(self):
        self._inorder_recursive(self.root)

    def _inorder_recursive(self, node):
        if node:
            self._inorder_recursive(node.left)
            print(node.point, end=" ")
            self._inorder_recursive(node.right)

    def preorder_traversal(self):
        self._preorder_recursive(self.root)

    def _preorder_recursive(self, node):
        if node:
            print(node.point, end=" ")
            self._preorder_recursive(node.left)
            self._preorder_recursive(node.right)

    def postorder_traversal(self):
        self._postorder_recursive(self.root)

    def _postorder_recursive(self, node):
        if node:
            self._postorder_recursive(node.left)
            self._postorder_recursive(node.right)
            print(node.point, end=" ")
    def draw_dots(self):

        self._draw_dots_recursive(self.root)

    def _draw_dots_recursive(self, node):
        if node:
            plt.scatter(node.point[0], node.point[1], color='blue')
            self._draw_dots_recursive(node.left)
            self._draw_dots_recursive(node.right)

    def draw_circle(self, center, radius):
        circle = plt.Circle(center, radius, color='red', fill=False)
        plt.gca().add_patch(circle)

    def print_tree(self):
        self._print_tree_recursive(self.root)

    def _print_tree_recursive(self, node, indent=""):
        if node:
            if node.left:
                self._print_tree_recursive(node.left, indent + "    ")
            print(indent + str(node.point))
            if node.right:
                self._print_tree_recursive(node.right, indent + "    ")

    def traverse_and_check_circle(self, center, radius):
        print(f"\n#############################################################################\n\t\tGets query for circle with {center=}, {radius=}\n#############################################################################")

        fig, ax = plt.subplots()

        self.draw_dots()

        self._traverse_and_check_circle_recursive(self.root, center, radius, ax)

        # Set the title and show the figure
        self.draw_circle(center, radius)
        ax.set_title(f"Query Circle: Center={center}, Radius={radius}")
        plt.grid()
        plt.show()

    def _traverse_and_check_circle_recursive(self, node, center, radius, ax):
        if node is None:
            return

        point = node.point

        if self._distance(point, center) <= radius ** 2:
            print(f"Point {point} is inside the circle.")
            ax.scatter(point[0], point[1], color='green')  # Paint the point in green
        print(f"Checking {point=}, {center=}, distance to center: {self._distance(point, center)}, {radius ** 2=}")

        axis = abs(node.depth % len(center))
        direction = "left/right"
        if axis == 1:
            direction = "up/down"

        msg = f"check if query region {direction} for {node.point} \n"
        print(msg)
        if center[axis] - radius <= node.point[axis]:
            if node.left is not None:
                print(f"We need to check left son {node.left.point}")
            self._traverse_and_check_circle_recursive(node.left, center, radius, ax)

        if node.point[axis] <= center[axis] + radius:
            if node.right is not None:
                print(f"We need to check right son {node.right.point}")
            self._traverse_and_check_circle_recursive(node.right, center, radius, ax)

def generate_random_dots(n):
    dots = []
    for _ in range(n):
        x = random.random() * 20  # Random x-coordinate between 0 and 1
        y = random.random() * 20 # Random y-coordinate between 0 and 1
        dots.append((x, y))
    return dots

def generate_random_circles(n):
    circles = []
    for _ in range(n):
        x = random.random() * 20  # Random x-coordinate between 0 and 1
        y = random.random() * 20 # Random y-coordinate between 0 and 1
        r = random.random() * 20  # Random y-coordinate between 0 and 1
        circles.append([(x, y), r])
    return circles

if __name__ == '__main__':
    points = [(0,5), (0.1, 0.9), (1.3, 0.5), (1.5, 3), (2.5, 3), (4, 2), (5,1)]
    circles = [[(2, 2), 2]]

    mode = -1
    while mode != 1 and mode != 0:
        mode = int(input("Enter 0 for manual input or 1 for automatic generation of points: "))

    n = int(input("Enter the number of points: "))
    m = int(input("Enter the number of circles: "))
    points = []

    circles = []

    if mode == 0:
        for i in range(n):
            x = float(input("Enter the x-coordinate for point {}: ".format(i + 1)))
            y = float(input("Enter the y-coordinate for point {}: ".format(i + 1)))
            points.append((x, y))
        for i in range(m):
            x = float(input("Enter the x-coordinate for circle center {}: ".format(i + 1)))
            y = float(input("Enter the y-coordinate for circle center {}: ".format(i + 1)))
            r = float(input("Enter the circle radius {}: ".format(i + 1)))
            circles.append([(x, y), r])
    elif mode == 1:
        points = generate_random_dots(n)
        circles = generate_random_circles(m)

    kdtree = KDTree(points)
    print(f"##############################################\n\t\tINIT POINTS:{points=}\n##########################################################################")
    print(f"##############################################\n\t\tINIT POINTS:{circles=}\n##########################################################################")

    points_in_circle = []
    for circle in circles:
        selector = InteractiveCircleSelector(circle[1], kdtree)
        kdtree.traverse_and_check_circle(circle[0], circle[1])

    plt.gca().set_aspect('equal', adjustable='box')

    plt.show()

