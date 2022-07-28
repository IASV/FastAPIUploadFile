from fastapi import FastAPI, HTTPException, status
from fastapi import Form, File, UploadFile
import os
import time

app = FastAPI()

@app.get("/")
def home():
    return {"home"}

@app.post("/contact")
async def contact(subject: str = Form(...), msg: str = Form(...)):
    return {
        "subject": subject,
        "message": msg
    }

@app.post("/create_user")
async def create_user(username: str = Form(...), password: str = Form(...), photo: UploadFile = File(...)):
    if photo.content_type != 'image/jpeg':
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Only valid images with format jpg'
        )
    
    await save_image(photo)
    
    return {
        "username": username,
        "password": password,
        "photo": {
            'filename': photo.filename,
            'content_type': photo.content_type
        }
    }
    
async def save_image(photo):
    temp_folder = './temp'
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
        
    content = await photo.read()
    
    print(f'{temp_folder}/{time.time()}.jpg')
    with open(f'{temp_folder}/{time.time()}.jpg', 'wb') as f:
        f.write(content)