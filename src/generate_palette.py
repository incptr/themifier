from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import colorsys


def sort_by_hue(rgb_list):
    """
    Sort a list of RGB colors based on their hue values.

    :param rgb_list: List of RGB colors represented as tuples (R, G, B).
    :return: List of RGB colors sorted by hue value.
    """
    # Define a custom sorting key based on hue value
    def hue_key(rgb_color):
        # Convert RGB to HSV and return hue value
        hsv = colorsys.rgb_to_hsv(
            rgb_color[0] / 255.0, rgb_color[1] / 255.0, rgb_color[2] / 255.0)
        return hsv[0]

    # Sort the list of RGB colors based on hue key
    sorted_colors = sorted(rgb_list, key=hue_key)

    return sorted_colors


def generate_palette(image_path, num_colors=15):
    # Load the image
    image = Image.open(image_path)

    # Convert the image into numpy array
    image_np = np.array(image)

    # Reshape the array to 2D array
    pixels = image_np.reshape(-1, 3)
    for i, channels in enumerate(pixels):
        if (max(channels) - min(channels)) < 20:
            pixels[i] = [0, 0, 0]

    # Apply KMeans clustering to find dominant colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the cluster centers
    colors = kmeans.cluster_centers_

    # Convert the colors to integer values
    colors = colors.astype(int)
    return sort_by_hue(colors)
    # print(colors)
    # colors_filtered = []
    # for c in colors:
    #     if (max(c) - min(c)) > 0:
    #         colors_filtered.append(c)
    #
    # return colors_filtered


def plot_palette(colors):
    # Create a color palette image
    palette = np.zeros((50, len(colors)*50, 3), dtype=np.uint8)

    # Fill the palette with each color
    for i, color in enumerate(colors):
        palette[:, i*50:(i+1)*50] = color

    # Display the palette
    plt.imshow(palette)
    plt.axis('off')
    plt.show()


# Example usage
# Replace 'your_image.jpg' with the path to your image file
image_path = 'nordic.png'
num_colors = 15  # Number of colors in the palette

# Generate palette and plot it
palette = generate_palette(image_path, num_colors)
print("Generated Color Palette:")
print(palette)
plot_palette(palette)
