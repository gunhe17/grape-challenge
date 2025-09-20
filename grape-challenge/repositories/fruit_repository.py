from typing import Optional, List, Dict, Any
from ..database.database_json import json_db

class FruitRepository:
    def __init__(self):
        self.table_name = "fruits"
    
    def create_fruit(self, template_id: int, status: str = '씨앗') -> Dict[str, Any]:
        fruit_data = {
            "template_id": template_id,
            "status": status
        }
        return json_db.insert(self.table_name, fruit_data)
    
    def get_by_id(self, fruit_id: int) -> Optional[Dict[str, Any]]:
        return json_db.find_one(self.table_name, id=fruit_id)
    
    def update_status(self, fruit_id: int, status: str) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, fruit_id, {"status": status})
    
    def get_fruits_by_template(self, template_id: int) -> List[Dict[str, Any]]:
        return json_db.find(self.table_name, template_id=template_id)
    
    def get_all_fruits(self) -> List[Dict[str, Any]]:
        return json_db.get_table(self.table_name)
    
    def update(self, fruit_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, fruit_id, kwargs)
    
    def delete(self, fruit_id: int) -> bool:
        return json_db.delete(self.table_name, fruit_id)

class FruitTemplateRepository:
    def __init__(self):
        self.table_name = "fruit_templates"
    
    def create_template(self, name: str, type: str = 'normal', **images) -> Dict[str, Any]:
        template_data = {
            "name": name,
            "type": type,
            **images
        }
        return json_db.insert(self.table_name, template_data)
    
    def get_by_id(self, template_id: int) -> Optional[Dict[str, Any]]:
        return json_db.find_one(self.table_name, id=template_id)
    
    def get_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        return json_db.find_one(self.table_name, name=name)
    
    def get_by_type(self, type: str) -> List[Dict[str, Any]]:
        return json_db.find(self.table_name, type=type)
    
    def get_all_templates(self) -> List[Dict[str, Any]]:
        return json_db.get_table(self.table_name)
    
    def update_template(self, template_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        return json_db.update(self.table_name, template_id, kwargs)
    
    def delete(self, template_id: int) -> bool:
        return json_db.delete(self.table_name, template_id)