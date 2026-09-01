# ============================================================
# [멘티 과제] 설비 점검 데이터 정제 · 전처리
# ============================================================
#
# 여러분이 할 일은 '받은 데이터를 분석할 수 있는 상태로 만들어 멘토에게 넘기는 것'입니다.
# 지시문을 그대로 따라가면 됩니다. 기대 출력이 적혀 있으니 스스로 채점하세요.
# 숫자가 다르면 앞 문제로 돌아가 확인하고, 그래도 안 맞으면 멘토에게 물어보세요.
#
# 최종 산출물: 정제결과_멘티.csv  (문제 10에서 만듭니다)
#
# 필요한 파일: 설비배치1.csv (같은 폴더에 두세요)
#   검사일시 / 생산라인(A·B·C) / 설비번호 / 온도 / 진동 / 회전수 / 압력 / 판정

import numpy as np
import pandas as pd

df = pd.read_csv("설비배치1.csv", encoding="utf-8-sig")
sensor = ["온도", "진동", "회전수", "압력"]


# ----------------------------------------
# 문제 1. 받은 파일을 열고 상태를 파악한다
# ----------------------------------------
print("문제 1-----------------------------------")
print(df.shape)
miss = df.isnull().sum()
miss = miss[miss > 0]
print(miss.to_dict())

print(type(df["진동"].iloc[0]).__name__)
print(df["판정"].value_counts().to_dict())
# ----------------------------------------
# 문제 2. 숫자로 저장되지 않은 열 고치기
# ----------------------------------------
print("\n문제 2-----------------------------------")
df["진동"] = pd.to_numeric(df["진동"], errors="coerce")
print(df["진동"].isnull().sum())
print(round(df["진동"].mean(), 2))
# ----------------------------------------
# 문제 3. 중복 행 제거
# ----------------------------------------
print("\n문제 3-----------------------------------")
print(df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)
print(df.shape)

# ----------------------------------------
# 문제 4. 결측 채우기
# ----------------------------------------
print("\n문제 4-----------------------------------")
temp4 = df["온도"].mean()
pressure4 = df["압력"].median()
vib4 = df["진동"].mean()

df["온도"] = df["온도"].fillna(temp4)
df["압력"] = df["압력"].fillna(pressure4)
df["진동"] = df["진동"].fillna(vib4)
print(df[sensor].isnull().sum().sum())

print(round(temp4, 2), round(pressure4, 2))
# ----------------------------------------
# 문제 5. 생산라인별 요약
# ----------------------------------------
print("\n문제 5-----------------------------------")
print(round(df.groupby("생산라인")[sensor].mean(), 2))
line = df["생산라인"].value_counts()
line = line.sort_index()
line = line.to_dict()
print(line)
# ----------------------------------------
# 문제 6. z-점수로 온도 이상 찾기
# ----------------------------------------
print("\n문제 6-----------------------------------")
temp = df["온도"].to_numpy()
temp_avg = np.mean(temp)
temp_std = np.std(temp, ddof=0)
print(round(temp_avg, 2), round(temp_std, 2))
z = (temp - temp_avg) / temp_std
print((abs(z) > 3).sum(), (abs(z) > 2).sum())

# ----------------------------------------
# 문제 7. IQR로 압력 이상 찾기
# ----------------------------------------
print("\n문제 7-----------------------------------")
pressure = df["압력"].to_numpy()
q1 = np.percentile(pressure, 25)
q3 = np.percentile(pressure, 75)
iqr = q3 - q1
lo = q1 - 1.5 * iqr
hi = q3 + 1.5 * iqr
print(round(lo, 2), round(hi, 2))
mask = (df["압력"] < lo) | (df["압력"] > hi)
print(np.sum(mask))
print(df.loc[mask, "생산라인"].value_counts().to_dict())
# ----------------------------------------
# 문제 8. 이상으로 판정된 행 제거
# ----------------------------------------
print("\n문제 8-----------------------------------")
print(df["생산라인"].value_counts().sort_index().to_dict())

o_mask = (df["압력"] >= lo) & (df["압력"] <= hi)
df = df[o_mask]
df = df.reset_index(drop=True)
print(df["생산라인"].value_counts().sort_index().to_dict())
print(df.shape)

# ----------------------------------------
# 문제 9. 0~1로 스케일 맞추고 파일로 남기기
# ----------------------------------------
print("\n문제 9-----------------------------------")
# minn = df[sensor].min()
# maxx = df[sensor].max()
answer = (df[sensor] - df[sensor].min()) / (df[sensor].max() - df[sensor].min())
print(answer.min().round(3).to_dict())
print(answer.max().round(3).to_dict())
print(answer.mean().round(3).to_dict())

result = pd.concat([df[["검사일시", "생산라인"]], answer.round(4)], axis=1)
result.to_csv("정규화_멘티.csv", index=False, encoding="utf-8-sig")

ans = pd.read_csv("정규화_멘티.csv", encoding="utf-8-sig")
print(ans.shape)


# ----------------------------------------
# 문제 10. 라인 인코딩하고 저장하기
# ----------------------------------------
print("\n문제 10-----------------------------------")

line_code = {"A라인": 0, "B라인": 1, "C라인": 2}
df["라인코드"] = df["생산라인"].map(line_code)
columns = ["검사일시", "생산라인", "라인코드", "온도", "진동", "회전수", "압력", "판정"]

a = df[columns]
a.to_csv("정제결과_멘티.csv", index=False, encoding="utf-8-sig")
checkk = pd.read_csv("정제결과_멘티.csv", encoding="utf-8-sig")
x = checkk.isnull().sum().sum()
y = checkk.duplicated().sum()

print(checkk.shape, x, y)
print(checkk.columns.tolist())
