import yaml

class Config:
	"""
		配置管理类，用于加载和存储配置信息
	"""
	def __init__(self, yaml_path):
		self.yaml_path = yaml_path
		self.config = self.load_yaml()

	def load_yaml(self):
		with open(self.yaml_path, 'r', encoding='utf-8') as f:
			return yaml.safe_load(f)
