from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image


def floyd_steinberg_dithering(image):
    # Получаем размеры изображения
    width, height = image.size

    # Проходим по каждому пикселю изображения
    for y in range(height):
        for x in range(width):
            # Получаем цвет текущего пикселя
            old_pixel = image.getpixel((x, y))

            # Преобразуем цвет в оттенки серого, вычисляя среднее значение компонент цвета
            new_pixel = sum(old_pixel) // 3

            # Заменяем текущий пиксель на новый оттенок серого
            image.putpixel((x, y), (new_pixel, new_pixel, new_pixel))

            # Вычисляем ошибку квантования, основанную на разнице между исходным и новым значением цвета
            quant_error = old_pixel[0] - new_pixel

            # Распространяем ошибку квантования на соседние пиксели согласно матрице Флойда-Стейнберга
            # (7/16 ошибки к пикселю справа, 3/16 к пикселю слева снизу, 5/16 к пикселю снизу, 1/16 к пикселю справа снизу)
            if x < width - 1:
                image.putpixel((x + 1, y), (image.getpixel((x + 1, y))[0] + quant_error * 7 // 16,) * 3)
            if x > 0 and y < height - 1:
                image.putpixel((x - 1, y + 1), (image.getpixel((x - 1, y + 1))[0] + quant_error * 3 // 16,) * 3)
            if y < height - 1:
                image.putpixel((x, y + 1), (image.getpixel((x, y + 1))[0] + quant_error * 5 // 16,) * 3)
            if x < width - 1 and y < height - 1:
                image.putpixel((x + 1, y + 1), (image.getpixel((x + 1, y + 1))[0] + quant_error * 1 // 16,) * 3)

    # Возвращаем изображение с примененным эффектом дизеринга
    return image


root = Tk()
root.withdraw()

file_path = askopenfilename()

original_image = Image.open(file_path)

grayscale_image = floyd_steinberg_dithering(original_image.copy())

original_image.show(title="Original Image")
grayscale_image.show(title="Grayscale Image")

grayscale_image.save("grayscale_image.png")
