#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    name = forms.CharField(min_length=4, max_length=32,
                           error_messages={
                                "required": u"用户名不能为空！",
                                "min_length": u"用户名不少于4个字符！",
                                "max_length": u"用户名不超过32个字符！",
                           })
    pwd = forms.CharField(min_length=6, max_length=32,
                          error_messages={
                              "required": u"密码不能为空！",
                              "min_length": u"密码不少于6个字符！",
                              "max_length": u"密码不超过32个字符！",
                          }
                          )
    pwd_confirm = forms.CharField(min_length=6, max_length=32,
                                  error_messages={
                                      "required": u"密码不能为空！",
                                      "min_length": u"密码不少于6个字符！",
                                      "max_length": u"密码不超过32个字符！",
                                  }
                                  )
    email = forms.EmailField(error_messages={
                                 "required": u"邮箱不能为空！",
                                 "invalid": u"邮箱格式错误！",
                             }
                             )


class LoginForm(forms.Form):
    name = forms.CharField(min_length=4, max_length=32,
                           error_messages={
                                "required": u"用户名不能为空！",
                                "min_length": u"用户名不少于4个字符！",
                                "max_length": u"用户名不超过32个字符！",
                           })
    pwd = forms.CharField(min_length=6, max_length=32,
                          error_messages={
                              "required": u"密码不能为空！",
                              "min_length": u"密码不少于6个字符！",
                              "max_length": u"密码不超过32个字符！",
                          }
                          )


class UrlForm(forms.Form):
    url = forms.URLField()
