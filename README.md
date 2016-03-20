# TSCTools4Python

#### 创建storage-dev 分支
**1. 功能：**
>
1. 解析出data文件夹下xml弹幕文件中的弹幕。
2. 设计数据库表格，将弹幕数据信息存入数据库。
**2. 环境要求**
>
1. mysql版本 >= 5.5.3
2. mysqldb 版本 >= 1.2.5
_原因：_由于弹幕数据中包含大量的特殊unicode字符，需要使用mysql中的utf8mb4编码方式存储（完全支持全部的unicode字符串），而mysql的5.5.3
版本及以上，mysqldb的1.2.5版本及以上支持utf8mb4编码。
