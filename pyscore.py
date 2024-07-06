
import pandas as pd
import numpy as np
import json
import os


def load_data(csv_file):
    # 读取Excel数据
    df = pd.read_csv(csv_file, encoding='utf-8')
    return df

def load_config(json_file):
    # 读取配置文件
    with open(json_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def grade_rank_desc(data, subject):
    # 计算排名，最高分排名第一，如果并列，排名相同
    n = data[f'{subject}年级排名']
    k = data[f'{subject}年级排名并列人数']  
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


def row_render(data, course):
    # 生成html表格的一行
    return f'''
    <tr>
        <th>{course}</th>
        <td>{data[course]}</td>
        <td>{data[f"{course}线级"]}</td>
        <td>{class_rank_desc(data, course)}</td>
        <td>{grade_rank_desc(data, course)}</td>
    </tr>
    '''

def list_render(list):
    '''生成html无序列表'''
    result = []
    result.append(f'<div class="h3">{len(list)}人</div>')
    result.append('<div><ul>')
    result.append('\n'.join([f'<li>{item}</li>' for item in list]))
    result.append('</ul></div>')
    return '\n'.join(result)
    

def save_students_report(df, config, grade_name):   
    
    all_courses = [course['课程'] for course in config['考试课程'] if course['是否开设'] == '是']
    title = config['考试名称']
    # 分别为每一名学生打印成绩单报告，html格式
    for i in range(len(df)):
        student = df.iloc[i]
        html = []
        html.append( f'''
        
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
        div.h3 {{
            font-size: 20px;
            font-weight: bold;
            text-align: left;
        }}
        h1{{text-align:center;}}
        </style>
        </head>
        <body>
        <h1>{title}-成绩单</h1>
        <table>
        <tr><th>学生</th><td colspan='4'>{student['学生']}</td></tr>
        <tr><th>班级</th><td colspan='4'>{student['班级']}</td></tr>
        <tr><th>科目</th><th>考试成绩</th><th>线级</th><th>班级排名</th><th>年级排名</th></tr>
        '''
        )
        html.append('\n'.join([row_render(student, course) for course in all_courses]) )
        html.append( f'''
        <tr><th>四科总分</th><td>{student['四科总分']}</td><td>{student['四科总分线级']}</td><td>{class_rank_desc(student,'四科')}</td><td>{grade_rank_desc(student,'四科')}</td></tr>
        <tr><th>七科总分</th><td>{student['七科总分']}</td><td>{student['七科总分线级']}</td><td>{class_rank_desc(student,'七科')}</td><td>{grade_rank_desc(student,'七科')}</td></tr>
        </table>
        </body>
        ''')
        
        htmls = '\n'.join(html)
        
        identity = f'{student["班级"]}-{student["学生"]}'
        
        # 判断output目录是否存在，不存在则创建
        if not os.path.exists(f'output/{grade_name}'):
            os.mkdir(f'output/{grade_name}')
        
        # 保存成绩单
        with open(f'output/{grade_name}/{identity}.html', 'w', encoding='utf-8') as f:
            f.write(htmls)
        print(f'{identity}的成绩单保存成功')
    pass


def save_classes_report(df, config, grade_name):
    '''保存班级报告'''
    all_courses = [course['课程'] for course in config['考试课程'] if course['是否开设'] == '是']
    title = config['考试名称']
    
    # 分别为每一个班级打印成绩单报告，html格式
    for i in range(len(df)):
        class_data = df.iloc[i]
        html = []
        html.append( f'''
        
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
            vertical-align: text-top;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        ul {{
            list-style-type: none;
            text-align: justify;
        }}
        li {{
            display: inline-block;
            width: 90px;
            margin-right: 10px;
        }}
        
        div.h3 {{
            font-size: 20px;
            font-weight: bold;
            padding-left: 40px;
            text-align: left;
        }}
        h1{{text-align:center;}}
        </style>
        </head>
        <body>
        <h1>{title}-班级报告</h1>
        <table>
        <tr><th>班级</th><td colspan='5'>{class_data['班级']}</td></tr>
        <tr><th>学生人数</th><td colspan='5'>{class_data['学生人数']}</td></tr>
        <tr><th>科目</th><th>平均分</th><th>最高分</th><th>最低分</th><th>中位数</th><th>标准差</th></tr>
        '''
        )
        html.append('\n'.join([f'''
        <tr>
            <th>{course}</th>
            <td>{class_data[f'{course}平均分']:.2f}</td>
            <td>{class_data[f'{course}最高分']}</td>
            <td>{class_data[f'{course}最低分']}</td>
            <td>{class_data[f'{course}中位数']}</td>
            <td>{class_data[f'{course}标准差']:.2f}</td>
        </tr>
        ''' for course in all_courses]) )
        
        html.append( f'''
        <tr><th>四科总分</th><td>{class_data['四科平均分']:.2f}</td><td>{class_data['四科最高分']}</td><td>{class_data['四科最低分']}</td><td>{class_data['四科中位数']}</td><td>{class_data['四科标准差']:.2f}</td></tr>
        <tr><th>七科总分</th><td>{class_data['七科平均分']:.2f}</td><td>{class_data['七科最高分']}</td><td>{class_data['七科最低分']}</td><td>{class_data['七科中位数']}</td><td>{class_data['七科标准差']:.2f}</td></tr>
        </table>
        <table>
        <tr><th>科目</th><th>A级成绩名单</th><th>B级成绩名单</th><th>C级成绩名单</th><th>D级成绩名单</th></tr>
        '''
        )
        html.append('\n'.join([f'''
        <tr>
            <th>{course}</th>
            <td>{list_render(class_data[f'{course}A级成绩名单'])}</td>
            <td>{list_render(class_data[f'{course}B级成绩名单'])}</td>
            <td>{list_render(class_data[f'{course}C级成绩名单'])}</td>
            <td>{list_render(class_data[f'{course}D级成绩名单'])}</td>
        </tr>
        ''' for course in all_courses]) )
        
        html.append( f'''
        </table>
        <table>
            
            <tr><th>7科A线名单</th><td>{list_render(class_data['7A线名单'])}</td>  </tr>
            <tr><th>6科A线名单</th><td>{list_render(class_data['6A线名单'])}</td>  </tr> 
            <tr><th>5科A线名单</th><td>{list_render(class_data['5A线名单'])}</td>  </tr>
            <tr><th>4科A线名单</th><td>{list_render(class_data['4A线名单'])}</td> </tr>  
            <tr><th>3科A线名单</th><td>{list_render(class_data['3A线名单'])}</td> </tr>  
            <tr><th>2科A线名单</th><td>{list_render(class_data['2A线名单'])}</td>  </tr> 
            <tr><th>1科A线名单</th><td>{list_render(class_data['1A线名单'])}</td></tr> 
            <tr><th>0科A线名单</th><td>{list_render(class_data['0A线名单'])}</td></tr> 
            
                  ''' )
        
        html.append( f'''
        </table>
        </body>
        ''')
        
        htmls = '\n'.join(html)
        
        identity = f'{class_data["班级"]}'
        
        # 判断output目录是否存在，不存在则创建
        if not os.path.exists(f'output/{grade_name}'):
            os.mkdir(f'output/{grade_name}')
            
        # 保存班级报告
        with open(f'output/{grade_name}/{identity}.html', 'w', encoding='utf-8') as f:
            f.write(htmls)
        print(f'{identity}的班级报告保存成功')
    pass

    

def get_grade_name(grade):
    '''年级名称'''
    if grade == 7:
        return '初一'
    elif grade == 8:
        return '初二'
    elif grade == 9:
        return '初三'
    else:
        return None

def read_data_of_grade(grade_name):
    '''读取年级考试成绩数据'''
    df_scores = load_data(f'data/{grade_name}/scores.csv')
    return df_scores
    

def read_levels_of_grade(grade_name):
    '''读取线级数据'''
    df_levels = load_data(f'data/{grade_name}/levels.csv')
    return df_levels

def read_config(grade_name):
    '''读取配置文件'''
    config = load_config(f'data/{grade_name}/config.json')
    return config

def calculate_classes(df_scores, df_levels, config):
    '''计算班级各科成绩的平均分、最高分、最低分、标准差、及格率、优秀率、线级分布等'''
    
    df_classes = pd.DataFrame()
    df_classes['班级'] = df_scores['班级'].unique()
    df_classes['学生人数'] = df_scores.groupby('班级')['学生'].count().values
    all_courses = [course['课程'] for course in config['考试课程'] if course['是否开设'] == '是']
    main_courses = [course['课程'] for course in config['考试课程'] if course['是否主课'] == '是']
    
    for course in all_courses:
        df_classes[f'{course}平均分'] = df_scores.groupby('班级')[course].mean().values
        df_classes[f'{course}最高分'] = df_scores.groupby('班级')[course].max().values
        df_classes[f'{course}最低分'] = df_scores.groupby('班级')[course].min().values
        df_classes[f'{course}中位数'] =  df_scores.groupby('班级')[course].median().values
        df_classes[f'{course}标准差'] = df_scores.groupby('班级')[course].std().values
        # 计算线级分布
        df_a = df_scores[df_scores[f'{course}线级'] == 'A线'].groupby('班级')['学生'].apply(list).reset_index(name=f'{course}A级成绩名单')
        df_b = df_scores[df_scores[f'{course}线级'] == 'B线'].groupby('班级')['学生'].apply(list).reset_index(name=f'{course}B级成绩名单')
        df_c = df_scores[df_scores[f'{course}线级'] == 'C线'].groupby('班级')['学生'].apply(list).reset_index(name=f'{course}C级成绩名单')
        df_d = df_scores[df_scores[f'{course}线级'] == 'D线'].groupby('班级')['学生'].apply(list).reset_index(name=f'{course}D级成绩名单')

        df_classes = df_classes.merge(df_a, on='班级', how='outer').fillna('')
        df_classes = df_classes.merge(df_b, on='班级', how='outer').fillna('')
        df_classes = df_classes.merge(df_c, on='班级', how='outer').fillna('')
        df_classes = df_classes.merge(df_d, on='班级', how='outer').fillna('')
        
        df_classes['四科平均分'] = df_scores.groupby('班级')['四科总分'].mean().values
        df_classes['四科最高分'] = df_scores.groupby('班级')['四科总分'].max().values
        df_classes['四科最低分'] = df_scores.groupby('班级')['四科总分'].min().values
        df_classes['四科中位数'] = df_scores.groupby('班级')['四科总分'].median().values
        df_classes['四科标准差'] = df_scores.groupby('班级')['四科总分'].std().values
        
        df_classes['七科平均分'] = df_scores.groupby('班级')['七科总分'].mean().values
        df_classes['七科最高分'] = df_scores.groupby('班级')['七科总分'].max().values
        df_classes['七科最低分'] = df_scores.groupby('班级')['七科总分'].min().values
        df_classes['七科中位数'] = df_scores.groupby('班级')['七科总分'].median().values
        df_classes['七科标准差'] = df_scores.groupby('班级')['七科总分'].std().values

    df_0A = df_scores[df_scores['A线数量'] == 0].groupby('班级')['学生'].apply(list).reset_index(name='0A线名单')
    df_1A = df_scores[df_scores['A线数量'] == 1].groupby('班级')['学生'].apply(list).reset_index(name='1A线名单')
    df_2A = df_scores[df_scores['A线数量'] == 2].groupby('班级')['学生'].apply(list).reset_index(name='2A线名单')
    df_3A = df_scores[df_scores['A线数量'] == 3].groupby('班级')['学生'].apply(list).reset_index(name='3A线名单')
    df_4A = df_scores[df_scores['A线数量'] == 4].groupby('班级')['学生'].apply(list).reset_index(name='4A线名单')
    df_5A = df_scores[df_scores['A线数量'] == 5].groupby('班级')['学生'].apply(list).reset_index(name='5A线名单')
    df_6A = df_scores[df_scores['A线数量'] == 6].groupby('班级')['学生'].apply(list).reset_index(name='6A线名单')
    df_7A = df_scores[df_scores['A线数量'] == 7].groupby('班级')['学生'].apply(list).reset_index(name='7A线名单')


    df_classes = df_classes.merge(df_7A, on='班级', how='outer').fillna('')
    df_classes = df_classes.merge(df_6A, on='班级', how='outer').fillna('')
    df_classes = df_classes.merge(df_5A, on='班级', how='outer').fillna('')
    df_classes = df_classes.merge(df_4A, on='班级', how='outer').fillna('')
    df_classes = df_classes.merge(df_3A, on='班级', how='outer').fillna('')
    df_classes = df_classes.merge(df_2A, on='班级', how='outer').fillna('')
    df_classes = df_classes.merge(df_1A, on='班级', how='outer').fillna('')
    df_classes = df_classes.merge(df_0A, on='班级', how='outer').fillna('')

    return df_classes  


def calculate_students(df_scores, df_levels, config):
    
    # 取配置中的“是否开设”=“是”的课程
    all_courses = [course['课程'] for course in config['考试课程'] if course['是否开设'] == '是']
    main_courses = [course['课程'] for course in config['考试课程'] if course['是否主课'] == '是']

    
     # 计算分数, 给df增加两列，四科总分和七科总分
    df_scores['四科总分'] = df_scores[main_courses].sum(axis=1)
    df_scores['七科总分'] = df_scores[all_courses].sum(axis=1)
    
    # 计算线级， 给df增加七列，分别为语文线级，数学线级，英语线级，政治线级，历史线级，地理线级，生物线级
    labels = list(df_levels['线级'].values)
    
    for course in all_courses:
        df_scores[f'{course}线级'] = pd.cut(df_scores[course], bins=list(df_levels[course].values)+[1000], labels=labels)
        df_scores["A线数量"] = df_scores.apply(lambda x: sum([1 for i in x[11:] if i == 'A线']), axis=1)
       
    for course in all_courses:
        # method='min'表示并列时取最小排名，ascending=False表示降序排名
        df_scores[f'{course}年级排名'] = df_scores[course].rank(method='min', ascending=False)
        df_scores[f'{course}年级排名并列人数'] = df_scores[course].map(df_scores[course].value_counts())
        df_scores[f'{course}班级排名'] = df_scores.groupby('班级')[course].rank(method='min', ascending=False)
        df_scores[f'{course}班级排名并列人数'] = df_scores.groupby(['班级', course])['学生'].transform('count')
        
        
        
    df_scores['四科总分线级'] = pd.cut(df_scores['四科总分'], bins=list(df_levels['四科总分'].values)+[1000], labels=labels)
    # 给df增加列， 分别按照四科总分和七科总分排名，最高分排名第一，取整数排名
    df_scores['四科年级排名'] = df_scores['四科总分'].rank(method='min', ascending=False)
    df_scores['四科年级排名并列人数'] =  df_scores['四科年级排名'].map(df_scores['四科年级排名'].value_counts())

    # 按照四科总分， 分别计算班级内排名，最高分排名第一，如果并列，排名相同
    df_scores['四科班级排名'] = df_scores.groupby('班级')['四科总分'].rank(method='min', ascending=False)
    df_scores['四科班级排名并列人数'] = df_scores.groupby(['班级', '四科总分'])['学生'].transform('count')

    df_scores['七科总分线级'] = pd.cut(df_scores['七科总分'], bins=list(df_levels['七科总分'].values)+[1000], labels=labels)
    df_scores['七科班级排名'] = df_scores.groupby('班级')['七科总分'].rank(method='min', ascending=False)
    df_scores['七科班级排名并列人数'] = df_scores.groupby(['班级', '七科总分'])['学生'].transform('count')
    df_scores['七科年级排名'] = df_scores['七科总分'].rank(method='min', ascending=False)
    df_scores['七科年级排名并列人数'] = df_scores['七科年级排名'].map(df_scores['七科年级排名'].value_counts())

    pass

# 入口是main
if __name__ == '__main__':
    
    # 接收用户输入
    grade = int(input('请输入年级： (7, 8, 9)'))
    
    while grade not in [7, 8, 9]:
        grade = int(input('输入有误，请输入年级： (7, 8, 9)'))
    
    # 读取指定年级的数据
    grade_name = get_grade_name(grade)
    df_scores = read_data_of_grade(grade_name)
    df_levels = read_levels_of_grade(grade_name)
    config = read_config(grade_name)
    
    # 判断output/{grade_name}目录是否存在，不存在则创建
    if not os.path.exists(f'output/{grade_name}'):
        os.makedirs(f'output/{grade_name}')
        
    
    calculate_students(df_scores, df_levels, config)
    
    # save Excel
    df_scores.to_csv(f'output/{grade_name}/scores-result.csv', encoding='utf-8', index=False)
    print('保存成功')
    
    # 保存成绩单
    save_students_report(df_scores, config, grade_name)
    
    df_classes = calculate_classes(df_scores, df_levels, config)
    
        # 判断output目录是否存在，不存在则创建

    # save Excel
    df_classes.to_csv(f'output/{grade_name}/classes-result.csv', encoding='utf-8', index=False)
    
    save_classes_report(df_classes, config, grade_name)