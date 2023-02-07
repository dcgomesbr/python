from typing import List


class Node:
    def __init__(self, data, parent=None):
        self.children = []
        self.data = data
        self.parent = parent

        if self.parent:
            self.parent.children.append(self)


class Solution:
    def __init__(self):
        self.solutions = []
        self.root = Node('root')

    def octBuilder(self, sl: list, oct_left: int, parent: Node):
        for i in range(3):
            if i + 1 > len(sl):
                continue

            datastr = ''.join(sl[0:i + 1])
            dataintgr = int(datastr)

            # too big
            if dataintgr > 255:
                continue

            # this should drop leading zeroes
            if len(datastr) != len(str(dataintgr)):
                continue

            min_pos_fill = oct_left # at least 1 in each remaining octet
            if len(sl) - (i + 1) < min_pos_fill:
                continue # can't allocate more chars

            # can't have leftovers
            min_pos_size = 1 if oct_left == 0 else (len(sl) - (i + 1)) / oct_left
            if min_pos_size > 3.0:
                continue

            node = Node(dataintgr, parent)

            nextsl = sl[i+1::]
            if oct_left - 1 >= 0:
                if len(nextsl) > 0:
                    self.octBuilder(nextsl, oct_left - 1, node)
            elif oct_left == 0 and len(nextsl) == 0:
                self.solutions.append(str(node.parent.parent.parent.data) + '.' +
                                      str(node.parent.parent.data) + '.' +
                                      str(node.parent.data) + '.' +
                                      str(node.data))

    def restoreIpAddresses(self, s: str) -> List[str]:
        self.octBuilder(list(s), 3, self.root)

        return self.solutions


print(Solution().restoreIpAddresses("101023"))

print(Solution().restoreIpAddresses("25525511135"))

print(Solution().restoreIpAddresses("0000"))

