from blackout_faces import blackout_faces

img, face_count = blackout_faces("image.jpg", padding=0, output_path="censored.png")
print(f"Blacked out {face_count} face(s)")