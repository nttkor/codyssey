hint1 = "1?3?5?"  # 6자리, 물음표 3개 → 후보 1000개 생성
hint2 = [
    "?0????", "?1????", "?2????", "?4????", "?5????",  # X자리 0~5 제거
    "?6????", "?7????", "?8????", "?9????", "1?30??",  # X자리 6~9 + 일부 Y자리 제거
    "1?31??", "1?32??", "1?33??", "1?34??", "1?36??",  # 1?3Y?? 중 일부 제거
    "1?37??", "1?38??", "1?39??", "1?3?50", "1?3?51"   # 1?3Y??, Z자리 50~51 제거
]
# 103552  103553  103554  103555  103556
# 103557  103558  103559  113552  113553
# 113554  113555  113556  113557  113558
# 113559  123552  123553  123554  123555
from itertools import product
def match(pattern, num):
    for p,n in zip(pattern, num):
        if p !='?' and p != n:
            return False
    return True

def generate1(pattern):
    glist = []
    cnt = pattern.count('?')
    for p in product('0123456789', repeat=cnt):
        num = ''
        idx=0
        for i,c in enumerate(pattern):
            if  c=='?':
                num += p[idx]
                idx+=1
            else:
                num += c
        if not any(match(h2,num) for h2 in hint2):
            glist.append(num)
    return glist



print(generate1(hint1))



# ---------------------------
# ③ 패턴을 실제 모든 후보로 전개
# ---------------------------
def generate(pattern):
    result = []
    question_count = pattern.count('?')

    # ? 개수만큼 product
    for digits in product("0123456789", repeat=question_count):
        filled = list(pattern)
        idx = 0
        for i in range(len(filled)):
            if filled[i] == '?':
                filled[i] = digits[idx]
                idx += 1
        result.append("".join(filled))

    return result


# ---------------------------
# ④ 전체 해결 함수
# ---------------------------
def solve(valid_pattern, invalid_patterns):
    # valid 패턴으로 모든 후보 생성
    candidates = generate(valid_pattern)

    # invalid 패턴에 하나라도 매칭되면 제거
    def is_invalid(num):
        return any(match(pat, num) for pat in invalid_patterns)

    filtered = [c for c in candidates if not is_invalid(c)]
    return filtered


# ---------------------------
# ⑤ 실행
# ---------------------------
if __name__ == "__main__":
    result = solve(hint1, hint2)
    print("가능한 비밀번호 개수:", len(result))
    print("일부 확인:", result[:20])  # 필요하면 전체 출력

