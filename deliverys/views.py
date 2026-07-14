import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mission
import json
from django.contrib import messages

# ============================================================
# 가게 + 메뉴 + 메뉴옵션 데이터
#   - category_data: 카테고리별 가게 리스트 (learn_list에서 사용)
#   - 각 가게(store)에 "id"와 "menus"를 추가해서
#     learn_menu / learn_menu_option에서 조회할 수 있게 함
#   - CATEGORY_MENUS: 카테고리별 대표 메뉴 + 옵션(수량/가격 계산용)
# ============================================================

CATEGORY_MENUS = {
    "분식": [
        {
            "id": 1, "name": "떡볶이", "price": 8000,
            "options": [
                {"name": "맵기 선택", "choices": [
                    {"label": "보통맛", "price_delta": 0},
                    {"label": "매운맛", "price_delta": 0},
                ]},
                {"name": "사리 추가", "choices": [
                    {"label": "없음", "price_delta": 0},
                    {"label": "치즈 추가", "price_delta": 1000},
                    {"label": "라면사리 추가", "price_delta": 1500},
                ]},
            ],
        },
        {
            "id": 2, "name": "모듬김밥", "price": 6000,
            "options": [
                {"name": "종류 선택", "choices": [
                    {"label": "야채김밥", "price_delta": 0},
                    {"label": "참치김밥", "price_delta": 1000},
                ]},
            ],
        },
    ],
    "중식": [
        {
            "id": 1, "name": "짬뽕", "price": 9000,
            "options": [
                {"name": "맵기 선택", "choices": [
                    {"label": "보통맛", "price_delta": 0},
                    {"label": "얼큰하게", "price_delta": 0},
                ]},
            ],
        },
        {
            "id": 2, "name": "짜장면", "price": 7000,
            "options": [
                {"name": "곱빼기 선택", "choices": [
                    {"label": "보통", "price_delta": 0},
                    {"label": "곱빼기", "price_delta": 2000},
                ]},
            ],
        },
    ],
    "족발보쌈": [
        {
            "id": 1, "name": "왕족발 (中)", "price": 28000,
            "options": [
                {"name": "맛 선택", "choices": [
                    {"label": "기본맛", "price_delta": 0},
                    {"label": "매운맛", "price_delta": 0},
                ]},
            ],
        },
        {
            "id": 2, "name": "보쌈정식", "price": 22000,
            "options": [],
        },
    ],
    "패스트푸드": [
        {
            "id": 1, "name": "불고기버거 세트", "price": 8000,
            "options": [
                {"name": "사이드 변경", "choices": [
                    {"label": "감자튀김", "price_delta": 0},
                    {"label": "치즈스틱", "price_delta": 1000},
                ]},
            ],
        },
        {
            "id": 2, "name": "치킨너겟 (10조각)", "price": 5000,
            "options": [],
        },
    ],
    "카페디저트": [
        {
            "id": 1, "name": "아메리카노", "price": 2500,
            "options": [
                {"name": "온도 선택", "choices": [
                    {"label": "따뜻하게(HOT)", "price_delta": 0},
                    {"label": "차갑게(ICE)", "price_delta": 0},
                ]},
                {"name": "사이즈 선택", "choices": [
                    {"label": "보통 사이즈", "price_delta": 0},
                    {"label": "큰 사이즈", "price_delta": 500},
                ]},
            ],
        },
        {
            "id": 2, "name": "치즈케이크", "price": 6500,
            "options": [],
        },
    ],
    "치킨가게": [
        {
            "id": 1, "name": "후라이드치킨", "price": 18000,
            "options": [
                {"name": "맛 선택", "choices": [
                    {"label": "후라이드", "price_delta": 0},
                    {"label": "양념", "price_delta": 1000},
                    {"label": "반반", "price_delta": 1000},
                ]},
            ],
        },
        {
            "id": 2, "name": "치킨무 추가", "price": 0,
            "options": [],
        },
    ],
}

