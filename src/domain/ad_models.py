from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class AdSummary(BaseModel):
    total_spend: float = Field(..., ge=0, description="总花费")
    total_sales: float = Field(..., ge=0, description="总销售额")
    total_impressions: int = Field(..., ge=0, description="总展示次数")
    total_clicks: int = Field(..., ge=0, description="总点击次数")
    average_acos: float = Field(..., ge=0, le=100, description="平均ACOS(%)")
    average_roas: float = Field(..., ge=0, description="平均ROAS")
    average_ctr: float = Field(..., ge=0, le=100, description="平均CTR(%)")
    average_cpc: float = Field(..., ge=0, description="平均CPC")
    campaign_count: int = Field(..., ge=0, description="广告活动数量")
    active_keywords: int = Field(..., ge=0, description="活跃关键词数量")
    period_start: datetime = Field(..., description="统计开始时间")
    period_end: datetime = Field(..., description="统计结束时间")
    
    @property
    def conversion_rate(self) -> float:
        if self.total_clicks == 0:
            return 0.0
        return (self.total_sales / self.total_clicks) * 100


class KeywordRanking(BaseModel):
    keyword: str = Field(..., min_length=1, description="关键词")
    rank: int = Field(..., ge=1, description="排名")
    impressions: int = Field(..., ge=0, description="展示次数")
    clicks: int = Field(..., ge=0, description="点击次数")
    ctr: float = Field(..., ge=0, le=100, description="点击率(%)")
    spend: float = Field(..., ge=0, description="花费")
    sales: float = Field(..., ge=0, description="销售额")
    acos: float = Field(..., ge=0, le=100, description="ACOS(%)")
    match_type: str = Field(..., description="匹配类型: exact, phrase, broad")
    campaign_name: str = Field(..., description="所属广告活动")
    updated_at: datetime = Field(default_factory=datetime.now, description="更新时间")


class Recommendation(BaseModel):
    recommendation_id: str = Field(..., description="建议ID")
    title: str = Field(..., min_length=5, max_length=100, description="建议标题")
    description: str = Field(..., min_length=10, max_length=500, description="建议描述")
    priority: str = Field(..., description="优先级: high, medium, low")
    category: str = Field(..., description="分类: bid, keyword, budget, targeting")
    expected_impact: str = Field(..., description="预期影响描述")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")
    action: Optional[str] = Field(default=None, description="建议操作")
    affected_entities: List[str] = Field(default_factory=list, description="受影响的实体")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    metadata: dict = Field(default_factory=dict, description="元数据")


class SearchTermAnalysis(BaseModel):
    search_term: str = Field(..., min_length=1, description="搜索词")
    impressions: int = Field(..., ge=0, description="展示次数")
    clicks: int = Field(..., ge=0, description="点击次数")
    conversions: int = Field(..., ge=0, description="转化次数")
    spend: float = Field(..., ge=0, description="花费")
    sales: float = Field(..., ge=0, description="销售额")
    is_targeted: bool = Field(..., description="是否已作为关键词")
    suggested_keyword: Optional[str] = Field(default=None, description="建议添加为关键词")
    match_type_suggestion: Optional[str] = Field(default=None, description="建议匹配类型")
