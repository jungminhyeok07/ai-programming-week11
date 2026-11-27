from pathlib import Path
import pandas as pd

#########################
########################
def 정제(df):
	정제된_df = df.copy()

	# 점수가 비어 있는 행을 삭제한다.
	정제된_df = 정제된_df.dropna(subset=["점수"])
	print(f"점수 결측 행 삭제 후: {len(정제된_df)}행")

	# 모든 열이 완전히 같은 중복 행을 하나만 남긴다.
	정제된_df = 정제된_df.drop_duplicates()
	print(f"중복 행 삭제 후: {len(정제된_df)}행")

	# 반과 과목의 앞뒤 공백을 제거한다.
	정제된_df["반"] = 정제된_df["반"].str.strip()
	정제된_df["과목"] = 정제된_df["과목"].str.strip()
	print(f"문자열 공백 제거 후: {len(정제된_df)}행")

	# 점수가 0 이상 100 이하인 행만 남긴다.
	정제된_df = 정제된_df[정제된_df["점수"].between(0, 100)]
	print(f"점수 범위 밖 행 삭제 후: {len(정제된_df)}행")

	return 정제된_df

df = pd.read_csv(Path(__file__).with_name("scores_2026.csv"))

print(df.shape) # (114, 5)
print(df["점수"].isna().sum()) # 6      ← 빈 칸이 몇 개인가
print(df.duplicated().sum())   # 4      ← 완전히 같은 행이 몇 개인가
print(df["반"].unique())       # ['2반' '1반' '1반 ']      ← 세 개?
print(df["과목"].unique())     # ['수학' '프로그래밍' '영어' '프로그래밍 ']
print(df["점수"].describe())   # max 999.0  min -5.0   ← 점수인데?

df = pd.read_csv(Path(__file__).with_name("scores_2026.csv"))
df = 정제(df)
print(sorted(df["반"].unique())) # ['1반', '2반']       ← 세 개에서 두 개로
print(sorted(df["과목"].unique())) # ['수학','영어','프로그래밍'] ← 네 개에서 세 개로

# 시작        114
# 빈 칸 제거  108      ← 114 - 108 = 6    진단표의 「빈 칸」과 같은가?
# 중복 제거   104      ← 108 - 104 = 4    진단표의 「중복」과 같은가?
# 범위 밖 제거 100     ← 104 - 100 = 4    999 세 개 + 음수 하나

# 정제된 데이터에서 과목이 수학인 행만 남긴다.
수학_df = df[df["과목"] == "수학"]
print(f"과목이 수학인 행 수: {len(수학_df)}행")

# 반별 점수 평균을 계산한다.
반별_평균 = df.groupby("반")["점수"].mean()
print("반별 점수 평균:")
print(반별_평균)

# 과목과 반별 점수 평균을 계산한다.
과목_반별_평균 = df.groupby(["과목", "반"])["점수"].mean()
print("과목·반별 점수 평균:")
print(과목_반별_평균)

# 반별 점수 개수, 평균, 중앙값, 최댓값을 표로 출력한다.
반별_통계 = df.groupby("반")["점수"].agg(
	["count", "mean", "median", "max"]
).rename(columns={
	"count": "개수",
	"mean": "평균",
	"median": "중앙값",
	"max": "최댓값",
}).round(2)
print("반별 점수 통계:")
print(반별_통계)




