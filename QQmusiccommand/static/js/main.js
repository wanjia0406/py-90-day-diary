// QQ音乐数据分析 - 主要JavaScript文件

// 全局变量
let allData = [];
let filteredData = [];
let currentPage = 1;
const itemsPerPage = 10;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// 初始化应用
async function initializeApp() {
    try {
        // 加载统计数据
        await loadStats();
        
        // 加载筛选选项
        await loadFilterOptions();
        
        // 加载初始数据
        await loadData();
        
        // 绑定事件监听器
        bindEventListeners();
        
        console.log('应用初始化完成');
    } catch (error) {
        console.error('初始化失败:', error);
        showMessage('应用初始化失败，请刷新页面重试', 'error');
    }
}

// 加载统计数据
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        if (Object.keys(stats).length > 0) {
            displayStats(stats);
        } else {
            displayDefaultStats();
        }
    } catch (error) {
        console.error('加载统计数据失败:', error);
        displayDefaultStats();
    }
}

// 显示统计数据
function displayStats(stats) {
    const statsGrid = document.getElementById('stats-grid');
    
    const statCards = [
        { label: '总歌曲数', value: stats.total_songs || 200 },
        { label: '艺术家数量', value: stats.total_artists || 28 },
        { label: '音乐风格', value: stats.total_genres || 8 },
        { label: '平均评分', value: stats.avg_rating || 7.2 },
        { label: '平均播放量', value: `${stats.avg_play_count || 6.9}M` }
    ];
    
    statsGrid.innerHTML = statCards.map(stat => `
        <div class="stat-card">
            <div class="stat-number">${stat.value}</div>
            <div class="stat-label">${stat.label}</div>
        </div>
    `).join('');
}

// 显示默认统计数据
function displayDefaultStats() {
    const statsGrid = document.getElementById('stats-grid');
    
    const defaultStats = [
        { label: '总歌曲数', value: 200 },
        { label: '艺术家数量', value: 28 },
        { label: '音乐风格', value: 8 },
        { label: '平均评分', value: 7.2 },
        { label: '平均播放量', value: '6.9M' }
    ];
    
    statsGrid.innerHTML = defaultStats.map(stat => `
        <div class="stat-card">
            <div class="stat-number">${stat.value}</div>
            <div class="stat-label">${stat.label}</div>
        </div>
    `).join('');
}

// 加载筛选选项
async function loadFilterOptions() {
    try {
        // 加载音乐风格选项
        const genreResponse = await fetch('/api/genres');
        const genres = await genreResponse.json();
        
        const genreSelect = document.getElementById('genre-filter');
        genreSelect.innerHTML = '<option value="">全部</option>';
        genres.forEach(genre => {
            const option = document.createElement('option');
            option.value = genre;
            option.textContent = genre;
            genreSelect.appendChild(option);
        });
        
        console.log('筛选选项加载完成');
    } catch (error) {
        console.error('加载筛选选项失败:', error);
    }
}

