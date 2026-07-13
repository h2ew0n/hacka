const MENU_STORAGE_KEY = "selectedDeliveryMenu";
const CART_STORAGE_KEY = "deliveryCart";

/*
 * 백엔드와 앞 페이지 연결이 아직 완성되지 않았을 때 사용할 기본값
 */
const DEFAULT_MENU = {
    id: 1,
    storeName: "BBQ 길음센터피스점",
    name: "황금올리브 핫 크리스피 + BBQ 감자튀김",
    description:
        "황금올리브치킨 핫크리스피+BBQ감자튀김\n기본 소스는 미포함이며, 옵션 추가 가능합니다.",
    price: 28000,
    image: window.LEARN_MENU_OPTION_CONFIG.defaultImage,

    drinkOptions: [
        {
            id: "drink-245",
            name: "콜라245ml추가 (1,000원)",
            price: 1000,
            checked: true,
        },
        {
            id: "drink-335",
            name: "콜라335ml추가 (1,500원)",
            price: 1500,
            checked: false,
        },
        {
            id: "drink-500",
            name: "콜라500ml추가 (2,000원)",
            price: 2000,
            checked: false,
        },
        {
            id: "drink-1250",
            name: "콜라1.25L추가 (3,000원)",
            price: 3000,
            checked: false,
        },
    ],

    sideOptions: [
        {
            id: "side-corn",
            name: "뿜치킹 콘립(4개)",
            price: 5000,
        },
        {
            id: "side-potato",
            name: "뿜치킹 감자튀김",
            price: 5000,
        },
        {
            id: "side-assorted-potato",
            name: "뿜치킹 모둠감자튀김",
            price: 12000,
        },
        {
            id: "side-shrimp",
            name: "뿜치킹 통새우 멘보샤(5개)",
            price: 7000,
        },
    ],

    extraOptions: [
        {
            id: "extra-pickle",
            name: "치킨무 추가",
            price: 1000,
        },
        {
            id: "extra-rice-uncooked",
            name: "즉석밥(비조리) 추가",
            price: 2000,
        },
        {
            id: "extra-rice-cooked",
            name: "즉석밥(조리) 추가",
            price: 2000,
        },
    ],
};


/*
 * localStorage에 메뉴 정보가 있으면 해당 정보를 사용하고,
 * 없거나 잘못된 데이터이면 DEFAULT_MENU를 사용합니다.
 */
function loadMenu() {
    try {
        const raw = localStorage.getItem(MENU_STORAGE_KEY);

        if (!raw) {
            return DEFAULT_MENU;
        }

        const parsed = JSON.parse(raw);

        if (!parsed || !parsed.name) {
            return DEFAULT_MENU;
        }

        return {
            ...DEFAULT_MENU,
            ...parsed,

            drinkOptions:
                Array.isArray(parsed.drinkOptions) &&
                parsed.drinkOptions.length > 0
                    ? parsed.drinkOptions
                    : DEFAULT_MENU.drinkOptions,

            sideOptions:
                Array.isArray(parsed.sideOptions)
                    ? parsed.sideOptions
                    : DEFAULT_MENU.sideOptions,

            extraOptions:
                Array.isArray(parsed.extraOptions)
                    ? parsed.extraOptions
                    : DEFAULT_MENU.extraOptions,
        };
    } catch (error) {
        console.error("메뉴 데이터를 불러오지 못했습니다.", error);
        return DEFAULT_MENU;
    }
}


const currentMenu = loadMenu();

let quantity = 1;


/*
 * 숫자를 28,000원 형태로 표시합니다.
 */
function formatPrice(price) {
    const safePrice = Number(price) || 0;

    return `${safePrice.toLocaleString("ko-KR")}원`;
}


/*
 * 메뉴 기본 정보를 화면에 표시합니다.
 */
function renderMenuInfo() {
    const headerTitle = document.getElementById("menu-header-title");
    const menuName = document.getElementById("menu-name");
    const menuDescription = document.getElementById("menu-description");
    const menuPrice = document.getElementById("menu-base-price");
    const menuImage = document.getElementById("menu-main-image");

    headerTitle.textContent = currentMenu.name;
    menuName.textContent = currentMenu.name;
    menuDescription.textContent = currentMenu.description;
    menuPrice.textContent = formatPrice(currentMenu.price);

    menuImage.src =
        currentMenu.image || window.LEARN_MENU_OPTION_CONFIG.defaultImage;

    menuImage.alt = currentMenu.name;
}


/*
 * 라디오 옵션 HTML을 생성합니다.
 */
function createRadioOption(option) {
    const label = document.createElement("label");
    label.className = "option-item";

    label.innerHTML = `
        <span class="option-choice">
            <input
                type="radio"
                name="drink"
                value="${option.id}"
                data-price="${option.price}"
                ${option.checked ? "checked" : ""}
            >
            <span>${option.name}</span>
        </span>

        <strong>+${formatPrice(option.price)}</strong>
    `;

    return label;
}


