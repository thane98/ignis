use pyo3::prelude::*;

#[pyclass]
pub struct PlayerRandomizationInfo {
    #[pyo3(get, set)]
    pub male_class: String,

    #[pyo3(get, set)]
    pub female_class: String,

    #[pyo3(get, set)]
    pub male_weapon_a000: String,

    #[pyo3(get, set)]
    pub female_weapon_a000: String,

    pub a000_paths: (String, String),

    pub a002_paths: (String, String),

    pub a005_paths: (String, String),
}

#[pymethods]
impl PlayerRandomizationInfo {
    #[new]
    pub fn new(
        male_class: String,
        female_class: String,
        male_weapon_a000: String,
        female_weapon_a000: String,
        a000_paths: (String, String),
        a002_paths: (String, String),
        a005_paths: (String, String),
    ) -> Self {
        PlayerRandomizationInfo {
            male_class,
            female_class,
            male_weapon_a000,
            female_weapon_a000,
            a000_paths,
            a002_paths,
            a005_paths,
        }
    }
}
