import jpholiday
import datetime
import random

AKE = 0
YAKIN = 1
NIKKINN = 2
YASUMI = 3

class Staff:
    def __init__(self, last_name, first_name, point, is_proper, last_day_shift_pattern,  max_shift_count, max_night_shift_count, current_shift_streak, id, current_off_day_count = 0, current_night_shift_count = 0, current_day_shift_count = 0, current_shift_count = 0):
        # 個人識別
        self.id = id
        self.last_name = last_name
        self.first_name = first_name

        # 基本は不変のもの
        self.point = point
        self.is_proper = is_proper

        # シフトを作る度に設定するもの
        self.max_night_shift_count = max_night_shift_count
        self.max_shift_count = max_shift_count

        # 状態
        # 前日の勤務形態(日勤、夜勤、明け、休み)
        self.last_day_shift_pattern = last_day_shift_pattern
        # 今の連続勤務日数
        self.current_shift_streak = current_shift_streak
        # 今シフトのトータル休み日数
        self.current_off_day_count = current_off_day_count
        # 今シフトのトータルの夜勤日数
        self.current_night_shift_count = current_night_shift_count
        # 今シフトのトータルの日勤日数
        self.current_day_shift_count = current_day_shift_count
        # 今シフトのトータル出勤日数
        self.current_shift_count = current_shift_count

    def __str__(self):
        return self.last_name + self.first_name

class ShiftDay:
    def __init__(self, day, day_point, night_point, day_people_count, night_people_count):
        # 日付
        self.day = day
        # 日勤に必要なポイント
        self.day_point = day_point
        # 夜勤に必要なポイント
        self.night_point = night_point
        # 日勤に必要な人数
        self.day_people_count = day_people_count
        # 夜勤に必要な人数
        self.night_people_count = night_people_count

    def __str__(self):
        return str(self.day)

def prepare_shift_days(start_date, end_date, normal_day_point=9, normal_night_point=2.5, holiday_day_point=1.7, holiday_night_point=2.5, normal_day_people_count=12, normal_night_people_count=3, holiday_day_people_count=2, holiday_night_people_count=3):
    # シフトデイの集合
    shift_days = []
    start_date = start_date
    end_date = end_date
    current_date = start_date

    while True:
        # 休日祝日の場合
        if current_date.weekday() >= 5 or jpholiday.is_holiday(current_date):
            shift_day = ShiftDay(current_date, holiday_day_point, holiday_night_point, holiday_day_people_count, holiday_night_people_count)
            shift_days.append(shift_day)
        # 平日の処理
        else:
            shift_day = ShiftDay(current_date, normal_day_point, normal_night_point, normal_day_people_count, normal_night_people_count)
            shift_days.append(shift_day)

        current_date = current_date + datetime.timedelta(days=1)

        if current_date == end_date:
            break
    
    return shift_days

