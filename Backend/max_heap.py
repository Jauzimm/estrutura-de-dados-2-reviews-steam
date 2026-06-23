from excecoes import HeapError

class MaxHeap:
    """
    Armazena itens como tuplas (score, dados) e mantém o maior score na raiz.
    """
    def __init__(self):
        self._heap = []

    def __len__(self):
        return len(self._heap)

    def is_empty(self):
        return len(self._heap) == 0

    def inserir(self, score: float, dados: dict):
        """Insere um elemento e restaura a propriedade heap (sift-up)."""
        self._heap.append((score, dados))
        self._sift_up(len(self._heap) - 1)

    def extrair_maximo(self) -> tuple[float, dict]:
        """Remove e retorna o elemento com maior score (sift-down)."""
        if self.is_empty():
            raise HeapError("A MaxHeap está vazia, não é possível extrair.")
        
        if len(self._heap) == 1:
            return self._heap.pop()

        maximo = self._heap[0]
        # Move o último elemento para a raiz e faz sift-down
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        
        return maximo

    def espiar_maximo(self) -> tuple[float, dict]:
        """Retorna o máximo sem remover."""
        if self.is_empty():
            raise HeapError("A MaxHeap está vazia.")
        return self._heap[0]

    def construir_heap(self, itens: list[tuple[float, dict]]):
        """Constrói a heap a partir de uma lista em O(N)."""
        self._heap = list(itens)
        n = len(self._heap)
        # Começa do último nó pai e faz sift-down até a raiz
        for i in range((n // 2) - 1, -1, -1):
            self._sift_down(i)

    def _sift_up(self, i: int):
        """Sobe o elemento na posição i até restaurar a propriedade."""
        pai = (i - 1) // 2
        while i > 0 and self._heap[i][0] > self._heap[pai][0]:
            # Troca com o pai
            self._heap[i], self._heap[pai] = self._heap[pai], self._heap[i]
            i = pai
            pai = (i - 1) // 2

    def _sift_down(self, i: int):
        """Desce o elemento na posição i até restaurar a propriedade."""
        n = len(self._heap)
        maior = i
        
        while True:
            esq = 2 * i + 1
            dir = 2 * i + 2
            
            # Verifica se filho esquerdo é maior que o nó atual
            if esq < n and self._heap[esq][0] > self._heap[maior][0]:
                maior = esq
                
            # Verifica se filho direito é maior que o maior atual
            if dir < n and self._heap[dir][0] > self._heap[maior][0]:
                maior = dir
                
            # Se o maior for o próprio nó atual, a propriedade foi restaurada
            if maior == i:
                break
                
            # Troca com o maior filho
            self._heap[i], self._heap[maior] = self._heap[maior], self._heap[i]
            i = maior
