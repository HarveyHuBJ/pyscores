import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


# 设置中文字体
font_path = 'C:\\Windows\\Fonts\\simhei.ttf'  # Windows 系统中的 SimHei 字体
fontprop = FontProperties(fname=font_path)


# 颜色设置 
# colors = ['skyblue', 'lightgreen', 'lightcoral']
sys_colors = {
    # 7 种蓝色  
    "blues": ['#332B3A', '#132666', '#3A4D8F', '#6A95CC', '#A1CAFF', '#3b409f' ],
    # 7 种不同程度的灰色
    "grays": ['#7f7f7f', '#7f7f7f', '#7f7f7f', '#7f7f7f', '#7f7f7f', '#7f7f7f', '#7f7f7f'],
    # 7 种绿色
    "greens": ['#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22'],
    # 7 种黄色
    "yellows": ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
    # 7 种红色
    "reds": ['#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
    # 7 种颜色， ABCDF
    "same_saturation": ['#d4220e', '#ef8b43', '#f3c632', '#90f36f', '#055c23', '#98df8a', '#d62728']
} 

class SubjectDistributionDrawer:

    def __init__(self):
        pass

    def plot_cluster_bar_chart(self, df, output_path):

        # 将df保存csv文件
        df.to_csv('data/temp_plot_cluster_bar_chart.csv')
   
        # 数据准备
        subjects = df.index.tolist()
        score_lines = df.columns.tolist()
        scores_data = df.values
      
        # 设置柱形图的位置
        n_subjects = len(subjects)
        n_score_lines = len(score_lines)
        bar_width = 0.125
        index = np.arange(n_subjects)

        # 绘制柱形图
        fig, ax = plt.subplots(figsize=(12, 6))

        # 设置图像宽度


        colors = sys_colors['same_saturation']

        
        # 绘制柱形图并添加数值标签
        for i, score_line in enumerate(score_lines):
            # 绘制柱形图
            pos = index + (i- n_score_lines/2)* bar_width
            bars = ax.bar(pos,  # 柱形图位置
                          scores_data[:, i], # 柱形图高度
                          bar_width, # 柱形图宽度
                          label=score_line, # 柱形图标签
                          color=colors[i] # 柱形图颜色
                          )
            # 在每个柱子的顶部添加数值标签
            for j, bar in enumerate(bars):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}',
                        ha='center', va='bottom', fontproperties=fontprop)

        # 添加标题和标签
        ax.set_xlabel('学科名称', fontproperties=fontprop)
        ax.set_ylabel('人数', fontproperties=fontprop)
        ax.set_title('各学科各分数线的人数分布', fontproperties=fontprop)
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(subjects, fontproperties=fontprop)
        ax.legend(prop=fontprop)

        # 检查输出路径是否存在
        dir_path = os.path.dirname(output_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # 将图表导出为png图片
        plt.savefig(output_path)