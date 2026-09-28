# meme-crop

自动裁剪表情包工具。针对手机截图中固定灰色背景、中间包含表情包图片的场景，自动检测背景色并裁剪出表情包本体。

## 原理

1. 取图片四角像素计算背景色
2. 用 BFS（广度优先搜索）找到与背景色差异超过阈值的最大连通区域
3. 自动加留白、裁剪、按序号命名输出

## 安装

```bash
# 依赖：Python 3 + Pillow
pip install Pillow

# 可选：安装到 PATH
cp meme-crop.py ~/.local/bin/meme-crop
chmod +x ~/.local/bin/meme-crop
```

## 用法

```bash
meme-crop <图片路径> [输出目录] [留白像素] [阈值]
```

### 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 图片路径 | 输入图片（必填） | - |
| 输出目录 | 裁剪结果保存位置 | `~/Pictures/表情包_日期/` |
| 留白像素 | 裁剪时边缘留白 | 3 |
| 阈值 | 与背景色的差异阈值 | 50 |

### 示例

```bash
# 基本用法
meme-crop photo.jpg

# 指定输出目录
meme-crop photo.jpg ~/Pictures/表情包

# 完整参数
meme-crop photo.jpg ~/Pictures/表情包 3 50
```

## 批量处理

```bash
for f in /path/to/images/*.jpg; do
    meme-crop "$f" ~/Pictures/表情包
done
```

## 输出

- 自动创建输出目录
- 按序号命名：`01_表情包.png`、`02_表情包.png`...
- 输出 PNG 格式，无损保存

## License

MIT
