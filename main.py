import time
from datetime import datetime, timedelta
import pyautogui
import pyperclip
import sys
import platform # 用来检测是什么系统

# ================= 极速配置区 =================
pyautogui.PAUSE = 0.01 
# ============================================

# 检测当前是 Mac 还是 Windows
# 如果是 Mac ('Darwin')，粘贴键设为 'command'，否则设为 'ctrl'
is_mac = platform.system() == 'Darwin'
paste_key = 'command' if is_mac else 'ctrl'

def get_seconds_until_target(target_hour, target_minute, target_second=0):
    """计算距离目标时间还有多少秒"""
    now = datetime.now()
    target_time = now.replace(hour=target_hour, minute=target_minute, second=target_second, microsecond=0)
    if target_time < now:
        target_time += timedelta(days=1)
    diff = target_time - now
    return diff.total_seconds(), target_time

print("="*50)
print(f"   天才才抢车助手【{'Mac' if is_mac else 'Win'} 】")
print("="*50)

try:
    msg = input("\n1. 输入要发送的消息: ")
    time_str = input("2. 输入时间 (格式 HH:MM:SS): ")
    
    try:
        h, m, s = map(int, time_str.split(':'))
    except ValueError:
        print("格式错误")
        sys.exit()

    # 预加载到剪贴板
    pyperclip.copy(msg)
    print(f"\n[状态] 内容已复制，等待发射...")
    
    wait_seconds, target_dt = get_seconds_until_target(h, m, s)
    print(f"[状态] 目标锁定: {target_dt.strftime('%H:%M:%S')}")
    
    # === Mac 用户特别提示 ===
    if is_mac:
        print(f"\n⚠️  重要提示：Mac 用户请确保终端已获得【辅助功能】权限")
        print(f"⚠️  否则无法控制键盘粘贴")
    # ======================

    print(f"\n请在倒计时结束前，点击微信输入框...")

    while True:
        now = datetime.now()
        delta = (target_dt - now).total_seconds()
        
        if delta > 1:
            print(f"\r倒计时: {int(delta)} 秒  ", end="")
            time.sleep(0.5)
        elif delta <= 0:
            # === 根据系统自动选择粘贴键 ===
            pyautogui.hotkey(paste_key, 'v')
            pyautogui.press('enter')
            # ==========================
            print(f"\n\n[命中] {datetime.now().strftime('%H:%M:%S.%f')}")
            break
        else:
            pass 

except Exception as e:
    print(f"错误: {e}")
