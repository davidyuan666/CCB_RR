from abc import ABC

import torch
import torch.nn as nn
from attention.sublayers import MultiHeadAttention, PositionalWiseFeedForward


class EncoderLayer(nn.Module, ABC):
    """
    Encoder layer composed with a multi-heads attention layer
    and a position-wise feed forward network.
    """

    def __init__(self, d_model, d_ffn, n_heads, d_k, d_v, dropout=0.1):
        super(EncoderLayer, self).__init__()
        self.slf_attn = MultiHeadAttention(n_heads, d_model, d_k, d_v, dropout=dropout)
        self.pos_ffn = PositionalWiseFeedForward(d_model, d_ffn, dropout=dropout)
        self.layer_norm = nn.LayerNorm(d_model, eps=1e-6)

    def forward(self, enc_input, padding_mask=None):
        
        residual1 = enc_input
        enc_input = self.layer_norm(enc_input)

        enc_output = self.slf_attn(enc_input, enc_input, enc_input, padding_mask=padding_mask)
        
        # residual connection
        enc_output = residual1 + enc_output
        
        residual2 = enc_output
        enc_input = self.layer_norm(enc_output)
        enc_output = self.pos_ffn(enc_input)
        
        # residual connection
        enc_output = residual2 + enc_output

        return enc_output


# if __name__ == "__main__":
#     inputs = torch.randint(0, 10, (16, 20, 64)).float()
#     enc = EncoderLayer(64, 2048, 8, 8, 8)
#     outputs = enc(inputs)
#     print(outputs.size())





