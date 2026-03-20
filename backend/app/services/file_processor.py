from fastapi import UploadFile, HTTPException
import os
import uuid
import shutil

class FileProcessor:
    file_extension = {".xlsx", ".xml", ".xls"}
    def vavalidate_file(self, file: UploadFile):
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in self.file_extension:
            raise HTTPException(status_code = 400, detail="Не подходящий формат")
    async def process_upload(self, file: UploadFile):
        self.validate_file(file)
        task_id = str(uuid.uuid4()) # создание id и сохраненние его
        file_path = await self._save_file(file, task_id)
        await self.send_to_broker(task_id, file_path)
        return task_id
