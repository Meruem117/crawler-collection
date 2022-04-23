# Bilibili Crawler

python crawler for bilibili ups and videos, written in 2021

## up_info

参数：

- up_id，即mid，点开up空间，url内获取

## up_videos

参数：

- up_id，同上
- up_name，复制完整名字即可
- total_page，总页数，点开up空间的投稿，即可获取

PS：对获取的视频数据作了判断，如果是联合投稿，up不是当前的up，不会记录数据（主要是用于解决数据库中，bvid作为唯一性约束时会重复的问题，如果采用其他索引、约束等，没有此类问题，则把判断的那两行语句删除即可）

## auto_bili

从数据库读取up列表，自动爬取所需数据

需自定义数据库参数，数据库表格结构为 (`id int`, `mid varchar(10)`, `name varchar(50)`)

配置好后执行即可
