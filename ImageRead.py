from PIL import Image
import numpy as np
import math
from decimal import Decimal, getcontext

class ImageRead():
    """sumary_line
    
    Keyword arguments:
    path: 图片地址
    black_price: 黑色价格
    color_price: 彩色价格
    black_up_price: 黑色递增价格
    color_up_price: 彩色递增价格
    Return: return_description
    """
    
    def __init__(self, path: str, black_down_price: str, color_down_price: str, black_up_price: str, color_up_price: str, is_world: bool = False):
        getcontext().prec = 28

        self.img_array = np.array(Image.open(path).convert('RGB'))
        self.width, self.height = self.img_array.shape[1], self.img_array.shape[0]
        self.black_down_price = Decimal(black_down_price)
        self.color_down_price = Decimal(color_down_price)
        self.black_up_price = Decimal(black_up_price)
        self.color_up_price = Decimal(color_up_price)

        if is_world: self.corpped_img()

        self.compute_colors_normal()
        self.compute_pirce()

    def compute_colors_normal(self):
        # self.null_count = np.sum(np.all(self.img_array == [70, 70, 70], axis=-1))
        self.total_pixels = self.img_array.shape[0] * self.img_array.shape[1]
        # 颜色数量
        self.black_count = np.sum(np.all(self.img_array == [0, 0, 0], axis=-1))
        self.white_count = np.sum(np.all(self.img_array == [255, 255, 255], axis=-1))
        self.color_count = self.total_pixels - self.black_count - self.white_count

        # 颜色覆盖率
        self.black_per = self.black_count / self.total_pixels * 100
        self.color_per = self.color_count / self.total_pixels * 100
        self.all_per = self.black_per + self.color_per
    
    def corpped_img(self):
        white = [255, 255, 255] # 定义白色像素

        white_pixels = np.where(np.all(self.img_array == white, axis=-1)) # 查找所有的白色像素

        if white_pixels[0].size > 0: # 确定图片的左上角和右下角
            top = white_pixels[0][0]
            left = white_pixels[1][0]
            bottom = white_pixels[0][-1]
            right = white_pixels[1][-1]
        else:
            top, left, bottom, right = None, None, None, None
        
        self.img_array = self.img_array[top:bottom, left: right] # 裁剪图片
        
        self.height, self.width = self.img_array.shape[0], self.img_array.shape[1]
    
    def compute_pirce(self):
        self.black_price = Decimal('0.0')
        self.color_price = Decimal('0.0')

        if self.black_per != 0:
            if self.black_per <= 5: self.black_price = self.black_down_price
            else: self.black_price = Decimal(str(self.black_per - 5)) * self.black_up_price + self.black_down_price

        if self.color_per != 0:
            if self.color_per <= 5: self.color_price = self.color_down_price
            else: self.color_price = Decimal(str(self.color_per - 5)) * self.color_up_price + self.color_down_price


        self.all_price = self.black_price + self.color_price



if __name__ == '__main__':

    ir = ImageRead('./Img/1.bmp', black_down_price=0.2, color_down_price=0.5, black_up_price=0.1, color_up_price=0.2)
    print(f'图片尺寸：{ir.height}, {ir.width}')
    print(f'总覆盖率：{ir.all_per}')
    print(f'黑覆盖率：{ir.black_per}')
    print(f'彩覆盖率：{ir.color_per}')
    print(f'黑色费用：{ir.black_price}')
    print(f'彩色费用：{ir.color_price}')
    print(f'总费用：{ir.all_price}')
    print('------')
    print(f'黑色数量：{ir.black_count}')
    print(f'白色数量：{ir.white_count}')
    print(f'彩色数量：{ir.color_count}')
    print(f'颜色总数：{ir.total_pixels}')