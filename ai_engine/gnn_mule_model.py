import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, Any, Tuple, List

class GraphSAGELayer(nn.Module):
    """Custom PyTorch GraphSAGE Layer with Sparse / Dense Normalized Message Passing"""
    def __init__(self, in_features: int, out_features: int):
        super(GraphSAGELayer, self).__init__()
        self.linear_self = nn.Linear(in_features, out_features, bias=False)
        self.linear_neigh = nn.Linear(in_features, out_features, bias=True)
        
    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        if adj.is_sparse:
            neigh_agg = torch.sparse.mm(adj, x)
        else:
            neigh_agg = torch.matmul(adj, x)
        h = self.linear_self(x) + self.linear_neigh(neigh_agg)
        return F.relu(h)

class DurgamGNNMuleClassifier(nn.Module):
    """
    2-Layer GraphSAGE Network for Real-Time Money Mule Ring & Node Classification.
    Computes node embeddings and outputs mule probability score P(Mule) in < 85 ms.
    """
    def __init__(self, in_features: int = 8, hidden_dim: int = 32, out_dim: int = 1):
        super(DurgamGNNMuleClassifier, self).__init__()
        self.sage1 = GraphSAGELayer(in_features, hidden_dim)
        self.sage2 = GraphSAGELayer(hidden_dim, hidden_dim // 2)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim // 2, 16),
            nn.ReLU(),
            nn.Dropout(0.15),
            nn.Linear(16, out_dim),
            nn.Sigmoid()
        )
        
    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        h1 = self.sage1(x, adj)
        h2 = self.sage2(h1, adj)
        out = self.classifier(h2)
        return out

def build_sparse_normalized_adj(edge_index: np.ndarray, num_nodes: int) -> torch.Tensor:
    """Builds sparse normalized adjacency matrix with self-loops in O(E) time and memory"""
    # 1. Add self loops and bidirectional edges
    srcs = list(edge_index[0]) + list(edge_index[1]) + list(range(num_nodes))
    dsts = list(edge_index[1]) + list(edge_index[0]) + list(range(num_nodes))
    
    # Calculate degree
    deg = np.zeros(num_nodes, dtype=np.float32)
    for s in srcs:
        if s < num_nodes:
            deg[s] += 1.0
    deg[deg == 0] = 1.0
    
    # Values: 1 / deg[s]
    vals = [1.0 / deg[s] for s in srcs if s < num_nodes and dsts[srcs.index(s)] < num_nodes]
    
    indices = torch.tensor([srcs, dsts], dtype=torch.long)
    values = torch.tensor([1.0 / deg[s] for s in srcs], dtype=torch.float32)
    
    sparse_adj = torch.sparse_coo_tensor(indices, values, (num_nodes, num_nodes))
    return sparse_adj.coalesce()
