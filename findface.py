import faiss
import numpy as np
import os
import face_recognition

faces_directory = "faces/"

def get_face_embeddings(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)
    return face_encodings[0] if face_encodings else None


database_embeddings = []
image_paths = []
for file_name in os.listdir(faces_directory):
    image_path = os.path.join(faces_directory, file_name)
    embedding = get_face_embeddings(image_path)
    if embedding is not None:
        database_embeddings.append(embedding)
        image_paths.append(image_path)

# Преобразование списка эмбеддингов в numpy массив
database_embeddings = np.array(database_embeddings).astype('float32')

# Создание индекса с помощью Faiss
d = database_embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(database_embeddings)

new_image_path = "new_user_photo.jpg"
new_embedding = get_face_embeddings(new_image_path)

if new_embedding is not None:
    new_embedding = np.array([new_embedding]).astype('float32')

    k = 3
    distances, indices = index.search(new_embedding, k)

    if distances[0][0] < 0.7:
        print(f"Найдено совпадение: {image_paths[indices[0][0]]} с расстоянием: {distances[0][0]}")
    else:
        print("Совпадение не найдено.")
else:
    print("Лицо не распознано на изображении.")
