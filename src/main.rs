//! YM4 GitRAM bridge: deterministic finite 4D SU(2) trials, not a continuum theorem.
#![forbid(unsafe_code)]

mod physics;
mod receipts;
mod sha256;

use std::env;
use std::path::Path;
use std::time::Instant;

fn run() -> Result<(), String> {
    let args: Vec<String> = env::args().collect();
    match args.as_slice() {
        [_, command, shard, source, directory] if command == "shard" => {
            let id: usize = shard.parse().map_err(|_| "invalid shard id".to_owned())?;
            receipts::write_shard(source, id, Path::new(directory))
        }
        [_, command, source, shard_directory, seal_directory] if command == "fan-in" => {
            receipts::verify_all(source, Path::new(shard_directory), Path::new(seal_directory))
        }
        [_, command, source, output_directory] if command == "baseline" => {
            let root = Path::new(output_directory);
            let start = Instant::now();
            for shard in 0..physics::SHARD_COUNT {
                receipts::write_shard(
                    source,
                    shard,
                    &root.join("shards").join(format!("shard-{shard}")),
                )?;
            }
            receipts::verify_all(source, &root.join("shards"), &root.join("seal"))?;
            let elapsed = start.elapsed().as_millis();
            println!(
                "GITRAM_BASELINE_PASS|shards=4|elapsed_ms={elapsed}|"
            );
            println!(
                "SCOPE|finite_4d_SU2=1|candidate=SYNTHETIC_CONTROL|"
            );
            println!("CONTINUUM|existence=OPEN|physical_mass_gap=OPEN|json=0");
            Ok(())
        }
        _ => Err(String::from(
            "usage: ym4-gitram shard ID SOURCE_SHA40 OUT_DIR | \
             fan-in SOURCE_SHA40 SHARDS_DIR SEAL_DIR | baseline SOURCE_SHA40 OUT_DIR",
        )),
    }
}

fn main() {
    if let Err(error) = run() {
        // No PASS marker is emitted on failure; nonzero exit propagates to Actions.
        eprintln!("YM4_GITRAM_FAIL|reason={}|json=0", error.replace('|', "_"));
        std::process::exit(2);
    }
}
