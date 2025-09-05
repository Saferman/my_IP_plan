def generate_tree(height=5):
    for i in range(height):
        print(" " * (height - i) + "*" * (2 * i + 1))
    print(" " * (height) + "|")  
generate_tree(10)