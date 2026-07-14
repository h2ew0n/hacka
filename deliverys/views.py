from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'deliverys/main.html')

# --- 학습 모드 ---
def learn_mission(request):
    return render(request, 'deliverys/learn_mission.html')

def learn_search(request):
    return render(request, 'deliverys/learn_search.html')

def learn_list(request):
    # 1. 검색어를 가져오기 (기본값은 '분식')
    keyword = request.GET.get('q', '분식')

    # 2. 카테고리별 데이터를 딕셔너리로 주기
    category_data = {
        "분식": [
            {"name": "동대문엽기떡볶이", "rating": "4.8", "review_count": "4,215", "min_order": "14,000원", "time": "약 25분", "img_url": "..."},
            {"name": "응급실 국물떡볶이", "rating": "4.6", "review_count": "1,980", "min_order": "12,000원", "time": "약 20분", "img_url": "..."},
            {"name": "싸다김밥", "rating": "4.7", "review_count": "850", "min_order": "10,000원", "time": "약 15분", "img_url": "..."},
            {"name": "스쿨푸드딜리버리", "rating": "4.5", "review_count": "1,230", "min_order": "15,000원", "time": "약 30분", "img_url": "..."}
        ],
        "중식": [
            {"name": "샹츠마라", "rating": "4.0", "review_count": "1,882", "min_order": "11,000원", "time": "약 22분", "img_url": "..."},
            {"name": "홍콩반점", "rating": "4.7", "review_count": "2,342", "min_order": "10,000원", "time": "약 22분", "img_url": "..."},
            {"name": "춘리마라탕", "rating": "4.7", "review_count": "3,208", "min_order": "13,000원", "time": "약 30분", "img_url": "..."},
            {"name": "피로반점", "rating": "5.0", "review_count": "1,308", "min_order": "11,000원", "time": "약 40분", "img_url": "..."}
        ],
        "족발보쌈": [
            {"name": "필동족발", "rating": "4.7", "review_count": "6", "min_order": "30,000원", "time": "약 19분", "img_url": "..."},
            {"name": "마왕족발", "rating": "5.0", "review_count": "2,719", "min_order": "30,000원", "time": "약 25분", "img_url": "..."},
            {"name": "원할머니보쌈족발", "rating": "4.9", "review_count": "165", "min_order": "20,000원", "time": "약 32분", "img_url": "..."},
            {"name": "피로족발", "rating": "5.0", "review_count": "2,308", "min_order": "15,000원", "time": "약 25분", "img_url": "..."}
        ],
        "패스트푸드": [
            {"name": "맥도날드", "rating": "4.3", "review_count": "588", "min_order": "14,000원", "time": "약 20분", "img_url": "..."},
            {"name": "롯데리아", "rating": "4.8", "review_count": "441", "min_order": "14,000원", "time": "약 19분", "img_url": "..."},
            {"name": "버거킹", "rating": "4.5", "review_count": "335", "min_order": "14,000원", "time": "약 26분", "img_url": "..."},
            {"name": "맘스터치", "rating": "4.9", "review_count": "800", "min_order": "16,000원", "time": "약 57분", "img_url": "..."}
        ],
        "카페디저트": [
            {"name": "메가MGC커피", "rating": "4.9", "review_count": "119", "min_order": "11,000원", "time": "약 20분", "img_url": "..."},
            {"name": "투썸플레이스", "rating": "4.8", "review_count": "41", "min_order": "15,000원", "time": "약 40분", "img_url": "..."},
            {"name": "던킨", "rating": "4.9", "review_count": "175", "min_order": "15,900원", "time": "약 15분", "img_url": "..."},
            {"name": "컴포즈커피", "rating": "4.8", "review_count": "158", "min_order": "8,900원", "time": "약 39분", "img_url": "..."}
        ],
        "치킨": [
            {"name": "교촌", "rating": "4.7", "review_count": "1,342", "min_order": "11,000원", "time": "약 22분", "img_url": "..."},
            {"name": "BHC", "rating": "4.9", "review_count": "744", "min_order": "20,000원", "time": "약 32분", "img_url": "..."},
            {"name": "BBQ", "rating": "4.9", "review_count": "469", "min_order": "18,000원", "time": "약 63분", "img_url": "..."},
            {"name": "굽네치킨", "rating": "5.0", "review_count": "1,013", "min_order": "18,000원", "time": "약 35분", "img_url": "..."}
        ]
    }

    # 3. 키워드 매핑 로직
    search_key = keyword
    if keyword in ["족발", "보쌈", "족발, 보쌈", "족발보쌈"]:
        search_key = "족발보쌈"
    elif keyword in ["패스트푸드", "햄버거", "버거"]:
        search_key = "패스트푸드"
    elif keyword in ["카페", "디저트", "커피", "카페디저트"]:
        search_key = "카페디저트"
    elif keyword in ["치킨", "통닭"]:
        search_key = "치킨"
    elif keyword in ["분식", "떡볶이", "김밥"]:
        search_key = "분식"
    elif keyword in ["마라탕", "짜장면", "짬뽕", "중식"]:
        search_key = "중식"

    # ★ 수정: keyword 대신 매핑이 완수된 search_key로 딕셔너리를 조회합니다.
    stores = category_data.get(search_key, category_data["분식"])

    # ★ 수정: target_store를 판별할 때도 변환된 search_key를 기준으로 잡아야 정확합니다.
    target_store = "동대문엽기떡볶이" 
    
    if search_key == "중식":
        target_store = "홍콩반점"
    elif search_key == "패스트푸드":
        target_store = "패스트푸드가게"
    elif search_key == "카페디저트":
        target_store = "카페디저트가게"
    elif search_key == "치킨":
        target_store = "치킨가게"
    elif search_key == "족발보쌈":
        target_store = "족보가게"

    return render(request, 'deliverys/learn_list.html', {
        'stores': stores,
        'keyword': keyword,
        'target_store': target_store 
    })

def learn_menu(request):
    return render(request, 'deliverys/learn_menu.html')

def learn_menu_option(request):
    return render(request, 'deliverys/learn_option.html')

def learn_cart(request):
    return render(request, 'deliverys/learn_cart.html')

def learn_payment(request):
    return render(request, 'deliverys/learn_payment.html')

def learn_success(request):
    return render(request, 'deliverys/learn_success.html')

# --- 활용 모드 (껍데기) ---
def apply_mission(request): return render(request, 'deliverys/apply_mission.html')
def apply_search(request): return render(request, 'deliverys/apply_search.html')
def apply_menu(request): return render(request, 'deliverys/apply_menu.html')
def apply_cart(request): return render(request, 'deliverys/apply_cart.html')
def apply_payment(request): return render(request, 'deliverys/apply_payment.html')
def apply_success(request): return render(request, 'deliverys/apply_success.html')