import face_recognition
from PIL import Image

names = ["arjun", "biden"]

for name in names:
    print(name)
index = int(input("Enter the index of the person you want to verify: "))


id_path = (
    "C:/Users/arjun/Desktop/Deltahacks stuff/face_verification/face_verification_images/"
    + names[index]
    + "1"
    + ".jpg"
)
photo_path = (
    "C:/Users/arjun/Desktop/Deltahacks stuff/face_verification/face_verification_images/"
    + names[index]
    + "2"
    + ".jpg"
)

Image.open(id_path).show()
Image.open(photo_path).show()

id_image = face_recognition.load_image_file(id_path)
id_image_encoding = face_recognition.face_encodings(id_image)[0]

camera_image = face_recognition.load_image_file(photo_path)
camera_image_encoding = face_recognition.face_encodings(camera_image)[0]

results = face_recognition.compare_faces([id_image_encoding], camera_image_encoding)

if results:
    print("They are the same person!")
else:
    print("They are not the same person!")
