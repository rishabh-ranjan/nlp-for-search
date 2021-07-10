### ANCE ###
# original:
# https://github.com/castorini/pyserini/blob/master/pyserini/dsearch/_model.py

import torch
from transformers import PreTrainedModel, RobertaConfig, RobertaModel

class AnceEncoder(PreTrainedModel):
    config_class = RobertaConfig
    base_model_prefix = 'ance_encoder'
    _keys_to_ignore_on_load_missing = [r'position_ids']
    _keys_to_ignore_on_load_unexpected = [r'pooler', r'classifier']

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.roberta = RobertaModel(config)
        self.embeddingHead = torch.nn.Linear(config.hidden_size, 768)
        self.norm = torch.nn.LayerNorm(768)

    def forward(self, input_ids, attention_mask):
        outputs = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = outputs.last_hidden_state
        pooled_output = sequence_output[:,0,:]
        pooled_output = self.norm(self.embeddingHead(pooled_output))
        return pooled_output

############

from transformers import AutoTokenizer, AutoModel

class Embedder:
    def __init__(self, model_path):
        self.ance = 'ance' in model_path
        if self.ance:
            self.model = AnceEncoder.from_pretrained(model_path)
        else:
            self.model = AutoModel.from_pretrained(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

    def __call__(self, inp):
        tok = self.tokenizer(inp, padding=True, return_tensors='pt')
        input_ids = tok.input_ids
        attention_mask = tok.attention_mask
        if self.ance:
            ret = self.model(input_ids=input_ids, attention_mask=attention_mask)
            return ret.tolist()
        else:
            ret = self.model(input_ids=input_ids, attention_mask=attention_mask, output_hidden_states=True)
            ret = torch.sum((ret.hidden_states[-2] * attention_mask[:,:,None]), dim=-2)/torch.sum(attention_mask, dim=-1)[:,None]
            return ret.tolist()
