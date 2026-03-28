"""
Основное, что я хочу сделать это с конвертировать айл в json и удалить основу
"""
import os
import json
import pandas as pd
from pathlib import Path

json_dir = "../json_files"
os.makedirs(json_dir, exist_ok= True)

class FileProcessor:
    async def convert_to_json(self, file_path: str) -> str:
        ext = Path(file_path).suffix.lower()
        try:
            if ext in [".xlsx", ".xls"]:
                data = self.read_excel(file_path)
            elif ext == ".csv":
                data = self.read_csv(file_path)
            elif ext == ".xml":
                data = self.read_xml(file_path)
            else:
                raise ValueError(f"не тот формат: {ext}")
            filename = Path(file_path).stem + ".json"
            json_path = os.path.join(json_dir, filename)
            with open(json_path, 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.remove(file_path)
            return json_path
        except Exception as e:
            json_path = file_path.replace(ext, ".json")
            if os.path.exists(json_path):
                os.remove(json_path)
            raise Exception(str(e))
    
    def read_excel(self, file_path: str):
        """Чтение Excel файла"""
        df = pd.read_excel(file_path, engine="openpyxl")
        return df.to_dict('records')
    
    def read_csv(self, file_path: str):
        for encoding in ['utf-8', 'cp1251', 'latin1']:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                return df.to_dict('records')
            except UnicodeDecodeError:
                continue
        raise ValueError("не получается прочитать cvs файл")
    
    def read_xml(self, file_path: str):
        df = pd.read_xml(file_path)
        return df.to_dict('records')
    def delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False