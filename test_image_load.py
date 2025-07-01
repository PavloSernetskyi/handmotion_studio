import cv2

img = cv2.imread("assets/beer_can.png", cv2.IMREAD_UNCHANGED)

if img is None:
    print("Image not found or failed to load.")
else:
    print("Image shape:", img.shape)
    cv2.imshow("Beer Can", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()