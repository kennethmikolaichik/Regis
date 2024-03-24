import cv2

# Load the image
img = cv2.imread('path/to/your/image.jpg')

# Check if the image is loaded successfully
if img is not None:
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Display the original image
    cv2.imshow('Original Image', img)

    # Display the grayscale image
    cv2.imshow('Grayscale Image', gray)

    # Wait for a key press and then close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error: Image not loaded.")
