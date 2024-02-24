from typing import TypedDict, List


IEdge = TypedDict('IEdge', {'source': str, 'target': str, 'weight': float})
IVertices = List[str]
