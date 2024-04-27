
import pandas as pd
import numpy as np


def load_data(csv_file):
    # 读取Excel数据
    df = pd.read_csv(csv_file, encoding='utf-8')
    return df

def grade_rank_desc(data, subject):
    # 计算排名，最高分排名第一，如果并列，排名相同
    n= data[f'{subject}年级排名']
    k =data[f'{subject}年级排名并列人数']  
    if(k<=1):
        return f'第{int(n)}名'
    else:
        return f'第{int(n)}名，共{k}人并列'
    
def class_rank_desc(data, subject):
    # 计算排名，最高分排名第一，如果并列，排名相同
    n= data[f'{subject}班级排名']
    k =data[f'{subject}班级排名并列人数']  
    if(k<=1):
        return f'第{int(n)}名'
    else:
        return f'第{int(n)}名，共{k}人并列'

def save_report(df):   
    # 分别为每一名学生打印成绩单报告，html格式
    for i in range(len(df)):
        student = df.iloc[i]
        html = f'''
        
        <html>
        <head>
        <style>
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        h1{{text-align:center;}}
        </style>
        </head>
        <body>
        <h1>成绩单</h1>
        <table>
        <tr><th>学生</th><td colspan='4'>{student['学生']}</td></tr>
        <tr><th>班级</th><td colspan='4'>{student['班级']}</td></tr>
        <tr><th>科目</th><th>期中成绩</th><th>线级</th><th>班级排名</th><th>年级排名</th></tr>
        <tr><th>语文</th><td>{student['语文']}</td><td>{student['语文线级']}</td><td>{class_rank_desc(student,'语文')}</td><td>{grade_rank_desc(student,'语文')}</td></tr>
        <tr><th>数学</th><td>{student['数学']}</td><td>{student['数学线级']}</td><td>{class_rank_desc(student,'数学')}</td><td>{grade_rank_desc(student,'数学')}</td></tr>
        <tr><th>英语</th><td>{student['英语']}</td><td>{student['英语线级']}</td><td>{class_rank_desc(student,'英语')}</td><td>{grade_rank_desc(student,'英语')}</td></tr>
        <tr><th>政治</th><td>{student['政治']}</td><td>{student['政治线级']}</td><td>{class_rank_desc(student,'政治')}</td><td>{grade_rank_desc(student,'政治')}</td></tr>
        <tr><th>历史</th><td>{student['历史']}</td><td>{student['历史线级']}</td><td>{class_rank_desc(student,'历史')}</td><td>{grade_rank_desc(student,'历史')}</td></tr>
        <tr><th>地理</th><td>{student['地理']}</td><td>{student['地理线级']}</td><td>{class_rank_desc(student,'地理')}</td><td>{grade_rank_desc(student,'地理')}</td></tr>
        <tr><th>生物</th><td>{student['生物']}</td><td>{student['生物线级']}</td><td>{class_rank_desc(student,'生物')}</td><td>{grade_rank_desc(student,'生物')}</td></tr>
        <tr><th>四科总分</th><td>{student['四科总分']}</td><td>{student['四科总分线级']}</td><td>{class_rank_desc(student,'四科')}</td><td>{grade_rank_desc(student,'四科')}</td></tr>
        <tr><th>七科总分</th><td>{student['七科总分']}</td><td>{student['七科总分线级']}</td><td>{class_rank_desc(student,'七科')}</td><td>{grade_rank_desc(student,'七科')}</td></tr>
        </table>
        </body>
        '''
        
        # 保存成绩单
        with open(f'data/{student["学生"]}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'{student["学生"]}的成绩单保存成功')


# 入口是main
if __name__ == '__main__':
    # 加载数据， df 含有表头‘学生’，‘班级’，‘语文’，‘数学’，‘英语’，‘政治’，‘历史’，‘地理’，‘生物’
    df_scores = load_data('data/scores-1.csv')
    
    # 加载数据， df 含有表头‘科目’，‘线级’，e.g.
    #线级	语文	数学	英语	政治	历史	地理	生物
    # A线	90	90	90	60	65	65	65
    # B线	80	80	80	50	56	56	56
    # C线	70	70	70	42	42	42	42
    # D线   0   0   0   0   0   0   0
    df_levels = load_data('data/levels.csv')
    
    
    
    # 计算分数, 给df增加两列，四科总分和七科总分
    df_scores['四科总分'] = df_scores[['语文', '数学', '英语', '政治']].sum(axis=1)
    df_scores['七科总分'] = df_scores[['语文', '数学', '英语', '政治', '历史', '地理', '生物']].sum(axis=1)
    
    # 计算线级， 给df增加七列，分别为语文线级，数学线级，英语线级，政治线级，历史线级，地理线级，生物线级
    labels = list(df_levels['线级'].values)
    
    
    df_scores['语文线级'] = pd.cut(df_scores['语文'], bins=list(df_levels['语文'].values)+[100], labels=labels)
    df_scores['数学线级'] = pd.cut(df_scores['数学'], bins=list(df_levels['数学'].values)+[100], labels=labels)
    df_scores['英语线级'] = pd.cut(df_scores['英语'], bins=list(df_levels['英语'].values)+[100], labels=labels)
    df_scores['政治线级'] = pd.cut(df_scores['政治'], bins=list(df_levels['政治'].values)+[100], labels=labels)
    df_scores['历史线级'] = pd.cut(df_scores['历史'], bins=list(df_levels['历史'].values)+[100], labels=labels)
    df_scores['地理线级'] = pd.cut(df_scores['地理'], bins=list(df_levels['地理'].values)+[100], labels=labels)
    df_scores['生物线级'] = pd.cut(df_scores['生物'], bins=list(df_levels['生物'].values)+[100], labels=labels)
    df_scores['四科总分线级'] = pd.cut(df_scores['四科总分'], bins=list(df_levels['四科总分'].values)+[1000], labels=labels)
    df_scores['七科总分线级'] = pd.cut(df_scores['七科总分'], bins=list(df_levels['七科总分'].values)+[1000], labels=labels)
    
    # 按照七科成绩， 分别计算排名，最高分排名第一，如果并列，排名相同
    # method='min'表示并列时取最小排名，ascending=False表示降序排名
    df_scores['语文年级排名'] = df_scores['语文'].rank(method='min', ascending=False)
    df_scores['语文年级排名并列人数'] = df_scores['语文'].map(df_scores['语文'].value_counts())
    df_scores['数学年级排名'] = df_scores['数学'].rank(method='min', ascending=False)
    df_scores['数学年级排名并列人数'] = df_scores['数学'].map(df_scores['数学'].value_counts())
    df_scores['英语年级排名'] = df_scores['英语'].rank(method='min', ascending=False)
    df_scores['英语年级排名并列人数'] = df_scores['英语'].map(df_scores['英语'].value_counts())
    df_scores['政治年级排名'] = df_scores['政治'].rank(method='min', ascending=False)
    df_scores['政治年级排名并列人数'] = df_scores['政治'].map(df_scores['政治'].value_counts())
    df_scores['历史年级排名'] = df_scores['历史'].rank(method='min', ascending=False)
    df_scores['历史年级排名并列人数'] = df_scores['历史'].map(df_scores['历史'].value_counts())
    df_scores['地理年级排名'] = df_scores['地理'].rank(method='min', ascending=False)
    df_scores['地理年级排名并列人数'] = df_scores['地理'].map(df_scores['地理'].value_counts())
    df_scores['生物年级排名'] = df_scores['生物'].rank(method='min', ascending=False)
    df_scores['生物年级排名并列人数'] = df_scores['生物'].map(df_scores['生物'].value_counts())
    
    
    # 给df增加列， 分别按照四科总分和七科总分排名，最高分排名第一，取整数排名
    df_scores['四科年级排名'] = df_scores['四科总分'].rank(method='min', ascending=False)
    df_scores['四科年级排名并列人数'] =  df_scores['四科年级排名'].map(df_scores['四科年级排名'].value_counts())
    df_scores['七科年级排名'] = df_scores['七科总分'].rank(method='min', ascending=False)
    df_scores['七科年级排名并列人数'] = df_scores['七科年级排名'].map(df_scores['七科年级排名'].value_counts())
    
    # 按照七科成绩， 分别计算排名，最高分排名第一，如果并列，排名相同
    df_scores['语文班级排名'] = df_scores.groupby('班级')['语文'].rank(method='min', ascending=False)
    df_scores['语文班级排名并列人数'] = df_scores.groupby(['班级', '语文'])['学生'].transform('count')
    df_scores['数学班级排名'] = df_scores.groupby('班级')['数学'].rank(method='min', ascending=False)
    df_scores['数学班级排名并列人数'] = df_scores.groupby(['班级', '数学'])['学生'].transform('count')
    df_scores['英语班级排名'] = df_scores.groupby('班级')['英语'].rank(method='min', ascending=False)
    df_scores['英语班级排名并列人数'] = df_scores.groupby(['班级', '英语'])['学生'].transform('count')
    df_scores['政治班级排名'] = df_scores.groupby('班级')['政治'].rank(method='min', ascending=False)
    df_scores['政治班级排名并列人数'] = df_scores.groupby(['班级', '政治'])['学生'].transform('count')
    df_scores['历史班级排名'] = df_scores.groupby('班级')['历史'].rank(method='min', ascending=False)
    df_scores['历史班级排名并列人数'] = df_scores.groupby(['班级', '历史'])['学生'].transform('count')
    df_scores['地理班级排名'] = df_scores.groupby('班级')['地理'].rank(method='min', ascending=False)
    df_scores['地理班级排名并列人数'] = df_scores.groupby(['班级', '地理'])['学生'].transform('count')
    df_scores['生物班级排名'] = df_scores.groupby('班级')['生物'].rank(method='min', ascending=False)
    df_scores['生物班级排名并列人数'] = df_scores.groupby(['班级', '生物'])['学生'].transform('count')
    # 按照四科总分， 分别计算班级内排名，最高分排名第一，如果并列，排名相同
    df_scores['四科班级排名'] = df_scores.groupby('班级')['四科总分'].rank(method='min', ascending=False)
    df_scores['四科班级排名并列人数'] = df_scores.groupby(['班级', '四科总分'])['学生'].transform('count')
    df_scores['七科班级排名'] = df_scores.groupby('班级')['七科总分'].rank(method='min', ascending=False)
    df_scores['七科班级排名并列人数'] = df_scores.groupby(['班级', '七科总分'])['学生'].transform('count')
    
    
    # 取学生， 班级， 语文班级排名，语文班级排名并列人数
    # df2= df[['学生', '班级', '语文',  '语文班级排名', '语文班级排名并列人数']]
    
    # 按班级、语文排名
    # df2 =  df2.sort_values(by=['班级', '语文班级排名']) 
    
    # 打印分数
    # print(df)
   # save Excel
    df_scores.to_csv('data/scores-2.csv', encoding='utf-8', index=False)
    print('保存成功')
    
    # 保存成绩单
    save_report(df_scores)