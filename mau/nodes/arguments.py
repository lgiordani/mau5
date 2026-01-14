# from mau.nodes.node import NodeData
# 
# 
# class UnnamedArgumentNodeData(NodeData):
#     """
#     This node contains an unnamed argument.
#     """
# 
#     type = "unnamed_argument"
# 
#     def __init__(self, value: str):
#         self.value = value
# 
#     def asdict(self):
#         base = super().asdict()
#         base["custom"] = {"value": self.value}
# 
#         return base
# 
# 
# class NamedArgumentNodeData(NodeData):
#     """
#     This node contains a named argument.
#     """
# 
#     type = "named_argument"
# 
#     def __init__(self, key: str, value: str):
#         self.key = key
#         self.value = value
# 
#     def asdict(self):
#         base = super().asdict()
#         base["custom"] = {"key": self.key, "value": self.value}
# 
#         return base
