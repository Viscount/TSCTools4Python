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

_原因：由于弹幕数据中包含大量的特殊unicode字符，需要使用mysql中的utf8mb4编码方式存储（完全支持全部的unicode字符串），而mysql的5.5.3
版本及以上，mysqldb的1.2.5版本及以上支持utf8mb4编码。_

**3. 数据库表**
数据库中只有两个表，**video**表（b站视频相关）和**barrage**表（b站弹幕相关信息）。

_video_表结构：
```
    cid = Column(String(30), primary_key=True)  # 视频对应的弹幕cid
    title = Column(Text, nullable=False)  # 视频的标题信息。
    tags = Column(Text, nullable=False)  # 视频的标签信息，格式为：一级标签\t二级标签...
    aid = Column(String(30), nullable=False)  # 视频的aid
    url = Column(Text, nullable=False)  # 视频的网址链接
```

_barrage_表结构：
```
    row_id = Column(String(30), primary_key=True)  # 弹幕在弹幕数据库中rowID 用于“历史弹幕”功能。
    play_timestamp = Column(String(50), nullable=False)  # 弹幕出现的时间 以秒数为单位。
    type = Column(Integer, nullable=False)  # 弹幕的模式1..3 滚动弹幕 4底端弹幕 5顶端弹幕 6.逆向弹幕 7精准定位 8高级弹幕
    font_size = Column(Integer, nullable=False)  # 字号， 12非常小,16特小,18小,25中,36大,45很大,64特别大
    font_color = Column(String(50), nullable=False)  # 字体的颜色 以HTML颜色的十位数为准
    unix_timestamp = Column(String(50), nullable=False)  # Unix格式的时间戳。基准时间为 1970-1-1 08:00:00
    pool = Column(Integer, nullable=False)  # 弹幕池 0普通池 1字幕池 2特殊池 【目前特殊池为高级弹幕专用】
    sender_id = Column(String(20), nullable=False)  # 发送者的ID，用于“屏蔽此弹幕的发送者”功能
    content = Column(Text, nullable=False)  # 弹幕内容
    # 外键信息
    video_cid = Column(String(30), ForeignKey("video.cid"))
    # 这样就可以使用movie.barrages获得该视频的所有弹幕信息。
    video = relationship(Video, backref=backref("barrages", uselist=True, cascade="delete, all"))
```

**4. 关于本地弹幕xml文件的解析**

调用```db.dao.bilibili_xml_parser.BilibiliXmlParser```中的```save_xml_barrage_to_db(xml_file_path)```方法。该方法返回True时，数据库操作成功。
_注：_
> ```xml_file_path``` 参数必须是 以 (\d)+.xml结尾的字符串，否则xml文件中的弹幕无法存入数据库。