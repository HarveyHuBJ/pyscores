
import pandas as pd
import numpy as np
import json
import os

from lib.model.ClassReportModel import ClassReportModel,SubjectStatScoreModel,SubjectDistributionModel,StudentScore
from lib.model.StudentReportModel import StudentReportModel,SubjectScoreModel

# import imgkit
class ScoreReporter:

    def __init__(self, csv_file, json_file, level_file):
        # self.csv_file = csv_file
        # self.json_file = json_file

        self.df_scores = self.load_data(csv_file)
        self.config = self.load_config(json_file)

        subjects = [course['课程'] for course in self.config['考试课程'] if course['是否开设'] == '是']

        self.levels = self.load_levels(level_file, list(subjects))
        

        self.studentsReports = []
        self.classesReports = []

    def load_data(self, csv_file):
        # 读取csv数据
        df = pd.read_csv(csv_file, encoding='utf-8')
        return df

    def load_config(self, json_file):
        # 读取配置文件
        with open(json_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

    def load_levels(self, level_file, subjects):
        # 读取csv数据
        df = pd.read_csv(level_file, encoding='utf-8')

        # 检查线级是否在配置文件中
        for subject in subjects:
            if subject not in df.columns:
                raise ValueError(f"课程'{subject}' 未在配置文件{level_file}中。")

        # set index = '线级'
        df.set_index('线级', inplace=True)
        return df


    def calculate_classes(self):
        '''计算班级各科成绩的平均分、最高分、最低分、标准差、及格率、优秀率、线级分布等'''
        
        df_scores,  config = self.df_scores, self.config


        df_classes = pd.DataFrame()
        df_classes['班级'] = df_scores['班级'].unique()
        df_classes['学生人数'] = df_scores.groupby('班级')['学生'].count().values
        all_courses = [course['课程'] for course in config['考试课程'] if course['是否开设'] == '是']
        main_courses = [course['课程'] for course in config['考试课程'] if course['是否主课'] == '是']
        
        for course in all_courses:
            df_classes[f'{course}平均分'] = df_scores.groupby('班级')[course].mean().values
            df_classes[f'{course}最高分'] = df_scores.groupby('班级')[course].max().values
            df_classes[f'{course}最低分'] = df_scores.groupby('班级')[course].min().values
            df_classes[f'{course}中位数'] = df_scores.groupby('班级')[course].median().values
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
            
            df_classes['主课平均分'] = df_scores.groupby('班级')['主课总分'].mean().values
            df_classes['主课最高分'] = df_scores.groupby('班级')['主课总分'].max().values
            df_classes['主课最低分'] = df_scores.groupby('班级')['主课总分'].min().values
            df_classes['主课中位数'] = df_scores.groupby('班级')['主课总分'].median().values
            df_classes['主课标准差'] = df_scores.groupby('班级')['主课总分'].std().values
            
            df_classes['全部平均分'] = df_scores.groupby('班级')['全部总分'].mean().values
            df_classes['全部最高分'] = df_scores.groupby('班级')['全部总分'].max().values
            df_classes['全部最低分'] = df_scores.groupby('班级')['全部总分'].min().values
            df_classes['全部中位数'] = df_scores.groupby('班级')['全部总分'].median().values
            df_classes['全部标准差'] = df_scores.groupby('班级')['全部总分'].std().values

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

        # return df_classes  

        result = []

        # 将df_classes 转换为ClassReportModel对象列表
        for index, row in df_classes.iterrows():
            class_report = ClassReportModel()
            class_report.title = row['班级']
            class_report.class_name = row['班级']
            class_report.student_amount = row['学生人数']
            class_report.subject_scores = [SubjectStatScoreModel(subject=subject, 
                                                                 average_score=row[f'{subject}平均分'], 
                                                                    top_score=row[f'{subject}最高分'], 
                                                                    bottom_score=row[f'{subject}最低分'], 
                                                                    median_score=row[f'{subject}中位数'], 
                                                                    stderr=row[f'{subject}标准差']) 
                                                                    for subject in all_courses]
            
            # class_report.subject_distributions = [SubjectDistributionModel(subject=subject, 
            #                                                             level_a_amount=row[f'{subject}A线数量'], 
            #                                                             level_b_amount=row[f'{subject}B线数量'], 
            #                                                             level_c_amount=row[f'{subject}C线数量'], 
            #                                                             level_d_amount=row[f'{subject}D线数量'], 
            #                                                             level_a_students=row[f'{subject}A线名单'].split(',') if row[f'{subject}A线名单'] else [],
            #                                                             level_b_students=row[f'{subject}B线名单'].split(',') if row[f'{subject}B线名单'] else [],
            #                                                             level_c_students=row[f'{subject}C线名单'].split(',') if row[f'{subject}C线名单'] else [],
            #                                                             level_d_students=row[f'{subject}D线名单'].split(',') if row[f'{subject}D线名单'] else []
            #                                                             )
            #                                                             for subject in all_courses  
            #                                                             ]
            
            # class_report.level_a_lists = [StudentScore(name=student, score=row[f'{subject}A线分数']) for subject in all_courses for student in row[f'{subject}A线名单'].split(',')]

            result.append(class_report)
            return result
            
  
    

    def calculate_students(self):
        
        df_scores, df_levels, config = self.df_scores, self.levels, self.config

        # 取配置中的“是否开设”=“是”的课程
        all_courses = [course['课程'] for course in config['考试课程'] if course['是否开设'] == '是']
        main_courses = [course['课程'] for course in config['考试课程'] if course['是否主课'] == '是']

        
        # 计算分数, 给df增加两列，主课总分和全部总分
        df_scores['主课总分'] = df_scores[main_courses].sum(axis=1)
        df_scores['全部总分'] = df_scores[all_courses].sum(axis=1)
        
        # 计算线级， 给df增加七列，分别为语文线级，数学线级，英语线级，政治线级，历史线级，地理线级，生物线级
        # labels = list(df_levels['线级'].values)
        # 取df_levels index
        labels = list(df_levels.index)
        
        for course in all_courses:
            df_scores[f'{course}线级'] = pd.cut(df_scores[course], bins=list(df_levels[course].values)+[1000], labels=labels, right=False)
            df_scores["A线数量"] = df_scores.apply(lambda x: sum([1 for i in x[11:] if i == 'A线']), axis=1)
        
        for course in all_courses:
            # method='min'表示并列时取最小排名，ascending=False表示降序排名
            df_scores[f'{course}年级排名'] = df_scores[course].rank(method='min', ascending=False)
            df_scores[f'{course}年级排名并列人数'] = df_scores[course].map(df_scores[course].value_counts())
            df_scores[f'{course}班级排名'] = df_scores.groupby('班级')[course].rank(method='min', ascending=False)
            df_scores[f'{course}班级排名并列人数'] = df_scores.groupby(['班级', course])['学生'].transform('count')
            
            
            
        df_scores['主课总分线级'] = pd.cut(df_scores['主课总分'], bins=list(df_levels['主课总分'].values)+[1000], labels=labels, right=False)
        # 给df增加列， 分别按照主课总分和全部总分排名，最高分排名第一，取整数排名
        df_scores['主课年级排名'] = df_scores['主课总分'].rank(method='min', ascending=False)
        df_scores['主课年级排名并列人数'] =  df_scores['主课年级排名'].map(df_scores['主课年级排名'].value_counts())

        # 按照主课总分， 分别计算班级内排名，最高分排名第一，如果并列，排名相同
        df_scores['主课班级排名'] = df_scores.groupby('班级')['主课总分'].rank(method='min', ascending=False)
        df_scores['主课班级排名并列人数'] = df_scores.groupby(['班级', '主课总分'])['学生'].transform('count')

        df_scores['全部总分线级'] = pd.cut(df_scores['全部总分'], bins=list(df_levels['全部总分'].values)+[1000], labels=labels, right=False)
        df_scores['全部班级排名'] = df_scores.groupby('班级')['全部总分'].rank(method='min', ascending=False)
        df_scores['全部班级排名并列人数'] = df_scores.groupby(['班级', '全部总分'])['学生'].transform('count')
        df_scores['全部年级排名'] = df_scores['全部总分'].rank(method='min', ascending=False)
        df_scores['全部年级排名并列人数'] = df_scores['全部年级排名'].map(df_scores['全部年级排名'].value_counts())

        # 返回 StudentReportModel list 对象
        
        result = []
        for index, row in df_scores.iterrows():
            student_report = StudentReportModel()
            student_report.title = "TBD"
            student_report.student_name = row['学生']
            student_report.class_name = row['班级']
            student_report.subject_scores = []
            for course in all_courses:
                subject_score = SubjectScoreModel()
                subject_score.subject = course
                subject_score.score = row[course]
                subject_score.score_level = row[f'{course}线级']
                subject_score.score_level_bound = df_levels[course][subject_score.score_level]
                subject_score.class_rank = row[f'{course}班级排名']
                subject_score.class_rank_amount = row[f'{course}班级排名并列人数']
                subject_score.grade_rank = row[f'{course}年级排名']
                subject_score.grade_rank_amount = row[f'{course}年级排名并列人数']
                subject_score.is_major = course in main_courses
                student_report.subject_scores.append(subject_score)


            main_summary = SubjectScoreModel()
            main_summary.subject = "主课总分"
            main_summary.score = row['主课总分']
            main_summary.score_level = row['主课总分线级']
            main_summary.score_level_bound = df_levels['主课总分'][main_summary.score_level]
            main_summary.class_rank = row['主课班级排名']
            main_summary.class_rank_amount = row['主课班级排名并列人数']
            main_summary.grade_rank = row['主课年级排名']
            main_summary.grade_rank_amount = row['主课年级排名并列人数']
            main_summary.is_major = True
            student_report.summary.append(main_summary)

            all_summary = SubjectScoreModel()
            all_summary.subject = "全部总分"
            all_summary.score = row['全部总分']
            all_summary.score_level = row['全部总分线级']
            all_summary.score_level_bound = df_levels['全部总分'][all_summary.score_level]
            all_summary.class_rank = row['全部班级排名']
            all_summary.class_rank_amount = row['全部班级排名并列人数']
            all_summary.grade_rank = row['全部年级排名']
            all_summary.grade_rank_amount = row['全部年级排名并列人数']
            student_report.summary.append(all_summary)
            result.append(student_report) 
        return result
                
                 
