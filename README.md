# EduLink智能班级中枢

## 📋 现有问题和解决方向

### ⚠️现有问题：
- 上课铃响后，学生不知道上什么课，无法及时做好课前准备
- 师生不知道当前天气，无法及时合理安排户外活动
- 老师要跟学生转达信息（如：班务信息，课堂作业，默写信息等）时要在教室和办公室之间奔走，比较耽误时间和效率
### ✅解决方向：
- 在预备铃响后，本作品自动播报接下来的课程，并显示在屏幕上
- 通过本作品查询天气，每隔一小时更新一次天气，并显示在屏幕上
- 通过从本团队开发的应用程序发送消息，本作品接收并播报消息

## 💡设计方案与技术实现

### 🛠️ 技术原理
- 使用Python语言编写本作品及应用程序
- 使用Unihiker库（Pygame库）实现显示
- 使用Requests库实现文字转语音与天气查询
- 使用Siot库发送MQTT请求实现消息发送与接收

### 📃 材料清单
- 行空板M10 及其套件（USB转Type-C数据线等）
- 音频播放器（支持USB接口）

### 📓 模型制作方案
- 精密测量行空板长宽高，以及需要留出的接口的位置与大小
- 三维建模与行空板大小相符的外壳，并预留出两个接口
- 将外壳套上行空板，做接口插拔测试

# 📥 使用教程
访问[EduLink官网](https://edulink.ryanincn11.top/)以查看教程

## 📜 开源协议
本项目采用 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/RyaninChina11/YCCJTechFestival2025/blob/main/LICENSE.md)

## ⚖️ 版权声明与致谢
本项目基于以下技术服务构建：
- 文字转语音功能由 [百度短文本在线合成API](https://cloud.baidu.com/doc/SPEECH/s/mlbxh7xie) 提供技术支持
- 天气查询功能由[高德天气查询API](https://lbs.amap.com/api/webservice/guide/api/weatherinfo) 提供技术支持
- MQTT消息托管由[EasyIoT](https://iot.dfrobot.com.cn/) 提供技术支持

本作品仅用于教育目的，未经授权不得用于商业用途

## 📞 联系方式
- 作者：肖梓航&孙轲俊
- 班级：六(1)班
- 邮箱：18149721348@163.com
- GitHub: [RyaninChina11](https://github.com/RyaninChina11)
