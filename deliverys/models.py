from django.db import models

# Create your models here.
class Mission(models.Model):
    """
    하나의 전체 미션 세션을 관리하는 모델 (예: '떡볶이 주문 미션')
    """
    title = models.CharField(max_length=100, verbose_name="미션 제목")
    description = models.TextField(verbose_name="미션 설명")
    step_guide = models.JSONField(
        default=list, 
        blank=True,
        help_text="각 단계별 가이드 GIF를 저장합니다.",
        verbose_name="단계별 GIF 경로 리스트"
    )
    answer_data = models.JSONField(
        default=dict, 
        blank=True, 
        help_text="각 단계별 정답 데이터를 JSON 형식으로 저장합니다.",
        verbose_name="정답 데이터 세트"
    )

    def __str__(self):
        return self.title