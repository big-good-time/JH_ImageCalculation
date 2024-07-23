from PIL import Image
import numpy as np
import math

class ImageRead():
    def __init__(self, path: str, black_down_price: float, color_down_price: float, black_up_price: float, color_up_price: float):
        self.img_array = np.array(Image.open(path).convert('RGB'))
        self.black_down_price = black_down_price
        self.color_down_price = color_down_price
        self.black_up_price = black_up_price
        self.color_up_price = color_up_price

        self.all_price = float(0)

        self.height, self.width = self.img_array.shape[0], self.img_array.shape[1]

        self.corpped_img()
        self.compute_colors()
        self.compute_price()
    
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
        
        self.corpped_array = self.img_array[top:bottom, left: right] # 裁剪图片
        
        self.new_height, self.new_width = self.corpped_array.shape[0], self.corpped_array.shape[1]
        
    
    def compute_colors(self):
        black = [0, 0, 0]
        white = [255, 255, 255]

        self.all_pixels = self.new_width * self.new_height

        self.black_count = np.sum(np.all(self.corpped_array == black, axis=-1))
        self.white_count = np.sum(np.all(self.corpped_array == white, axis=-1))
        self.color_count = self.all_pixels - self.black_count - self.white_count

        self.black_per = math.ceil(self.black_count / self.all_pixels * 100)
        self.color_per = math.ceil(self.color_count / self.all_pixels * 100)
        self.all_per = self.black_per + self.color_per
    
    def compute_price(self):
        if self.black_per <= 5: self.black_price = self.black_down_price
        else: self.black_price = (self.black_per - 5) * self.black_up_price + self.black_down_price

        if self.color_per <= 5: self.color_price = self.color_down_price
        else: self.color_price = (self.color_per - 5) * self.color_up_price + self.color_down_price

        if self.black_per == 0: self.black_price = 0
        if self.color_per == 0: self.color_price = 0

        self.all_price = self.black_price + self.color_price


if __name__ == '__main__':
    ir = ImageRead('./Img/1.bmp', black_down_price=0.2, color_down_price=0.5, black_up_price=0.1, color_up_price=0.2)
    print(f'图片尺寸：{ir.new_width}, {ir.new_height}')
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
    print(f'颜色总数：{ir.all_pixels}')
        