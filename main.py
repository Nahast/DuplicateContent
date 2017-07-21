import sys
from pathlib import Path

# ===== SHINGLING ======
#
SHINGLE_SIZE = 5

def get_shingles(f, size):
    shingles = set()
    buf = f # read entire file
    for i in range(0, len(buf)-size+1):
        yield buf[i:i+size]

# ===== JACCARD ======
#
def jaccard(set1, set2):
    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    return x / float(y)

# ===== MAIN ======
#
def main():
    fil = Path('items.txt')
    f = open('items.txt', 'r')
    #print(''.join(f.readline()))
    texts = f.readlines()
    for t in texts:
        shingles1 = set(get_shingles(t, size=SHINGLE_SIZE))
        shingles2 = set(get_shingles(t, size=SHINGLE_SIZE))

    print(jaccard(shingles1, shingles2))
    print("\n*+*+*+*+*+* END *+*+*+*+*+*\n")
    # ADD TIMER

# ===== EXECUTE =====
#
if __name__ == '__main__':
    main()
