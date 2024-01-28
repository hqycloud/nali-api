# 导入所需的模块
import socket
import subprocess
import re

# 创建一个socket对象
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# 绑定0.0.0.0:8899
s.bind(('::', 8899))

# 监听连接
s.listen()

# 循环接受和处理请求
while True:
    # 接受一个连接
    conn, addr = s.accept()
    
    # 接收客户端的数据
    data = conn.recv(1024)
    
    # 如果数据不为空
    if data:
        # 将数据转换为字符串
        data = data.decode('gbk')
        
        # 从字符串中提取ip参数
        ip = re.search(r'ip=([0-9a-fA-F:.]+)', data)
        
        # 如果找到了ip参数
        if ip:
            # 获取ip的值
            ip = ip.group(1)
            
            # 调用nali命令获取ip的地理位置
            nali = subprocess.run(['nali', ip], capture_output=True)
            
            # 将nali的输出转换为字符串
            nali = nali.stdout.decode()
            
            # 从nali的输出中截取ip的地理位置
            location = re.search(r'\[(.+)\]', nali)
            
            # 如果找到了地理位置
            if location:
                # 获取地理位置的值
                location = location.group(1)
                
                # 构造响应的内容
                response = location
            else:
                # 如果没有找到地理位置，构造响应的内容
                response = f'抱歉，无法获取IP {ip} 的地理位置，请等待几分钟同步数据库'
        else:
            # 如果没有找到ip参数，构造响应的内容
            response = '参数有误，正确示例：https://ip-api.hqycloud.top/ip=8.8.8.8'
    else:
        # 如果数据为空，构造响应的内容
        response = '无参数！正确示例：https://ip-api.hqycloud.top/ip=8.8.8.8'
    
    # 发送HTTP响应的版本和状态码
    conn.sendall(b'HTTP/1.1 200 OK\r\n')
    
    # 发送HTTP响应的内容类型
    conn.sendall(b'Content-Type: text/plain; charset=utf-8\r\n')
    
    # 发送空行
    conn.sendall(b'\r\n')
    
    # 发送响应的内容给客户端
    conn.sendall(response.encode())
    
    # 关闭连接
    conn.close()