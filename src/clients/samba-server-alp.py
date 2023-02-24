from yast import ycpbuiltins
import sys, traceback
sys.path.append(sys.path[0]+"/../include/samba-server-alp")
from wizards import Sequence

if __name__ == "__main__":
    try:
        Sequence()
    except Exception as e:
        ycpbuiltins.y2error(str(e))
        ycpbuiltins.y2error(traceback.format_exc())