/*
 * 체크박스 옵션 HTML을 생성합니다.
 */
function createCheckboxOption(option, groupName) {
    const label = document.createElement("label");
    label.className = "option-item";

    label.innerHTML = `
        <span class="option-choice">
            <input
                type="checkbox"
                name="${groupName}"
                value="${option.id}"
                data-price="${option.price}"
            >
            <span>${option.name}</span>
        </span>

        <strong>+${formatPrice(option.price)}</strong>
    `;

    return label;
}


/*
 * 옵션 목록을 화면에 출력합니다.
 */
function renderOptions() {
    const drinkOptionList =
        document.getElementById("drink-option-list");

    const sideOptionList =
        document.getElementById("side-option-list");

    const extraOptionList =
        document.getElementById("extra-option-list");

    drinkOptionList.innerHTML = "";
    sideOptionList.innerHTML = "";
    extraOptionList.innerHTML = "";

    currentMenu.drinkOptions.forEach((option) => {
        drinkOptionList.appendChild(createRadioOption(option));
    });

    currentMenu.sideOptions.forEach((option) => {
        sideOptionList.appendChild(
            createCheckboxOption(option, "side"),
        );
    });

    currentMenu.extraOptions.forEach((option) => {
        extraOptionList.appendChild(
            createCheckboxOption(option, "extra"),
        );
    });
}


/*
 * 선택된 옵션 가격을 계산합니다.
 */
function getSelectedOptionPrice() {
    const selectedInputs = document.querySelectorAll(
        '.menu-option-form input:checked',
    );

    let optionPrice = 0;

    selectedInputs.forEach((input) => {
        optionPrice += Number(input.dataset.price) || 0;
    });

    return optionPrice;
}


/*
 * 총 주문 가격을 계산합니다.
 */
function calculateTotalPrice() {
    const menuPrice = Number(currentMenu.price) || 0;
    const optionPrice = getSelectedOptionPrice();

    return (menuPrice + optionPrice) * quantity;
}


/*
 * 수량과 총금액을 화면에 반영합니다.
 */
function updateOrderSummary() {
    const quantityValue =
        document.getElementById("quantity-value");

    const addCartButton =
        document.getElementById("add-cart-button");

    quantityValue.textContent = `${quantity}개`;

    addCartButton.textContent =
        `${formatPrice(calculateTotalPrice())} 담기`;
}


/*
 * 현재 선택 상태를 장바구니 데이터로 만듭니다.
 */
function createCartItem() {
    const selectedDrink = document.querySelector(
        'input[name="drink"]:checked',
    );

    const selectedSides = [
        ...document.querySelectorAll(
            'input[name="side"]:checked',
        ),
    ];

    const selectedExtras = [
        ...document.querySelectorAll(
            'input[name="extra"]:checked',
        ),
    ];

    return {
        menuId: currentMenu.id,
        storeName: currentMenu.storeName,
        menuName: currentMenu.name,
        menuImage: currentMenu.image,
        basePrice: currentMenu.price,
        quantity,
        totalPrice: calculateTotalPrice(),

        drink: selectedDrink
            ? {
                  id: selectedDrink.value,
                  price: Number(selectedDrink.dataset.price) || 0,
              }
            : null,

        sides: selectedSides.map((input) => ({
            id: input.value,
            price: Number(input.dataset.price) || 0,
        })),

        extras: selectedExtras.map((input) => ({
            id: input.value,
            price: Number(input.dataset.price) || 0,
        })),
    };
}


/*
 * 장바구니 정보를 localStorage에 저장합니다.
 */
function saveCartItem() {
    try {
        const cartItem = createCartItem();

        localStorage.setItem(
            CART_STORAGE_KEY,
            JSON.stringify(cartItem),
        );

        window.location.href =
            window.LEARN_MENU_OPTION_CONFIG.cartUrl;
    } catch (error) {
        console.error("장바구니 저장에 실패했습니다.", error);
        alert("장바구니에 메뉴를 담지 못했습니다.");
    }
}


/*
 * 버튼 및 옵션 이벤트를 연결합니다.
 */
function bindEvents() {
    const decreaseButton =
        document.getElementById("quantity-decrease");

    const increaseButton =
        document.getElementById("quantity-increase");

    const addCartButton =
        document.getElementById("add-cart-button");

    decreaseButton.addEventListener("click", () => {
        if (quantity <= 1) {
            return;
        }

        quantity -= 1;
        updateOrderSummary();
    });

    increaseButton.addEventListener("click", () => {
        quantity += 1;
        updateOrderSummary();
    });

    document
        .getElementById("menu-option-form")
        .addEventListener("change", updateOrderSummary);

    addCartButton.addEventListener("click", saveCartItem);
}


/*
 * 페이지 초기화
 */
function initializeMenuOptionPage() {
    renderMenuInfo();
    renderOptions();
    bindEvents();
    updateOrderSummary();
}

document.addEventListener(
    "DOMContentLoaded",
    initializeMenuOptionPage,
);