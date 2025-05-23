import os
import cv2
import random
from glob import glob
from PIL import Image
from tqdm import tqdm
# 文件夹路径
video_dir = "vids"
confuse_dir = "confuse"
output_dir = "outputs"

os.makedirs(output_dir, exist_ok=True)

def extract_frames(video_path, interval=0.5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    frames = []
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frames.append(frame)
        count += 1
    cap.release()
    return frames

def process_frame(frame):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert("RGBA")
    if random.random() < 0.7:
        confuse_images = glob(os.path.join(confuse_dir, '*'))
        if confuse_images:
            confuse_path = random.choice(confuse_images)
            confuse_img = Image.open(confuse_path).convert("RGBA")

            # 计算缩放比例，保持等比，缩放到原图最大边的1/5
            w, h = img.size
            max_dim = max(w, h)
            scale = (max_dim / 5) / max(confuse_img.width, confuse_img.height)
            new_size = (int(confuse_img.width * scale), int(confuse_img.height * scale))
            confuse_img = confuse_img.resize(new_size)

            # 随机粘贴位置
            x = random.randint(0, w - confuse_img.width)
            y = random.randint(0, h - confuse_img.height)
            img.paste(confuse_img, (x, y), confuse_img)
    return img.convert("RGB")

# 主流程
video_files = glob(os.path.join(video_dir, '*'))
img_count = 0

for video_path in video_files:
    frames = extract_frames(video_path, interval=0.5)
    for i, frame in tqdm(enumerate(frames)):
        processed_img = process_frame(frame)
        output_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(video_path))[0]}_frame{i}_{img_count}.jpg")
        processed_img.save(output_path)
        img_count += 1
