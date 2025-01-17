import torch
import numpy as np
from torch.utils.data import Dataset
from data_preprocessing import DataPreprocessing

class MyDataset(Dataset):
    def __init__(self,dataset_path = "dataset/train_preprocessed.txt",T=280):
        self.dataPreprocessor = DataPreprocessing()
        self.data = self.dataPreprocessor.load_text(dataset_path)
        self.T = T

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):

        sentence = self.data[idx]
        # extract the label
        labels,sentence= self.dataPreprocessor.extract_diacritics_with_previous_letter('s'+sentence)

        # check sentence length
        if len(sentence) > self.T:
            sentence = sentence[:self.T]
            labels = labels[:self.T]
        else:
            for i in range(self.T - len(sentence)):
                sentence += '0'
                labels.append('0')
        
        assert len(sentence) == self.T
        assert len(labels) == self.T

        # convert the sentence to one hot encoding
        sentence = self.dataPreprocessor.convert_sentence_to_vector(sentence)

        # convert the labels to one hot encoding
        labels = self.dataPreprocessor.convert_labels_to_indices(labels)

        # pad the sentence and labels if smaller than T
        temp = np.zeros((self.T, 39))
        if self.T > sentence.shape[0]:
            temp[:sentence.shape[0], :] = sentence
            sentence = temp
        else:
            sentence = sentence[:self.T, :]
        

        # reshape the labels   
        labels = labels.reshape(-1,1)

        # convert the sentence and labels to tensors
        sentence = torch.tensor(sentence, dtype=torch.float32)
        labels = torch.LongTensor(labels)

        return sentence, labels
