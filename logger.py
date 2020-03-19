from datetime import datetime

def l(str):
    print(
        "%s : %s" %
        (datetime.now().strftime("%Y/%m/%d %H:%M:%S"), str))