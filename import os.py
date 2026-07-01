import os
import cv2
import numpy as np

# === CONFIGURATION ===
video_input_path = "input_video.mp4"  # <-- Change this to your video file
output_dir = "Video Images"
os.makedirs(output_dir, exist_ok=True)

# === ENCRYPTION PROCESS ===
cam = cv2.VideoCapture(video_input_path)
frame_rate = int(cam.get(cv2.CAP_PROP_FPS))
frame_count = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Convert to grayscale and normalize
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(float) / 255.0

    # Generate encryption key
    key = np.random.normal(0, 0.1, gray.shape) + np.finfo(float).eps

    # Encrypt: divide by key
    encrypted = gray / key

    # Save encrypted frame
    frame_filename = os.path.join(output_dir, f"frame_{frame_count}.jpg")
    key_filename = os.path.join(output_dir, f"key_{frame_count}.npy")
    cv2.imwrite(frame_filename, np.clip(encrypted * 255, 0, 255).astype(np.uint8))

    # Save key
    np.save(key_filename, key)

    frame_count += 1

cam.release()
print(f"Encryption complete. Total frames encrypted: {frame_count}")

# === DECRYPTION PROCESS ===
for i in range(frame_count):
    encrypted_img_path = os.path.join(output_dir, f"frame_{i}.jpg")
    key_path = os.path.join(output_dir, f"key_{i}.npy")

    # Load encrypted frame and key
    encrypted = cv2.imread(encrypted_img_path, cv2.IMREAD_GRAYSCALE).astype(float) / 255.0
    key = np.load(key_path)

    # Decrypt: multiply by key
    decrypted = encrypted * key
    decrypted_display = np.clip(decrypted * 255, 0, 255).astype(np.uint8)

    # Display decrypted frame
    cv2.imshow("Decrypted Frame", decrypted_display)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
