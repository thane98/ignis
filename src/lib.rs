mod player_randomization_info;

use pyo3::exceptions::Exception;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use rand_pcg::Pcg64;

use std::collections::HashMap;
use std::path::Path;

use player_randomization_info::PlayerRandomizationInfo;
use rand::prelude::*;
use serde_json::json;

#[pyfunction]
pub fn randomize_scripts(
    scripts: Vec<(String, String)>,
    replacements: HashMap<String, String>,
) -> PyResult<()> {
    let chunk_size = scripts.len() / 4;
    let chunks = scripts.chunks(chunk_size);
    let mut threads = Vec::new();
    for chunk in chunks {
        let chunk: Vec<(String, String)> = chunk.iter().cloned().collect();
        let replacements = replacements.clone();
        let handle = std::thread::spawn(move || {
            for (source, dest) in chunk {
                // Disassemble the script.
                let raw = std::fs::read(source).unwrap();
                let mut ast = exalt::disassemble_v3ds(&raw).unwrap();
                let mut dirty = false;

                // Perform replacement on string literals.
                for func in &mut ast {
                    for i in 0..func.args.len() {
                        let replacement = if let exalt::EventArg::Str(text) = &mut func.args[i] {
                            dirty = true;
                            replacements.get(text).map(|x| x.to_owned())
                        } else {
                            None
                        };
                        if let Some(text) = replacement {
                            func.args[i] = exalt::EventArg::Str(text);
                        }
                    }
                    for i in 0..func.code.len() {
                        let replacement = if let exalt::Opcode::StrLoad(text) = &mut func.code[i] {
                            dirty = true;
                            replacements.get(text).map(|x| x.to_owned())
                        } else {
                            None
                        };
                        if let Some(text) = replacement {
                            func.code[i] = exalt::Opcode::StrLoad(text);
                        }
                    }
                }

                // Assemble and write the script.
                if dirty {
                    let path = Path::new(&dest);
                    let parent = path.parent().unwrap();
                    let fname = path.file_name().unwrap().to_str().unwrap();
                    let compiled_script = exalt::gen_v3ds_code(fname, &ast).unwrap();
                    std::fs::create_dir_all(parent).unwrap();
                    std::fs::write(dest, compiled_script).unwrap();
                }
            }
        });
        threads.push(handle);
    }
    for thread in threads {
        thread
            .join()
            .map_err(|_| Exception::py_err("Script randomization failed"))?;
    }
    Ok(())
}

#[pyfunction]
pub fn randomize_terrain_scripts(
    scripts: Vec<(String, String)>,
    items: Vec<String>,
    seed: i64,
) -> PyResult<()> {
    let chunk_size = scripts.len() / 4;
    let chunks = scripts.chunks(chunk_size);
    let mut threads = Vec::new();
    for chunk in chunks {
        let chunk: Vec<(String, String)> = chunk.iter().cloned().collect();
        let items = items.clone();
        let handle = std::thread::spawn(move || {
            let mut random = Pcg64::seed_from_u64(seed as u64);
            for (source, dest) in chunk {
                // Disassemble the script.
                let raw = std::fs::read(source).unwrap();
                let mut ast = exalt::disassemble_v3ds(&raw).unwrap();
                let mut dirty = false;

                // Perform replacement on string literals.
                for func in &mut ast {
                    for i in 0..func.code.len() {
                        let replacement = if let exalt::Opcode::StrLoad(text) = &mut func.code[i] {
                            if text.starts_with("IID_") {
                                dirty = true;
                                Some(items[random.gen_range(0..items.len())].clone())
                            } else {
                                None
                            }
                        } else {
                            None
                        };
                        if let Some(text) = replacement {
                            func.code[i] = exalt::Opcode::StrLoad(text);
                        }
                    }
                }

                // Assemble and write the script.
                if dirty {
                    let path = Path::new(&dest);
                    let parent = path.parent().unwrap();
                    let fname = path.file_name().unwrap().to_str().unwrap();
                    let compiled_script = exalt::gen_v3ds_code(fname, &ast).unwrap();
                    std::fs::create_dir_all(parent).unwrap();
                    std::fs::write(dest, compiled_script).unwrap();
                }
            }
        });
        threads.push(handle);
    }
    for thread in threads {
        thread
            .join()
            .map_err(|_| Exception::py_err("Script randomization failed"))?;
    }
    Ok(())
}

