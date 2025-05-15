import re

chuoi = input("Nhập chuỗi: ")

# Tìm tất cả các số nguyên (cả âm và dương)
so_nguyen = re.findall(r'-?\d+', chuoi)

# Chuyển các chuỗi số thành số nguyên
so_nguyen = [int(num) for num in so_nguyen]

tong_duong = 0
tong_am = 0

# Duyệt qua từng số để cộng vào tổng tương ứng
for num in so_nguyen:
    if num >= 0:
        tong_duong += num
    else:
        tong_am += num

print("Giá trị dương:", tong_duong)
print("Giá trị âm:", tong_am)
