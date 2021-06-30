use pyo3::exceptions::Exception;
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use rand_pcg::Pcg64;

use std::collections::HashMap;
use std::path::Path;

use rand::prelude::*;

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

#[pymodule]
pub fn ignis(_: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<paragon::GameData>()?;
    m.add_wrapped(wrap_pyfunction!(randomize_scripts))?;
    m.add_wrapped(wrap_pyfunction!(randomize_terrain_scripts))?;
    Ok(())
}
