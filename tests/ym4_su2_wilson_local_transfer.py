"""YM4 exact rational SU(2) Wilson plaquette transfer: local benchmark.

Conjugation-projected one spatial-circle link, Wilson timelike plaquette,
character eigenvalues, Wilson moments, certified representation tails, and
aligned six-staple conditional Haar mean. All arithmetic uses integer pairs.
The 4D interacting Gauss-law transfer and continuum gap remain OPEN.
"""
from math import factorial, gcd


class R:
    __slots__ = ("n", "d")

    def __init__(self, n, d=1):
        if type(n) is not int or type(d) is not int or d == 0:
            raise ValueError("integer_rational_required")
        if d < 0:
            n, d = -n, -d
        g = gcd(n, d)
        self.n, self.d = n // g, d // g

    @staticmethod
    def of(x):
        if isinstance(x, R):
            return x
        if type(x) is int:
            return R(x)
        raise ValueError("noninteger_rational_operand")

    def __add__(self, x):
        x = R.of(x)
        return R(self.n * x.d + x.n * self.d, self.d * x.d)

    __radd__ = __add__

    def __neg__(self):
        return R(-self.n, self.d)

    def __sub__(self, x):
        return self + -R.of(x)

    def __rsub__(self, x):
        return R.of(x) + -self

    def __mul__(self, x):
        x = R.of(x)
        return R(self.n * x.n, self.d * x.d)

    __rmul__ = __mul__

    def div(self, x):
        x = R.of(x)
        if x.n == 0:
            raise ValueError("division_by_zero")
        return R(self.n * x.d, self.d * x.n)

    def power(self, k):
        if type(k) is not int or k < 0:
            raise ValueError("nonnegative_integer_power_required")
        # Exponent validated above: multiplication stays integer-only.
        num, den = 1, 1
        bn, bd = self.n, self.d
        while k:
            if k % 2:
                num *= bn
                den *= bd
            bn *= bn
            bd *= bd
            k //= 2
        return R(num, den)

    def __lt__(self, x):
        x = R.of(x)
        return self.n * x.d < x.n * self.d

    def __le__(self, x):
        x = R.of(x)
        return self.n * x.d <= x.n * self.d

    def __eq__(self, x):
        try:
            x = R.of(x)
        except ValueError:
            return False
        return self.n == x.n and self.d == x.d

    def __str__(self):
        return str(self.n) if self.d == 1 else str(self.n) + "/" + str(self.d)

    def __repr__(self):
        return "R(" + str(self.n) + "," + str(self.d) + ")"


def require(condition, label):
    if not condition:
        raise ValueError(label)


def bessel_j_interval(m, beta, last_k=20):
    """J_m(x)=sum_(k>=0) (x*x/4)^k / (k!*(k+m)!).

    Exact positive rational partial sum and a rigorous omitted geometric tail.
    I_m(x)=(x/2)^m*J_m(x). The functions here contain no float values.
    """
    beta = R.of(beta)
    require(beta.n > 0 and type(m) is int and m >= 1,
            "positive_beta_and_order_required")
    require(type(last_k) is int and 0 <= last_k <= 128,
            "invalid_taylor_cutoff")
    t = (beta * beta).div(4)
    term = R(1, factorial(m))
    total = term
    for k in range(1, last_k + 1):
        term = term * t.div(k * (k + m))
        total = total + term
    first_omitted = term * t.div((last_k + 1) * (last_k + 1 + m))
    next_ratio = t.div((last_k + 2) * (last_k + 2 + m))
    require(next_ratio < R(1), "uncontrolled_bessel_tail")
    upper = total + first_omitted.div(R(1) - next_ratio)
    require(total < upper, "bessel_bounds_ordering")
    return total, upper


def character_eigen_interval(r, beta, last_k=20):
    """For normalized Wilson Haar convolution: lambda_r=I_(r+1)/I_1."""
    require(type(r) is int and 0 <= r <= 128,
            "invalid_character_index")
    beta = R.of(beta)
    require(beta.n > 0, "invalid_Wilson_beta")
    if r == 0:
        return R(1), R(1)
    d0, d1 = bessel_j_interval(1, beta, last_k)
    a0, a1 = bessel_j_interval(r + 1, beta, last_k)
    factor = beta.div(2).power(r)
    lo = factor * a0.div(d1)
    hi = factor * a1.div(d0)
    require(R(0) < lo and lo < hi and hi < R(1),
            "character_spectral_interval_invalid")
    return lo, hi


def connected_wilson_interval(beta, time, last_k=20):
    """W=(1/2)Tr(U)=chi_1(U)/2, C_t=(lambda_1)^t/4."""
    require(type(time) is int and 0 <= time <= 64, "invalid_time")
    if time == 0:
        return R(1, 4), R(1, 4)
    lo, hi = character_eigen_interval(1, beta, last_k)
    return lo.power(time).div(4), hi.power(time).div(4)


