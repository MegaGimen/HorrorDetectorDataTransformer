import os
import json
import shutil
from tqdm import tqdm
# 设置路径
image_dir = r'dataset\2390241_1747984261\Images'
annotation_file = r'dataset\2390241_1747984261\Annotations\coco_info.json'
output_dir = r'outputs'

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 读取 COCO 标注文件
with open(annotation_file, 'r', encoding='utf-8') as f:
    coco = json.load(f)

# 获取标签为 1 的所有图像 ID
image_ids_with_label_1 = set(
    ann['image_id'] for ann in coco['annotations'] if ann['category_id'] == 1
)

# 获取图像 ID 到文件名的映射
id_to_filename = {img['id']: img['file_name'] for img in coco['images']}

# 提取并复制图像
for image_id in tqdm(image_ids_with_label_1):
    if image_id in id_to_filename:
        filename = id_to_filename[image_id]
        src_path = os.path.join(image_dir, filename)
        dst_path = os.path.join(output_dir, filename)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
        else:
            print(f"Image not found: {src_path}")

print("Done.")
