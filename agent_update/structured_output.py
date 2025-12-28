from pydantic import BaseModel,Field

class FileInfo(BaseModel):
    """
    文件信息模型
    
    Attributes:
        type: 文件类型，如：python文件、文本文件、配置文件等
        methods: 文件中定义的方法/函数名称列表，用逗号分隔
        nums: 文件中方法/函数的数量
    """
    type: str = Field(description="文件类型，如：python文件、文本文件、配置文件等")
    methods: str = Field(description="文件中定义的方法/函数名称列表，用逗号分隔")
    nums: int =Field(description="文件中方法/函数的数量")

