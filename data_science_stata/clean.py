import csv

input_file = 'csv/uefa_player_stats.csv'
output_file = 'csv/ucl_player_stats.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Chuyển đổi goals và assists về số nguyên (hoặc 0 nếu rỗng)
        goals = int(row['goals']) if row['goals'].isdigit() else 0
        assists = int(row['assists']) if row['assists'].isdigit() else 0

        # Giữ lại cầu thủ nếu goals > 0 hoặc assists > 0
        if not (goals == 0 and assists == 0):
            writer.writerow(row)

print(f"Đã lọc xong, kết quả lưu ở {output_file}")