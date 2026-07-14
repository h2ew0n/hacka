from django.urls import path
from . import views

app_name = 'deliverys'

urlpatterns = [
    path('', views.main, name='main'),  # 1. 공통 메인 화면(시작 화면)

    path('learning/mission/', views.learn_mission, name='learn_mission'),   # 2. 미션 화면
    path('learning/search/', views.learn_search, name='learn_search'),  # 3. 메뉴 검색
    path('learning/list/', views.learn_list, name='learn_list'),     # 4. 식당 리스트
    path('learning/menu/', views.learn_menu, name='learn_menu'),    # 5. 메뉴 선택
    path('learning/menu_option/', views.learn_menu_option, name='learn_menu_option'),   # 6. 메뉴 옵션
    path('learning/cart/', views.learn_cart, name='learn_cart'),    # 7. 장바구니
    path('learning/payment/', views.learn_payment, name='learn_payment'),   # 8. 결제
    path('learning/success/', views.learn_success, name='learn_success'),  # 9. 성공 화면

    # 활용 세션 (Application Mode - 추후 구현)
    path('apply/mission/', views.apply_mission, name='apply_mission'),
    path('apply/search/', views.apply_search, name='apply_search'),
    path('apply/menu/', views.apply_menu, name='apply_menu'),
    path('apply/cart/', views.apply_cart, name='apply_cart'),
    path('apply/payment/', views.apply_payment, name='apply_payment'),
    path('apply/success/', views.apply_success, name='apply_success'),
]