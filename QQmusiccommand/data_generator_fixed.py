#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ音乐歌单数据生成器 - 修复版
为数据可视化项目创建模拟数据集
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_qq_music_data(num_songs=200):
    """
    生成QQ音乐歌单数据
    
    Parameters:
    num_songs (int): 生成的歌曲数量
    
    Returns:
    pd.DataFrame: 包含歌曲信息的DataFrame
    """
    
    # 设置随机种子以确保结果可重现
    np.random.seed(42)
    random.seed(42)
    
    # 定义数据
    artists = [
        '周杰伦', '林俊杰', '邓紫棋', '薛之谦', '李荣浩', '华晨宇', 'Taylor Swift', 
        'Ed Sheeran', 'Ariana Grande', 'Billie Eilish', 'The Weeknd', 'Dua Lipa',
        '陈奕迅', '王菲', '张学友', '刘德华', '蔡依林', '五月天', 'S.H.E',
        'BTS', 'Blackpink', 'TWICE', 'IU', '汪峰', '宋冬野', '马頔', '陈鸿宇', '赵雷'
    ]
    
    genres = ['流行', '摇滚', '民谣', '电子', '说唱', 'R&B', '爵士', '古典']
    
    song_names = [
        '告白气球', '演员', '小幸运', '青春修炼手册', '宠爱', '追光者', 
        '成都', '南山南', '董小姐', '理想', '斑马斑马', '安和桥',
        'Faded', 'Alone', 'Unity', 'Spectre', 'Animals', 'Titanium',
        'Blinding Lights', 'Save Your Tears', 'The Hills', 'Starboy',
        '中国有嘻哈', '嘻哈帝国', '说唱听我的', ' freestyle', 'battle',
        'What A Wonderful World', 'Fly Me To The Moon', 'Take Five',
        '月光奏鸣曲', '命运交响曲', '小夜曲', '天鹅湖', '卡农', '欢乐颂',
        '夜曲', '稻香', '青花瓷', '简单爱', '七里香', '晴天',
        '修炼爱情', '可惜没如果', '那些你很冒险的梦', '醉赤壁',
        '光年之外', '泡沫', '手心的蔷薇', '倒数', '句号',
        '绅士', '丑八怪', '演员', '意外', '天外来物',
        '模特', '李白', '不将就', '年少有为', '麻雀'
    ]
    
    albums = [
        '青春纪念册', '时光机', '梦想起航', '音乐之旅', '情感日记', '城市之光',
        '星空漫步', '心灵之声', '回忆碎片', '未来序曲', '经典重现', '新歌精选',
        '热门单曲', '年度精选', '最佳合集', '音乐盛典', '流行金曲', '经典回顾'
    ]
    
    # 生成数据
    data = []
    
    for i in range(num_songs):
        # 选择音乐风格
        genre = np.random.choice(genres)
        
        # 选择歌曲名称
        song_name = np.random.choice(song_names)
        
        # 根据风格选择艺术家
        if genre == '流行':
            popular_artists = ['周杰伦', '林俊杰', '邓紫棋', 'Taylor Swift', 'Ariana Grande', '薛之谦', '李荣浩']
            artist = np.random.choice([a for a in artists if a in popular_artists])
        elif genre == '摇滚':
            rock_artists = ['汪峰', '五月天', 'Beyond']
            artist = np.random.choice([a for a in artists if a in rock_artists])
        elif genre == '民谣':
            folk_artists = ['宋冬野', '马頔', '陈鸿宇', '赵雷']
            artist = np.random.choice([a for a in artists if a in folk_artists])
        else:
            artist = np.random.choice(artists)
        
        # 生成其他字段
        album = np.random.choice(albums)
        release_year = np.random.randint(2010, 2025)
        
        # 播放量（使用对数正态分布模拟真实数据）
        play_count = int(np.random.lognormal(15, 2))
        play_count = min(play_count, 100000000)  # 限制最大播放量
        
        # 歌曲时长（2-6分钟）
        duration = np.random.randint(120, 361)
        
        # 用户评分（1-10分，偏向高分）
        rating = round(np.random.beta(7, 3) * 9 + 1, 1)
        
        # 音乐特征（0-1之间的数值）
        danceability = round(np.random.beta(3, 2), 3)  # 舞蹈性
        energy = round(np.random.beta(2, 2), 3)        # 能量
        valence = round(np.random.beta(2, 3), 3)       # 情绪积极性
        acousticness = round(np.random.beta(2, 4), 3)  # 原声性
        
        # 创建歌曲记录
        song_data = {
            'song_id': i + 1,
            'song_name': song_name,
            'artist': artist,
            'album': album,
            'genre': genre,
            'release_year': release_year,
            'play_count': play_count,
            'duration': duration,
            'rating': rating,
            'danceability': danceability,
            'energy': energy,
            'valence': valence,
            'acousticness': acousticness
        }
        
        data.append(song_data)
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 添加一些衍生字段
    df['duration_minutes'] = round(df['duration'] / 60, 2)
    df['play_count_millions'] = round(df['play_count'] / 1000000, 2)
    
    return df

def save_data(df, filename='qq_music_data.csv'):
    """
    保存数据到CSV文件
    
    Parameters:
    df (pd.DataFrame): 要保存的数据
    filename (str): 文件名
    """
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"数据已保存到 {filename}")
    print(f"数据集包含 {len(df)} 首歌曲")

def basic_statistics(df):
    """
    输出基础统计信息
    
    Parameters:
    df (pd.DataFrame): 数据集
    """
    print("=== 数据集基础统计 ===")
    print(f"总歌曲数: {len(df)}")
    print(f"艺术家数量: {df['artist'].nunique()}")
    print(f"音乐风格: {', '.join(df['genre'].unique())}")
    print(f"年份范围: {df['release_year'].min()} - {df['release_year'].max()}")
    print(f"平均播放量: {df['play_count'].mean():.0f}")
    print(f"平均评分: {df['rating'].mean():.1f}")
    
    print("\n=== 各风格歌曲分布 ===")
    genre_counts = df['genre'].value_counts()
    for genre, count in genre_counts.items():
        print(f"{genre}: {count}首 ({count/len(df)*100:.1f}%)")

def main():
    """主函数"""
    print("正在生成QQ音乐歌单数据...")
    
    # 生成数据
    df = generate_qq_music_data(200)
    
    # 保存数据
    save_data(df)
    
    # 输出统计信息
    basic_statistics(df)
    
    # 显示前5行数据
    print("\n=== 数据预览 ===")
    print(df.head())
    
    print("\n数据生成完成！")

if __name__ == "__main__":
    main()