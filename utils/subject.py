import json

class SubjectLookup:
    def __init__(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.cache = {}
        self._build_cache(self.data)
    
    def _build_cache(self, data, parent_code=""):
        """递归构建 code->name 的缓存字典"""
        for key, items in data.items():
            if isinstance(items, list):
                for item in items:
                    # 如果有子科目，递归处理
                    if 'subjects' in item:
                        for sub in item['subjects']:
                            self.cache[sub['code']] = sub['name']
                    # 主科目
                    self.cache[item['code']] = item['name']
                    # 如果有子科目但已经处理过，这里就不再重复处理
    
    def get_name(self, code):
        """根据 code 获取 name"""
        return self.cache.get(code, f"未找到 code: {code}")
    
    def search_by_code(self, code):
        """另一种方式：动态搜索（如果不想构建缓存）"""
        return self._search_recursive(self.data, code)
    
    def _search_recursive(self, data, target_code):
        """递归搜索 code"""
        for key, items in data.items():
            if isinstance(items, list):
                for item in items:
                    if item['code'] == target_code:
                        return item['name']
                    if 'subjects' in item:
                        for sub in item['subjects']:
                            if sub['code'] == target_code:
                                return sub['name']
        return f"未找到 code: {target_code}"

# 使用示例
if __name__ == "__main__":
    lookup = SubjectLookup('subject.json')
    
    # 方法1：使用缓存查找（推荐，一次构建，多次查询）
    print(lookup.get_name("1001"))           # 输出: 库存现金
    print(lookup.get_name("1001.01"))        # 输出: 工商银行
    print(lookup.get_name("2221"))           # 输出: 应交税费
    print(lookup.get_name("9999"))           # 输出: 未找到 code: 9999
    
    # # 方法2：动态搜索（适合单次查询或数据量小的情况）
    # print(lookup.search_by_code("1001.02"))  # 输出: 农业银行
    # print(lookup.search_by_code("4001"))     # 输出: 实收资本