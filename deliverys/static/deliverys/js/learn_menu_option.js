console.log("learn_menu_option.js 실행됨");

document.addEventListener("DOMContentLoaded", function () {
    const config = window.LEARN_MENU_OPTION_CONFIG || {};

    const menuHeaderTitle = document.getElementById("menu-header-title");
    const menuMainImage = document.getElementById("menu-main-image");
    const menuNameElement = document.getElementById("menu-name");
    const menuDescriptionElement = document.getElementById("menu-description");
    const menuBasePriceElement = document.getElementById("menu-base-price");

    const firstOptionList = document.getElementById("drink-option-list");
    const secondOptionList = document.getElementById("side-option-list");
    const thirdOptionList = document.getElementById("extra-option-list");

    const firstOptionSection =
        document.getElementById("first-option-section") ||
        firstOptionList?.closest(".option-section");

    const secondOptionSection =
        document.getElementById("second-option-section") ||
        secondOptionList?.closest(".option-section");

    const thirdOptionSection =
        document.getElementById("third-option-section") ||
        thirdOptionList?.closest(".option-section");

    const firstOptionTitle =
        document.getElementById("first-option-title") ||
        firstOptionSection?.querySelector(".option-heading h2");

    const secondOptionTitle =
        document.getElementById("second-option-title") ||
        secondOptionSection?.querySelector(".option-heading h2");

    const thirdOptionTitle =
        document.getElementById("third-option-title") ||
        thirdOptionSection?.querySelector(".option-heading h2");

    const quantityDecreaseButton = document.getElementById("quantity-decrease");
    const quantityIncreaseButton = document.getElementById("quantity-increase");
    const quantityValueElement = document.getElementById("quantity-value");
    const addCartButton = document.getElementById("add-cart-button");

    const requiredElements = [
        menuHeaderTitle,
        menuMainImage,
        menuNameElement,
        menuDescriptionElement,
        menuBasePriceElement,
        firstOptionList,
        secondOptionList,
        thirdOptionList,
        quantityDecreaseButton,
        quantityIncreaseButton,
        quantityValueElement,
        addCartButton
    ];

    if (requiredElements.some((element) => !element)) {
        console.error("learn_menu_option.html에서 필요한 요소를 찾지 못했습니다.");
        return;
    }

    let quantity = 1;
    let selectedFirstOptionPrice = 0;
    let selectedSecondOptionPrices = [];
    let selectedThirdOptionPrices = [];

    const toast = createToast();
    let toastTimer = null;

    function createToast() {
        let element = document.getElementById("cartToast");

        if (!element) {
            element = document.createElement("div");
            element.id = "cartToast";
            element.setAttribute("role", "status");
            element.setAttribute("aria-live", "polite");

            const screen =
                document.querySelector(".menu-option-screen") ||
                document.body;

            screen.appendChild(element);
        }

        

        const screen = document.querySelector(".menu-option-screen");
        if (screen) {
            screen.style.position = "relative";
        }

        return element;
    }

    function showToast(message) {
        if (!toast) return;

        toast.textContent =
            message || "미션에 맞는 옵션을 선택해주세요.";

        toast.classList.remove("show");

        void toast.offsetWidth;

        toast.classList.add("show");

        clearTimeout(toastTimer);

        toastTimer = setTimeout(function () {
            toast.classList.remove("show");
        }, 2200);
    }

    const menuOptionData = {
        "엽기떡볶이": {
            store: "엽기떡볶이",
            name: "엽기떡볶이",
            description: "매콤한 국물과 쫄깃한 떡이 어우러진 대표 떡볶이 메뉴입니다.",
            price: 14000,
            image: "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNjAyMTdfMTQ4%2FMDAxNzcxMzI1OTUyNTc3.CUW5kwV5RMbWoq8UUzbGU8tTcmavL18_aWLmtoe0BZgg.4SDZ6c4yYhOnbQsfgPa_lw0p2RujCbtjygjW6hZfa2Yg.JPEG%2F%25BA%25A3%25BD%25BA%25C6%25AE%25BC%25BC%25C6%25AE.jpg&type=a340",
            firstTitle: "맵기 선택",
            firstRequired: true,
            firstOptions: [
                { name: "착한맛", price: 0 },
                { name: "초보맛", price: 0 },
                { name: "덜매운맛", price: 0 },
                { name: "오리지널", price: 0 },
                { name: "매운맛", price: 0 }
            ],
            secondTitle: "토핑 추가선택",
            secondOptions: [
                { name: "중국당면 추가", price: 2500 },
                { name: "치즈 추가", price: 3000 },
                { name: "베이컨 추가", price: 3000 }
            ],
            thirdTitle: "사이드 추가선택",
            thirdOptions: [
                { name: "모둠튀김", price: 7000 },
                { name: "주먹김밥", price: 3000 },
                { name: "계란찜", price: 5000 }
            ]
        },
        "짬뽕": {
            store: "홍콩반점",
            name: "짬뽕",
            description: "불향을 입힌 채소와 해물이 들어간 얼큰한 국물 짬뽕입니다.",
            price: 8000,
            image: "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fi.pinimg.com%2F736x%2Ff6%2Fb6%2Fd1%2Ff6b6d10cb9a7a3adf34d581fe6c09f03.jpg&type=a340",
            firstTitle: "맵기 선택",
            firstRequired: true,
            firstOptions: [
                { name: "기본맛", price: 0 },
                { name: "덜 맵게", price: 0 },
                { name: "더 맵게", price: 0 }
            ],
            secondTitle: "메뉴 추가선택",
            secondOptions: [
                { name: "곱빼기", price: 1000 },
                { name: "공깃밥", price: 1000 },
                { name: "군만두 추가", price: 5000 }
            ],
            thirdTitle: "요청사항",
            thirdOptions: [
                { name: "단무지 추가", price: 0 },
                { name: "양파 추가", price: 0 }
            ]
        },
        "불고기버거 세트": {
            store: "맥도날드",
            name: "불고기버거 세트",
            description: "달콤한 불고기 소스가 어우러진 버거와 후렌치 후라이, 음료로 구성된 세트입니다.",
            price: 6000,
            image: "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxODA4MDdfMTI4%2FMDAxNTMzNjE5NjY4MzI4.BNQzfoRZagiIbqtAQ-uIm6k-5Prrr9CmoBATOaWCvi8g.yWzD2-97jU-ghShgmheo3CIf6mF1ygTILjmXabqHPfQg.PNG.ynos33%2Fprov_201803260924164710.png&type=a340",
            firstTitle: "음료 선택",
            firstRequired: true,
            firstOptions: [
                { name: "코카콜라", price: 0 },
                { name: "코카콜라 제로", price: 0 },
                { name: "스프라이트", price: 0 },
                { name: "환타", price: 0 }
            ],
            secondTitle: "사이드 선택",
            secondOptions: [
                { name: "후렌치 후라이", price: 0 },
                { name: "맥너겟 4조각으로 변경", price: 1500 },
                { name: "치즈스틱으로 변경", price: 1800 }
            ],
            thirdTitle: "추가 선택",
            thirdOptions: [
                { name: "치즈 추가", price: 700 },
                { name: "패티 추가", price: 1500 },
                { name: "소스 추가", price: 300 }
            ]
        },
        "큐브라떼": {
            store: "메가mgc",
            name: "큐브라떼",
            description: "진한 에스프레소 큐브에 고소한 우유를 더해 즐기는 라떼입니다.",
            price: 4500,
            image: "https://shop-phinf.pstatic.net/20250604_251/1749000649710wJiF7_JPEG/83133457863318362_856819931.jpg?type=o1000",
            firstTitle: "온도 선택",
            firstRequired: true,
            firstOptions: [
                { name: "아이스", price: 0 },
                { name: "핫", price: 0 }
            ],
            secondTitle: "샷·시럽 추가",
            secondOptions: [
                { name: "에스프레소 샷 추가", price: 500 },
                { name: "바닐라 시럽 추가", price: 500 },
                { name: "헤이즐넛 시럽 추가", price: 500 }
            ],
            thirdTitle: "기타 선택",
            thirdOptions: [
                { name: "휘핑크림 추가", price: 500 },
                { name: "우유 적게", price: 0 },
                { name: "얼음 적게", price: 0 }
            ]
        },
        "오리지널": {
            store: "굽네",
            name: "오리지널",
            description: "기름에 튀기지 않고 오븐에 구워 담백하게 즐기는 굽네 대표 메뉴입니다.",
            price: 18000,
            image: "https://sitem.ssgcdn.com/37/40/73/item/1000599734037_i1_750.jpg",
            firstTitle: "소스 선택",
            firstRequired: true,
            firstOptions: [
                { name: "소스 없음", price: 0 },
                { name: "굽네 갈비천왕 소스", price: 500 },
                { name: "굽네 마블링 소스", price: 500 }
            ],
            secondTitle: "사이드 추가선택",
            secondOptions: [
                { name: "웨지감자", price: 4000 },
                { name: "치즈볼", price: 5000 },
                { name: "바게트볼", price: 3500 }
            ],
            thirdTitle: "음료 추가선택",
            thirdOptions: [
                { name: "콜라 1.25L", price: 2500 },
                { name: "콜라 500mL", price: 1500 },
                { name: "무 추가", price: 500 }
            ]
        },
        "보쌈": {
            store: "피로족발",
            name: "보쌈",
            description: "부드럽게 삶은 수육과 아삭한 보쌈김치를 함께 즐기는 메뉴입니다.",
            price: 14000,
            image: "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fthumb2.gettyimageskorea.com%2Fimage_preview%2F700%2F201711%2FMBRF%2FMBRF17017894.jpg&type=a340",
            firstTitle: "사이즈 선택",
            firstRequired: true,
            firstOptions: [
                { name: "소", price: 0 },
                { name: "중", price: 7000 },
                { name: "대", price: 14000 }
            ],
            secondTitle: "사이드 추가선택",
            secondOptions: [
                { name: "막국수", price: 6000 },
                { name: "주먹밥", price: 4000 },
                { name: "보쌈김치 추가", price: 3000 }
            ],
            thirdTitle: "기타 선택",
            thirdOptions: [
                { name: "쌈 채소 추가", price: 2000 },
                { name: "마늘·고추 추가", price: 1000 },
                { name: "새우젓 추가", price: 500 }
            ]
        }
    };

    const missionAnswers = {
        "엽기떡볶이": {
            first: "오리지널",
            second: ["치즈 추가"],
            third: [],
            quantity: 2
        },
        "짬뽕": {
            first: "덜 맵게",
            second: ["군만두 추가"],
            third: [],
            quantity: 1
        },
        "불고기버거 세트": {
            first: "코카콜라",
            second: ["치즈스틱으로 변경"],
            third: [],
            quantity: 2
        },
        "큐브라떼": {
            first: "아이스",
            second: [],
            third: [],
            quantity: 1
        },
        "오리지널": {
            first: "소스 없음",
            second: ["치즈볼"],
            third: [],
            quantity: 4
        },
        "보쌈": {
            first: "중",
            second: [],
            third: ["쌈 채소 추가"],
            quantity: 3
        }
    };

    const savedMenuText = localStorage.getItem("selectedMenu");
    let savedMenu = null;

    try {
        savedMenu = savedMenuText ? JSON.parse(savedMenuText) : null;
    } catch (error) {
        console.error("선택 메뉴 정보를 읽지 못했습니다.", error);
    }

    const params = new URLSearchParams(window.location.search);
    const queryMenuName = params.get("menu");

    const selectedMenuName =
        queryMenuName ||
        savedMenu?.name ||
        "오리지널";

    const currentMenu =
        menuOptionData[selectedMenuName] ||
        createFallbackMenu(savedMenu);

    const currentMission =
        missionAnswers[selectedMenuName] ||
        null;

    renderMenu(currentMenu);
    updateTotalPrice();

    function createFallbackMenu(menu) {
        return {
            store: menu?.store || "",
            name: menu?.name || "선택한 메뉴",
            description: "선택한 메뉴의 추가 옵션을 골라주세요.",
            price: Number(menu?.price) || 0,
            image: menu?.image || config.defaultImage || "",
            firstTitle: "기본 선택",
            firstRequired: true,
            firstOptions: [{ name: "기본", price: 0 }],
            secondTitle: "추가 선택",
            secondOptions: [],
            thirdTitle: "기타 선택",
            thirdOptions: []
        };
    }

    function renderMenu(menu) {
        menuHeaderTitle.textContent = menu.name;
        menuNameElement.textContent = menu.name;
        menuDescriptionElement.textContent = menu.description;
        menuBasePriceElement.textContent = formatPrice(menu.price);
        menuMainImage.src = menu.image || config.defaultImage || "";
        menuMainImage.alt = menu.name;

        if (firstOptionTitle) {
            firstOptionTitle.textContent = menu.firstTitle || "필수 선택";
        }

        if (secondOptionTitle) {
            secondOptionTitle.textContent = menu.secondTitle || "추가 선택";
        }

        if (thirdOptionTitle) {
            thirdOptionTitle.textContent = menu.thirdTitle || "기타 선택";
        }

        const firstOptions = Array.isArray(menu.firstOptions)
            ? menu.firstOptions
            : [];

        const secondOptions = Array.isArray(menu.secondOptions)
            ? menu.secondOptions
            : [];

        const thirdOptions = Array.isArray(menu.thirdOptions)
            ? menu.thirdOptions
            : [];

        renderRadioOptions(firstOptionList, firstOptions);
        renderCheckboxOptions(secondOptionList, secondOptions, "second");
        renderCheckboxOptions(thirdOptionList, thirdOptions, "third");

        if (firstOptionSection) {
            firstOptionSection.style.display =
                firstOptions.length > 0 ? "" : "none";
        }

        if (secondOptionSection) {
            secondOptionSection.style.display =
                secondOptions.length > 0 ? "" : "none";
        }

        if (thirdOptionSection) {
            thirdOptionSection.style.display =
                thirdOptions.length > 0 ? "" : "none";
        }
    }

    function renderRadioOptions(container, options) {
        container.innerHTML = "";
        const correctFirstOption = currentMission?.first || "";

        options.forEach(function (option) {
            const label = document.createElement("label");
            label.className = "option-item";

            const shouldCheckByDefault =
                currentMenu.name === "오리지널" &&
                option.name === "소스 없음";

            label.innerHTML = `
                <span class="option-left">
                    <input
                        type="radio"
                        name="first-option"
                        value="${escapeHtml(option.name)}"
                        data-price="${option.price}"
                        ${shouldCheckByDefault ? "checked" : ""}
                    >
                    <span class="option-name">${escapeHtml(option.name)}</span>
                </span>

                <strong class="option-price">
                    ${formatAdditionalPrice(option.price)}
                </strong>
            `;

            const input = label.querySelector("input");

            input.addEventListener("change", function () {
                if (
                    correctFirstOption &&
                    option.name !== correctFirstOption
                ) {
                    this.checked = false;
                    showToast(`이 옵션은 미션이 아닙니다.`);
                    return;
                }

                selectedFirstOptionPrice =
                    Number(this.dataset.price) || 0;

                updateTotalPrice();
            });

            container.appendChild(label);
        });

        const checkedInput =
            container.querySelector('input[name="first-option"]:checked');

        selectedFirstOptionPrice =
            checkedInput
                ? Number(checkedInput.dataset.price) || 0
                : 0;
    }

    function renderCheckboxOptions(container, options, groupName) {
        container.innerHTML = "";
        const correctOptions = currentMission?.[groupName] || [];

        options.forEach(function (option) {
            const label = document.createElement("label");
            label.className = "option-item";

            label.innerHTML = `
                <span class="option-left">
                    <input
                        type="checkbox"
                        name="${groupName}-option"
                        value="${escapeHtml(option.name)}"
                        data-price="${option.price}"
                    >
                    <span class="option-name">${escapeHtml(option.name)}</span>
                </span>

                <strong class="option-price">
                    ${formatAdditionalPrice(option.price)}
                </strong>
            `;

            const input = label.querySelector("input");

            input.addEventListener("change", function () {
                if (
                    correctOptions.length === 0 ||
                    !correctOptions.includes(option.name)
                ) {
                    this.checked = false;

                    showToast(
                        correctOptions.length === 0
                            ? `이 옵션은 미션이 아닙니다.`
                            : `이 옵션은 미션이 아닙니다.`
                    );
                    return;
                }

                updateCheckedOptionPrices(groupName);
                updateTotalPrice();
            });

            container.appendChild(label);
        });
    }

    function updateCheckedOptionPrices(groupName) {
        const checkedInputs = document.querySelectorAll(
            `input[name="${groupName}-option"]:checked`
        );

        const prices = Array.from(checkedInputs).map(function (input) {
            return Number(input.dataset.price) || 0;
        });

        if (groupName === "second") {
            selectedSecondOptionPrices = prices;
        }

        if (groupName === "third") {
            selectedThirdOptionPrices = prices;
        }
    }

    function getSelectedRadioValue() {
        const selected = document.querySelector(
            'input[name="first-option"]:checked'
        );

        return selected ? selected.value : "";
    }

    function getSelectedCheckboxValues(groupName) {
        return Array.from(
            document.querySelectorAll(
                `input[name="${groupName}-option"]:checked`
            )
        ).map(function (input) {
            return input.value;
        });
    }

    function hasSameOptions(selected, correct) {
        if (selected.length !== correct.length) {
            return false;
        }

        return correct.every(function (option) {
            return selected.includes(option);
        });
    }

    function isMissionComplete() {
        if (!currentMission) {
            return false;
        }

        return (
            getSelectedRadioValue() === currentMission.first &&
            hasSameOptions(
                getSelectedCheckboxValues("second"),
                currentMission.second
            ) &&
            hasSameOptions(
                getSelectedCheckboxValues("third"),
                currentMission.third
            ) &&
            quantity === currentMission.quantity
        );
    }

    function getOneMenuPrice() {
        const secondTotal = selectedSecondOptionPrices.reduce(
            (sum, price) => sum + price,
            0
        );

        const thirdTotal = selectedThirdOptionPrices.reduce(
            (sum, price) => sum + price,
            0
        );

        return (
            currentMenu.price +
            selectedFirstOptionPrice +
            secondTotal +
            thirdTotal
        );
    }

    function updateTotalPrice() {
        const totalPrice = getOneMenuPrice() * quantity;
        quantityValueElement.textContent = `${quantity}개`;
        addCartButton.textContent = `${formatPrice(totalPrice)} 담기`;
    }

    quantityDecreaseButton.addEventListener("click", function () {
        if (quantity <= 1) {
            showToast("수량은 1개 이상입니다.");
            return;
        }

        quantity -= 1;
        updateTotalPrice();
    });

    quantityIncreaseButton.addEventListener("click", function () {
        if (!currentMission) {
            showToast("찾을 수 없습니다.");
            return;
        }

        if (quantity >= currentMission.quantity) {
            showToast(`이 미션의 수량은 ${currentMission.quantity}개입니다.`);
            return;
        }

        quantity += 1;
        updateTotalPrice();
    });

    addCartButton.addEventListener("click", function () {
        if (!currentMission) {
            showToast("찾을 수 없습니다.");
            return;
        }

        if (quantity !== currentMission.quantity) {
            showToast(`수량을 ${currentMission.quantity}개로 해주세요.`);
            return;
        }

        if (!isMissionComplete()) {
            showToast("옵션을 정확히 선택하세요.");
            return;
        }

        const firstSelected = document.querySelector(
            'input[name="first-option"]:checked'
        );

        const cartItem = {
            store: currentMenu.store,
            name: currentMenu.name,
            image: currentMenu.image,
            basePrice: currentMenu.price,
            firstOption: firstSelected?.value || "",
            secondOptions: getSelectedCheckboxValues("second"),
            thirdOptions: getSelectedCheckboxValues("third"),
            quantity: quantity,
            totalPrice: getOneMenuPrice() * quantity
        };

        localStorage.setItem(
            "selectedCartItem",
            JSON.stringify(cartItem)
        );

        window.location.href =
            config.cartUrl ||
            addCartButton.dataset.cartUrl;
    });

    bindWrongButton(
        'button[aria-label="공유"]',
        "공유 버튼이 아닙니다! 미션에 제시된 옵션을 선택해주세요."
    );

    bindWrongButton(
        'button[aria-label="검색"]',
        "검색 버튼이 아닙니다! 현재 메뉴의 미션 옵션을 선택해주세요."
    );

    bindWrongButton(
        '.menu-option-header button[aria-label="장바구니"]',
        "아직 장바구니 단계가 아닙니다! 미션 옵션을 먼저 선택해주세요."
    );

    bindWrongButton(
        ".send-opinion-button",
        "미션 옵션을 선택해주세요."
    );

    document.querySelectorAll(".stage-item").forEach(function (stageItem) {
        stageItem.addEventListener("click", function (event) {
            event.preventDefault();
            showToast("지금은 메뉴 옵션을 선택하는 단계입니다.");
        });
    });

    function bindWrongButton(selector, message) {
        const element = document.querySelector(selector);

        if (!element) {
            return;
        }

        element.addEventListener("click", function (event) {
            event.preventDefault();
            showToast(message);
        });
    }

    function formatPrice(price) {
        return Number(price).toLocaleString("ko-KR") + "원";
    }

    function formatAdditionalPrice(price) {
        const numberPrice = Number(price) || 0;

        if (numberPrice === 0) {
            return "추가금 없음";
        }

        return "+" + numberPrice.toLocaleString("ko-KR") + "원";
    }

    function escapeHtml(value) {
        return String(value)
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }
});