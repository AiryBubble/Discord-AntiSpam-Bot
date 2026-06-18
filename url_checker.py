import requests
from urllib.parse import urlparse
import re
import time

# URLhausフィルターリストのURL
URLHAUS_FILTER_URL = "https://urlhaus-filter.pages.dev/urlhaus-filter.txt"

# フィルターリストのキャッシュ
_filter_cache = {
    'domains': set(),
    'patterns': [],
    'last_update': 0,
    'update_interval': 3600  # 1時間ごとに更新
}

def download_filter_list():
    """URLhausフィルターリストをダウンロードして解析"""
    try:
        response = requests.get(URLHAUS_FILTER_URL, timeout=10)
        
        if response.status_code == 200:
            domains = set()
            patterns = []
            
            for line in response.text.split('\n'):
                line = line.strip()
                
                if not line or line.startswith('!') or line.startswith('['):
                    continue
                
                # ||example.com^ → example.com
                if line.startswith('||') and '^' in line:
                    domain = line[2:].split('^')[0]
                    if domain:
                        domains.add(domain)
                        pattern = re.escape(domain).replace(r'\*', '.*')
                        patterns.append(re.compile(pattern, re.IGNORECASE))
                
                elif not line.startswith(('|', '/', '@', '#')) and '.' in line:
                    domain = line.rstrip('^')
                    domains.add(domain)
                    pattern = re.escape(domain).replace(r'\*', '.*')
                    patterns.append(re.compile(pattern, re.IGNORECASE))
            
            _filter_cache['domains'] = domains
            _filter_cache['patterns'] = patterns
            _filter_cache['last_update'] = time.time()
            
            print(f"URLhausフィルターを更新: {len(domains)} ドメイン")
            return True
        
    except Exception as e:
        print(f"フィルター更新エラー: {e}")
    
    return False

def ensure_filter_updated():
    """フィルターが最新かチェックし、必要なら更新"""
    current_time = time.time()
    
    if (not _filter_cache['patterns'] or 
        current_time - _filter_cache['last_update'] > _filter_cache['update_interval']):
        download_filter_list()
    
    return bool(_filter_cache['patterns'])

def extract_domain_from_url(url):
    """URLからドメイン部分を抽出"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        parsed = urlparse(url)
        domain = parsed.netloc
        
        if domain.startswith('www.'):
            domain = domain[4:]
        
        return domain
    except:
        return None

def check_url_with_urlhaus(url):
    """
    URLhausフィルターを使用してURLのマルウェアチェック
    
    Returns:
        bool: マルウェアが検出された場合はTrue
    """
    try:
        if not ensure_filter_updated():
            return False
        
        domain = extract_domain_from_url(url)
        if not domain:
            return False
        
        # ドメインの直接一致をチェック
        if domain in _filter_cache['domains']:
            return True
        
        # 正規表現パターンでチェック
        full_url = url
        if not full_url.startswith(('http://', 'https://')):
            full_url = 'http://' + full_url
        
        for pattern in _filter_cache['patterns']:
            if pattern.search(full_url) or pattern.search(domain):
                return True
        
        return False
        
    except Exception as e:
        print(f"URLチェックエラー: {e}")
        return False