import sys
from pathlib import Path


# ===== MAIN ======
#
def main():
    fil = Path('items.txt')
    f = open('items.txt', 'r')
    #print(''.join(f.readline()))
    texts = f.readlines()
    print(size(texts))
    print("\n*+*+*+*+*+* END *+*+*+*+*+*\n")

# ===== EXECUTE =====
#
if __name__ == '__main__':
    main()
