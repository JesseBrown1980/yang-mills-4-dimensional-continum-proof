#!/usr/bin/env python3
"""Exact integer multiplicity checks for the Gaussian blocking comparison."""


def require(ok, name):
    if not ok:
        raise ValueError(name)


def emit(*fields):
    print("|".join(("YM4_VOL14",) + fields + ("json=0",)))


def triangle(b):
    counts = [0] * (2*b-1)
    for i in range(b):
        for j in range(b):
            counts[i+j] += 1
    return counts


def main():
    emit("straight_S_ge=b/4", "scope=GAUSSIAN")
    emit("averaged_S_le=(2b^2+1)^2/(9b^4)", "scope=GAUSSIAN")
    for b in (1,3,9,27,81):
        c = triangle(b)
        sq = sum(x*x for x in c)
        require(sum(c) == b*b and max(c) == b, "multiplicity")
        require(3*sq == b*(2*b*b+1), "triangle_square")
        num = (2*b*b+1)*(2*b*b+1)
        den = 9*b*b*b*b
        require(b*b*sq*sq*den == num*b*b*b*b*b*b*b*b, "norm_formula")
        require(num <= den, "uniform_upper")
        if b >= 3:
            require(4*num < b*den, "strict_gaussian_separation")
        emit("b="+str(b), "sum_triangle_sq="+str(sq),
             "upper_num="+str(num), "upper_den="+str(den))
    for b in range(3,244):
        num = (2*b*b+1)*(2*b*b+1)
        den = 9*b*b*b*b
        require(4*num < b*den, "separation_range")
        require(b*b > 1, "unsmeared_surface_not_uniform")
    emit("negative_control=unsmeared_perimeter", "separation_at_b_ge3=YES")
    emit("nonlinear_R_G=OPEN", "physical_mass_gap=OPEN")


if __name__ == "__main__":
    main()