// 加载数据
async function loadData(filters = {}) {
    try {
        let url = '/api/data';
        
        // 如果有筛选条件，使用筛选API
        if (Object.keys(filters).length > 0) {
            url = '/api/filter';
            const params = new URLSearchParams(filters);
            url += '?' + params.toString();
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        allData = data;
        filteredData = [...allData];
        
        displayData();
        updateResultCount();
        
    } catch (error) {
        console.error('加载数据失败:', error);
        showMessage('数据加载失败', 'error');
    }
}

// 显示数据表格
function displayData() {
    const tableBody = document.getElementById('table-body');
    
    if (filteredData.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="8" class="empty-state">
                    <h4>暂无数据</h4>
                    <p>请尝试调整筛选条件或重置筛选</p>
                </td>
            </tr>
        `;
        return;
    }
    
    // 分页显示数据
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageData = filteredData.slice(startIndex, endIndex);
    
    tableBody.innerHTML = pageData.map(item => `
        <tr>
            <td>${item.song_id}</td>
            <td>${item.song_name}</td>
            <td>${item.artist}</td>
            <td>${item.album}</td>
            <td><span class="genre-tag">${item.genre}</span></td>
            <td>${item.release_year}</td>
            <td>${item.play_count_millions}M</td>
            <td>
                <span class="rating ${getRatingClass(item.rating)}">${item.rating}</span>
            </td>
        </tr>
    `).join('');
}

// 获取评分样式类
function getRatingClass(rating) {
    if (rating >= 8) return 'rating-high';
    if (rating >= 6) return 'rating-medium';
    return 'rating-low';
}

// 更新结果计数
function updateResultCount() {
    const resultCount = document.getElementById('result-count');
    resultCount.textContent = `共找到 ${filteredData.length} 首歌曲`;
}

// 绑定事件监听器
function bindEventListeners() {
    // 筛选按钮
    document.getElementById('filter-btn').addEventListener('click', applyFilters);
    
    // 重置按钮
    document.getElementById('reset-btn').addEventListener('click', resetFilters);
    
    // 评分滑块
    const minRatingSlider = document.getElementById('min-rating');
    const maxRatingSlider = document.getElementById('max-rating');
    const minRatingValue = document.getElementById('min-rating-value');
    const maxRatingValue = document.getElementById('max-rating-value');
    
    minRatingSlider.addEventListener('input', function() {
        minRatingValue.textContent = this.value;
    });
    
    maxRatingSlider.addEventListener('input', function() {
        maxRatingValue.textContent = this.value;
    });
    
    // 艺术家搜索输入框
    document.getElementById('artist-search').addEventListener('input', debounce(applyFilters, 300));
    
    // 年份输入框
    document.getElementById('year-from').addEventListener('input', debounce(applyFilters, 300));
    document.getElementById('year-to').addEventListener('input', debounce(applyFilters, 300));
    
    // 音乐风格选择框
    document.getElementById('genre-filter').addEventListener('change', applyFilters);
}

// 应用筛选
function applyFilters() {
    const filters = {};
    
    const genre = document.getElementById('genre-filter').value;
    const artist = document.getElementById('artist-search').value.trim();
    const minRating = document.getElementById('min-rating').value;
    const maxRating = document.getElementById('max-rating').value;
    const yearFrom = document.getElementById('year-from').value;
    const yearTo = document.getElementById('year-to').value;
    
    if (genre) filters.genre = genre;
    if (artist) filters.artist = artist;
    if (minRating > 1) filters.min_rating = minRating;
    if (maxRating < 10) filters.max_rating = maxRating;
    if (yearFrom) filters.year_from = parseInt(yearFrom);
    if (yearTo) filters.year_to = parseInt(yearTo);
    
    loadData(filters);
}

// 重置筛选
function resetFilters() {
    document.getElementById('genre-filter').value = '';
    document.getElementById('artist-search').value = '';
    document.getElementById('min-rating').value = 1;
    document.getElementById('max-rating').value = 10;
    document.getElementById('min-rating-value').textContent = '1.0';
    document.getElementById('max-rating-value').textContent = '10.0';
    document.getElementById('year-from').value = '';
    document.getElementById('year-to').value = '';
    
    currentPage = 1;
    loadData();
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 显示消息
function showMessage(message, type = 'info') {
    // 移除现有的消息
    const existingMessage = document.querySelector('.message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // 创建新消息
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // 插入到页面顶部
    const container = document.querySelector('.container');
    container.insertBefore(messageDiv, container.firstChild);
    
    // 3秒后自动移除
    setTimeout(() => {
        if (messageDiv.parentNode) {
            messageDiv.remove();
        }
    }, 3000);
}

// 添加额外的CSS样式
const additionalStyles = `
    <style>
        .genre-tag {
            display: inline-block;
            padding: 4px 8px;
            background: #667eea;
            color: white;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .rating {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            min-width: 40px;
            text-align: center;
        }
        
        .rating-high {
            background: #d4edda;
            color: #155724;
        }
        
        .rating-medium {
            background: #fff3cd;
            color: #856404;
        }
        
        .rating-low {
            background: #f8d7da;
            color: #721c24;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .empty-state h4 {
            margin-bottom: 10px;
            color: #333;
        }
    </style>
`;

// 添加样式到页面头部
document.head.insertAdjacentHTML('beforeend', additionalStyles);