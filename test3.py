import cv2
import numpy as np
import geocoder
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Function to get GPS Coordinates
def get_gps_coordinates():
    g = geocoder.ip('me')  # Uses IP-based geolocation
    return g.latlng if g.latlng else (0.0, 0.0)

# Capture Image from Webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if ret:
    # Get GPS Coordinates and Current Time
    latitude, longitude = get_gps_coordinates()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    gps_text = f"Lat: {latitude:.6f}, Lon: {longitude:.6f}"
    
    # Convert OpenCV image to PIL format
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # Load Pushpin Icon
    try:
        pushpin = Image.open("static/img/pushpin.png").resize((30, 30))
    except:
        pushpin = None  # If icon is missing, continue without it

    # Define Box Position (Bottom Left)
    img_w, img_h = img_pil.size
    rect_w, rect_h = 350, 80  # Width and Height of GPS Box
    rect_x = 20  # Positioned at the left side
    rect_y = img_h - rect_h - 20  # Positioned near the bottom

    # Create Rounded Rectangle (White Background)
    radius = 20
    rectangle = Image.new("RGB", (rect_w, rect_h), (255, 255, 255))
    mask = Image.new("L", (rect_w, rect_h), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle((0, 0, rect_w, rect_h), radius, fill=255)

    # Paste Rectangle onto Image
    img_pil.paste(rectangle, (rect_x, rect_y), mask)

    # Load Font and Draw Text
    font = ImageFont.truetype("static/fonts/ARIAL.ttf", 20)
    text_x, text_y = rect_x + 50, rect_y + 10  # Offset for pushpin icon
    time_x, time_y = rect_x + 50, rect_y + 40  # Position time below GPS

    draw.text((text_x, text_y), gps_text, font=font, fill=(0, 0, 0))
    draw.text((time_x, time_y), f"Time: {current_time}", font=font, fill=(0, 0, 0))

    # Paste Pushpin Icon if Available
    if pushpin:
        img_pil.paste(pushpin, (rect_x + 10, rect_y + 15), pushpin)

    # Convert back to OpenCV format
    final_img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    # Save and Show Image
    output_path = "image_with_gps.jpg"
    cv2.imwrite(output_path, final_img)
    cv2.imshow("GPS Image", final_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f"Image saved: {output_path} with GPS overlay and time at bottom left")
else:
    print("Failed to capture image.")