def character_sup_tail(beta, retained_r):
    """Uniform norm bound on normalized kernel after characters r<=retained_r.

    |chi_r(U)| <= r+1 and (r+1)^2 lambda_r is bounded by
    A*(r+1)*(beta/2)^r/r!, where A >= exp(beta^2/4).
    For t<1 use exp(t)<=1/(1-t), otherwise exp(t)<3^ceil(t).
    The rational ratio of successive majorants decreases with r.
    """
    beta = R.of(beta)
    require(beta.n > 0 and beta <= R(4), "beta_outside_certified_range")
    require(type(retained_r) is int and 1 <= retained_r <= 128,
            "invalid_character_cutoff")
    t = (beta * beta).div(4)
    if t < R(1):
        amplitude = R(1).div(R(1) - t)
    else:
        ceil_t = (t.n + t.d - 1) // t.d
        amplitude = R(R(3).power(ceil_t).n)
    p = beta.div(2)
    k = retained_r + 1
    first = amplitude * R(k + 1, factorial(k)) * p.power(k)
    next_ratio = p * R(k + 2, (k + 1) ** 2)
    require(next_ratio < R(1), "character_tail_ratio_uncontrolled")
    return first.div(R(1) - next_ratio)


def aligned_six_staple_mean(beta_four_dim, last_k=20):
    """Condition on six aligned (+I) 4D staples.

    Local Haar density is exp(6*beta*cos(theta)); its mean normalized trace
    is d/dkappa log Z(kappa) = I_2(kappa)/I_1(kappa).
    """
    beta_four_dim = R.of(beta_four_dim)
    require(beta_four_dim.n > 0, "invalid_four_dim_beta")
    kappa = 6 * beta_four_dim
    return character_eigen_interval(1, kappa, last_k)


def check_frozen_row(beta, cutoff, six_staple_beta, ratio_range,
                     c2_range, c4_range):
    rlo, rhi = character_eigen_interval(1, R(beta), 20)
    c2lo, c2hi = connected_wilson_interval(R(beta), 2, 20)
    c4lo, c4hi = connected_wilson_interval(R(beta), 4, 20)
    require(ratio_range[0] < rlo and rhi < ratio_range[1],
            "frozen_ratio_interval_miss")
    require(c2_range[0] < c2lo and c2hi < c2_range[1],
            "frozen_C2_interval_miss")
    require(c4_range[0] < c4lo and c4hi < c4_range[1],
            "frozen_C4_interval_miss")
    require((rhi - rlo) < R(1, 10 ** 25), "insufficient_ratio_precision")
    require(character_sup_tail(R(beta), cutoff) < R(1, 10 ** 12),
            "character_sup_tail_failure")
    require(aligned_six_staple_mean(six_staple_beta) == (rlo, rhi),
            "four_dim_six_staple_beta_normalization_mismatch")
    return (
        "YM4_SU2_LOCAL_WILSON|beta=" + str(beta)
        + "|one_link_lambda1_lower=" + str(rlo)
        + "|one_link_lambda1_upper=" + str(rhi)
        + "|C0=1/4|C2_lower=" + str(c2lo)
        + "|C2_upper=" + str(c2hi)
        + "|C4_lower=" + str(c4lo)
        + "|C4_upper=" + str(c4hi)
        + "|character_cutoff=" + str(cutoff)
        + "|uniform_tail_lt_1e-12=PASS"
        + "|aligned_4D_beta=" + str(six_staple_beta)
        + "|original_full4D_transfer=OPEN|json=0"
    )


def receipt():
    million = 10 ** 6
    rows = [
        "YM4_SU2_SOURCE|action=beta_times_one_minus_halftrace"
        "|Haar_convolution=Wilson_plaquette"
        "|gauge_projection=conjugation_average"
        "|lambda_r=I_rplus1_over_I1"
        "|Wilson=chi1_over_2|json=0"
    ]
    rows.append(check_frozen_row(
        1, 12, R(1, 6),
        (R(240193, million), R(240195, million)),
        (R(14422, million), R(14425, million)),
        (R(831, million), R(834, million)),
    ))
    rows.append(check_frozen_row(
        4, 24, R(2, 3),
        (R(658046, million), R(658049, million)),
        (R(108255, million), R(108258, million)),
        (R(46876, million), R(46880, million)),
    ))
    rows.append(
        "YM4_SU2_LOCAL_VERDICT|character_coefficients=EXACT_IDENTITY"
        "|Bessel_rational_enclosures=PASS|C0_C2_C4=PASS"
        "|aligned_six_staples=PASS"
        "|Gauss_full4D=OPEN|physical_full4D_moments=OPEN"
        "|continuum_mass_gap=OPEN|json=0"
    )
    return "\n".join(rows) + "\n"


if __name__ == "__main__":
    print(receipt(), end="")
