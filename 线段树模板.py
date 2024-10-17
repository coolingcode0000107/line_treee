class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)  # 线段树数组
        self.lazy = [0] * (4 * self.n)  # 懒惰标记数组
        self.build(0, 0, self.n - 1, data)

    def build(self, node, start, end, data):
        # 构建线段树
        if start == end:
            # 叶子节点
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2
            # 递归构建左右子树
            self.build(left_child, start, mid, data)
            self.build(right_child, mid + 1, end, data)
            # 当前节点的值是左右子节点的和
            self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def update_range(self, node, start, end, L, R, value):
        # 更新区间 [L, R]，增加 value
        if self.lazy[node] != 0:
            # 如果当前节点有懒标记，需要先处理
            self.tree[node] += (end - start + 1) * self.lazy[node]  # 处理当前区间
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]  # 标记左子树
                self.lazy[2 * node + 2] += self.lazy[node]  # 标记右子树
            self.lazy[node] = 0  # 清除当前节点的懒标记

        # 没有交集，直接返回
        if start > end or start > R or end < L:
            return

        # 完全覆盖当前区间
        if start >= L and end <= R:
            self.tree[node] += (end - start + 1) * value
            if start != end:
                self.lazy[2 * node + 1] += value
                self.lazy[2 * node + 2] += value
            return

        # 部分覆盖，递归更新左右子树
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        self.update_range(left_child, start, mid, L, R, value)
        self.update_range(right_child, mid + 1, end, L, R, value)
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query_range(self, node, start, end, L, R):
        # 查询区间 [L, R] 的和
        if self.lazy[node] != 0:
            # 如果当前节点有懒标记，需要先处理
            self.tree[node] += (end - start + 1) * self.lazy[node]
            if start != end:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0

        # 没有交集，返回0
        if start > end or start > R or end < L:
            return 0

        # 完全覆盖当前区间
        if start >= L and end <= R:
            return self.tree[node]

        # 部分覆盖，查询左右子树
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        left_sum = self.query_range(left_child, start, mid, L, R)
        right_sum = self.query_range(right_child, mid + 1, end, L, R)
        return left_sum + right_sum

    # 封装的方便调用接口
    def update(self, L, R, value):
        # 更新区间 [L, R]
        self.update_range(0, 0, self.n - 1, L, R, value)

    def query(self, L, R):
        # 查询区间 [L, R] 的和
        return self.query_range(0, 0, self.n - 1, L, R)
