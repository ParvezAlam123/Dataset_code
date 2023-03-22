import json 


class Nuscene():
   def __init__(self):
   
      self.table_names = ['category', 'attribute', 'visibility', 'instance', 'sensor', 'calibrated_sensor', 'ego_pose', 'log', 'scene', 'sample', 'sample_data', 'sample_annotation', 'map']
      
      
      self.category = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/category.json")
      self.attribute = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/attribute.json")
      self.visibility = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/visibility.json")
      self.instance = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/instance.json")
      self.sensor = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/sensor.json")
      self.calibrated_sensor = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/calibrated_sensor.json")
      self.ego_pose = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/ego_pose.json")
      self.log = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/log.json")
      self.scene = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/scene.json")
      self.sample = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/sample.json")
      self.sample_data = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/sample_data.json")
      self.sample_annotation = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/sample_annotation.json")
      self.map = self.load_table("/media/parvez_alam/Expansion/Nuscene_Asia/Train/Metadata/v1.0-trainval_meta/v1.0-trainval/map.json")
      
      
      self.token2ind = self.token2ind() 
      self.sample_decorate()
      
      
      
      
      
      
   def load_table(self, path):
      f = open(path, 'r')
      file_read = f.read()
      file_load = json.loads(file_read)
      
      return file_load 
   
      
   def get(self, table_name, token):
      
      if table_name == 'category':
         return self.category[self.token2ind['category'][token]] 
         
      if table_name == 'attribute' :
         return self.attribute[self.token2ind['attribute'][token]]
         
      if table_name == 'visibility':
         return self.visibility[self.token2ind['visibility'][token]] 
         
      if table_name == 'instance':
         return self.instance[self.token2ind['instance'][token]]
         
      if table_name == 'sensor':
         return self.sensor[self.token2ind['sensor'][token]] 
         
      if table_name == 'calibrated_sensor' :
         return self.calibrated_sensor[self.token2ind['calibrated_sensor'][token]] 
         
      if table_name == 'ego_pose' :
         return self.ego_pose[self.token2ind['ego_pose'][token]] 
         
      if table_name == 'log':
         return self.log[self.token2ind['log'][token]] 
         
      if table_name == 'scene' :
         return self.scene[self.token2ind['scene'][token]] 
         
      if table_name == 'sample' :
         return self.sample[self.token2ind['sample'][token]] 
         
      if table_name == 'sample_annotation' :
         return self.sample_annotation[self.token2ind['sample_annotation'][token]] 
         
      if table_name == 'map' :
         return self.map[self.token2ind['map'][token]] 
         
      if table_name == 'sample_data' :
         return self.sample_data[self.token2ind['sample_data'][token]] 
         
         
   
   def sample_decorate(self):
      
      # Decorate (add short-cut) sample annnotation table with for category_name 
      for record in self.sample_annotation:
         inst = self.get('instance', record['instance_token'])
         record['category_name'] = self.get('category', inst['category_token'])['name']
      
      # Decorates (adds short-cut) sample_data with sensor information. 
      for record in self.sample_data:
         cs_record = self.get('calibrated_sensor', record['calibrated_sensor_token'])
         sensor_record = self.get('sensor', cs_record['sensor_token'])
         record['sensor_modality'] = sensor_record['modality']
         record['channel'] = sensor_record['channel'] 
         
         
      # Reverse-Index samples with sample_data and annotations.
      for record in self.sample:
         record['data'] = {}
         record['anns'] = [] 
         
      for record in self.sample_data:
         if record['is_key_frame']:
            sample_record = self.get('sample', record['sample_token']) 
            sample_record['data'][record['channel']] = record['token']
            
      for ann_record in self.sample_annotation:
         sample_record = self.get('sample', ann_record['sample_token'])
         sample_record['anns'].append(ann_record['token'])
         
         
         
         
         
    
    
       
          
   
   def token2ind(self):
      token2ind = {}
      for table in self.table_names:
         token2ind[table] = {} 
         
      for i in range(len(self.category)):
         token2ind['category'][self.category[i]['token']] = i 
         
      for i in range(len(self.attribute)):
         token2ind['attribute'][self.attribute[i]['token']] = i 
         
      for i in range(len(self.visibility)):
         token2ind['visibility'][self.visibility[i]['token']] = i
         
      for i in range(len(self.instance)):
         token2ind['instance'][self.instance[i]['token']] = i 
         
      for i in range(len(self.sensor)):
         token2ind['sensor'][self.sensor[i]['token']] = i 
         
      for i in range(len(self.calibrated_sensor)):
         token2ind['calibrated_sensor'][self.calibrated_sensor[i]['token']] = i 
         
      for i in range(len(self.ego_pose)):
         token2ind['ego_pose'][self.ego_pose[i]['token']] = i 
         
      for i in range(len(self.log)):
         token2ind['log'][self.log[i]['token']] = i 
         
      for i in range(len(self.scene)):
         token2ind['scene'][self.scene[i]['token']] = i 
         
      for i in range(len(self.sample)):
         token2ind['sample'][self.sample[i]['token']] = i 
         
      for i in range(len(self.sample_data)):
         token2ind['sample_data'][self.sample_data[i]['token']] = i 
         
      for i in range(len(self.sample_annotation)):
         token2ind['sample_annotation'][self.sample_annotation[i]['token']] = i 
         
      for i in range(len(self.map)):
         token2ind['map'][self.map[i]['token']] = i 
         
      return token2ind 
      
      

  


obj = Nuscene() 

my_scene = obj.scene[0]
first_sample_token = my_scene['first_sample_token']

my_sample = obj.get('sample', first_sample_token) 

sensor = 'LIDAR_TOP'

token = my_sample['data'][sensor]


print(obj.get('sample_data', token))















   


