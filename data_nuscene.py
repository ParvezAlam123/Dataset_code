import os
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader

class NuScenesDataset(Dataset):
    def __init__(self, data_root, split, transform=None):
        self.data_root = data_root
        self.split = split
        self.transform = transform
        
        # Get the paths to the files for the selected split
        self.sample_data_path = os.path.join(data_root, 'samples', self.split)
        self.sample_annotation_path = os.path.join(data_root, 'sample_annotations', self.split)
        self.scene_path = os.path.join(data_root, 'scenes', self.split)
        self.category_path = os.path.join(data_root, 'category.json')
        
        # Load the category information
        self.category = self.load_json(self.category_path)
        self.category2id = {c['name']: c['token'] for c in self.category}
        
        # Get a list of all the sample data and annotations
        self.sample_data = self.get_all_files(self.sample_data_path)
        self.sample_annotation = self.get_all_files(self.sample_annotation_path)
        
    def __len__(self):
        return len(self.sample_data)
    
    def __getitem__(self, idx):
        # Get the sample data
        sample_data_token = self.sample_data[idx]
        sample_data = self.load_json(sample_data_token)
        
        # Get the corresponding sample annotation
        sample_annotation_token = os.path.join(self.sample_annotation_path, sample_data['anns'][0])
        sample_annotation = self.load_json(sample_annotation_token)
        
        # Load the image data
        image_path = os.path.join(self.data_root, 'samples', self.split, sample_data['filename'])
        image = self.load_image(image_path)
        
        # Load the point cloud data
        point_cloud_path = os.path.join(self.data_root, 'lidar', self.split, sample_data['lidar_path'])
        point_cloud = self.load_point_cloud(point_cloud_path)
        
        # Get the category ID for the object
        category_id = self.category2id[sample_annotation['category_name']]
        
        # Get the bounding box for the object
        bbox = sample_annotation['bbox']
        
        # Apply any transforms
        if self.transform:
            image, point_cloud, bbox = self.transform(image, point_cloud, bbox)
        
        # Convert data to PyTorch tensors
        image = torch.from_numpy(image).float()
        point_cloud = torch.from_numpy(point_cloud).float()
        category_id = torch.tensor(category_id).long()
        bbox = torch.from_numpy(bbox).float()
        
        return image, point_cloud, category_id, bbox
    
    def get_all_files(self, path):
        """Get a list of all files in a directory."""
        return [os.path.join(path, f) for f in os.listdir(path)]
    
    def load_json(self, path):
        """Load JSON data from a file."""
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    
    def load_image(self, path):
        """Load an image file as a numpy array."""
        image = Image.open(path)
        image = np.array(image)
        return image
    
    def load_point_cloud(self, path):
        """Load a point cloud file as a numpy array."""
        point_cloud = np.fromfile(path, dtype=np.float32).reshape(-1, 5)
        return point_cloud

