import pymysql
       
        
# 将list内容直接导入到mysql数据库(好像不太稳定，主要是由于数据格式有问题)
# 数据少的时候还是可以的
if __name__ == '__main__':
    data = []
    con = pymysql.connect(host='localhost', user='root', passwd='123', db='db', charset='utf8')
    cursor = con.cursor()
    strSQL = ""
    for i in range(len(data)):
        strSQL += "('" + data[i][0] + "'"
        for j in range(1, len(data[i])):
            strSQL += ",'" + data[i][j] + "'"
        strSQL += '),'
    sql = strSQL[:-1]
    sql = "insert into series values " + sql
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()