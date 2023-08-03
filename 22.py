import hashlib

class Node:
    def __init__(self, value):
        self.value = value
        self.branches = {}
    
    def get_hash(self):
        return hashlib.sha256(self.value.encode()).hexdigest()


class MerklePatriciaTree:
    def __init__(self):
        self.root = None
    
    def insert(self, key, value):
        if not self.root:
            self.root = Node('')
        
        node = self.root
        for i in range(len(key)):
            if key[i] not in node.branches:
                node.branches[key[i]] = Node('')
            
            node = node.branches[key[i]]
        
        node.value = value
    
    def get(self, key):
        node = self.root
        for i in range(len(key)):
            if key[i] not in node.branches:
                return None
            
            node = node.branches[key[i]]
        
        return node.value
    
    def get_root_hash(self):
        return self.root.get_hash() if self.root else None


# 测试示例
tree = MerklePatriciaTree()
tree.insert('key1', 'value1')
tree.insert('key2', 'value2')
tree.insert('key3', 'value3')

print(tree.get('key1'))
print(tree.get('key2'))
print(tree.get('key3'))

print(tree.get_root_hash())
