class Solution(object):
    def min_distance(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: int
        """

        return self.min_distance3(word1, word2)

    @staticmethod
    def min_distance1(word1, word2):
        n = len(word1)
        m = len(word2)
        if n == 0 or m == 0:
            return max(n, m)
        dp = [[0] * (m + 1) for j in xrange(n + 1)]
        for i in xrange(1, n + 1):
            dp[i][0] = i
            if i == 1:
                for j in xrange(1, m + 1):
                    dp[0][j] = j
            for j in xrange(1, m + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = min(dp[i][j - 1] + 1, dp[i - 1][j] + 1, dp[i - 1][j - 1] + 1)
        return dp[-1][-1]

    @staticmethod
    def min_distance2(word1, word2):
        n = len(word1)
        m = len(word2)

        if n > m:
            word1, word2 = word2, word1
            n, m = m, n
        if n == 0:
            return m
        dp = [i for i in xrange(n + 1)]
        dp_ij = 0
        for j in xrange(1, m + 1):
            for i in xrange(1, n + 1):
                c = 0 if word1[i - 1] == word2[j - 1] else 1
                # dp[i] == dp[i][j-1]
                # dp[i-1] == dp[i-1][j-1]
                # d_ij == dp[i-1][j]
                dp_i_1_j_1 = dp[i - 1] + c
                dp_i_1_j = dp_ij if i > 1 else j
                # dp[i-1][j-1] for the next is dp[i-1][j]
                dp[i - 1] = dp_i_1_j

                #dp_ij = min(min(dp_i_1_j, dp_i_j1) + 1, dp_i_1_j_1 + c)
                dp_ij = dp_i_1_j + 1 if dp_i_1_j < dp[i] else dp[i] + 1
                dp_ij = dp_ij if dp_ij < dp_i_1_j_1 else dp_i_1_j_1

            dp[-1] = dp_ij

        return dp[-1]

    @staticmethod
    def min_distance3(word1, word2):
        def min_distance_idx(ia, ib):
            if ia < 0:
                return ib + 1
            elif ib < 0:
                return ia + 1

            if result[ia][ib] == -1:
                if word1[ia] == word2[ib]:
                    result[ia][ib] = min_distance_idx(ia - 1, ib - 1)
                else:
                    add_dis = min_distance_idx(ia, ib - 1)
                    del_dis = min_distance_idx(ia - 1, ib)
                    rep_dis = min_distance_idx(ia - 1, ib - 1)
                    result[ia][ib] = 1 + min(add_dis, del_dis, rep_dis)

            return result[ia][ib]

        result = [[-1] * len(word2) for _ in word1]
        return min_distance_idx(len(word1) - 1, len(word2) - 1)
