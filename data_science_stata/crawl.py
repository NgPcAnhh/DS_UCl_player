import requests
import csv
import time
import random

url = 'https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit=200&offset=0&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=goals%2Cminutes_played_official%2Cmatches_appearance%2Cassists%2Cdistance_covered%2Ctop_speed'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

def get_stat(statistics, stat_name):
    for stat in statistics:
        if stat.get('name') == stat_name:
            return stat.get('value', '')
    return ''

def crawl_and_save_csv():
    all_players = []
    offset = 0
    limit = 200

    while True:
        paged_url = f'https://compstats.uefa.com/v1/player-ranking?competitionId=1&limit={limit}&offset={offset}&optionalFields=PLAYER%2CTEAM&order=DESC&phase=TOURNAMENT&seasonYear=2025&stats=goals%2Cminutes_played_official%2Cmatches_appearance%2Cassists%2Cdistance_covered%2Ctop_speed'
        response = requests.get(paged_url, headers=headers)
        if response.status_code != 200:
            print(f"Request failed at offset {offset}: {response.status_code}")
            break
        
        try:
            data = response.json()
        except Exception as e:
            print("JSON decode error:", e)
            break
        
        # Nếu trả về là list, dùng trực tiếp; nếu có key 'items', lấy ra
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and 'items' in data:
            items = data['items']
        else:
            print("Không nhận diện được cấu trúc JSON trả về")
            break

        if not items:
            break

        for item in items:
            # Lấy tên cầu thủ theo tiếng Anh
            player_name = (
                item.get('player', {})
                .get('translations', {})
                .get('name', {})
                .get('EN', '')
            )
            statistics = item.get('statistics', [])
            row = {
                'player_name': player_name,
                'goals': get_stat(statistics, 'goals'),
                'minutes_played_official': get_stat(statistics, 'minutes_played_official'),
                'assists': get_stat(statistics, 'assists'),
                'distance_covered': get_stat(statistics, 'distance_covered'),
                'top_speed': get_stat(statistics, 'top_speed'),
            }
            all_players.append(row)
        
        # Nếu trả về là list, không biết tổng số lượng, break khi ít hơn limit
        if len(items) < limit:
            break
        offset += limit
        time.sleep(random.uniform(1.5, 3.5))

    # Lưu với UTF-8 BOM để tránh lỗi font ở Excel hoặc phần mềm đọc CSV
    with open('csv/ucl_stats.csv', 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['player_name', 'goals', 'minutes_played_official', 'assists', 'distance_covered', 'top_speed']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_players:
            writer.writerow(row)
    print(f"Đã lưu {len(all_players)} cầu thủ vào uefa_player_stats_utf8.csv")

if __name__ == '__main__':
    crawl_and_save_csv()