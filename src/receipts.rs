//! HBP/HBI/SHA/SH/HASH byte-stable receipts and fail-closed GitRAM fan-in.
//! A digest-only local anchor is an integrity commitment, NOT a digital signature.
use crate::physics::{self, Fraction, SHARD_COUNT};
use crate::sha256;
use std::collections::BTreeSet;
use std::fs;
use std::path::Path;

const FILES: [&str; 4] = ["trace.hbp", "index.hbi", "anchor.hbp", "SHA256SUMS"];

pub fn source_is_pinned(source: &str) -> bool {
    source.len() == 40
        && source
            .bytes()
            .all(|b| b.is_ascii_hexdigit() && !b.is_ascii_uppercase())
}

fn digest(data: &[u8]) -> String {
    sha256::hash_bytes(data)
}

struct ShardFiles {
    files: Vec<(&'static str, Vec<u8>)>,
    action: Fraction,
}

fn expected_shard(source: &str, id: usize) -> Result<ShardFiles, String> {
    physics::require(
        source_is_pinned(source),
        "source commit must be 40 lowercase hex digits",
    )?;
    physics::require(id < SHARD_COUNT, "unregistered GitRAM shard")?;
    let seed = physics::seed_for_shard(id);
    let trits = physics::candidate(id);
    let report = physics::evaluate(id, &trits)?;
    let trit_word = physics::trit_word(&trits);
    let gen_hash = digest(format!("YM4-GENESIS|v0|{source}|{id}|json=0").as_bytes());

    let candidate_core = format!(
        "YM4CANDIDATE|kind=SYNTHETIC_CONTROL|shard={id}|seed={seed}|trits64={trit_word}|model_sha256=NONE|source_commit={source}"
    );
    let candidate_sha = digest(candidate_core.as_bytes());
    let hash1 = digest(format!("{gen_hash}|{candidate_sha}|candidate").as_bytes());
    let candidate_line = format!(
        "{candidate_core}|record_sha256={candidate_sha}|prev_hash={gen_hash}|hash={hash1}|json=0\n"
    );

    let result_core = format!(
        "YM4RESULT|shard={id}|action_num={}|action_den={}|links=64|plaquettes={}|gauge_covariance=PASS|trace_invariance=PASS|fault_controls={}/2|scope=FINITE_ONLY",
        report.action.n, report.action.d, report.checked_plaquettes, report.fault_controls
    );
    let result_sha = digest(result_core.as_bytes());
    let hash2 = digest(format!("{hash1}|{result_sha}|result").as_bytes());
    let result_line =
        format!("{result_core}|record_sha256={result_sha}|prev_hash={hash1}|hash={hash2}|json=0\n");

    let header =
        format!("YM4HBP|schema=ym4.qnn.gitram.v0|shard={id}|source_commit={source}|json=0\n");
    let trace = format!("{header}{candidate_line}{result_line}");
    let index_header =
        format!("HBIHDR|schema=ym4.qnn.gitram.v0|shard={id}|file=trace.hbp|json=0\n");
    let candidate_row_sha = digest(candidate_line.as_bytes());
    let result_row_sha = digest(result_line.as_bytes());
    let first_offset = header.len();
    let second_offset = first_offset + candidate_line.len();
    let index = format!(
        "{index_header}HBI|part=candidate|offset={first_offset}|length={}|hbp_sha256={candidate_row_sha}|sh={}|json=0\nHBI|part=result|offset={second_offset}|length={}|hbp_sha256={result_row_sha}|sh={}|json=0\n",
        candidate_line.len(), &candidate_row_sha[..16],
        result_line.len(), &result_row_sha[..16],
    );
    let trace_sha = digest(trace.as_bytes());
    let index_sha = digest(index.as_bytes());
    let anchor = format!(
        "YM4ANCHOR|schema=ym4.qnn.gitram.v0|shard={id}|source_commit={source}|hbp_sha256={trace_sha}|hbi_sha256={index_sha}|chain_hash={hash2}|sh={}|json=0\n",
        &hash2[..16]
    );
    let anchor_sha = digest(anchor.as_bytes());
    let manifest =
        format!("{trace_sha}  trace.hbp\n{index_sha}  index.hbi\n{anchor_sha}  anchor.hbp\n");
    Ok(ShardFiles {
        files: vec![
            ("trace.hbp", trace.into_bytes()),
            ("index.hbi", index.into_bytes()),
            ("anchor.hbp", anchor.into_bytes()),
            ("SHA256SUMS", manifest.into_bytes()),
        ],
        action: report.action,
    })
}

pub fn write_shard(source: &str, id: usize, root: &Path) -> Result<(), String> {
    let out = expected_shard(source, id)?;
    fs::create_dir_all(root).map_err(|e| format!("cannot create shard directory: {e}"))?;
    for (name, bytes) in &out.files {
        fs::write(root.join(name), bytes).map_err(|e| format!("cannot write {name}: {e}"))?;
    }
    verify_shard(source, id, root)?;
    println!(
        "GITRAM_SHARD_PASS|shard={id}|source_commit={source}|action_num={}|action_den={}|plaquettes=96|fault_controls=2/2|json=0",
        out.action.n, out.action.d
    );
    Ok(())
}

pub fn verify_shard(source: &str, id: usize, root: &Path) -> Result<Fraction, String> {
    let expected = expected_shard(source, id)?;
    let names = fs::read_dir(root)
        .map_err(|e| format!("missing shard directory {id}: {e}"))?
        .map(|entry| {
            let entry = entry.map_err(|e| format!("cannot read shard entry: {e}"))?;
            physics::require(
                entry.file_type().map_err(|e| e.to_string())?.is_file(),
                "shard must contain only regular files",
            )?;
            Ok(entry.file_name().to_string_lossy().into_owned())
        })
        .collect::<Result<BTreeSet<String>, String>>()?;
    let required: BTreeSet<String> = FILES.iter().map(|s| (*s).to_owned()).collect();
    physics::require(
        names == required,
        "shard files missing, duplicated or unexpected",
    )?;
    for (name, exact) in expected.files {
        let bytes = fs::read(root.join(name)).map_err(|e| format!("cannot read {name}: {e}"))?;
        physics::require(
            bytes == exact,
            &format!("shard {id} {name}: exact content/hash/provenance mismatch"),
        )?;
    }
    Ok(expected.action)
}

fn sealed_files(source: &str, root_sha: &str, action: Fraction) -> Vec<(&'static str, Vec<u8>)> {
    let seal_hash = digest(format!("YM4-GITRAM-SEAL|{source}|{root_sha}|4").as_bytes());
    let trace = format!(
        "YM4SEAL|schema=ym4.qnn.gitram.v0|source_commit={source}|shards=4|action_sum_num={}|action_sum_den={}|anchor_root_sha256={root_sha}|sh={}|hash={seal_hash}|status=PASS|scope=FINITE_ONLY|json=0\n",
        action.n, action.d, &root_sha[..16]
    );
    let trace_sha = digest(trace.as_bytes());
    let index = format!(
        "HBI|part=seal|offset=0|length={}|hbp_sha256={trace_sha}|sh={}|json=0\n",
        trace.len(),
        &trace_sha[..16]
    );
    let index_sha = digest(index.as_bytes());
    let anchor = format!(
        "YM4SEALANCHOR|source_commit={source}|hbp_sha256={trace_sha}|hbi_sha256={index_sha}|hash={seal_hash}|sh={}|json=0\n",
        &seal_hash[..16]
    );
    let anchor_sha = digest(anchor.as_bytes());
    let sums =
        format!("{trace_sha}  SEALED.hbp\n{index_sha}  SEALED.hbi\n{anchor_sha}  SEALED.anchor\n");
    vec![
        ("SEALED.hbp", trace.into_bytes()),
        ("SEALED.hbi", index.into_bytes()),
        ("SEALED.anchor", anchor.into_bytes()),
        ("SHA256SUMS", sums.into_bytes()),
    ]
}

pub fn verify_all(source: &str, root: &Path, seal_dir: &Path) -> Result<(), String> {
    physics::require(source_is_pinned(source), "untrusted source format")?;
    let mut found = BTreeSet::new();
    for entry in fs::read_dir(root).map_err(|e| format!("cannot read fan-in root: {e}"))? {
        let entry = entry.map_err(|e| e.to_string())?;
        physics::require(
            entry.file_type().map_err(|e| e.to_string())?.is_dir(),
            "fan-in only accepts shard directories",
        )?;
        found.insert(entry.file_name().to_string_lossy().into_owned());
    }
    let expected_names: BTreeSet<String> =
        (0..SHARD_COUNT).map(|id| format!("shard-{id}")).collect();
    physics::require(
        found == expected_names,
        "fan-in missing, duplicate or extra shard",
    )?;

    let mut actions = Fraction::zero();
    let mut anchors = String::from("YM4-ANCHOR-ROOT-v0\n");
    for id in 0..SHARD_COUNT {
        let path = root.join(format!("shard-{id}"));
        actions = actions.plus(verify_shard(source, id, &path)?);
        let anchor = fs::read(path.join("anchor.hbp"))
            .map_err(|e| format!("cannot read shard anchor: {e}"))?;
        anchors.push_str(&format!("{id}|{}\n", digest(&anchor)));
    }
    let root_sha = digest(anchors.as_bytes());
    let expected_seal = sealed_files(source, &root_sha, actions);
    fs::create_dir_all(seal_dir).map_err(|e| format!("cannot create seal directory: {e}"))?;
    for (name, bytes) in expected_seal {
        fs::write(seal_dir.join(name), bytes).map_err(|e| format!("cannot write seal: {e}"))?;
    }
    println!(
        "GITRAM_FANIN_PASS|shards=4|action_sum_num={}|action_sum_den={}|anchor_root_sha256={root_sha}|scope=FINITE_ONLY|json=0",
        actions.n, actions.d
    );
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn tamper_and_missing_are_fail_closed() {
        let src = "a".repeat(40);
        let root = std::env::temp_dir().join(format!("ym4-gitram-test-{}", std::process::id()));
        let shards = root.join("shards");
        let _ = fs::remove_dir_all(&root);
        fs::create_dir_all(&shards).unwrap();
        for id in 0..SHARD_COUNT {
            write_shard(&src, id, &shards.join(format!("shard-{id}"))).unwrap();
        }
        verify_all(&src, &shards, &root.join("seal")).unwrap();
        let trace = shards.join("shard-2/trace.hbp");
        let original = fs::read(&trace).unwrap();
        let mut corrupt = original.clone();
        corrupt[0] ^= 1;
        fs::write(&trace, &corrupt).unwrap();
        assert!(verify_all(&src, &shards, &root.join("seal")).is_err());
        fs::write(&trace, original).unwrap();
        fs::remove_dir_all(shards.join("shard-3")).unwrap();
        assert!(verify_all(&src, &shards, &root.join("seal")).is_err());
        assert!(verify_shard(&"f".repeat(40), 2, &shards.join("shard-2")).is_err());
        let _ = fs::remove_dir_all(&root);
    }

    #[test]
    fn source_format_cannot_be_unpinned() {
        assert!(source_is_pinned(&"a".repeat(40)));
        assert!(!source_is_pinned(&"A".repeat(40)));
        assert!(!source_is_pinned("not-a-source"));
    }
}
