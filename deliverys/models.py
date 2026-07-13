from django.db import models

# Create your models here.
class Mission(models.Model):
    """
    하나의 전체 미션 세션을 관리하는 모델 (예: '떡볶이 주문 미션')
    """
    title = models.CharField(max_length=100, verbose_name="미션 제목")
    description = models.TextField(verbose_name="미션 설명")
    

    answer_data = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="각 단계별 정답 데이터를 JSON 형식으로 저장합니다.",
        verbose_name="정답 데이터 세트"
    )

    def __str__(self):
        return self.title


class DeliveryStepView(models.Model):
    """
    각 미션의 '단계별 화면 데이터'를 관리하는 모델
    (검색창, 메뉴판, 장바구니, 결제창)
    """
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='steps')
    
    step_number = models.IntegerField(verbose_name="단계 번호 (1~5)")
    
    guide_text = models.TextField(verbose_name="우측 가이드 설명문")
    guide_image = models.ImageField(upload_to='guides/', blank=True, null=True, verbose_name="우측 가이드 GIF/이미지")
    
    view_data = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="왼쪽 배달앱 UI 렌더링에 필요한 더미 데이터를 저장합니다.",
        verbose_name="화면 구성 데이터"
    )

    class Meta:
        # 하나의 미션 안에서 단계 번호는 중복될 수 없음
        unique_together = ('mission', 'step_number')
        ordering = ['step_number']

    def __str__(self):
        return f"{self.mission.title} - Step {self.step_number}"