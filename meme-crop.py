#!/usr/bin/env python3
"""
meme-crop - 自动裁剪表情包
自动检测灰色背景，裁剪中间的非背景区域
"""

import sys
import os
from PIL import Image
from datetime import datetime
from collections import deque


def detect_background_color(img):
    """取四角像素作为背景色"""
    w, h = img.size
    corners = [
        img.getpixel((0, 0)),
        img.getpixel((w - 1, 0)),
        img.getpixel((0, h - 1)),
        img.getpixel((w - 1, h - 1)),
    ]
    r = sum(c[0] for c in corners) // 4
    g = sum(c[1] for c in corners) // 4
    b = sum(c[2] for c in corners) // 4
    return (r, g, b)


def find_largest_component(img, bg_color, threshold=50):
    """用 BFS 找到最大的连通区域"""
    w, h = img.size
    pixels = img.load()
    visited = [[False] * w for _ in range(h)]
    
    def is_content(x, y):
        if visited[y][x]:
            return False
        p = pixels[x, y]
        diff = abs(p[0] - bg_color[0]) + abs(p[1] - bg_color[1]) + abs(p[2] - bg_color[2])
        return diff > threshold
    
    def bfs(start_x, start_y):
        queue = deque([(start_x, start_y)])
        visited[start_y][start_x] = True
        min_x, min_y = start_x, start_y
        max_x, max_y = start_x, start_y
        count = 0
        
        while queue:
            x, y = queue.popleft()
            count += 1
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y
            
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and is_content(nx, ny):
                    visited[ny][nx] = True
                    queue.append((nx, ny))
        
        return (min_x, min_y, max_x + 1, max_y + 1), count
    
    best_bbox = None
    best_count = 0
    
    for y in range(h):
        for x in range(w):
            if is_content(x, y):
                bbox, count = bfs(x, y)
                if count > best_count:
                    best_count = count
                    best_bbox = bbox
    
    return best_bbox


def crop_meme(input_path, output_dir=None, padding=3, threshold=50):
    """自动裁剪表情包"""
    img = Image.open(input_path).convert('RGB')
    
    bg_color = detect_background_color(img)
    print(f"检测到背景色: RGB{bg_color}")
    
    bbox = find_largest_component(img, bg_color, threshold)
    if bbox is None:
        print("未找到内容区域")
        return None
    
    x1, y1, x2, y2 = bbox
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(img.width, x2 + padding)
    y2 = min(img.height, y2 + padding)
    
    cropped = img.crop((x1, y1, x2, y2))
    
    if output_dir is None:
        output_dir = os.path.expanduser(f"~/Pictures/表情包_{datetime.now().strftime('%Y%m%d')}")
    os.makedirs(output_dir, exist_ok=True)
    
    existing = [f for f in os.listdir(output_dir) if f.endswith('.png')]
    count = len(existing) + 1
    output_path = os.path.join(output_dir, f"{count:02d}_表情包.png")
    
    cropped.save(output_path, 'PNG')
    print(f"已保存: {output_path}")
    print(f"尺寸: {cropped.width}x{cropped.height}")
    
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: meme-crop <input> [output_dir] [padding] [threshold]")
        print("示例: meme-crop photo.jpg ~/Pictures/表情包_20260928 3 50")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    padding = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    threshold = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    
    crop_meme(input_path, output_dir, padding, threshold)
