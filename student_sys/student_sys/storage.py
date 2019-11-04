# coding=utf-8
from PIL import Image, ImageDraw, ImageFont
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


class WatermarkStorage(FileSystemStorage):
    """
    自定义的Storage，基于文件系统的这个Storage来做的。
    其中，字体部分（fontfamily参数）可以由自己指定本地的字体文件路径
    """
    def save(self, name, content, max_length=None):
        """
        重写save(),把要保存的图片进行水印处理，接着再保存。
        """
        # 处理逻辑
        if 'image' in content.content_type:
            # 加水印
            image = self.watermark_with_text(content, 'Fnanshan', 'red')
            content = self.convert_image_to_file(image, name)

        return super().save(name, content, max_length=max_length)

    def convert_image_to_file(self, image, name):
        """
        把最终打上水印的图片对象Image转换为文件对象，也就是转换为我们引入的BytesIO对象
        """
        print('====== run convert_image_to_file ======')
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)

    def watermark_with_text(self, file_obj, text, color, fontfamily=None):
        """
        :param fontfamily: 可以由自己指定本地的字体文件路径
        """
        print('====== run watermark_with_text ======')
        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        x = (width - textWidth - margin) / 2    # 计算横轴位置
        y = height - textHeight - margin        # 计算纵轴位置
        draw.text((x, y), text, color, font)
        return image