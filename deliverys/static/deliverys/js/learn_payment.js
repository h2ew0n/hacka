/* ============================================
   learn_payment.js
   결제(learn_payment) 화면 전용 스크립트

   [데이터 연동 규칙]
   - learn_cart 에서 "알뜰배달 주문하기"를 누르면 localStorage['ld_payment']에
       {
         store: {...},
         items: [...],
         menuTotal: 25000,
         deliveryFee: 1000,
         total: 26000
       }
     형태로 저장해둔다. 이 페이지는 그 값을 그대로 읽어서 보여준다.
   위 값이 없을 경우, 화면 확인용 기본 샘플 데이터(스크린샷 기준 값)를 사용한다.
   ============================================ */

(function () {
    const PAYMENT_KEY = "ld_payment";

    const DEFAULT_PAYMENT = {
        menuTotal: 25000,
        deliveryFee: 1000,
        total: 26000,
    };

    const AGREEMENTS = [
        { id: "delivery", label: "배달상품 주의사항 동의" },
        { id: "privacy", label: "개인정보 제3자 제공 동의" },
        { id: "terms", label: "이용약관" },
        { id: "notice", label: "유의사항" },
    ];

    function loadPayment() {
        try {
            const raw = localStorage.getItem(PAYMENT_KEY);
            if (!raw) return DEFAULT_PAYMENT;
            const parsed = JSON.parse(raw);
            if (
                !parsed ||
                typeof parsed.menuTotal !== "number" ||
                typeof parsed.deliveryFee !== "number" ||
                typeof parsed.total !== "number"
            ) {
                return DEFAULT_PAYMENT;
            }
            return parsed;
        } catch (e) {
            return DEFAULT_PAYMENT;
        }
    }

    function formatWon(n) {
        return n.toLocaleString("ko-KR") + "원";
    }

    /* ---------- 토스트 메시지 ---------- */
    let toastTimer = null;
    function showToast(message) {
        const toast = document.getElementById("paymentToast");
        if (!toast) return;
        toast.textContent = message || "이 버튼이 아닙니다!";
        toast.classList.add("show");
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => {
            toast.classList.remove("show");
        }, 1500);
    }

    /* ---------- 결제 금액 렌더링 ---------- */
    function renderPayment(payment) {
        document.getElementById("menuAmount").textContent = formatWon(payment.menuTotal);
        document.getElementById("deliveryFeeAmount").textContent = formatWon(payment.deliveryFee);
        document.getElementById("expectedAmount").textContent = formatWon(payment.total);
        document.getElementById("payAmount").textContent = formatWon(payment.total);
    }

    /* ---------- 약관/동의 아코디언 렌더링 ---------- */
    function renderAgreements() {
        const wrap = document.getElementById("agreementList");
        wrap.innerHTML = AGREEMENTS.map(
            (item) => `
            <div class="payment-agreement-row" data-agreement-toggle="${item.id}">
                <span>${item.label}</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M6 12L10 8L6 4" stroke="#666666" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div class="payment-agreement-detail" id="agreement-detail-${item.id}">${item.label} 내용입니다.</div>
        `
        ).join("");

        wrap.querySelectorAll("[data-agreement-toggle]").forEach((row) => {
            row.addEventListener("click", () => {
                const id = row.getAttribute("data-agreement-toggle");
                const detail = document.getElementById(`agreement-detail-${id}`);
                row.classList.toggle("open");
                if (detail) detail.classList.toggle("open");
            });
        });
    }

    /* ---------- 기능이 없는 버튼들: 클릭 시 메시지만 표시 ---------- */
    function bindNonFunctionalButtons() {
        document.querySelectorAll("[data-msg]").forEach((el) => {
            if (el.dataset.msgBound) return;
            el.dataset.msgBound = "true";
            el.addEventListener("click", () => showToast("이 버튼이 아닙니다!"));
        });
    }

    /* ---------- 결제하기 ---------- */
    function goToSuccess() {
        if (window.LEARN_PAYMENT_URLS && window.LEARN_PAYMENT_URLS.success) {
            window.location.href = window.LEARN_PAYMENT_URLS.success;
        }
    }

    document.addEventListener("DOMContentLoaded", () => {
        const payment = loadPayment();
        renderPayment(payment);
        renderAgreements();
        bindNonFunctionalButtons();
        document.getElementById("payBtn").addEventListener("click", goToSuccess);
    });
})();