#[pyfunction]
pub fn fix_b016_shura_weapons(
    input_path: String,
    output_path: String,
    weapon1: String,
    weapon2: String,
) -> PyResult<()> {
    let mut dirty = false;
    let weapons = vec![weapon1, weapon2];
    let mut next_weapons_index = 0;
    let raw_script = std::fs::read(&input_path)?;
    let mut script = exalt::disassemble_v3ds(&raw_script)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    for func in &mut script {
        for i in 1..func.code.len() {
            let replacement = if let exalt::Opcode::CallByName(text, _) = &func.code[i] {
                if text == "ev::ItemGainSilent" {
                    let item = weapons[next_weapons_index].clone();
                    next_weapons_index = (next_weapons_index + 1) % weapons.len();
                    Some(item)
                } else {
                    None
                }
            } else {
                None
            };
            if let Some(iid) = replacement {
                if i > 0 {
                    func.code[i - 1] = exalt::Opcode::StrLoad(iid);
                    dirty = true;
                }
            }
        }
    }
    if dirty {
        let path = Path::new(&output_path);
        let parent = path
            .parent()
            .ok_or(Exception::py_err("Error finding script path parent"))?;
        let compiled_script = exalt::gen_v3ds_code("B016.cmb", &script)
            .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
        std::fs::create_dir_all(parent)?;
        std::fs::write(path, compiled_script)?;
    }
    Ok(())
}

