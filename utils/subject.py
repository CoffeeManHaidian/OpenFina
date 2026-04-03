from models.bookset import SubjectStore


class SubjectLookup:
    def __init__(self, bookset_db_path):
        self.store = SubjectStore(bookset_db_path)
        self.refresh()

    def refresh(self):
        self.data = self.store.get_tree_data()
        self.cache = {}
        self._build_cache(self.data)

    def _build_cache(self, data):
        for items in data.values():
            for item in items:
                self.cache[item["code"]] = item["name"]
                for child in item.get("subjects", []):
                    self.cache[child["code"]] = child["name"]

    def get_name(self, code):
        return self.cache.get(code, f"未找到 code: {code}")

    def get_tree_data(self):
        return self.data
