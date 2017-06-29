
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
# from io import StringIO
from io import BytesIO
import string


# linux系统中 你的字体文件存放的位置
font_path = 'Library/Fonts/Monaco.ttf'

# windows中字体文件的位置, 你可以从C:\Windows\Fonts中去找你想要的字体文件，注意ttf格式和ttc是不同的
#font_path = 'D:\python\mybbs02\Library\Fonts\Monaco.ttf'

# 生成几位数的验证码
number = 4

# 生成验证码图片的高度和宽度
size = (100, 30)

# 背景颜色，(0, 0, 0) 为黑色， (255, 255, 255)为白色
bg_color = (255, 255, 255)

# 字体颜色: 蓝色
font_color = (0, 0, 255)

# 干扰线颜色: 红色
line_color = (255, 0, 0)

# 是否要加入干扰线
draw_line = True

# 加入干扰线条数的上下限
line_number = (4, 9)


# 生成随机字符串用于绘制验证码图片
def gen_text():
    """ 从 字母+数字 组成的列表source中，随机挑选4个字符，拼接成我们需要的验证码字符串 """
    # string.ascii_letters 返回字母（大写+小写）
    source = list(string.ascii_letters)
    # 将0-9也添加到 列表source中
    for index in range(0, 10):
        source.append(str(index))
    # random.sample(squence, k) 从 指定序列 中 随机获取 指定长度 的片断
    # 将该4个字符拼接成一个字符串，并返回
    return ''.join(random.sample(source, number))  # number是生成验证码的位数


# 绘制干扰线的函数
# 传入用于操作图片的对象 draw 图片的宽度 图片的高度
def gene_line(draw, width, height):
    # random.randint(0,99) 随机获取一个整数
    # begin, end 随机生成起点和终点
    # 起点和终点是相对于图片的左手角的位移，故需要是二元素元组格式
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))

    # draw 是传入的一个用来操作图片的对象，draw.line()使用对象的line方法
    draw.line([begin, end], fill=line_color)


# 生成最终的验证码图片
def gene_code():
    # 获取验证码图片的宽度和高度
    width, height = size

    # 新建图片对象 指定mode  大小 背景颜色

    image = Image.new('RGBA', (width, height), bg_color)

    """
    Creates a new image with the given mode and size.

    :param mode: The mode to use for the new image. See:
       :ref:`concept-modes`.
    :param size: A 2-tuple, containing (width, height) in pixels.
    :param color: What color to use for the image.  Default is black.
       If given, this should be a single integer or floating point value
       for single-band modes, and a tuple for multi-band modes (one value
       per band).  When creating RGB images, you can also use color
       strings as supported by the ImageColor module.  If the color is
       None, the image is not initialised.
    :returns: An :py:class:`~PIL.Image.Image` object.
    """

    # 验证码的字体和字体大小
    # 创建字体对象（指定字体的路径，字体大小， ）
    font = ImageFont.truetype(font_path, 25, index=0)

    # ImageDraw.Draw(im, mode=None)
    # 创建一个可用来对image进行操作的对象。
    # 对所有即将使用ImageDraw中操作的图片都要先进行这个对象的创建。
    draw = ImageDraw.Draw(image)

    # 生产字符串
    text = gen_text()

    # 为验证码指定字体，然后获取指定字体后的大小
    # font.getsize(text) 返回一个二元素元组，为指定text在指定字体大小之后的size
    font_width, font_height = font.getsize(text)

    # 将字符串绘制到图片中，text(self, xy, text, fill=None, font=None, anchor=None,*args, **kwargs):
    # xy 绘制的起点（即相对于图片左上角的位移， 格式为2个元素的元组）
    # text 要绘制到图片的字符串
    # fill 要绘制的字提的颜色
    # font 要绘制的字体的字体类型
    draw.text(
        ((width - font_width) / 100, (height - font_height) / 4),
        text,
        font=font,
        fill=font_color
    )  # 填充字符串

    # 是否添加干扰线
    if draw_line:
        # 从指定的干扰线条数范围内获取本次要生成的干扰线的条数
        num = random.randint(*line_number)
        # 调用n次添加干扰线的函数
        for n in range(1, num):
            gene_line(draw, width, height)

    # 创建扭曲 比较复杂，可以不加图片扭曲；语法如下：
    # transform(self, size, method, data=None, resample=NEAREST, fill=1):
    # 参数解释：
    # size: The output size. 经过transform函数处理后输出的图片的大小
    # method ：有如下集中方法：参考： http://blog.csdn.net/icamera0/article/details/50706666
        # PIL.Image.EXTENT: (cut out a rectangular subregion) 切出一个矩形的子区域 ,可用于放大 缩小 镜像
        # PIL.Image.AFFINE: (affine transform) 仿射变换
            # 对当前的图像进行仿射变换，变换结果体现在给定尺寸的新图像中。
            # 变量data是一个6元组(a, b, c, d, e,f)，包含一个仿射变换矩阵的第一个两行。
            # 输出图像中的每一个像素（x，y），新值由输入图像的位置（ax + by + c, dx + ey + f）的像素产生，
            # 使用最接近的像素进行近似。这个方法用于原始图像的缩放、转换、旋转和裁剪。
        # PIL.Image.PERSPECTIVE:(perspective transform) 透视变换
        # PIL.Image.QUAD:(map a quadrilateral to a rectangle or)
        # PIL.Image.MESH:(map a number of source quadrilaterals)
    image = image.transform(
        (width + 20, height + 10),
        Image.AFFINE,
        (1, -0.6, 0, -0.1, 1, 0),
        Image.BILINEAR
    )

    # 滤镜 ImageFilter中调用哪个滤镜就实现哪种效果，这里调用的SMOOTH
    image = image.filter(ImageFilter.SMOOTH)

    # stream = StringIO()   # 内存中像文件一下读写str类型的数据
    stream = BytesIO()  # 在内存中向文件一样读写二进制类型的数据

    # img_data = image.tobytes()

    # 图像的保存分两种方式：
    # 方式一：指定文件名  image.save('file_name.jpg')
    # 方式二: 指定一个文件对象 save(self, fp, format=None, **params)
    # 方式二:必须提供扩展名（format）。详情见源码的解释.
    image.save(stream, 'gif')

    # 从obj中读取数据 stream.getvalue()
    img_data = stream.getvalue()

    # 释放内存

    stream.close()

    # 定义函数返回值
    # 生成验证码图片是返回给前端用户的，后端我们自己知道验证码的内容。
    return text, img_data

if __name__ == "__main__":
    # 如果只是单纯的想生成图片，修改一下gene_code()函数，传入文件名，然后向这样调用即可：
    # 保存验证码图片的 路径  和 文件名 注意windows系统和linux系统的不同
    # gene_code('D:\python\mybbs02', 'test_checkcode')

    gene_code()
