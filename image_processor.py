import os;
import random;
import cv2;
import numpy as np;

clear = lambda:os.system('cls');

def main():
    path, img = ask_path();
    clear();
    show_info(img);

    while True:
        print("\nЧто сделать?");
        print("1 – Применить эффект")
        print("2 – Сохранить изображение");
        choice = input("Ваш выбор: ").strip();
        if choice == "1":
            clear();
            print("\nДоступные эффекты:");
            for k, (descr,_) in Effects.items():
                print(f"{k} – {descr}");
            try:
                eff = int(input("Номер эффекта: "));
                if eff not in Effects:
                    raise ValueError;
            except ValueError:
                print("Нет такого эффекта.");
                continue;
            img = Effects[eff][1](img)
            print("Эффект применён.");
        elif choice == "2":
            while True:
                name = input("Имя файла для сохранения (с расширением .png/.jpg и т.д.): ").strip();
                try:
                    cv2.imwrite(name, img);
                    print(f"Сохранено как {name}");
                    break;
                except Exception as e:
                    print("Не удалось сохранить:", e, "– попробуйте другое имя.");
            break;
        else:
            print("Нужно ввести 1 или 2.");

def ask_path():
    while True:
        path = input("Введите путь к изображению: ").strip();
        if not os.path.isfile(path):
            print("Файл не найден. Попробуйте ещё раз.");
            continue;
        img = cv2.imread(path);
        if img is None:
            print("Не удалось загрузить изображение (возможно, это не картинка).");
            continue;
        return path, img;

def show_info(img):
    h, w, d = img.shape;
    print(f"Параметры изображения: высота={h}, ширина={w}, глубина={d}, тип={img.dtype}");

def to_gray(img):
    h, w, d = img.shape;
    gray = np.zeros((h, w), dtype=np.uint8);
    for y in range(h):
        for x in range(w):
            gray[y, x] = int(np.mean(img[y, x]));
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR);

def flip_v(img):
    h, w, d = img.shape;
    flipped = np.zeros_like(img);
    for y in range(h):
        flipped[y] = img[h - 1 - y];
    return flipped;

def flip_h(img):
    h, w, d = img.shape;
    flipped = np.zeros_like(img);
    for y in range(h):
        for x in range(w):
            flipped[y, x] = img[y, w - 1 - x];
    return flipped;

def random_square(img):
    h, w, d = img.shape;
    color = input("Введите цвет в формате B,G,R (например, 0,0,255 для красного): ");
    try:
        b, g, r = map(int, color.split(","));
        color_np = np.array([b, g, r], dtype=np.uint8);
    except Exception:
        print("Неправильный цвет, будет использован белый.");
        color_np = np.array([255, 255, 255], dtype=np.uint8);

    size = 50;
    start_y = random.randint(0, h - size);
    start_x = random.randint(0, w - size);
    res = img.copy();
    for y in range(start_y, start_y + size):
        for x in range(start_x, start_x + size):
            res[y, x] = color_np;
    return res;

def add_noise(img):
    h, w, d = img.shape;
    res = img.copy();
    total = h * w;
    noise_count = int(0.1 * total);
    for _ in range(noise_count):
        y = random.randint(0, h - 1);
        x = random.randint(0, w - 1);
        res[y, x] = np.random.randint(0, 256, size=3, dtype=np.uint8);
    return res;

def change_brightness(img):
    try:
        beta = int(input("На сколько изменить яркость? (от -255 до 255): "));
    except ValueError:
        beta = 30;
    h, w, d = img.shape;
    res = np.zeros_like(img);
    for y in range(h):
        for x in range(w):
            for c in range(d):
                val = int(img[y, x, c]) + beta;
                val = max(0, min(255, val));
                res[y, x, c] = val;
    return res;

def blur_manual(img):
    h, w, d = img.shape;
    res = np.zeros_like( img );
    for c in range(d):
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                patch = img[y - 1:y + 2, x - 1:x + 2, c];
                res[y, x, c] = int(np.mean(patch));
    res[0, :] = img[0, :];
    res[-1, :] = img[-1, :];
    res[:, 0] = img[:, 0];
    res[:, -1] = img[:, -1];
    return res;

Effects = {
    1: ("Сделать ч/б", to_gray),
    2: ("Отразить по вертикали", flip_v),
    3: ("Отразить по горизонтали", flip_h),
    4: ("Закрасить случайный квадрат", random_square),
    5: ("Добавить шум", add_noise),
    6: ("Изменить яркость", change_brightness),
    7: ("Размытие (blur)", blur_manual),
}

main();