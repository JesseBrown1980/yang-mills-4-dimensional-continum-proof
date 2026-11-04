#!/bin/bash
# The small form of the compiled-level check, for a repository with no Cargo package: C and C++ files, and Rust files built alone. The full form, for Cargo packages and their call graphs, is compiled_float_check.py in the Yang-Mills and SU(N) repositories.
# Each tracked C or C++ file is compiled -O0 -S and its assembly read for scalar float opcodes, scalar float moves, and calls to soft-float and libm routines. Moves of __int128 use movaps and movdqa, so those two do not count.
# Each tracked Rust file is built alone with rustc 1.81.0 at opt-level 0, the way the full form builds a loose file. Its LLVM IR is read for float types and instructions, with names and quoted text removed first, for assembly text naming float registers or opcodes, and for the standard library's float paths by symbol. Its MIR is read for f16, f32, f64 and f128, and holds what IR no longer shows: const evaluation, statics, dead functions and constants folded while the IR is built.
# Scope: what g++ and rustc 1.81.0 compile on this runner, with their default cfg. A library's own bodies are not read, and a tracked Cargo.toml stops this form, because a package needs the full one. Integer only, json=0.
# usage: no_float_compiled.sh check | plants
set -uo pipefail
OPS='^[[:space:]]+((v?(add|sub|mul|div|sqrt|min|max|ucomi|comi|cmp[a-z]*)s[sd])|v?cvt[a-z0-9]+|f(ld|st|add|sub|mul|div|sqrt|ild|ist|xch|chs|abs|com|ucom)[a-z0-9]*)([[:space:]]|$)'
MOVES='^[[:space:]]+(v?movs[sd]|v?movd|v?movq)[[:space:]].*%[xy]mm[0-9]'
CALLS='^[[:space:]]+call[ql]?[[:space:]]+\*?_*(__(add|sub|mul|div|neg|extend|trunc|fixuns|fix|floatun|float|cmp|unord|eq|ne|ge|gt|le|lt|pow)[a-z0-9]*(tf|xf|df|sf|hf|bf|td|dd|sd)[0-9]?[a-z0-9]*|__bid_[a-z0-9_]+|__dpd_[a-z0-9_]+|(sqrt|cbrt|pow|exp|exp2|expm1|log|log2|log10|log1p|sin|cos|tan|asin|acos|atan|atan2|sinh|cosh|tanh|floor|ceil|round|trunc|rint|nearbyint|fmod|fabs|hypot|ldexp|frexp|modf|strtod|strtof|strtold|atof|lround|llround|lrint|llrint|tgamma|lgamma|erf|erfc)[fl]?)(@PLT)?[[:space:]]*$'
# The same reads as the full form's loose-file path: IR_FP and MIR_FP after names and quoted text go, ASM_FP inside the quoted text of an assembly line, STD_FP on symbols.
IR_FP='\b(double|float|half|bfloat|fp128|x86_fp80|ppc_fp128|fadd|fsub|fmul|fdiv|frem|fneg|fcmp|sitofp|uitofp|fptosi|fptoui|fpext|fptrunc)\b'
IR_ASM='^[[:space:]]*module[[:space:]]+asm\b|\b(call|invoke)\b.*\basm\b'
ASM_FP='\b([xyz]mm[0-9]+|st\([0-9]\)|v?(add|sub|mul|div|sqrt|min|max|ucomi|comi|cmp[a-z]*)s[sdhq]|v?cvt[a-z0-9_]+|f(ld|st|add|sub|mul|div|sqrt|ild|ist|xch|chs|abs|com|ucom)[a-z0-9_]*)\b'
STD_FP='_ZN4core3fmt5float|_ZN4core3num7flt2dec|_ZN4core3num7dec2flt|_ZN3std3f32|_ZN3std3f64|_ZN4core3f32|_ZN4core3f64'
MIR_FP='\bf(16|32|64|128)\b|[0-9]_?f(16|32|64|128)\b'

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

# Prints the count of float lines in one Rust file built alone, in its IR and MIR, or exits 2 when it does not compile.
read_rust() {
  local src=$1 d kind=lib ir asm std mir
  d=$(mktemp -d)
  if grep -q -E '\bfn[[:space:]]+main[[:space:]]*\(' "$src"; then kind=bin; fi
  rustc +1.81.0 --edition 2021 --crate-type "$kind" --crate-name loose -A warnings -C opt-level=0 -C codegen-units=1 --emit=llvm-ir,mir --out-dir "$d" "$src" || { rm -rf "$d"; return 2; }
  ir=$(grep -v -E '^(;|source_filename|target )' "$d/loose.ll" | sed -E 's/"[^"]*"/""/g; s/[@%!#][^[:space:]]*//g' | grep -c -E "$IR_FP" || true)
  asm=$(grep -E "$IR_ASM" "$d/loose.ll" | grep -o -E '"[^"]*"' | grep -c -i -E "$ASM_FP" || true)
  std=$(grep -c -E "$STD_FP" "$d/loose.ll" || true)
  mir=$(grep -v -E '^[[:space:]]*(//|debug |scope )' "$d/loose.mir" | sed -E 's/"([^"\\]|\\.)*"/""/g' | grep -c -E "$MIR_FP" || true)
  rm -rf "$d"
  echo $((ir + asm + std + mir))
}