def calculate_shift(shift_days, staffs):
    shift = dict()
    ans = dict()
    for shift_day in shift_days:
        # 日勤のスタッフプール
        nikkinn_pool = []

        # 夜勤のポイントが1以上のスタッフプール
        yakin_upper_1 = []

        # 夜勤のポイントが1未満のスタッフプール
        yakin_under_1 = []

        # 日勤に割り当たった人
        nikkin = []

        # 夜勤に割り当たった人
        yakin = []

        # 明けに割り当たった人
        ake = []

        # 休みに割り当たった人
        yasumi = []

        # 明けのシフトを確定させる
        for staff in staffs:
            if staff.last_day_shift_pattern == YAKIN:
                ake.append(staff)

        # スタッフの条件によってスタッフのプールを作る
        for staff in staffs:
            # 昨日までで6連勤 or 昨日が夜勤 or トータルの出勤日数に達している
            if staff.current_shift_streak >= 6 or staff.last_day_shift_pattern == YAKIN or staff.current_shift_count >= staff.max_shift_count:
                continue

            nikkinn_pool.append(staff)

        # 日勤のシフトを確定させる
        nikkin_success = False
        for i in range(10000):
            nikkin = random.sample(nikkinn_pool, shift_day.day_people_count)
            nikkin_point = 0

            for nikkin_staff in nikkin:
                nikkin_point += nikkin_staff.point

            if nikkin_point >= shift_day.day_point:
                nikkin_success = True
                break

        if not nikkin_success:
            for i in range(10000):
                nikkin = random.sample(nikkinn_pool, shift_day.day_people_count + 1)
                nikkin_point = 0

                for nikkin_staff in nikkin:
                    nikkin_point += nikkin_staff.point

                if nikkin_point >= shift_day.day_point:
                    nikkin_success = True
                    break

        if not nikkin_success:
            for i in range(10000):
                nikkin = random.sample(nikkinn_pool, shift_day.day_people_count + 2)
                nikkin_point = 0

                for nikkin_staff in nikkin:
                    nikkin_point += nikkin_staff.point

                if nikkin_point >= shift_day.day_point:
                    nikkin_success = True
                    break

        # スタッフの条件によってスタッフのプールを作る
        for staff in staffs:
            # 昨日までで6連勤 or 昨日が夜勤 or トータルの出勤日数に達している
            if staff.current_shift_streak >= 6 or staff.last_day_shift_pattern == YAKIN or staff.current_shift_count >= staff.max_shift_count or staff in nikkin:
                continue
            # 一か月に取りうる夜勤の最大数に達していないスタッフをプールに入れる
            if staff.current_night_shift_count < staff.max_night_shift_count:
                if staff.point >= 1:
                    yakin_upper_1.append(staff)
                else:
                    yakin_under_1.append(staff)

        yakin_success = False

        # 日勤でシフト確定した人を夜勤に入れないようにする
        for key, yakin_upper_1_staff in enumerate(yakin_upper_1):
            if yakin_upper_1_staff in nikkin:
                del yakin_upper_1[key]
        
        for key, yakin_under_1_staff in enumerate(yakin_under_1):
            if yakin_under_1_staff in nikkin:
                del yakin_under_1[key]

        # 夜勤を確定させる
        for i in range(100):
            yakin = random.sample(yakin_upper_1, 1) + random.sample(yakin_under_1, shift_day.night_people_count-1)
            yakin_point = 0

            for yakin_staff in yakin:
                yakin_point += yakin_staff.point

            if yakin_point >= shift_day.night_point:
                yakin_success = True
                break
        
        if not yakin_success:
            for i in range(100):
                yakin = random.sample(yakin_upper_1, 2) + random.sample(yakin_under_1, shift_day.night_people_count-2)
                yakin_point = 0

                for yakin_staff in yakin:
                    yakin_point += yakin_staff.point

                if yakin_point >= shift_day.night_point:
                    yakin_success = True
                    break

        if not yakin_success:
            for i in range(100):
                yakin = random.sample(yakin_upper_1, 3) + random.sample(yakin_under_1, shift_day.night_people_count-3)
                yakin_point = 0

                for yakin_staff in yakin:
                    yakin_point += yakin_staff.point

                if yakin_point >= shift_day.night_point:
                    yakin_success = True
                    break
        
        # 休みのシフトを確定させる
        for staff in staffs:
            if staff in yakin or staff in nikkin:
                continue
            else:
                yasumi.append(staff)

        # 夜勤か日勤が確定できていなかったら例外を発生させる
        if not yakin_success or not nikkin_success:
            print(yakin_success, nikkin_success)
            raise Exception
        
        # シフト表に記録する
        shift[shift_day] = [nikkin, yakin]

        #######################################################################################

        #######################################################################################

        # スタッフの情報更新
        for staff in staffs:
            if staff.last_day_shift_pattern == YAKIN:
                staff.last_day_shift_pattern = AKE
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
            elif staff in nikkin:
                staff.last_day_shift_pattern = NIKKINN
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
                staff.current_day_shift_count += 1
            elif staff in yakin:
                staff.last_day_shift_pattern = YAKIN
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
                staff.current_night_shift_count += 1
            else:
                staff.last_day_shift_pattern = YASUMI
                staff.current_shift_streak = 0
                staff.current_off_day_count += 1
    return shift

# 関数の実行
start_date = datetime.date(2024, 4, 2)
end_date = datetime.date(2024, 5, 1)

# テスト用のスタッフを作成
shift_pattern = [YAKIN, NIKKINN, YASUMI, AKE]    
name_pool = ["佐藤", "山田", "朝倉", "斎藤", "渡辺", "堀口", "堀江", "グスタボ", "マッキー", "浜辺", "湊", "宝鐘", "かなえる", "樋口", "白石", "小坂", "与田", "設楽", "フリーレン"]
test_staffs = []
test_point = [1,2, 1.0, 0.8, 0.7]

for i in range(30):
    staff = Staff(random.choice(name_pool), random.choice(name_pool), random.choice(test_point),False, random.choice(shift_pattern), 20, 6, 0, i)
    test_staffs.append(staff)

# テスト用のシフトの日付の範囲を用意
test_shift_days = prepare_shift_days(start_date, end_date)

# テスト用のシフトを作成
calculated_shift = calculate_shift(test_shift_days, test_staffs)
a ='かぶりなし'

for date in calculated_shift:
    print('■ ' + str(date))
    print(" 日勤")
    for nikkin_staff in calculated_shift[date][0]:
        print(str(nikkin_staff.id) + ':' + nikkin_staff.last_name + nikkin_staff.first_name)
    print()
    print(" 夜勤")
    for yakin_staff in calculated_shift[date][1]:
        print(str(yakin_staff.id) + ':' + yakin_staff.last_name + yakin_staff.first_name)
        if yakin_staff in calculated_shift[date][0]:
            a = 'かぶってます！！'
    print(a)
    print()
    print()