#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ音乐歌单数据可视化 - Flask Web应用
简单的Web应用，展示数据分析结果
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import json
import os

app = Flask(__name__)

# 全局变量存储数据
df = None

def load_data():
    """加载数据到内存"""
    global df
    try:
        df = pd.read_csv('QQmusiccommand\qq_music_data.csv')
        print(f"成功加载 {len(df)} 条数据记录")
    except FileNotFoundError:
        print("警告: 未找到数据文件 qq_music_data.csv")
        df = None

@app.route('/')
def index():
    """主页路由"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """获取所有数据的API"""
    if df is None:
        load_data()
    
    if df is not None:
        # 返回前50条数据
        data = df.head(50).to_dict('records')
        return jsonify(data)
    else:
        return jsonify([])

@app.route('/api/stats')
def get_stats():
    """获取统计信息的API"""
    if df is None:
        load_data()
    
    if df is not None:
        stats = {
            'total_songs': len(df),
            'total_artists': df['artist'].nunique(),
            'total_genres': df['genre'].nunique(),
            'avg_rating': round(df['rating'].mean(), 1),
            'avg_play_count': round(df['play_count_millions'].mean(), 2),
            'year_range': f"{df['release_year'].min()}-{df['release_year'].max()}",
            'genre_distribution': df['genre'].value_counts().to_dict(),
            'top_artists': df['artist'].value_counts().head(10).to_dict()
        }
        return jsonify(stats)
    else:
        return jsonify({})

@app.route('/api/filter')
def filter_data():
    """根据条件筛选数据的API"""
    if df is None:
        load_data()
    
    if df is None:
        return jsonify([])
    
    # 获取筛选参数
    genre = request.args.get('genre', '')
    artist = request.args.get('artist', '')
    min_rating = request.args.get('min_rating', type=float)
    max_rating = request.args.get('max_rating', type=float)
    year_from = request.args.get('year_from', type=int)
    year_to = request.args.get('year_to', type=int)
    
    # 开始筛选
    filtered_df = df.copy()
    
    if genre:
        filtered_df = filtered_df[filtered_df['genre'] == genre]
    
    if artist:
        filtered_df = filtered_df[filtered_df['artist'].str.contains(artist, case=False, na=False)]
    
    if min_rating is not None:
        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]
    
    if max_rating is not None:
        filtered_df = filtered_df[filtered_df['rating'] <= max_rating]
    
    if year_from is not None:
        filtered_df = filtered_df[filtered_df['release_year'] >= year_from]
    
    if year_to is not None:
        filtered_df = filtered_df[filtered_df['release_year'] <= year_to]
    
    # 返回筛选结果（限制数量）
    result = filtered_df.head(20).to_dict('records')
    return jsonify(result)

@app.route('/api/genres')
def get_genres():
    """获取所有音乐风格的API"""
    if df is None:
        load_data()
    
    if df is not None:
        genres = df['genre'].unique().tolist()
        return jsonify(genres)
    else:
        return jsonify([])

@app.route('/api/artists')
def get_artists():
    """获取所有艺术家的API"""
    if df is None:
        load_data()
    
    if df is not None:
        artists = df['artist'].unique().tolist()
        return jsonify(artists)
    else:
        return jsonify([])

@app.route('/analysis')
def analysis():
    """分析页面路由"""
    return render_template('analysis.html')

@app.route('/about')
def about():
    """关于页面路由"""
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    """404错误处理"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """500错误处理"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    # 启动时加载数据
    load_data()
    
    # 运行Flask应用
    app.run(debug=True, host='0.0.0.0', port=5000)