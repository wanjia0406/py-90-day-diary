#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ音乐歌单数据可视化 - 基础版本
使用Matplotlib和Seaborn创建静态图表
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib import font_manager

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_output_dir():
    """创建输出目录"""
    if not os.path.exists('charts'):
        os.makedirs('charts')
    if not os.path.exists('static/charts'):
        os.makedirs('static/charts')

def load_data():
    """加载数据"""
    try:
        df = pd.read_csv('qq_music_data.csv')
        print(f"成功加载数据，共{len(df)}条记录")
        return df
    except FileNotFoundError:
        print("未找到数据文件，请先运行data_generator_fixed.py")
        return None

def plot_genre_distribution(df):
    """音乐风格分布饼图"""
    plt.figure(figsize=(10, 8))
    
    genre_counts = df['genre'].value_counts()
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF', '#FFCC66', '#CC99FF']
    
    wedges, texts, autotexts = plt.pie(genre_counts.values, 
                                      labels=genre_counts.index,
                                      autopct='%1.1f%%',
                                      colors=colors,
                                      startangle=90)
    
    # 美化文本
    for text in texts:
        text.set_fontsize(12)
        text.set_fontweight('bold')
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    plt.title('QQ音乐歌单 - 音乐风格分布', fontsize=16, fontweight='bold', pad=20)
    plt.axis('equal')
    
    # 保存图片
    plt.savefig('charts/genre_distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig('static/charts/genre_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 音乐风格分布图已生成")

def plot_year_distribution(df):
    """发行年份分布直方图"""
    plt.figure(figsize=(12, 6))
    
    # 创建直方图
    plt.hist(df['release_year'], bins=15, color='skyblue', alpha=0.7, edgecolor='black')
    
    # 添加统计信息
    mean_year = df['release_year'].mean()
    plt.axvline(mean_year, color='red', linestyle='--', linewidth=2, label=f'平均年份: {mean_year:.1f}')
    
    plt.xlabel('发行年份', fontsize=12)
    plt.ylabel('歌曲数量', fontsize=12)
    plt.title('歌曲发行年份分布', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 保存图片
    plt.savefig('charts/year_distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig('static/charts/year_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 发行年份分布图已生成")

def plot_artist_songs(df):
    """艺术家歌曲数量柱状图"""
    plt.figure(figsize=(14, 8))
    
    # 统计每个艺术家的歌曲数量
    artist_counts = df['artist'].value_counts().head(15)
    
    # 创建柱状图
    bars = plt.bar(range(len(artist_counts)), artist_counts.values, 
                   color='lightcoral', alpha=0.8)
    
    # 设置x轴标签
    plt.xticks(range(len(artist_counts)), artist_counts.index, 
               rotation=45, ha='right')
    
    # 添加数值标签
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.xlabel('艺术家', fontsize=12)
    plt.ylabel('歌曲数量', fontsize=12)
    plt.title('TOP15 艺术家歌曲数量', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    plt.savefig('charts/artist_songs.png', dpi=300, bbox_inches='tight')
    plt.savefig('static/charts/artist_songs.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 艺术家歌曲数量图已生成")

def plot_play_count_trend(df):
    """播放量趋势分析"""
    plt.figure(figsize=(12, 6))
    
    # 按年份统计平均播放量
    yearly_plays = df.groupby('release_year')['play_count_millions'].mean()
    
    # 创建折线图
    plt.plot(yearly_plays.index, yearly_plays.values, 
             marker='o', linewidth=2, markersize=8, color='purple')
    
    plt.xlabel('发行年份', fontsize=12)
    plt.ylabel('平均播放量 (百万)', fontsize=12)
    plt.title('各年份歌曲平均播放量趋势', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # 添加数值标签
    for x, y in zip(yearly_plays.index, yearly_plays.values):
        plt.annotate(f'{y:.1f}M', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontweight='bold')
    
    # 保存图片
    plt.savefig('charts/play_count_trend.png', dpi=300, bbox_inches='tight')
    plt.savefig('static/charts/play_count_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 播放量趋势图已生成")

def plot_rating_vs_plays(df):
    """评分与播放量关系散点图"""
    plt.figure(figsize=(12, 8))
    
    # 创建散点图
    scatter = plt.scatter(df['rating'], df['play_count_millions'], 
                         c=df['energy'], cmap='viridis', alpha=0.6, s=60)
    
    # 添加颜色条
    cbar = plt.colorbar(scatter)
    cbar.set_label('能量值', fontsize=12)
    
    plt.xlabel('用户评分', fontsize=12)
    plt.ylabel('播放量 (百万)', fontsize=12)
    plt.title('用户评分与播放量关系图', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # 添加趋势线
    z = np.polyfit(df['rating'], df['play_count_millions'], 1)
    p = np.poly1d(z)
    plt.plot(df['rating'], p(df['rating']), "r--", alpha=0.8, linewidth=2)
    
    # 保存图片
    plt.savefig('charts/rating_vs_plays.png', dpi=300, bbox_inches='tight')
    plt.savefig('static/charts/rating_vs_plays.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 评分与播放量关系图已生成")

def plot_duration_distribution(df):
    """歌曲时长分布"""
    plt.figure(figsize=(12, 6))
    
    # 创建直方图
    plt.hist(df['duration_minutes'], bins=20, color='lightgreen', 
             alpha=0.7, edgecolor='black')
    
    # 添加统计信息
    mean_duration = df['duration_minutes'].mean()
    plt.axvline(mean_duration, color='red', linestyle='--', 
                linewidth=2, label=f'平均时长: {mean_duration:.1f}分钟')
    
    plt.xlabel('歌曲时长 (分钟)', fontsize=12)
    plt.ylabel('歌曲数量', fontsize=12)
    plt.title('歌曲时长分布', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 保存图片
    plt.savefig('charts/duration_distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig('static/charts/duration_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 歌曲时长分布图已生成")

def plot_genre_heatmap(df):
    """音乐特征热力图"""
    plt.figure(figsize=(10, 8))
    
    # 计算各风格的平均特征
    genre_features = df.groupby('genre')[['danceability', 'energy', 'valence', 'acousticness']].mean()
    
    # 创建热力图
    sns.heatmap(genre_features, annot=True, cmap='YlOrRd', 
                fmt='.3f', cbar_kws={'label': '平均值'})
    
    plt.title('各音乐风格特征热力图', fontsize=16, fontweight='bold')
    plt.xlabel('音乐特征', fontsize=12)
    plt.ylabel('音乐风格', fontsize=12)
    
    # 保存图片
    plt.savefig('charts/genre_heatmap.png', dpi=300, bbox_inches='tight')
    plt.savefig('static/charts/genre_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✓ 音乐特征热力图已生成")

def generate_all_charts():
    """生成所有图表"""
    print("开始生成图表...")
    
    # 创建输出目录
    create_output_dir()
    
    # 加载数据
    df = load_data()
    if df is None:
        return
    
    print(f"正在处理{len(df)}条数据...")
    
    # 生成各类图表
    try:
        plot_genre_distribution(df)
        plot_year_distribution(df)
        plot_artist_songs(df)
        plot_play_count_trend(df)
        plot_rating_vs_plays(df)
        plot_duration_distribution(df)
        plot_genre_heatmap(df)
        
        print("\n🎉 所有图表生成完成！")
        print("图表保存在: charts/ 和 static/charts/ 文件夹")
        
        # 输出数据基本信息
        print(f"\n📊 数据概览:")
        print(f"- 总歌曲数: {len(df)}")
        print(f"- 艺术家数量: {df['artist'].nunique()}")
        print(f"- 音乐风格: {df['genre'].nunique()}种")
        print(f"- 年份范围: {df['release_year'].min()}-{df['release_year'].max()}")
        print(f"- 平均评分: {df['rating'].mean():.1f}")
        
    except Exception as e:
        print(f"生成图表时出错: {e}")

def main():
    """主函数"""
    generate_all_charts()

if __name__ == "__main__":
    main()