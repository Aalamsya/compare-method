# coding=utf-8
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
    for i in range(1, row_num): # 获取第i行的数据
        row_data = sh.row_values(i)
        row_list.append(str(row_data[1])) # 打印每一行的内容，打印出的为列表的形式
        index.append(sh.cell(i,1).ctype)#0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        question.append(row_data[4])
    return row_list,index,question

def saveActicleName(name):
    file_handle = open(home+'questionOfXlsx/'+name+'_ArticleName', mode='w')
    row_list, index, question = readXlsx(name)
    for i in range(0,len(index)):
        if index[i]==1:
            print row_list[i]
            file_handle.write(str(row_list[i])+'\n')
        else:
            pass
    file_handle.close()

def saveActicleQuestion(name):
    row_list, index, question = readXlsx(name)
    article = ''
    for i in range(0, len(index)):
        if index[i]==1:
            article = row_list[i]
            file_handle = open(home+'questionOfXlsx/'+name+'/'+article, mode='w')
            file_handle.write(str(question[i]) + '\n')
            file_handle.close()
        else:
            file_handle = open(home+'questionOfXlsx/'+name+'/'+article, mode='a')
            file_handle.write(str(question[i].encode("utf-8"))+'\n')
            file_handle.close()

if __name__ == "__main__":
    saveActicleName("1-100")
    saveActicleQuestion("1-100")



