# -*- coding: utf-8 -*-
import os


def get_FileSize(filePath):
    """
    获取文件大小（M）
    :param filePath:
    :return:
    """
    fsize = os.path.getsize(filePath)
    fsize = fsize / float(1024 * 1024)
    return round(fsize, 2)


# 通常访问者的IP就在其中，所以我们可以用下列方法获取用户的真实IP：
# X-Forwarded-For:简称XFF头，它代表客户端，也就是HTTP的请求端真实的IP，只有在通过了HTTP 代理或者负载均衡服务器时才会添加该项。
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]#所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')#这里获得代理ip
    return ip
