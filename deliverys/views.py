import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mission
import json

# ALL_STORES = [
#     {"id": 1, "name": "동대문엽기떡볶이", "category": "분식", "menus": [{"id": 101, "name": "엽기떡볶이", "price": 14000}]},
#     {"id": 2, "name": "홍콩반점", "category": "중식", "menus": [{"id": 201, "name": "짬뽕", "price": 8000}]},
#     {"id": 3, "name": "굽네치킨", "category": "치킨", "menus": [{"id": 301, "name": "오리지널", "price": 16000}]}
# ]

# Create your views here.


def initialize_simulation(request):
    all_mission = Mission.objects.all()
    
    if not all_mission.exists():
        return render(request, 'deliverys/error.html', {'message': '등록된 미션이 없습니다.'})
        
    chosen_mission = random.choice(all_mission)

    # 💾 세션에 완벽하게 데이터 주입
    request.session['cart_data'] = {
        'mission_title': chosen_mission.title,
        'mission_description': chosen_mission.description,
        'step_guide': chosen_mission.step_guide,
        'answer_data': chosen_mission.answer_data,

        'current_stage': 1,
        'selected_store': None,
        'items': [],
        'total_price': 0
    }
    request.session.modified = True
    
    # 🚀 핵심: 세션을 디스크에 완전히 저장시킨 후, 미션 페이지로 리다이렉트합니다!
    return redirect('deliverys:learn_mission')

def main(request):
    initialize_simulation(request)
    return render(request, 'deliverys/main.html')

# --- 학습 모드 ---
def learn_mission(request):
    cart_data = request.session.get('cart_data')
    
    if not cart_data:
        return redirect('deliverys:main')
    
    answer = cart_data.get('answer_data', {})
    
    context = {
        'store': answer.get('store'),
        'menu': answer.get('menu'),
        'count': answer.get('count')
    }
    
    return render(request, 'deliverys/learn_mission.html', context)

def learn_search(request):
    return render(request, 'deliverys/learn_search.html')

