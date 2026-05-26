import cv2
import piexif
import geocoder
import piexif.helper
from datetime import datetime

# Function to convert decimal GPS coordinates to EXIF format
def convert_to_exif_gps(coord):
    d = int(coord)
    m = int((coord - d) * 60)
    s = (coord - d - m / 60) * 3600
    return [(d, 1), (m, 1), (int(s * 100), 100)]  # Exif format (deg, min, sec)

# Get GPS Coordinates (Replace with actual GPS module if available)
g = geocoder.ip('me')  # Uses IP-based geolocation
latitude, longitude = g.latlng

# Capture Image from Webcam
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)
cap.release()

# Create EXIF metadata with GPS
exif_dict = {"GPS": {
    piexif.GPSIFD.GPSLatitudeRef: "N" if latitude >= 0 else "S",
    piexif.GPSIFD.GPSLatitude: convert_to_exif_gps(abs(latitude)),
    piexif.GPSIFD.GPSLongitudeRef: "E" if longitude >= 0 else "W",
    piexif.GPSIFD.GPSLongitude: convert_to_exif_gps(abs(longitude)),
    piexif.GPSIFD.GPSMapDatum: piexif.helper.UserComment.dump(f"Captured on {datetime.now()}")
}}

# Insert GPS metadata into image
exif_bytes = piexif.dump(exif_dict)
piexif.insert(exif_bytes, image_path)

print(f"Image saved with GPS location: {latitude}, {longitude}")
