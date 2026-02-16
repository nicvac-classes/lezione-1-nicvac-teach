#include <fstream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iostream>

using namespace std;

int main() {
    int T;
    scanf("%d", &T);

    while (T--) {
        int N, K;
        scanf("%d %d", &N, &K);

        // L = mcm(2, K): serve mod 2 per il turno, mod K per la vittoria
        int L = lcm(2, K);

        // dp[n][t] = true se Alice vince con n pietre rimaste e t turni giocati (mod L)
        vector<vector<bool>> dp(N + 1, vector<bool>(L, false));

        // Caso base: 0 pietre rimaste -> Alice vince sse turni divisibili per K
        for (int t = 0; t < L; t++) {
            dp[0][t] = (t % K == 0);
        }

        // Riempimento DP
        for (int n = 1; n <= N; n++) {
            for (int t = 0; t < L; t++) {
                int t_next = (t + 1) % L;
                int max_take = min(K, n);

                if (t % 2 == 0) {
                    // Turno di Alice: basta UNA mossa che porti a vittoria
                    dp[n][t] = false;
                    for (int i = 1; i <= max_take; i++) {
                        if (dp[n - i][t_next]) {
                            dp[n][t] = true;
                            break;
                        }
                    }
                } else {
                    // Turno di Bob: Alice vince solo se TUTTE le mosse portano a vittoria
                    dp[n][t] = true;
                    for (int i = 1; i <= max_take; i++) {
                        if (!dp[n - i][t_next]) {
                            dp[n][t] = false;
                            break;
                        }
                    }
                }
            }
        }

        printf("%s\n", dp[N][0] ? "Alice" : "Bob");
    }

    return 0;
}