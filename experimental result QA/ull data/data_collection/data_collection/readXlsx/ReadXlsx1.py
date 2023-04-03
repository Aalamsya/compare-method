# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xlrd # 文件的名字

#将收集好的xlsx与TXT文本提取出文章名以及每篇文章对应的问题
home = "/home/hw/Desktop/QA_data_collection/data_collection/"
def readXlsx(name):
    file_name = home+"xlsx/"+name+".xlsx" # 打开文件
    bk = xlrd.open_workbook(file_name)
    sh = bk.sheet_by_name("Sheet1")
    row_num = sh.nrows  #行数
    row_list = []#文章名字集合
    index = []#文章名字单元类别集合
    question = []
    problem_type=[]
    for i in range(1, row_num): # 获取第i行的数据
        row_data = sh.row_values(i)
        row_list.append(str(row_data[1])) # 打印每一行的内容，打印出的为列表的形式
        index.append(sh.cell(i,1).ctype)#0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        question.append(row_data[4])
        problem_type.append(row_data[3].lower())
    return row_list,index,question,problem_type   #row_list文章名  index为是文章名所在单元的类型，question为问题

def saveActicleName(name):
    file_handle = open(home+'questionOfXlsx/'+name+'_ArticleName', mode='w')
    row_list, index, question,_= readXlsx(name)
    for i in range(0,len(index)):
        if index[i]==1:
            print row_list[i]
            file_handle.write(str(row_list[i])+'\n')
        else:
            pass
    file_handle.close()

def saveActicleQuestion(name):
    row_list, index, question,problem_type = readXlsx(name)
    article = ''
    num = 0
    text = 0
    article=''
    for i in range(0, len(index)):
        if index[i]==1:
            if text == 1:
                file = open(home + "numberOfArticle.txt", mode='a')
                file.write(article+'\t'+str(num) + '\n')
                file.close()
            num = 1
            article = row_list[i]
            file_handle = open(home+'questionOfXlsx/'+name+'/'+article, mode='w')
            file_handle.write(str(question[i]).encode("utf8")+'\t'+problem_type[i]+ '\n')
            file_handle.close()
            text=1
        else:
            num = num+1
            file_handle = open(home+'questionOfXlsx/'+name+'/'+article, mode='a')
            file_handle.write(str(question[i].encode("utf-8"))+'\t'+problem_type[i]+'\n')
            file_handle.close()
    file = open(home + "numberOfArticle.txt", mode='a')
    file.write(article + '\t' + str(num) + '\n')
    file.close()

if __name__ == "__main__":
    path = "701-800"
    saveActicleName(path)
    saveActicleQuestion(path)



