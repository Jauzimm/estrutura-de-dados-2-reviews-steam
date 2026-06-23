"""Exceções customizadas para o pipeline de processamento de reviews."""


class PipelineError(Exception):
    """Base para erros do pipeline."""
    pass


class DataProcessingError(PipelineError):
    """Erro relacionado ao processamento/limpeza do dataset."""
    pass


class NLPProcessingError(PipelineError):
    """Erro relacionado ao processamento NLP (spaCy)."""
    pass


class GraphError(PipelineError):
    """Erro relacionado à construção do grafo ou PageRank."""
    pass


class SelectionError(PipelineError):
    """Erro na seleção de reviews ou na exportação dos resultados."""
    pass


class HeapError(PipelineError):
    """Erro relacionado à MaxHeap."""
    pass
