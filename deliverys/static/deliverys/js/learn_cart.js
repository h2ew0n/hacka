/* ============================================
   learn_cart.js
   장바구니(learn_cart) 화면 전용 스크립트

   [데이터 연동 규칙]
   - learn_search 에서 고른 가게 정보  -> localStorage['ld_store']
       { "name": "BBQ OO점", "image": "🍗" }
   - learn_menu / learn_menu_option 에서 담은 메뉴 -> localStorage['ld_cartItems']
       [
         {
           "id": "item-1",
           "menuName": "황올 반 + 양념 반",
           "optionLines": ["활올 부분육 선택 : 한마리", "..."],
           "unitPrice": 25000,   // 옵션이 반영된 1개당 가격
           "qty": 1,             // learn_menu(_option) 에서 선택한 수량
           "image": "🍗"
         }
       ]
   위 값이 없을 경우, 화면 확인용 기본 샘플 데이터를 사용한다.
   ============================================ */

(function () {
    const STORE_KEY = "ld_store";
    const CART_KEY = "ld_cartItems";
    const DELIVERY_FEE = 1000; // 알뜰배달 고정 배달팁

    const DEFAULT_STORE = { name: "BBQ OO점", image: "🍗" };

    const DEFAULT_CART_ITEMS = [
        {
            id: "sample-1",
            menuName: "황올 반 + 양념 반",
            optionLines: [
                "가격: 24,000원",
                "황올 부분육 선택 : 한마리",
                "음료 추가선택 (2) 콜라 245ml 추가",
                "소스 추가 선택: 기본 소스 미제공",
            ],
            unitPrice: 25000,
            qty: 1,
            image: "🍗",
        },
    ];

    const RECO_ITEMS = [
        { name: "제로콜라 1.25L", price: 3000, image: "🥤" },
        { name: "스프라이트 1.25L", price: 3000, image: "🥤" },
    ];

    const SAVER_DELIVERY_ID = "saver"; // 알뜰배달 식별자

    const DELIVERY_METHODS = [
        { id: "home", name: "한집 배달", fee: 2000, time: "14~20분 후 도착", selected: false },
        { id: SAVER_DELIVERY_ID, name: "알뜰 배달", fee: 1000, time: "14~20분 후 도착", selected: false },
        { id: "store", name: "가게 배달", fee: 2500, time: "14~20분 후 도착", selected: false },
        { id: "pickup", name: "픽업", fee: 0, time: "14~20분 후 도착", selected: false },
        { id: "instore", name: "매장 식사", fee: 0, time: "14~20분 후 도착", selected: false },
    ];

    let store = loadStore();
    let cartItems = loadCartItems();

    function loadStore() {
        try {
            const raw = localStorage.getItem(STORE_KEY);
            if (!raw) return DEFAULT_STORE;
            const parsed = JSON.parse(raw);
            if (!parsed || !parsed.name) return DEFAULT_STORE;
            return parsed;
        } catch (e) {
            return DEFAULT_STORE;
        }
    }

    function loadCartItems() {
        try {
            const raw = localStorage.getItem(CART_KEY);
            if (!raw) return JSON.parse(JSON.stringify(DEFAULT_CART_ITEMS));
            const parsed = JSON.parse(raw);
            if (!Array.isArray(parsed) || parsed.length === 0) {
                return JSON.parse(JSON.stringify(DEFAULT_CART_ITEMS));
            }
            return parsed;
        } catch (e) {
            return JSON.parse(JSON.stringify(DEFAULT_CART_ITEMS));
        }
    }

    function saveCartItems() {
        localStorage.setItem(CART_KEY, JSON.stringify(cartItems));
    }

    function formatWon(n) {
        return n.toLocaleString("ko-KR") + "원";
    }

    function getMenuTotal() {
        return cartItems.reduce((sum, item) => sum + item.unitPrice * item.qty, 0);
    }

    /* ---------- 토스트 메시지 ---------- */
    let toastTimer = null;
    function showToast(message) {
        const toast = document.getElementById("cartToast");
        if (!toast) return;
        toast.textContent = message || "이 버튼이 아닙니다!";
        toast.classList.add("show");
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => {
            toast.classList.remove("show");
        }, 1500);
    }

    /* ---------- 렌더링 ---------- */
    function render() {
        renderStore();
        renderCartItems();
        renderReco();
        renderDelivery();
        renderPayment();
        bindNonFunctionalButtons();
    }

    function renderStore() {
        document.getElementById("storeThumb").textContent = store.image || "🍗";
        document.getElementById("storeName").textContent = store.name || "가게 이름";
    }

    function renderCartItems() {
        const wrap = document.getElementById("cartItemList");
        wrap.innerHTML = "";

        cartItems.forEach((item) => {
            const card = document.createElement("div");
            card.className = "cart-item";

            const optionHtml = (item.optionLines || [])
                .map((line) => `<p class="cart-item-option-line">${line}</p>`)
                .join("");

            card.innerHTML = `
                <div class="cart-item-main">
                    <div class="cart-item-info">
                        <p class="cart-item-name">${item.menuName}</p>
                        ${optionHtml}
                        <p class="cart-item-price">${formatWon(item.unitPrice * item.qty)}</p>
                    </div>
                    <div class="cart-item-thumb">${item.image || "🍗"}</div>
                </div>
                <div class="cart-item-controls">
                    <button type="button" class="cart-opt-btn" data-msg>옵션 변경</button>
                    <div class="cart-trash-qty">
                        <button type="button" class="cart-trash-btn" data-msg>
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" fill="none">
                                <path d="M8.33337 9.1665V14.1665" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M11.6666 9.1665V14.1665" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M15.8333 5V16.6667C15.8333 17.1087 15.6577 17.5326 15.3451 17.8452C15.0326 18.1577 14.6087 18.3333 14.1666 18.3333H5.83329C5.39127 18.3333 4.96734 18.1577 4.65478 17.8452C4.34222 17.5326 4.16663 17.1087 4.16663 16.6667V5" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M2.5 5H17.5" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M6.66663 4.99984V3.33317C6.66663 2.89114 6.84222 2.46722 7.15478 2.15466C7.46734 1.8421 7.89127 1.6665 8.33329 1.6665H11.6666C12.1087 1.6665 12.5326 1.8421 12.8451 2.15466C13.1577 2.46722 13.3333 2.89114 13.3333 3.33317V4.99984" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                        <div class="cart-qty-box">
                            <span class="cart-qty-value">${item.qty}</span>
                            <button type="button" class="cart-qty-plus" data-qty-plus="${item.id}" data-msg>+</button>
                        </div>
                    </div>
                </div>
                <button type="button" class="cart-add-menu-btn" data-msg>+  메뉴 추가</button>
            `;

            wrap.appendChild(card);
        });
    }

    function renderReco() {
        const wrap = document.getElementById("recoList");
        wrap.innerHTML = RECO_ITEMS.map(
            (reco) => `
            <div class="cart-reco-item">
                <div class="cart-reco-info">
                    <div class="cart-reco-thumb-info">
                        <div class="cart-reco-thumb">${reco.image}</div>
                        <div class="cart-reco-name-price">
                            <p class="cart-reco-name">${reco.name}</p>
                            <p class="cart-reco-price">${formatWon(reco.price)}</p>
                        </div>     
                    </div>
                    <button type="button" class="cart-reco-add-btn" data-msg>+</button>
                </div>
            </div>
        `
        ).join("");
    }

    function renderDelivery() {
        const wrap = document.getElementById("deliveryList");
        wrap.innerHTML = DELIVERY_METHODS.map((d) => {
            // 알뜰배달만 실제로 선택 가능한 버튼이고, 나머지는 눌러도 메시지만 뜬다.
            const clickAttr = d.id === SAVER_DELIVERY_ID
                ? `data-delivery-select="${d.id}"`
                : "data-msg";
            return `
            <div class="cart-delivery-row ${d.selected ? "selected" : ""}" ${clickAttr}>
                <div>
                    <p class="cart-delivery-name">${d.name}</p>
                    <p class="cart-delivery-time">${d.time}</p>
                </div>
                <span class="cart-delivery-fee">${d.fee === 0 ? "무료" : formatWon(d.fee)}</span>
            </div>
        `;
        }).join("");

        wrap.querySelectorAll("[data-delivery-select]").forEach((el) => {
            el.addEventListener("click", () => {
                const id = el.getAttribute("data-delivery-select");
                const target = DELIVERY_METHODS.find((d) => d.id === id);
                if (!target) return;
                target.selected = !target.selected; // 이미 선택돼 있으면 해제, 아니면 선택
                render();
            });
        });
    }

    function renderPayment() {
        const menuTotal = getMenuTotal();
        const total = menuTotal + DELIVERY_FEE;

        document.getElementById("menuAmount").textContent = formatWon(menuTotal);
        document.getElementById("deliveryFeeAmount").textContent = formatWon(DELIVERY_FEE);
        document.getElementById("expectedAmount").textContent = formatWon(total);
        document.getElementById("bottomTotal").textContent = formatWon(total);
    }

    /* ---------- 기능이 없는 버튼들: 클릭 시 메시지만 표시 ---------- */
    function bindNonFunctionalButtons() {
        document.querySelectorAll("[data-msg]").forEach((el) => {
            if (el.dataset.msgBound) return;
            el.dataset.msgBound = "true";
            el.addEventListener("click", () => showToast("이 버튼이 아닙니다!"));
        });
    }

    /* ---------- 알뜰배달 주문하기 ---------- */
    function goToPayment() {
        const saverSelected = DELIVERY_METHODS.find((d) => d.id === SAVER_DELIVERY_ID)?.selected;

        if (!saverSelected) {
            showToast("알뜰 배달을 선택해주세요!");
            return;
        }
        
        const menuTotal = getMenuTotal();
        const total = menuTotal + DELIVERY_FEE;

        const payload = {
            store: store,
            items: cartItems,
            menuTotal: menuTotal,
            deliveryFee: DELIVERY_FEE,
            total: total,
        };
        localStorage.setItem("ld_payment", JSON.stringify(payload));

        if (window.LEARN_CART_URLS && window.LEARN_CART_URLS.payment) {
            window.location.href = window.LEARN_CART_URLS.payment;
        }
    }

    document.addEventListener("DOMContentLoaded", () => {
        render();
        document.getElementById("orderBtn").addEventListener("click", goToPayment);
    });
})();