def learn_list(request):
    cart_data = request.session.get('cart_data')
    if not cart_data:
        return redirect('deliverys:main')
    # 1. 검색어를 가져오기 (기본값은 '분식')
    keyword = request.GET.get('q', '분식')

    # 2. 카테고리별 데이터를 딕셔너리로 주기
    category_data = {
        "분식": [
            {"name": "동대문엽기떡볶이", "rating": "4.8", "review_count": "4,215", "min_order": "14,000원", "time": "약 25분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMjA0MDJfNDkg%2FMDAxNjQ4ODY3OTU2NDM2.QYrmT95DrVgSuly-dmRcmktUncf-U0v0sRMgMjyqv5sg.BTbS5JWr46IfciX4ivstoYcF7tjiU5mEvTXKiPSDuJ8g.PNG.tlstnqls0719%2Fimage%25A3%25A5EF%25A3%25A5BC%25A3%25A585EF%25A3%25A5EF%25A3%25A5BC%25A3%25A585BC%25A3%25A5EF%25A3%25A5BC%25A3%25A5858D1%25A3%25A5EF%25A3%25A5BC%25A3%25A585EF%25A3%25A5EF%25A3%25A5BC%25A3%25A585BC%25A3%25A5EF%25A3%25A5BC%25A3%25A5858Dremo.png&type=a340"},
            {"name": "응급실 국물떡볶이", "rating": "4.6", "review_count": "1,980", "min_order": "12,000원", "time": "약 20분", "img_url": "https://search.pstatic.net/sunny/?src=https%3A%2F%2Ffile.albamon.com%2FAlbamon%2FRecruit%2FPhoto%2FC-Photo-View%3FFN%3D2023%2F10%2F18%2FJK_CO_ordnwj23101811220964.jpg&type=a340"},
            {"name": "싸다김밥", "rating": "4.7", "review_count": "850", "min_order": "10,000원", "time": "약 15분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA5MTdfMjc3%2FMDAxNjMxODEzMzQ3NzAx.nK5A9xXIPyHAXbdA4HiYJvgAMBQ7tKhWMNcAUJDQIfMg.0CtkGVCp9l6RUZQ0jGw2WV4waYaQndwgEqjU12R91y8g.PNG.write90%2Fimage.png&type=a340"},
            {"name": "스쿨푸드딜리버리", "rating": "4.5", "review_count": "1,230", "min_order": "15,000원", "time": "약 30분", "img_url":"https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F5612%2F2018%2F12%2F31%2F0000003589_001_20181231150209821.jpg&type=a340"}
        ],
        "중식": [
            {"name": "샹츠마라", "rating": "4.0", "review_count": "1,882", "min_order": "11,000원", "time": "약 22분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNDA3MjlfMjE5%2FMDAxNzIyMTc5MTcyMDM2.tUzxvTpcCFSbB4P6GojGKbNsy-z9M-uRPqmS1CsVcukg.8lk1m6p-R2aabSLguUovs5RtzQ6PG_gVdC9mMvS_PCIg.JPEG%2FIMG_1968.jpg&type=a340"},
            {"name": "홍콩반점", "rating": "4.7", "review_count": "2,342", "min_order": "10,000원", "time": "약 22분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxODA5MTdfMjMz%2FMDAxNTM3MTUzNDgyNDU0.H3eJQ5VRxHRZmEiz3clVr8wZ5ebw_bJKZXwx-XRZ210g.Cq-P5Yz6YCwQNn7tfQv5C9EUzp5rxT0ZcJuJi21Qhgwg.PNG.mkg_suwon%2F1526310256285_icon.png&type=a340"},
            {"name": "춘리마라탕", "rating": "4.7", "review_count": "3,208", "min_order": "13,000원", "time": "약 30분", "img_url": "https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210527_229%2F1622119587759T9BH6_JPEG%2FE3DimFBPxC9IAoEa-i3Dz0zw.jpg&type=a340"},
            {"name": "피로반점", "rating": "5.0", "review_count": "1,308", "min_order": "11,000원", "time": "약 40분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNjAxMTFfMjEw%2FMDAxNzY4MTA0MjM2NzA2.yy9ObHkY-JmclOxyaCKrGalZtzGpti4n38Fg2EeoR4kg.RPxmLgwsvcxRMHcEVicNedZzdMdYCoaPc6uwVhtaCVog.JPEG%2Fgen_1768104175_1_9167.jpg&type=a340"}
        ],
        "족발보쌈": [
            {"name": "필동족발", "rating": "4.7", "review_count": "6", "min_order": "30,000원", "time": "약 19분", "img_url": "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fimage.utoimage.com%2Fpreview%2Fcp871385%2F2018%2F12%2F201812006026_500.jpg&type=a340"},
            {"name": "마왕족발", "rating": "5.0", "review_count": "2,719", "min_order": "30,000원", "time": "약 25분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDA1MTJfMTc0%2FMDAxNTg5MjY4MDAzMDUw.oXWjTwyyzdUL08UEoeOvTxuQosiFLMARugsFkj-0cTIg.zlpoLoFK3vbyFZ7wjxlcXabWsK43KkYwzF06J7qRY28g.JPEG.gudwnslaaa%2F111.jpg&type=a340"},
            {"name": "원할머니보쌈족발", "rating": "4.9", "review_count": "165", "min_order": "20,000원", "time": "약 32분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxODAzMTdfMTg1%2FMDAxNTIxMjU3NTQyNjIy.hWedEryCnB3iwmxcQSG4-t3FI9M8TtvGCgRjgaorBM4g.Dc60BKN6pxH6A7jCa9BXPHBzRwcVkZi0w2rlVjPM8YEg.PNG.rrd753%2F20180317_115229.png&type=a340"},
            {"name": "피로족발", "rating": "5.0", "review_count": "2,308", "min_order": "15,000원", "time": "약 25분", "img_url": "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fthumb2.gettyimageskorea.com%2Fimage_preview%2F700%2F201711%2FMBRF%2FMBRF17017941.jpg&type=a340"}
        ],
        "패스트푸드": [
            {"name": "맥도날드", "rating": "4.3", "review_count": "588", "min_order": "14,000원", "time": "약 20분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxODA2MTFfMTIx%2FMDAxNTI4NzAyNTQwMTcy.uGwJ0VME93FnIOu8TMtYodB5SL7r936q5mFHe4obdmgg.H8ZHqFCRj5BLKdDNx4ICaghnU7_aU722WpW2qpJEWrIg.JPEG.thenemolab%2F%25B8%25C6%25B5%25B5%25B3%25AF%25B5%25E52018.jpg&type=a340"},
            {"name": "롯데리아", "rating": "4.8", "review_count": "441", "min_order": "14,000원", "time": "약 19분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20140506_37%2Fcheapburger_13993863873401cmr0_PNG%2FB7%253FA5B8AEBEC6_BCBCB7CEC7FC_red.png&type=a340"},
            {"name": "버거킹", "rating": "4.5", "review_count": "335", "min_order": "14,000원", "time": "약 26분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNTA0MzBfMjE5%2FMDAxNzQ2MDE1NjU0ODgx.qzhAJ2VyLavjwgrdFc4pZizZA1eZZWd-9L4nBgf1bvUg.PLTQpNanVV-QmShD7VypjW_w-0myuXf10xqtI_xKh_0g.JPEG%2F%25B9%25F6%25B0%25C5%25C5%25B7%25B7%25CE%25B0%25ED.jpg&type=a340"},
            {"name": "맘스터치", "rating": "4.9", "review_count": "800", "min_order": "16,000원", "time": "약 57분", "img_url": "https://search.pstatic.net/sunny/?src=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2F1IHuH%2F857c123390f073525a870f48c8b5c2fd6be67633&type=a340"}
        ],
        "카페디저트": [
            {"name": "메가MGC커피", "rating": "4.9", "review_count": "119", "min_order": "11,000원", "time": "약 20분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMjA4MzBfMTMw%2FMDAxNjYxODMzNDg1MTg5.mMm-TihJp_csGsgvk-TzU6KkBGQjzYK9By3Gbqd7qQcg.XplQ7wUaYKb2yv5FnI4jZcQVLELvhazs_znUThcR-7og.PNG.po00206%2Fbi_logo1.png&type=l340_165"},
            {"name": "투썸플레이스", "rating": "4.8", "review_count": "41", "min_order": "15,000원", "time": "약 40분", "img_url": "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fi.pinimg.com%2F736x%2Ff8%2Fef%2F91%2Ff8ef915154fe8b822b451aea4a7a8e48.jpg&type=a340"},
            {"name": "던킨", "rating": "4.9", "review_count": "175", "min_order": "15,900원", "time": "약 15분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxOTA4MDFfMzgg%2FMDAxNTY0NjQ1OTAzMjMz.SbUOz-VXJlS37BNTTFw1fTTuIEUDJA6o9iJbpOq4wMUg.NVxuAMl9ZxwhmEeqpdRe_h9pMDHhPB69NIgTNH4m4Zkg.JPEG.duckdesign%2F0cHLGe6M_400x400.jpg&type=a340"},
            {"name": "컴포즈커피", "rating": "4.8", "review_count": "158", "min_order": "8,900원", "time": "약 39분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNTA5MjVfNCAg%2FMDAxNzU4Nzc2MTI4MjM0.MWQHWzzVUtOWVH1EnLQ7h4xJ1sp5BAxSmK--t3yllQcg.L64Dnhspxm8ozjiMgG0EvcGU-00AGs1wE-MiF-tacEcg.PNG%2F%25B4%25D9%25BF%25EE%25B7%25CE%25B5%25E5_%25281%2529.png&type=a340"}
        ],
        "치킨": [
            {"name": "교촌", "rating": "4.7", "review_count": "1,342", "min_order": "11,000원", "time": "약 22분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F5562%2F2020%2F08%2F14%2F0000012854_001_20200814102054160.jpg&type=a340"},
            {"name": "BHC", "rating": "4.9", "review_count": "744", "min_order": "20,000원", "time": "약 32분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA2MTZfMjg3%2FMDAxNjIzODA2NDc3NjY5.ooK9MfX81XTOznDbUiJCgeg5zl30JbOAJtypG0id_zMg.TR1JrvWOQQXvTWdNrYriizVaP0PovnTy2sIsoXfw-mgg.JPEG.congha%2Fbhc1.jpg&type=a340"},
            {"name": "BBQ", "rating": "4.9", "review_count": "469", "min_order": "18,000원", "time": "약 63분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzEyMTVfMjE1%2FMDAxNzAyNjE2NDQ4MzMy.IMCFZgy0hrz0r6kLG2c8yEkCJtbK7wJyTNMcBVbyTiog.Zgxr85up_ouZX9T1hvT8qngh0sB4IG6E1pfjKG2ra9Ig.PNG.moneyhero7779%2Fimage.png&type=a340"},
            {"name": "굽네치킨", "rating": "5.0", "review_count": "1,013", "min_order": "18,000원", "time": "약 35분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDExMTZfMjc5%2FMDAxNjA1NDg0MzU0MDM5.SiiTJ_-VMrrdUdOQIkyn9RfAblNai0oxIKNbuD6Dpvcg.7vFXLFcesuPJVaE3vznJ7BAwE6-9Sihqry36bmy9myQg.PNG.ryowoo48%2F%25BD%25BA%25C5%25A9%25B8%25B0%25BC%25A6_2020-11-16_%25BF%25C0%25C0%25FC_8.51.52.png&type=a340"}
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
        target_store = "맥도날드"
    elif search_key == "카페디저트":
        target_store = "메가MGC커피"
    elif search_key == "치킨":
        target_store = "굽네치킨"
    elif search_key == "족발보쌈":
        target_store = "피로족발"

    return render(request, 'deliverys/learn_list.html', {
        'stores': stores,
        'keyword': keyword,
        'target_store': target_store 
    })

def learn_menu(request):
    cart_data = request.session.get('cart_data')
    if not cart_data:
        return redirect('deliverys:main')
    
    return render(request, 'deliverys/learn_menu.html')

def learn_menu_option(request):
    return render(request, 'deliverys/learn_menu_option.html')

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

# --learn_mission 몇인분 count 뽑기 --
# def learn_mission(request):
#     context = {
#         'count': random.randint(1,5),
#     }
#     return render(request, 'deliverys/learn_mission.html', context)