import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Node:
   
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
   
    def __init__(self):
        self.root = None

    def insert(self, key):
       
        if self.search(key):  # Check if the key already exists
            return  # Do not insert if the key is already present
        new_node = Node(key)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if key < current.val:
                    if current.left is None:
                        current.left = new_node
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        break
                    else:
                        current = current.right

    def search(self, key):
       
        return self._search(self.root, key)

    def _search(self, node, key):
        
        if node is None:
            return False
        if node.val == key:
            return True
        elif key < node.val:
            return self._search(node.left, key)  # Correctly search in left subtree
        else:
            return self._search(node.right, key)  # Correctly search in right subtree

    def delete(self, key):
       
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
     
        if node is None:
            return node
        if key < node.val:
            node.left = self._delete(node.left, key)
        elif key > node.val:
            node.right = self._delete(node.right, key)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node with two children: Get the inorder successor (smallest in the right subtree)
            min_larger_node = self._min_value_node(node.right)
            node.val = min_larger_node.val
            node.right = self._delete(node.right, min_larger_node.val)
        return node

    def _min_value_node(self, node):
       
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_positions(self):
       
        positions = {}
        self._get_positions(self.root, 0, 0, positions, 4)  # Start with a horizontal distance of 4
        return positions

    def _get_positions(self, node, x, y, positions, horizontal_distance):
       
        if node is not None:
            positions[node.val] = (x, y)
            self._get_positions(node.left, x - horizontal_distance, y - 1, positions, horizontal_distance / 2)
            self._get_positions(node.right, x + horizontal_distance, y - 1, positions, horizontal_distance / 2)

    def find_node(self, key):
       
        return self._find_node(self.root, key)

    def _find_node(self, node, key):
      
        if node is None or node.val == key:
            return node
        if key < node.val:
            return self._find_node(node.left, key)
        else:
            return self._find_node(node.right, key)

    def inorder_traversal(self):
      
        return self._inorder_traversal(self.root)

    def _inorder_traversal(self, node):
        
        return self._inorder_traversal(node.left) + [node.val] + self._inorder_traversal(node.right) if node else []

class SearchEngine:
   
    def __init__(self, master):
        self.master = master
        self.master.title("نمایش درخت جستجوی دودویی")
        self.master.geometry("800x600")
        self.master.configure(bg="#FFC0CB")  # Set background color to pink

        self.bst = BinarySearchTree()

        # Create UI elements
        self.setup_interface()

    def setup_interface(self):
      
        # Labels and Entry for data input
        self.label = tk.Label(self.master, text="عدد را وارد کنید:", bg="#FFC0CB")
        self.label.pack(pady=10)

        self.data_entry = tk.Entry(self.master)
        self.data_entry.pack(pady=5)

        # Button to add data
        self.add_button = tk.Button(self.master, text="اضافه کردن داده", command=self.add_data)
        self.add_button.pack(pady=5)

        # Button to delete data
        self.delete_button = tk.Button(self.master, text="حذف داده", command=self.delete_data)
        self.delete_button.pack(pady=5)

        # Label to display sorted data
        self.sorted_label = tk.Label(self.master, text="اعداد مرتب شده:", bg="#FFC0CB", font=("Arial", 14))
        self.sorted_label.pack(pady=10)

        # Frame for the sorted numbers text box and scrollbar
        self.sorted_frame = tk.Frame(self.master)
        self.sorted_frame.pack(pady=5)

        # Text box to display sorted numbers
        self.sorted_text = tk.Text(self.sorted_frame, height=5, width=50)
        self.sorted_text.pack(side=tk.LEFT)

        # Scrollbar for the text box
        self.scrollbar = tk.Scrollbar(self.sorted_frame, command=self.sorted_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the text box to use the scrollbar
        self.sorted_text.config(yscrollcommand=self.scrollbar.set)

        # Create a canvas for displaying the tree
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(pady=20)

        self.display_data()  # Initialize with an empty display

    def add_data(self):
       
        data = self.data_entry.get()
        if data.isdigit():
            self.bst.insert(int(data))
            self.data_entry.delete(0, tk.END)  # Clear entry field
            self.display_data()  # Automatically display data after adding
            self.update_sorted_display()  # Update sorted display

    def delete_data(self):
        
        data = self.data_entry.get()
        if data.isdigit():
            self.bst.delete(int(data))
            self.data_entry.delete(0, tk.END)  # Clear entry field
            self.display_data()  # Automatically display data after deleting
            self.update_sorted_display()  # Update sorted display

    def update_sorted_display(self):
        
        sorted_values = self.bst.inorder_traversal()
        self.sorted_text.config(state=tk.NORMAL)  # Enable editing
        self.sorted_text.delete(1.0, tk.END)  # Clear current text
        self.sorted_text.insert(tk.END, " ".join(map(str, sorted_values)))  # Insert sorted values
        self.sorted_text.config(state=tk.DISABLED)  # Make the text box read-only

    def display_data(self):
      
        # Clear the previous plot
        self.ax.clear()
        positions = self.bst.get_positions()

        # Plot nodes
        for key, (x, y) in positions.items():
            self.ax.scatter(x, y, s=500, c='lightblue', edgecolors='black', linewidth=2, alpha=0.8, zorder=2)
            self.ax.text(x, y, str(key), fontsize=12, ha='center', va='center', fontweight='bold')

        # Draw lines between nodes
        for key, (x, y) in positions.items():
            node = self.bst.find_node(key)  # Use the find_node method from BinarySearchTree
            if node:
                if node.left:
                    child_x, child_y = positions[node.left.val]
                    self.ax.plot([x, child_x], [y, child_y], 'k-', lw=2, alpha=0.5)  # Straight line
                if node.right:
                    child_x, child_y = positions[node.right.val]
                    self.ax.plot([x, child_x], [y, child_y], 'k-', lw=2, alpha=0.5)  # Straight line

        self.ax.axis('off')  # Remove axis for better visibility of the tree
        self.canvas.draw()  # Update the canvas

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = SearchEngine(root)
    root.mainloop()