category_data = {
    "분식": [
        {"name": "동대문엽기떡볶이", "rating": "4.8", "review_count": "4,215", "min_order": "14,000원", "time": "약 25분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMjA0MDJfNDkg%2FMDAxNjQ4ODY3OTU2NDM2.QYrmT95DrVgSuly-dmRcmktUncf-U0v0sRMgMjyqv5sg.BTbS5JWr46IfciX4ivstoYcF7tjiU5mEvTXKiPSDuJ8g.PNG.tlstnqls0719%2Fimage%25A3%25A5EF%25A3%25A5BC%25A3%25A585EF%25A3%25A5EF%25A3%25A5BC%25A3%25A585BC%25A3%25A5EF%25A3%25A5BC%25A3%25A5858D1%25A3%25A5EF%25A3%25A5BC%25A3%25A585EF%25A3%25A5EF%25A3%25A5BC%25A3%25A585BC%25A3%25A5EF%25A3%25A5BC%25A3%25A5858Dremo.png&type=a340"},
        {"name": "응급실 국물떡볶이", "rating": "4.6", "review_count": "1,980", "min_order": "12,000원", "time": "약 20분", "img_url": "https://search.pstatic.net/sunny/?src=https%3A%2F%2Ffile.albamon.com%2FAlbamon%2FRecruit%2FPhoto%2FC-Photo-View%3FFN%3D2023%2F10%2F18%2FJK_CO_ordnwj23101811220964.jpg&type=a340"},
        {"name": "싸다김밥", "rating": "4.7", "review_count": "850", "min_order": "10,000원", "time": "약 15분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA5MTdfMjc3%2FMDAxNjMxODEzMzQ3NzAx.nK5A9xXIPyHAXbdA4HiYJvgAMBQ7tKhWMNcAUJDQIfMg.0CtkGVCp9l6RUZQ0jGw2WV4waYaQndwgEqjU12R91y8g.PNG.write90%2Fimage.png&type=a340"},
        {"name": "스쿨푸드딜리버리", "rating": "4.5", "review_count": "1,230", "min_order": "15,000원", "time": "약 30분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F5612%2F2018%2F12%2F31%2F0000003589_001_20181231150209821.jpg&type=a340"}
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
    "치킨가게": [
        {"name": "교촌", "rating": "4.7", "review_count": "1,342", "min_order": "11,000원", "time": "약 22분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F5562%2F2020%2F08%2F14%2F0000012854_001_20200814102054160.jpg&type=a340"},
        {"name": "BHC", "rating": "4.9", "review_count": "744", "min_order": "20,000원", "time": "약 32분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA2MTZfMjg3%2FMDAxNjIzODA2NDc3NjY5.ooK9MfX81XTOznDbUiJCgeg5zl30JbOAJtypG0id_zMg.TR1JrvWOQQXvTWdNrYriizVaP0PovnTy2sIsoXfw-mgg.JPEG.congha%2Fbhc1.jpg&type=a340"},
        {"name": "BBQ", "rating": "4.9", "review_count": "469", "min_order": "18,000원", "time": "약 63분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzEyMTVfMjE1%2FMDAxNzAyNjE2NDQ4MzMy.IMCFZgy0hrz0r6kLG2c8yEkCJtbK7wJyTNMcBVbyTiog.Zgxr85up_ouZX9T1hvT8qngh0sB4IG6E1pfjKG2ra9Ig.PNG.moneyhero7779%2Fimage.png&type=a340"},
        {"name": "굽네치킨", "rating": "5.0", "review_count": "1,013", "min_order": "18,000원", "time": "약 35분", "img_url": "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDExMTZfMjc5%2FMDAxNjA1NDg0MzU0MDM5.SiiTJ_-VMrrdUdOQIkyn9RfAblNai0oxIKNbuD6Dpvcg.7vFXLFcesuPJVaE3vznJ7BAwE6-9Sihqry36bmy9myQg.PNG.ryowoo48%2F%25BD%25BA%25C5%25A9%25B8%25B0%25BC%25A6_2020-11-16_%25BF%25C0%25C0%25FC_8.51.52.png&type=a340"}
    ]
}

# 가게마다 고유 id, 소속 카테고리, 메뉴 목록(CATEGORY_MENUS에서 가져옴)을 부여
_next_store_id = 1
STORES_BY_ID = {}
for _cat_name, _store_list in category_data.items():
    for _store in _store_list:
        _store["id"] = _next_store_id
        _store["category"] = _cat_name
        _store["menus"] = CATEGORY_MENUS.get(_cat_name, [])
        STORES_BY_ID[_next_store_id] = _store
        _next_store_id += 1


def get_store_or_none(store_id):
    return STORES_BY_ID.get(store_id)


def get_menu_or_none(store, menu_id):
    if not store:
        return None
    return next((m for m in store["menus"] if m["id"] == menu_id), None)


def _find_store_img(name):
    """category_data에서 정확한 상호명으로 로고 이미지를 찾아온다."""
    for store_list in category_data.values():
        for store in store_list:
            if store["name"] == name:
                return store["img_url"]
    return ""


# learn_menu.js / learn_menu_option.js 에서 쓰는 짧은 가게 키(굽네, 홍콩반점 등)를
# category_data 안의 실제 상호명과 이어주는 매핑.
# 이렇게 하면 로고 URL을 views.py의 category_data 한 곳에서만 관리하면 된다.
STORE_LOGOS_FOR_JS = {
    "굽네": _find_store_img("굽네치킨"),
    "홍콩반점": _find_store_img("홍콩반점"),
    "맥도날드": _find_store_img("맥도날드"),
    "메가mgc": _find_store_img("메가MGC커피"),
    "엽기떡볶이": _find_store_img("동대문엽기떡볶이"),
    "피로족발": _find_store_img("피로족발"),
}


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

        'current_stage': 1
    }
    request.session.modified = True

    # 🚀 핵심: 세션을 디스크에 완전히 저장시킨 후, 미션 페이지로 리다이렉트합니다!
    return redirect('deliverys:learn_mission')

def main(request):
    return render(request, 'deliverys/main.html')