#[pyfunction]
pub fn apply_mu_class_randomization(py: Python, info: Py<PlayerRandomizationInfo>) -> PyResult<()> {
    let info = info.try_borrow(py)?;
    let reg = handlebars::Handlebars::new();

    // A000: Inject new opcodes into the script to reclass the player immediately
    // after loading the chapter resources.
    let raw_script = std::fs::read(&info.a000_paths.0)?;
    let mut script = exalt::disassemble_v3ds(&raw_script)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    for func in &mut script {
        if func.function_type == 7 {
            let snippet = String::from_utf8_lossy(include_bytes!("A000Snippet.yml")).to_string();
            let rendered_snippet = reg
                .render_template(
                    &snippet,
                    &json!({
                        "mclass": &info.male_class,
                        "fclass": &info.female_class,
                        "mitem": &info.male_weapon_a000,
                        "fitem": &info.female_weapon_a000,
                    }),
                )
                .map_err(|err| Exception::py_err(err.to_string()))?;
            let opcodes = exalt::load_opcodes(&rendered_snippet)
                .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
            func.frame_size += 1;
            func.code = opcodes;
        }
        if func.function_type == 8 {
            let snippet = String::from_utf8_lossy(include_bytes!("A000Snippet2.yml")).to_string();
            func.code = exalt::load_opcodes(&snippet)
                .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
        }
    }
    let compiled_script = exalt::gen_v3ds_code("A000.cmb", &script)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    std::fs::write(&info.a000_paths.1, compiled_script)?;

    // A002: Don't remove the old weapon when the player gets Ganglari.
    let a002_snippet = String::from_utf8_lossy(include_bytes!("A002Snippet.yml")).to_string();
    let opcodes = exalt::load_opcodes(&a002_snippet)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    let raw_script = std::fs::read(&info.a002_paths.0)?;
    let mut script = exalt::disassemble_v3ds(&raw_script)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    for func in &mut script {
        if func.function_type == 12 {
            func.code = opcodes;
            break;
        }
    }
    let compiled_script = exalt::gen_v3ds_code("A002.cmb", &script)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    std::fs::write(&info.a002_paths.1, compiled_script)?;

    // A005: Handle reclassing between original and feral dragon.
    let raw_script = std::fs::read(&info.a005_paths.0)?;
    let mut script = exalt::disassemble_v3ds(&raw_script)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    for func in &mut script {
        if func.function_type == 13 {
            let a005_snippet =
                String::from_utf8_lossy(include_bytes!("A005Snippet2.yml")).to_string();
            let a005_snippet = reg
                .render_template(
                    &a005_snippet,
                    &json!({
                        "mclass": &info.male_class,
                        "fclass": &info.female_class,
                    }),
                )
                .map_err(|err| Exception::py_err(err.to_string()))?;
            let opcodes = exalt::load_opcodes(&a005_snippet)
                .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
            func.code = opcodes;
        }
    }
    let compiled_script = exalt::gen_v3ds_code("A005.cmb", &script)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    std::fs::write(&info.a005_paths.1, compiled_script)?;

    let all_006_chapters = vec![
        ("B006.cmb", info.b006_paths.clone()),
        ("C006.cmb", info.c006_paths.clone()),
    ];
    for (script_name, paths) in all_006_chapters {
        if let Some(paths) = &paths {
            let raw_script = std::fs::read(&paths.0)?;
            let mut script = exalt::disassemble_v3ds(&raw_script)
                .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
            for func in &mut script {
                if func.function_type == 12 {
                    let snippet =
                        String::from_utf8_lossy(include_bytes!("006Snippet.yml")).to_string();
                    let snippet = reg
                        .render_template(
                            &snippet,
                            &json!({
                                "mitem": &info.male_weapon_006,
                                "fitem": &info.female_weapon_006,
                            }),
                        )
                        .map_err(|err| Exception::py_err(err.to_string()))?;
                    let opcodes = exalt::load_opcodes(&snippet)
                        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
                    func.code.pop();
                    func.code.extend(opcodes);
                }
            }
            let compiled_script = exalt::gen_v3ds_code(script_name, &script)
                .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
            std::fs::write(&paths.1, compiled_script)?;
        }
    }

    Ok(())
}

#[pyfunction]
pub fn apply_fe14_animation_fixes(raw_archive: Vec<u8>, output_path: String) -> PyResult<()> {
    let snippet = String::from_utf8_lossy(include_bytes!("AnimFixSnippet.txt")).to_string();
    let bin_archive = mila::BinArchive::from_bytes(&raw_archive)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    let mut unpacked_archive = asset_pack_rs::unpack(&bin_archive)
        .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
    if !unpacked_archive.contains("uEAnim_Eliserep_non") {
        unpacked_archive.push_str("\n");
        unpacked_archive.push_str(&snippet);
        let bin_archive = asset_pack_rs::pack(&unpacked_archive)
            .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
        let raw_archive = bin_archive.serialize()
            .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
        let compressed_archive = mila::LZ13CompressionFormat {}
            .compress(&raw_archive)
            .map_err(|err| Exception::py_err(format!("{:?}", err)))?;
        std::fs::write(output_path, compressed_archive)?;
    }
    Ok(())
}

#[pymodule]
pub fn ignis(_: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<paragon::GameData>()?;
    m.add_class::<PlayerRandomizationInfo>()?;
    m.add_wrapped(wrap_pyfunction!(randomize_scripts))?;
    m.add_wrapped(wrap_pyfunction!(randomize_terrain_scripts))?;
    m.add_wrapped(wrap_pyfunction!(apply_mu_class_randomization))?;
    m.add_wrapped(wrap_pyfunction!(fix_b016_shura_weapons))?;
    m.add_wrapped(wrap_pyfunction!(apply_fe14_animation_fixes))?;
    Ok(())
}
