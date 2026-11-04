#!/bin/bash
# The small form of the compiled-level check, for a repository whose only compiled code is C++. The full form, for Rust too, is compiled_float_check.py in the Yang-Mills and SU(N) repositories.
# Each tracked C or C++ file is compiled -O0 -S and its assembly read for scalar float opcodes, scalar float moves, and calls to soft-float and libm routines. Moves of __int128 use movaps and movdqa, so those two do not count.
# Scope: what g++ compiles on this runner, with its default cfg. A library's own bodies are not read, and a tracked Cargo.toml stops this form, because Rust needs the full one. Integer only, json=0.
# usage: no_float_compiled.sh check | plants
set -uo pipefail
OPS='^[[:space:]]+((v?(add|sub|mul|div|sqrt|min|max|ucomi|comi|cmp[a-z]*)s[sd])|v?cvt[a-z0-9]+|f(ld|st|add|sub|mul|div|sqrt|ild|ist|xch|chs|abs|com|ucom)[a-z0-9]*)([[:space:]]|$)'
MOVES='^[[:space:]]+(v?movs[sd]|v?movd|v?movq)[[:space:]].*%[xy]mm[0-9]'
CALLS='^[[:space:]]+call[ql]?[[:space:]]+\*?_*(__(add|sub|mul|div|neg|extend|trunc|fixuns|fix|floatun|float|cmp|unord|eq|ne|ge|gt|le|lt|pow)[a-z0-9]*(tf|xf|df|sf|hf|bf|td|dd|sd)[0-9]?[a-z0-9]*|__bid_[a-z0-9_]+|__dpd_[a-z0-9_]+|(sqrt|cbrt|pow|exp|exp2|expm1|log|log2|log10|log1p|sin|cos|tan|asin|acos|atan|atan2|sinh|cosh|tanh|floor|ceil|round|trunc|rint|nearbyint|fmod|fabs|hypot|ldexp|frexp|modf|strtod|strtof|strtold|atof|lround|llround|lrint|llrint|tgamma|lgamma|erf|erfc)[fl]?)(@PLT)?[[:space:]]*$'

# Prints the count of float operations in one source file, or exits 2 when it does not compile.
read_one() {
  local src=$1 asm compiler
  asm=$(mktemp)
  case "$src" in
    *.c) compiler=(gcc -std=gnu17) ;;
    *) compiler=(g++ -std=c++23) ;;
  esac
  "${compiler[@]}" -w -O0 -S "$src" -o "$asm" || { rm -f "$asm"; return 2; }
  grep -c -E "$OPS|$MOVES|$CALLS" "$asm" || true
  rm -f "$asm"
}

check() {
  local fails=0 files=0 src n
  if [ -n "$(git ls-files '*Cargo.toml' '*.rs')" ]; then
    echo "COMPILED_CPP_SMALL|result=FAIL|reason=rust_in_this_repository_needs_the_full_form|json=0"
    return 1
  fi
  while IFS= read -r src; do
    files=$((files + 1))
    if n=$(read_one "$src"); then
      echo "COMPILED_CPP|file=$src|fp_ops=$n|json=0"
      [ "$n" = 0 ] || fails=$((fails + 1))
    else
      echo "COMPILED_CPP_NOT_BUILT|file=$src|json=0"
      fails=$((fails + 1))
    fi
  done < <(git ls-files '*.c' '*.cc' '*.cpp' '*.cxx')
  echo "COMPILED_CPP_DONE|files=$files|failed=$fails|json=0"
  [ "$fails" = 0 ]
}

plants() {
  local d fails=0 name src n
  d=$(mktemp -d)
  cat > "$d/plain_double.cpp" <<'EOF'
int main() { volatile double a = 1; volatile double b = 3; return static_cast<int>(a / b * 9); }
EOF
  cat > "$d/float_suffix_exponent.cpp" <<'EOF'
int main() { auto x = 1e5f; return static_cast<int>(x) & 1; }
EOF
  cat > "$d/cmath_no_float_word.cpp" <<'EOF'
#include <cmath>
int main() { return static_cast<int>(std::sqrt(2)); }
EOF
  cat > "$d/quad_soft_float.cpp" <<'EOF'
int main() { volatile __float128 a = 1; volatile __float128 b = 3; return static_cast<int>(a / b * 9); }
EOF
  cat > "$d/decimal_soft_float.c" <<'EOF'
int main(void) { volatile _Decimal64 a = 3; volatile _Decimal64 b = 2; return (int)(a / b); }
EOF
  cat > "$d/inline_asm.cpp" <<'EOF'
int main() { long long o, a = 1, b = 3; __asm__("cvtsi2sdq %1,%%xmm0\n cvtsi2sdq %2,%%xmm1\n divsd %%xmm1,%%xmm0\n movq %%xmm0,%0" : "=r"(o) : "r"(a), "r"(b) : "xmm0", "xmm1"); return static_cast<int>(o & 1); }
EOF
  cat > "$d/control_wide_integer.cpp" <<'EOF'
int main() { volatile __int128 a = 7; volatile __int128 b = a * a; __int128 c[4] = {a, b, a, b}; __int128 d[4]; for (int i = 0; i < 4; i++) d[i] = c[i]; return static_cast<int>(d[1] % 5); }
EOF
  cat > "$d/control_vector_string.cpp" <<'EOF'
#include <string>
#include <vector>
int main() { std::vector<std::string> v{"a", "b"}; v.push_back(std::to_string(12)); return static_cast<int>(v.size()); }
EOF
  for src in "$d"/*; do
    name=$(basename "$src")
    n=$(read_one "$src") || n=not_built
    case "$name" in
      control_*) [ "$n" = 0 ] && r=GREEN || { r=WRONG; fails=$((fails + 1)); } ;;
      *) [ "$n" != 0 ] && [ "$n" != not_built ] && r=RED || { r=WRONG; fails=$((fails + 1)); } ;;
    esac
    echo "PLANT|lang=cpp|name=$name|fp_ops=$n|result=$r|json=0"
  done
  rm -rf "$d"
  echo "PLANTS_DONE|lang=cpp|failed=$fails|json=0"
  [ "$fails" = 0 ]
}

case "${1:-}" in
  check) check ;;
  plants) plants ;;
  *) echo "usage: no_float_compiled.sh check | plants"; exit 2 ;;
esac