check() {
  local fails=0 cpp=0 rust=0 src n
  if [ -n "$(git ls-files '*Cargo.toml')" ]; then
    echo "COMPILED_SMALL|result=FAIL|reason=a_cargo_package_needs_the_full_form|json=0"
    return 1
  fi
  while IFS= read -r src; do
    cpp=$((cpp + 1))
    if n=$(read_one "$src"); then
      echo "COMPILED_CPP|file=$src|fp_ops=$n|json=0"
      [ "$n" = 0 ] || fails=$((fails + 1))
    else
      echo "COMPILED_CPP_NOT_BUILT|file=$src|json=0"
      fails=$((fails + 1))
    fi
  done < <(git ls-files '*.c' '*.cc' '*.cpp' '*.cxx')
  while IFS= read -r src; do
    rust=$((rust + 1))
    if n=$(read_rust "$src"); then
      echo "COMPILED_RUST|file=$src|fp_lines=$n|json=0"
      [ "$n" = 0 ] || fails=$((fails + 1))
    else
      echo "COMPILED_RUST_NOT_BUILT|file=$src|json=0"
      fails=$((fails + 1))
    fi
  done < <(git ls-files '*.rs')
  echo "COMPILED_DONE|cpp_files=$cpp|rust_files=$rust|failed=$fails|json=0"
  [ "$fails" = 0 ]
}

plants() {
  local d fails=0 name src n lang r
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
  cat > "$d/plain_f64.rs" <<'EOF'
fn main() { let a = std::env::args().count() as f64; println!("{}", (a / 3.0) as u8); }
EOF
  cat > "$d/c_double_alias.rs" <<'EOF'
fn main() { let n = std::env::args().count() as std::ffi::c_double; println!("{}", (n / 3 as std::ffi::c_double) as u8); }
EOF
  cat > "$d/type_from_a_macro.rs" <<'EOF'
macro_rules! t { () => { f32 }; }
type Q = t!();
fn main() { let n = std::env::args().count() as Q; println!("{}", (n * 0.5) as u8); }
EOF
  cat > "$d/const_folded.rs" <<'EOF'
const X: u8 = (1.5f64 * 2.0) as u8;
fn main() { println!("{}", X); }
EOF
  cat > "$d/dead_function.rs" <<'EOF'
fn unused() -> f64 { 0.5 }
fn main() {}
EOF
  cat > "$d/library_no_main.rs" <<'EOF'
pub fn half(a: f32) -> f32 { a / 2.0 }
EOF
  cat > "$d/duration_seconds.rs" <<'EOF'
fn main() { let s = std::time::Duration::from_secs(3).as_secs_f64(); println!("{}", s as u8); }
EOF
  cat > "$d/inline_asm.rs" <<'EOF'
use std::arch::asm;
fn main() { let mut x: u64 = 3; unsafe { asm!("cvtsi2sd xmm0, {0}", "cvttsd2si {0}, xmm0", inout(reg) x, out("xmm0") _); } println!("{}", x); }
EOF
  cat > "$d/control_integer.rs" <<'EOF'
use std::collections::HashMap;
fn main() { let mut m = HashMap::new(); m.insert(String::from("a"), 7u64); let n: i64 = "12".parse().unwrap(); println!("{} {} {}", m["a"] * 3, n, u128::MAX / 3); }
EOF
  cat > "$d/control_threads.rs" <<'EOF'
fn main() { let h = std::thread::spawn(|| (1u64..100).sum::<u64>()); println!("{}", h.join().unwrap()); }
EOF
  cat > "$d/control_words_in_a_string.rs" <<'EOF'
fn main() { println!("f64 double 0.5 float"); }
EOF
  for src in "$d"/*; do
    name=$(basename "$src")
    case "$name" in
      *.rs) lang=rust; n=$(read_rust "$src") || n=not_built ;;
      *) lang=cpp; n=$(read_one "$src") || n=not_built ;;
    esac
    case "$name" in
      control_*) [ "$n" = 0 ] && r=GREEN || { r=WRONG; fails=$((fails + 1)); } ;;
      *) [ "$n" != 0 ] && [ "$n" != not_built ] && r=RED || { r=WRONG; fails=$((fails + 1)); } ;;
    esac
    echo "PLANT|lang=$lang|name=$name|fp_ops=$n|result=$r|json=0"
  done
  rm -rf "$d"
  echo "PLANTS_DONE|failed=$fails|json=0"
  [ "$fails" = 0 ]
}

case "${1:-}" in
  check) check ;;
  plants) plants ;;
  *) echo "usage: no_float_compiled.sh check | plants"; exit 2 ;;
esac
