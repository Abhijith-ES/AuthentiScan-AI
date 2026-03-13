import os
import time

UPLOAD_FOLDER = "backend/uploads"

def cleanup_old_files(max_age_seconds=600):
    now = time.time()

    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)

            if file_age > max_age_seconds:
                os.remove(file_path)