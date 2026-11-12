/* Check of [H, Eq (12.15)] (eq:charpy, log R + 1.312 <= G(R) <= log R + 1.354).
 * Build: gcc -O2 -o eq_12_15 eq_12_15.c -lm && ./eq_12_15
 *
 * Claim: the proof says (12.12) gives (12.15) for R >= 4*10^7 and that
 * 120 <= R <= 4*10^7 is checked numerically.  But with d = 1, (12.12) gives
 * G(R) >= log R + c_E - 7.284 R^(-1/3) >= log R + 1.312 only for
 * R >= (7.284/(c_E - 1.312))^3 = 4.43*10^7, so [4*10^7, 4.43*10^7) is covered
 * by neither step.  The inequality itself is true there (margin ~0.02).
 *
 * Book inputs:
 *   l2normls.tex:358-367  (12.12), d = 1, f_1(1) = 1, constant 7.284;
 *   l2normls.tex:369-371  c_E = 1.3325822...;
 *   l2normls.tex:374-381  (12.15) and the sentence on its proof (R >= 4*10^7
 *                         by (12.12); 120 <= R <= 4*10^7 numerically).
 *   G(R) = sum_{r<=R} mu^2(r)/phi(r) (l2normls.tex:331).
 * Method: thresholds from (12.12); then a sieve of G(n) in long double for
 * n <= 4.45*10^7 (G is constant on [n, n+1), so the lower bound needs
 * G(n) >= log(n+1) + 1.312 and the upper bound G(n) <= log n + 1.354).
 * Confirms if the lower-bound threshold exceeds 4*10^7, (12.12) at R = 4*10^7
 * gives less than 1.312, and (12.15) holds on [4*10^7, 4.45*10^7].
 *
 * Ported from a 2026-11-06 check script.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define N 44500000
int main(void) {
    const double cE = 1.3325822;
    double thr_lo = pow(7.284 / (cE - 1.312), 3), thr_hi = pow(7.284 / (1.354 - cE), 3);
    double at4e7 = cE - 7.284 * pow(4e7, -1.0 / 3);
    printf("(12.12) gives the lower bound of (12.15) only for R >= %.6e\n", thr_lo);
    printf("(12.12) gives the upper bound of (12.15) for R >= %.6e\n", thr_hi);
    printf("(12.12) at R = 4e7: G(R) >= log R + %.6f\n", at4e7);
    unsigned *phi = malloc((N + 1) * sizeof *phi);
    unsigned char *sq = malloc(N + 1);
    for (long i = 0; i <= N; i++) { phi[i] = i; sq[i] = 1; }
    for (long p = 2; p <= N; p++) if (phi[p] == p) {
        for (long k = p; k <= N; k += p) phi[k] -= phi[k] / p;
        if (p <= N / p) for (long k = p * p; k <= N; k += p * p) sq[k] = 0;
    }
    long double G = 0;
    double minlo = 1e9, mingap = 1e9, maxhi = -1e9, maxgap = -1e9; long nlo = 0, nhi = 0;
    for (long n = 1; n <= N; n++) {
        if (sq[n]) G += 1.0L / phi[n];
        double lo = (double)(G - logl((long double)n + 1)), hi = (double)(G - logl((long double)n));
        if (n >= 182 && lo < minlo) { minlo = lo; nlo = n; }
        if (n >= 120 && hi > maxhi) { maxhi = hi; nhi = n; }
        if (n >= 40000000) { if (lo < mingap) mingap = lo; if (hi > maxgap) maxgap = hi; }
    }
    printf("min_{182<=n<=%d} G(n) - log(n+1) = %.6f at n = %ld\n", N, minlo, nlo);
    printf("max_{120<=n<=%d} G(n) - log n   = %.6f at n = %ld\n", N, maxhi, nhi);
    printf("on [4e7, %d]: min G(n)-log(n+1) = %.6f, max G(n)-log n = %.6f\n", N, mingap, maxgap);
    if (thr_lo > 4e7 && at4e7 < 1.312 && mingap >= 1.312 && maxgap <= 1.354)
        printf("CONFIRMED: (12.12) gives the lower bound of (12.15) only for R >= %.4e, so [4e7, %.4e) is covered by neither step of the proof, though (12.15) holds there (min G(R) - log R = %.4f).\n", thr_lo, thr_lo, mingap);
    else
        printf("NOT CONFIRMED: the threshold or the sieve values do not match the claim.\n");
    return 0;
}
