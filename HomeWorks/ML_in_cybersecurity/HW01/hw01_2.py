import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import os
from collections import Counter
import tldextract  # Для извлечения домена/бренда из URL

# Configuration
API_URL = "https://openphish.com/feed.txt"
INTERVAL_SECONDS = 30  # 5 minutes
RUN_DURATION_HOURS = 1
CSV_FILE = "phishing_data.csv"


def parse_openphish_api():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        urls = [url.strip() for url in response.text.split('\n') if url.strip()]
        data = []
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for url in urls:
            # Извлекаем бренд из домена (простой способ: subdomain или domain)
            extracted = tldextract.extract(url)
            brand = extracted.domain if extracted.domain else 'Unknown'  # Можно улучшить: проверка на ключевые слова (bank, paypal и т.д.)

            data.append({
                'url': url,
                'brand': brand,
                'time': current_time  # Время парсинга как время обнаружения
            })

        print(f"Found {len(data)} total URLs from API")
        return data
    except Exception as e:
        print(f"Error parsing API: {e}")
        return []


def load_existing_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=['url', 'brand', 'time'])


def save_data(new_data, existing_df):
    if not new_data:
        return existing_df

    new_df = pd.DataFrame(new_data)

    # Фильтруем только новые URL (дубликаты по URL)
    new_urls = set(new_df['url'].tolist())
    existing_urls = set(existing_df['url'].tolist()) if not existing_df.empty else set()
    truly_new_data = new_df[~new_df['url'].isin(existing_urls)]

    if truly_new_data.empty:
        print("No new entries found")
        return existing_df

    # Добавляем новые
    combined_df = pd.concat([existing_df, truly_new_data], ignore_index=True)
    combined_df.to_csv(CSV_FILE, index=False)

    print(f"Saved {len(truly_new_data)} new entries")
    return combined_df


def get_statistics(df, start_time, end_time):
    if df.empty:
        return {'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
                'unique_urls': 0,
                'top_brands': []}

    unique_urls = len(df['url'].unique())
    brand_counts = Counter(df['brand'].dropna())
    top_brands = brand_counts.most_common(3)

    stats = {
        'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'unique_urls': unique_urls,
        'top_brands': top_brands
    }
    return stats


def main():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=RUN_DURATION_HOURS)
    existing_df = load_existing_data()

    print(f"Starting parser at {start_time}")
    print(f"Using API: {API_URL}")

    while datetime.now() < end_time:
        new_data = parse_openphish_api()
        existing_df = save_data(new_data, existing_df)

        remaining_time = (end_time - datetime.now()).total_seconds() / 60
        print(f"Parsed at {datetime.now()}. Remaining: {remaining_time:.1f} min")

        if remaining_time > 5:
            time.sleep(INTERVAL_SECONDS)

    # Статистика
    stats = get_statistics(existing_df, start_time, datetime.now())

    print("\n" + "=" * 50)
    print("Final Statistics:")
    print(f"Start Time: {stats['start_time']}")
    print(f"End Time: {stats['end_time']}")
    print(f"Unique URLs: {stats['unique_urls']}")
    print("Top 3 Most Attacked Brands:")
    for i, (brand, count) in enumerate(stats['top_brands'], 1):
        print(f"{i}. {brand}: {count}")
    print("=" * 50)

    # Сохраняем статистику в отдельный файл для удобства
    with open("statistics.txt", "w") as f:
        f.write(f"Start Time: {stats['start_time']}\n")
        f.write(f"End Time: {stats['end_time']}\n")
        f.write(f"Unique URLs: {stats['unique_urls']}\n")
        f.write("Top 3 Brands:\n")
        for brand, count in stats['top_brands']:
            f.write(f"- {brand}: {count}\n")


if __name__ == "__main__":
    main()