from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'deliverys/main.html')

# --- 학습 모드 ---
def learn_mission(request):
    return render(request, 'deliverys/learn_mission.html')

def learn_search(request):
    return render(request, 'deliverys/learn_search.html')

# deliverys/views.py

def learn_list(request):
    # search_query = request.GET.get('q', '') 
    
    # print(f"지정된 검색어: {search_query}")

    # context = {
    #     'search_query': search_query,
    # }
    
    return render(request, 'deliverys/learn_list.html', context)

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