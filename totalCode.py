#!/usr/bin/env python3
import RPi.GPIO as GPIO
import smtplib
import time
from email.message import EmailMessage

# ===== 传感器配置 =====
SENSOR_PIN = 4        # GPIO4 (BCM编号)
CHECK_INTERVAL = 0.006     # 检测间隔（小时）
last_status = None     # 上一次状态记录

# ===== 邮箱配置 (163示例) =====
SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 25
SENDER_EMAIL = "nuist202283890005@163.com"
SENDER_PASSWORD = "BCNqp7YjdFUZZKYL"  # 授权码
RECEIVER_EMAIL = "nuist202283890005@163.com"

# ===== GPIO初始化 =====
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    GPIO.add_event_detect(SENSOR_PIN, GPIO.BOTH, 
                        callback=status_changed, 
                        bouncetime=300)
    print("GPIO初始化完成")

# ===== 传感器状态变化回调 =====
def status_changed(channel):
    global last_status
    current_status = GPIO.input(channel)
    
    # 状态映射 (0=干燥需要浇水，1=湿润)
    status_map = {
        0: ("需要浇水！", "[警报] 植物缺水"),
        1: ("水分充足", "[正常] 植物状态良好")
    }
    
    # 仅当状态变化时发送邮件
    
    message, subject = status_map[current_status]
    send_email(subject, f"检测时间: {time.strftime('%Y-%m-%d %H:%M')}\n当前状态: {message}")
    last_status = current_status
    print(f"状态变化: {message}")

# ===== 邮件发送函数 =====
def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        # 使用SSL加密连接
        with smtplib.SMTP() as server:
            server.connect(SMTP_SERVER,SMTP_PORT)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("邮件发送成功")

    except Exception as e:
        print(f"邮件发送失败: {str(e)}")

# ===== 主程序 =====
if __name__ == "__main__":
    try:
        setup_gpio()
        print("植物监控系统已启动...")
        while True:
            time.sleep(60)  # 保持主线程运行

    except KeyboardInterrupt:
        print("\n程序终止")
    finally:
        GPIO.cleanup()
