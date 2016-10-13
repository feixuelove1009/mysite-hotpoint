#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Python 3.5
from django.utils.safestring import mark_safe


# 计算页面信息的类
class PageInfo:
    def __init__(self, current, total_item, per_items=10):
        self.__current = current
        self.__per_items = per_items
        self.__total_item = total_item

    # 计算起始条目序号
    def begin(self):
        return (self.__current-1) * self.__per_items

    # 计算结束条目序号
    def end(self):
        return self.__current * self.__per_items

    # 计算总页数
    def total_page(self):  # 总页数
        result = divmod(self.__total_item, self.__per_items)
        if result[1] == 0:
            return result[0]
        else:
            return result[0]+1


def custom_pager(base_url, current_page, total_page, show_page_number_per_side=5):
    """
    怕页数太多，因此决定当前页面左边显示指定页的跳转标签，右边也显示指定页的跳转标签。
    默认指定5页！下面是默认计算公式：
    总页数<11:    0 -- total_page
    总页数>11:
        当前页大于5： current_page-5 -- current_page+5
                      current_page+5是否超过总页数,超过总页数，end就是总页数
        当前页小于5： 0 -- 11
    :param base_url: 跳转地址基础,例如"/index/"
    :param current_page: 当前页
    :param total_page: 总页数
    :param show_page_number_per_side: 除了当前页序号外左右各显示几个页面序号，默认5个。
    :return:
    """

    sp = show_page_number_per_side

    if total_page <= sp*2+1:
        begin = 0
        end = total_page
    else:
        if current_page > sp:
            begin = current_page - sp
            end = current_page + sp
            if end > total_page:
                end = total_page
        else:
            begin = 0
            end = current_page + sp
    # 开始生成page标签
    pager_list = []
    pager_list.append("<nav class='pull-right'>")
    pager_list.append('<ul class="pagination">')
    # 生成首页标签
    if current_page <= 1:
        first = "<li class='disabled'><a href='#'>首页</a></li>"
    else:
        first = "<li><a href='%s?p=%d'>首页</a></li>" % (base_url, 1)
    pager_list.append(first)
    # 生成“上一页”标签
    if current_page <= 1:
        prev = "<li class='disabled'><a href='#'>上一页</a></li>"
    else:
        prev = "<li><a href='%s?p=%d'>上一页</a></li>" % (base_url, current_page-1)
    pager_list.append(prev)
    # 循环生成数字标签
    for i in range(begin+1, end+1):
        # 给予当前页面激活的样式
        if i == current_page:
            temp = "<li class='active'><a href='%s?p=%d'>%d</a></li>" % (base_url, i, i)
        else:
            temp = "<li><a href='%s?p=%d'>%d</a></li>" % (base_url, i, i)
        pager_list.append(temp)

    # 生成下一页和末页标签
    if current_page >= total_page:
        the_next = "<li class='disabled'><a href='#'>下一页</a></li>"
    else:
        the_next = "<li><a href='%s?p=%d'>下一页</a></li>" % (base_url, current_page+1)
    pager_list.append(the_next)
    if current_page >= total_page:
        last = "<li class='disabled'><a href='#'>末页</a></li>"
    else:
        last = "<li><a href='%s?p=%d'>末页</a></li>" % (base_url, total_page)
    pager_list.append(last)
    pager_list.append("</ul>")
    pager_list.append("</nav>")

    # 拼接列表里的所有元素形成大的字符串，准备提供给模板进行渲染
    result = ''.join(pager_list)
    # mark_safe模块确保你的字符串不会因为xss安全机制被html拒绝，而是正常生成标签。
    return mark_safe(result)
