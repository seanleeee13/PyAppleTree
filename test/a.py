# def fibo(n):
#     if n <= 1:
#         return n
#     return fibo(n - 1) + fibo(n - 2)
# print(fibo(int(input())))

import random
import time

# 🏃 [5유형/3,2] 개별 실행은 미미하나 수만 번 호출됨
def validate_item(weight, limit):
    # time.sleep(0.1)
    return 0 <= weight <= limit

# 🔥 [1유형/1,1] 리스트 정렬 및 조작 - 연산 집중형
def sort_inventory(items):
    # 불필요하게 반복 정렬하여 부하를 만듦
    for _ in range(100):
        items.sort(key=lambda x: x[1] / (x[0] + 1), reverse=True)
    return items

# 🌀 [2유형/2,1] 핵심 로직 - 무거운 재귀 (복합 병목)
def knapsack_recursive(capacity, items, n):
    if n == 0 or capacity == 0:
        return 0
    
    # 여기서 가벼운 함수를 계속 부름
    if not validate_item(items[n-1][0], capacity):
        return knapsack_recursive(capacity, items, n-1)
    
    # 중복 계산이 폭발하는 재귀 지점
    return max(
        items[n-1][1] + knapsack_recursive(capacity - items[n-1][0], items, n-1),
        knapsack_recursive(capacity, items, n-1)
    )

# 🚦 [3유형/2,2] 알고리즘 실행 입구
def solve_problem():
    # 데이터 생성
    items = [(random.randint(1, 30), random.randint(10, 100)) for _ in range(25)]
    capacity = 100
    
    # 1. 전처리 계층 호출
    sorted_items = sort_inventory(items)
    
    # 2. 메인 알고리즘 계층 호출
    result = knapsack_recursive(capacity, sorted_items, len(sorted_items))
    return result

# 🚦 [3유형/2,2] 최상위 서비스 입구
def run_service():
    print("PyRoot 알고리즘 분석 시작...")
    final_res = solve_problem()
    print(f"최적 가치: {final_res}")

if __name__ == "__main__":
    run_service()