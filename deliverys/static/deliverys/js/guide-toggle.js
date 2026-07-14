function getGuideEnabled() {
    var saved = localStorage.getItem('deliverys_guideEnabled');
    return saved === null ? true : saved === 'true';
}

function applyGuideState() {
    var enabled = getGuideEnabled();
    // body에 'guide-hidden' 클래스를 붙였다 뗐다 함
    // 실제 화면 변화(숨김, 가운데 정렬)는 전부 CSS가 담당
    document.body.classList.toggle('guide-hidden', !enabled);
    updateToggleLabel();
}

function toggleGuide() {
    var enabled = getGuideEnabled();
    localStorage.setItem('deliverys_guideEnabled', (!enabled).toString());
    applyGuideState();
}

function updateToggleLabel() {
    var label = document.getElementById('guide-toggle-label');
    if (!label) return;
    label.textContent = getGuideEnabled() ? '설명 끄기' : '설명 켜기';
}

document.addEventListener('DOMContentLoaded', applyGuideState);