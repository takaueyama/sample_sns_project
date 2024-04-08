import jpholiday
import datetime
import random
import numpy as np
from models import ShiftDay, Staff
from making_shift_utils2 import prepare_shift_days, calculate_shift, shift_pattern_counter

AKE = 0
YAKIN = 1
NIKKINN = 2
YASUMI = 3

# テスト用のスタッフを作成
shift_pattern = [YAKIN, NIKKINN, YASUMI, AKE]    
name_pool = ["佐藤", "山田", "朝倉", "斎藤", "渡辺", "堀口", "堀江", "グスタボ", "マッキー", "浜辺", "湊", "宝鐘", "かなえる", "樋口", "白石", "小坂", "与田", "設楽", "フリーレン"]
last_name_pool = ["佐藤", "山田", "朝倉", "斎藤", "渡辺", "堀口", "堀江", "浜辺", "湊", "宝鐘", "樋口", "白石", "小坂", "与田", "設楽"]
first_name_pool = ['太郎', '未来', '海', '裕', '祐介', '旬', '智也', 'ジョン', 'ジョニー', 'ニック', 'タイラー', '信之', '太子', '信長']
test_staffs = []
test_point = [1,2, 1.1, 1.0, 0.8, 0.7]

test_staffs2 = []
test_staff2_id = 0

# テスト用のシフトを作成
# 夜勤が普通回数で、ポイントが1.0、5人
for i in range(5):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 1.0, False, 3, 20, 7, 0, test_staff2_id)
    test_staffs2.append(staff)
    test_staff2_id += 1

# 昨日が夜勤
for i in range(2):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 1.0, False, 1, 20, 7, 0, test_staff2_id)
    test_staffs2.append(staff)
    test_staff2_id += 1

# 夜勤が普通回数で、ポイントが0.7、5人
for i in range(5):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 0.7, False, 3, 20, 7, 0, test_staff2_id)
    test_staffs2.append(staff)
    test_staff2_id += 1

# 昨日が夜勤
for i in range(1):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 0.7, False, 1, 20, 7, 0, test_staff2_id)
    test_staffs2.append(staff)
    test_staff2_id += 1

# 夜勤が少な目で、ポイントが1.0、6人
for i in range(6):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 1.0, True, 3, 20, 3, 0, test_staff2_id)
    test_staffs2.append(staff)
    test_staff2_id += 1

# 夜勤なしで、ポイントが1.0、3人
for i in range(3):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 1.0, False, 3, 20, 0, 0, test_staff2_id)
    test_staffs2.append(staff)
    test_staff2_id += 1

# 夜勤なしで、ポイントが0.7、2人
for i in range(2):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 0.7, False, 3, 20, 0, 0, test_staff2_id)
    test_staffs2.append(staff)
    test_staff2_id += 1

# シフトの開始日と終了日を設定
start_date = datetime.date(2024, 4, 21)
end_date = datetime.date(2024, 5, 20)

# テスト用のシフトの日付の範囲を用意
test_shift_days = prepare_shift_days(start_date, end_date)

# test_staffs2を表示する
# for staff in test_staffs2:
#     print(str(staff.id) + ': ' + str(staff) + ', ポイント: ' + str(staff.point) + ', max夜勤: ' + str(staff.max_night_shift_count))
# exit()

# テスト用のシフトを作成
# while True:
#     try:
#         calculated_shift = calculate_shift(test_shift_days, test_staffs2)
#         break
#     except Exception as e:
#         print(e)

calculated_shift = calculate_shift(test_shift_days, test_staffs2)

print(calculated_shift)


shift_list = ['明け', '夜勤', '日勤', '休み']

#表状にシフトを出力する
print('        ', end='')
for staff in test_staffs2:
    print(str(staff.id) + '　', end='')

print('')
print('--------------------')

for i in range(len(test_shift_days)):
    print(str(test_shift_days[i])[-5:] + ': ', end='')
    for j in range(len(test_staffs2)):
        staff = test_staffs2[j]
        print(shift_list[int(calculated_shift[i][j])][0] + '  ', end='')
    print('\n')

for staff in test_staffs2:
    shift_pattern = shift_pattern_counter(calculated_shift, staff)
    print(str(staff.id) + ': ' + '出勤:' + str(shift_pattern[4]) + ', 日勤：' + str(shift_pattern[NIKKINN]) + ', 夜勤：' + str(shift_pattern[YAKIN]) + ', 明け：' + str(shift_pattern[AKE]) + ', 休み：' + str(shift_pattern[YASUMI]))


# # test_staffs2を表示する
# for staff in test_staffs2:
#     print(str(staff.id) + ': ' + str(staff) + ', ポイント: ' + str(staff.point) + ', max夜勤: ' + str(staff.max_night_shift_count))