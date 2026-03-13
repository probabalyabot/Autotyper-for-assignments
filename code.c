#include <stdio.h>
#include <string.h>

#define MAX 20

int n, minPenalty;
int profit[MAX], deadline[MAX], exec_time[MAX];
int totalProfit;

int feasible(int mask) {
    int sumTime = 0, maxDead = 0;
    for (int i = 0; i < n; i++) {
        if (mask & (1 << i)) {
            sumTime += exec_time[i];
            if (deadline[i] > maxDead) maxDead = deadline[i];
        }
    }
    return sumTime <= maxDead;
}


void bnb(int idx, int mask, int penalty) {
    // Prune: current penalty already >= best known
    if (penalty >= minPenalty) return;

    
    if (idx == n) {
        if (feasible(mask)) {
            // penalty = sum of profits of excluded jobs
            if (penalty < minPenalty) minPenalty = penalty;
        }
        return;
    }

    
    bnb(idx + 1, mask | (1 << idx), penalty);

    
    bnb(idx + 1, mask, penalty + profit[idx]);
}

int main() {
    scanf("%d", &n);
    totalProfit = 0;
    for (int i = 0; i < n; i++) {
        scanf("%d %d %d", &profit[i], &deadline[i], &exec_time[i]);
        totalProfit += profit[i];
    }

    minPenalty = totalProfit; // worst case: miss all jobs
    bnb(0, 0, 0);

    printf("Minimum Total Penalty: %d\n", minPenalty);
    printf("Maximum Total Profit: %d\n", totalProfit - minPenalty);
    return 0;
}