# --- 학습 모드 ---
def learn_mission(request):
    initialize_simulation(request)
    cart_data = request.session.get('cart_data')

    if not cart_data:
        return redirect('deliverys:main')

    answer = cart_data.get('answer_data', {})

    context = {
        'store': answer.get('store'),
        'menu': answer.get('menu'),
        'count': answer.get('count'),
        'extra': answer.get('extra'),
    }

    return render(request, 'deliverys/learn_mission.html', context)

def learn_search(request):
    cart_data = request.session.get('cart_data')
    
    if not cart_data:
        return redirect('deliverys:main')
    
    answer = cart_data.get('answer_data', {})
    
    context = {
        'store': answer.get('store'),
        'menu': answer.get('menu'),
        'count': answer.get('count'),
        'extra': answer.get('extra'),
    }
    return render(request, 'deliverys/learn_search.html', context)

def learn_list(request):
    cart_data = request.session.get('cart_data')
    if not cart_data:
        return redirect('deliverys:main')

    answer = cart_data.get('answer_data', {})
    correct_keyword = answer.get('category')
    store = answer.get('store'),
    menu = answer.get('menu'),
    count =  answer.get('count'),
    extra = answer.get('extra'),
    # 1. 검색어를 가져오기 (기본값은 '분식')
    keyword = request.GET.get('q', '분식')

    error_message = None

    # ① 전체 가게 이름 중에 검색어가 포함되는 가게를 전부 모으기
    matched_stores = []
    for cat_name, store_list in category_data.items():
        for store in store_list:
            if keyword in store["name"]:
                matched_stores.append(store)

    if matched_stores:
        # 상호명으로 매칭되더라도, 그 가게가 이번 미션의 정답 카테고리에
        # 속하는지 반드시 확인한다. (다른 카테고리 가게 이름을 검색해서
        # 통과되는 것을 막기 위함)
        correct_matched_stores = [
            s for s in matched_stores if s.get("category") == correct_keyword
        ]

        if not correct_matched_stores:
            messages.error(
                request,
                f"틀렸습니다! '{keyword}'은(는) 이번 미션에 맞는 카테고리가 아닙니다. 미션을 다시 확인해 보세요!",
            )
            return redirect('deliverys:learn_search')

        stores = correct_matched_stores
        target_store = correct_matched_stores[0]["name"]
    else:
        # ② 상호명에 안 걸리면 카테고리 키워드 매핑으로 시도
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

        if search_key != correct_keyword:
            messages.error(request, f"틀렸습니다! '{keyword}'은(는) 이번 미션에 \n 맞는 카테고리가 아닙니다.")

            return redirect('deliverys:learn_search')

        if search_key in category_data:
            stores = category_data[search_key]
            target_store = "동대문엽기떡볶이"
            if search_key == "중식":
                target_store = "홍콩반점"
            elif search_key == "패스트푸드":
                target_store = "맥도날드"
            elif search_key == "카페디저트":
                target_store = "메가MGC커피"
            elif search_key == "치킨가게":
                target_store = "굽네치킨"
            elif search_key == "족발보쌈":
                target_store = "피로족발"
        else:
            # ③ 어디에도 안 걸리는 검색어
            stores = []
            target_store = None
            error_message = f'"{keyword}"에 대한 검색 결과가 없습니다.'

    return render(request, 'deliverys/learn_list.html', {
        'stores': stores,
        'keyword': keyword,
        'target_store': target_store,
        'error_message': error_message,
        'store': store,
        'menu': menu,
        'count': count,
        'extra': extra
    })

def learn_menu(request):
    cart_data = request.session.get('cart_data')
    if not cart_data:
        return redirect('deliverys:main')
    answer = cart_data.get('answer_data', {})
    
    context = {
        'store': answer.get('store'),
        'menu': answer.get('menu'),
        'count': answer.get('count'),
        'extra': answer.get('extra'),
    }

    return render(request, 'deliverys/learn_menu.html', context)

def learn_menu_option(request):
    cart_data = request.session.get('cart_data')
    if not cart_data:
        return redirect('deliverys:main')
    answer = cart_data.get('answer_data', {})
   
    context = {
        'store_logos_json': json.dumps(STORE_LOGOS_FOR_JS, ensure_ascii=False),
        'store': answer.get('store'),
        'menu': answer.get('menu'),
        'count': answer.get('count'),
        'extra': answer.get('extra'),
    }
    return render(request, 'deliverys/learn_menu_option.html', context)

def learn_cart(request):
    cart_data = request.session.get('cart_data')
    if not cart_data:
        return redirect('deliverys:main')
    answer = cart_data.get('answer_data', {})
   
    context = {
        'store': answer.get('store'),
        'menu': answer.get('menu'),
        'count': answer.get('count'),
        'extra': answer.get('extra'),
    }
    return render(request, 'deliverys/learn_cart.html', context)

def learn_payment(request):
    cart_data = request.session.get('cart_data')
    if not cart_data:
        return redirect('deliverys:main')
    answer = cart_data.get('answer_data', {})
   
    context = {
        'store': answer.get('store'),
        'menu': answer.get('menu'),
        'count': answer.get('count'),
        'extra': answer.get('extra'),
    }
    return render(request, 'deliverys/learn_payment.html', context)

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