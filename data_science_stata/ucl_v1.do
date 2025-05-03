***************************************
* DO-FILE PHÂN TÍCH DỮ LIỆU BÓNG ĐÁ  *
***************************************

* 1. Khởi tạo môi trường làm việc
clear
set more off, permanently

* 2. Đặt thư mục làm việc
cd "C:\Users\ADMIN\OneDrive\Máy tính\tai lieu hoc tap\kinh tế lượng\data_science_stata\csv"

* 3. Ghi log kết quả
capture log close
capture log using ucl_player_stats.log, replace

* 4. Import dữ liệu CSV
import delimited ucl_player_stats.csv, clear

* 5. Tạo biến STT nếu cần (dùng làm chỉ mục hoặc cho chuỗi thời gian)
gen STT = _n

* 6. Sắp xếp dữ liệu theo STT (tùy chọn)
sort STT

**************************************************
* PHẦN 1: THỐNG KÊ MÔ TẢ
**************************************************

* 6.1 Thống kê mô tả chung cho các chỉ số thi đấu
tabstat goals minutes_played_official assists distance_covered top_speed, ///
    statistics(mean count max min range sd variance cv semean skewness kurtosis median) ///
    columns(statistics)

* 6.2 Bảng tần suất (frequency tables)
tabulate goals
tabulate assists

* 6.3 Thống kê mô tả theo từng mức độ ghi bàn (goals)
tabstat minutes_played_official assists distance_covered top_speed, ///
    statistics(mean count max min range sd variance cv semean skewness kurtosis median) ///
    by(goals) columns(statistics)

* 6.4 Phân tích tương quan giữa các biến
pwcorr goals minutes_played_official assists distance_covered top_speed, sig

**************************************************
* PHẦN 2: HỒI QUY TUYẾN TÍNH ĐƠN GIẢN
**************************************************

regress goals minutes_played_official assists distance_covered top_speed

**************************************************
* PHẦN 3: KIỂM ĐỊNH GIẢ THUYẾT MÔ HÌNH
**************************************************

* 3.1 Kiểm định Ramsey RESET (đúng dạng mô hình hay không)
ovtest

* 3.2 Kiểm định đa cộng tuyến
vif

* 3.3 Cài đặt chuỗi thời gian nếu muốn kiểm định tự tương quan (dựa vào STT)
tsset STT

* 3.4 Kiểm định tự tương quan
estat durbinalt         // Durbin alternative test
* Nếu muốn dùng Breusch-Godfrey bậc 1:
* Cần cài đặt nếu chưa có:
* ssc install bgodfrey
bgodfrey, lags(1)

* 3.5 Kiểm định phương sai sai số thay đổi
estat imtest            // Kiểm định White
estat hettest           // Breusch–Pagan

**************************************************
* KẾT THÚC PHÂN TÍCH
**************************************************
log close
